from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import time
import json

from ..schemas import AnalyzeRequest, AnalyzePageRequest, AnalyzeResponse, RedFlag, SafeAlternative, AlternativesPayload
from ..models import Scan
from ..database import get_db
from ..services.analyzer import analyze_message, get_risk_level
from ..services.url_checker import CompositeURLChecker, is_trusted_domain
from ..services.alternatives import find_safe_alternative, get_safer_alternatives

from ..services.ai_explainer import generate_ai_explanation

router = APIRouter()
url_checker = CompositeURLChecker()

@router.post("/analyze", response_model=AnalyzeResponse, tags=["Analyze"])
async def analyze_endpoint(request: AnalyzeRequest, db: Session = Depends(get_db)):
    start = time.time()
    try:
        result = analyze_message(
            message_text=request.message_text,
            sender=request.sender,
            sender_contact=request.sender_contact,
            explicit_url=str(request.url) if request.url else None,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    # Check extracted URLs using CompositeURLChecker
    urls_to_check = result["extracted_urls"]
    if urls_to_check:
        rep_results = await url_checker.check_urls(urls_to_check)
        for rep in rep_results:
            result["red_flags"].append({
                "rule": f"Flagged URL ({rep['provider']})",
                "points": 25,
                "explanation": rep["details"],
                "evidence": rep["url"]
            })
            result["risk_score"] = min(100, result["risk_score"] + 25)

    # Re-evaluate risk level & verdict after URL reputation check
    if result["risk_score"] >= 75:
        result["risk_level"] = "Critical"
        result["verdict"] = "Likely phishing"
    elif result["risk_score"] >= 50:
        result["risk_level"] = "High"
        result["verdict"] = "Likely scam"
    elif result["risk_score"] >= 25:
        result["risk_level"] = "Suspicious"
        result["verdict"] = "Needs caution"

    # Optional AI explanation enrichment
    ai_desc = await generate_ai_explanation(
        message_text=request.message_text,
        risk_level=result["risk_level"],
        red_flags=result["red_flags"]
    )
    if ai_desc:
        result["recommendation"] += f" AI Summary: {ai_desc}"

    elapsed_ms = int((time.time() - start) * 1000)

    # Persist scan
    scan = Scan(
        message_text=result["masked_message"],
        sender=request.sender,
        sender_contact=request.sender_contact,
        extracted_urls=json.dumps(result["extracted_urls"]),
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        verdict=result["verdict"],
        reasons=json.dumps(result["red_flags"]),
        recommendation=result["recommendation"],
        processing_time_ms=elapsed_ms,
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)

    red_flags = [RedFlag(**rf) for rf in result["red_flags"]]
    return AnalyzeResponse(
        risk_score=result["risk_score"],
        risk_level=result["risk_level"],
        verdict=result["verdict"],
        red_flags=red_flags,
        recommendation=result["recommendation"],
        processing_time_ms=elapsed_ms,
    )


@router.post("/analyze-page", response_model=AnalyzeResponse, tags=["Analyze"])
async def analyze_page_endpoint(request: AnalyzePageRequest, db: Session = Depends(get_db)):
    """Endpoint used by the Chrome Extension to scan a full webpage content and extracted links."""
    start = time.time()

    # Truncate text to max 10,000 characters for safety
    safe_text = request.page_text[:10000] if request.page_text else ""
    links_to_scan = (request.links or [])[:20]  # Scans max 20 links
    all_urls = list(set([request.page_url] + links_to_scan))

    page_is_trusted = is_trusted_domain(request.page_url)

    if page_is_trusted:
        # Check only external links on trusted domains
        external_links = [u for u in links_to_scan if not is_trusted_domain(u)]
        rep_results = await url_checker.check_urls(external_links) if external_links else []

        if not rep_results:
            risk_score = 0
            risk_level = "Low"
            verdict = "Verified official site"
            red_flags = []
            recommendation = f"This webpage is hosted on a verified official domain ({request.page_url}). Safe to interact."
        else:
            red_flags_list = [
                {
                    "rule": f"Flagged External Link ({rep['provider']})",
                    "points": 25,
                    "explanation": rep["details"],
                    "evidence": rep["url"]
                } for rep in rep_results
            ]
            risk_score = min(100, len(rep_results) * 25)
            risk_level = "Suspicious" if risk_score < 50 else "High"
            verdict = "Contains suspicious links"
            red_flags = [RedFlag(**rf) for rf in red_flags_list]
            recommendation = "This page is official, but contains external links that may be suspicious. Exercise caution."
    else:
        # Standard evaluation for unknown/unverified web domains
        combined_content = f"Page Title: {request.page_title}\nURL: {request.page_url}\nContent: {safe_text}"
        result = analyze_message(
            message_text=combined_content,
            sender=f"Webpage: {request.page_title}",
            sender_contact=request.page_url,
            explicit_url=request.page_url
        )

        rep_results = await url_checker.check_urls(all_urls) if all_urls else []
        for rep in rep_results:
            result["red_flags"].append({
                "rule": f"Flagged Webpage Link ({rep['provider']})",
                "points": 20,
                "explanation": rep["details"],
                "evidence": rep["url"]
            })
            result["risk_score"] = min(100, result["risk_score"] + 20)

        risk_score = result["risk_score"]
        risk_level = get_risk_level(risk_score)
        verdict = {
            "Low": "Probably safe",
            "Suspicious": "Needs caution",
            "High": "Likely scam",
            "Critical": "Likely phishing",
        }[risk_level]
        recommendation = result["recommendation"]
        red_flags = [RedFlag(**rf) for rf in result["red_flags"]]

    elapsed_ms = int((time.time() - start) * 1000)

    safe_alt = None
    safer_alts_payload = None
    if risk_level in ["Suspicious", "High", "Critical"]:
        alt_payload = await get_safer_alternatives(request.page_url, request.page_title, safe_text, db)
        if alt_payload:
            safer_alts_payload = AlternativesPayload(**alt_payload)
            if alt_payload.get("alternatives"):
                top_alt = alt_payload["alternatives"][0]
                safe_alt = SafeAlternative(
                    name=top_alt["name"],
                    url=top_alt["url"],
                    explanation=top_alt["reason"]
                )

    # Persist page scan
    scan = Scan(
        message_text=f"[PAGE SCAN] {request.page_title} - {request.page_url}",
        sender="Chrome Extension",
        sender_contact=request.page_url,
        extracted_urls=json.dumps(all_urls),
        risk_score=risk_score,
        risk_level=risk_level,
        verdict=verdict,
        reasons=json.dumps([rf.dict() for rf in red_flags]),
        recommendation=recommendation,
        processing_time_ms=elapsed_ms,
    )
    db.add(scan)
    db.commit()

    return AnalyzeResponse(
        risk_score=risk_score,
        risk_level=risk_level,
        verdict=verdict,
        red_flags=red_flags,
        recommendation=recommendation,
        processing_time_ms=elapsed_ms,
        safe_alternative=safe_alt,
        safer_alternatives_data=safer_alts_payload
    )

