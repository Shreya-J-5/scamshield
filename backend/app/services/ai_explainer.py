from typing import List, Dict, Any, Optional
import httpx
from ..config import settings

async def generate_ai_explanation(
    message_text: str,
    risk_level: str,
    red_flags: List[Dict[str, Any]]
) -> Optional[str]:
    """Generates an optional AI-enriched summary explanation using Gemini REST API if key is present.
    If no key is configured or API fails, returns None.
    """
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    flag_summary = ", ".join([f"{f['rule']} ({f['points']} pts)" for f in red_flags])
    prompt = f"""
You are a cybersecurity expert assistant for ScamShield.
Analyze the following message and security assessment results to provide a 2-sentence user-friendly explanation of why this message is considered {risk_level} risk.

Message: "{message_text}"
Detected Red Flags: {flag_summary}

Keep your answer concise, calm, actionable, and under 50 words. Do NOT make definitive claims like 100% scam.
"""

    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        async with httpx.AsyncClient(timeout=4.0) as client:
            res = await client.post(url, json=payload)
            if res.status_code == 200:
                data = res.json()
                text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                return text
    except Exception:
        pass

    return None
