import os
import json
import time
import re
import httpx
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse
from ..config import settings

# ---------------------------------------------------------------------------
# HARD ANTI-GENERIC FILTER (DO NOT RECOMMEND UNLESS CATEGORY = AI CHATBOT)
# ---------------------------------------------------------------------------
GENERIC_AI_DOMAINS = {
    "chatgpt.com",
    "claude.ai",
    "perplexity.ai",
    "gemini.google.com",
    "copilot.microsoft.com",
    "openai.com"
}

# ---------------------------------------------------------------------------
# TASK-ORIENTED CURATED CATEGORY TAXONOMY
# ---------------------------------------------------------------------------
CURATED_TASK_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "pdf-compression": {
        "category": "PDF Tools",
        "sub_category": "PDF Compression",
        "primary_task": "Compress PDF files online to reduce file size",
        "input_type": "PDF File",
        "output_type": "Compressed PDF",
        "keywords": ["compress pdf", "reduce pdf size", "pdf optimizer", "shrink pdf", "pdf compression"],
        "alternatives": [
            {
                "name": "iLovePDF Compress",
                "domain": "ilovepdf.com",
                "url": "https://www.ilovepdf.com/compress_pdf",
                "description": "Compress PDF file size while optimizing for maximal PDF quality.",
                "reason": "Top-rated online tool specifically for compressing PDFs safely.",
                "primary_task": "Compress PDF files",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Smallpdf Compress",
                "domain": "smallpdf.com",
                "url": "https://smallpdf.com/compress-pdf",
                "description": "Reduce the size of your PDF online without losing quality.",
                "reason": "Established, secure PDF compression service.",
                "primary_task": "Compress PDF files",
                "relevance_score": 0.96,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Popular / Trusted"
            },
            {
                "name": "PDF24 Compress",
                "domain": "tools.pdf24.org",
                "url": "https://tools.pdf24.org/en/compress-pdf",
                "description": "Free online tool to reduce PDF file size without file limits.",
                "reason": "100% free PDF compressor with strict privacy deletion.",
                "primary_task": "Compress PDF files",
                "relevance_score": 0.95,
                "tags": ["free", "privacy", "fast"],
                "category_label": "Free & Privacy-focused"
            },
            {
                "name": "Adobe Acrobat Online Compress",
                "domain": "adobe.com",
                "url": "https://www.adobe.com/acrobat/online/compress-pdf.html",
                "description": "Official Adobe web tool for PDF compression.",
                "reason": "Official industry standard PDF compression portal.",
                "primary_task": "Compress PDF files",
                "relevance_score": 0.94,
                "tags": ["trusted", "fast"],
                "category_label": "Official Standard"
            }
        ]
    },
    "pdf-general": {
        "category": "PDF Tools",
        "sub_category": "PDF Utility",
        "primary_task": "Merge, convert, split, or edit PDF files online",
        "input_type": "PDF File",
        "output_type": "Processed PDF",
        "keywords": ["pdf", "merge pdf", "convert pdf", "pdf editor", "split pdf"],
        "alternatives": [
            {
                "name": "iLovePDF",
                "domain": "ilovepdf.com",
                "url": "https://www.ilovepdf.com",
                "description": "Complete suite for working with PDF documents.",
                "reason": "Trusted, full-featured PDF utility suite.",
                "primary_task": "Edit and convert PDF files",
                "relevance_score": 0.96,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Smallpdf",
                "domain": "smallpdf.com",
                "url": "https://smallpdf.com",
                "description": "Easy-to-use online PDF editor and converter.",
                "reason": "Secure PDF editing platform.",
                "primary_task": "Edit and convert PDF files",
                "relevance_score": 0.94,
                "tags": ["free", "trusted"],
                "category_label": "Popular / Trusted"
            }
        ]
    },
    "image-compression": {
        "category": "Image Tools",
        "sub_category": "Image Compression",
        "primary_task": "Compress PNG, JPEG, and WebP images online",
        "input_type": "Image File",
        "output_type": "Compressed Image",
        "keywords": ["compress image", "tiny png", "compress jpeg", "reduce image size", "image optimizer", "shrink image"],
        "alternatives": [
            {
                "name": "TinyPNG",
                "domain": "tinypng.com",
                "url": "https://tinypng.com",
                "description": "Smart WebP, PNG and JPEG compression tool.",
                "reason": "Industry standard for image compression with zero visual quality loss.",
                "primary_task": "Compress images",
                "relevance_score": 0.99,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Squoosh",
                "domain": "squoosh.app",
                "url": "https://squoosh.app",
                "description": "Open-source in-browser image compressor built by Google Chrome Labs.",
                "reason": "100% private in-browser image compression with live side-by-side preview.",
                "primary_task": "Compress images",
                "relevance_score": 0.97,
                "tags": ["free", "privacy", "fast"],
                "category_label": "Privacy-focused"
            },
            {
                "name": "Compress JPEG",
                "domain": "compressjpeg.com",
                "url": "https://compressjpeg.com",
                "description": "Batch compress JPEG and PNG images online.",
                "reason": "Fast batch image compression utility.",
                "primary_task": "Compress images",
                "relevance_score": 0.92,
                "tags": ["free", "fast"],
                "category_label": "Fast Batch Compression"
            }
        ]
    },
    "background-removal": {
        "category": "Image Tools",
        "sub_category": "Background Removal",
        "primary_task": "Remove background from photos and images automatically",
        "input_type": "Image File",
        "output_type": "Transparent PNG",
        "keywords": ["remove background", "bg remover", "transparent background", "cut out image", "remove bg"],
        "alternatives": [
            {
                "name": "remove.bg",
                "domain": "remove.bg",
                "url": "https://www.remove.bg",
                "description": "Automatic AI image background remover in 5 seconds.",
                "reason": "Dedicated, instant background removal tool.",
                "primary_task": "Remove image background",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Adobe Express BG Remover",
                "domain": "adobe.com",
                "url": "https://www.adobe.com/express/feature/image/remove-background",
                "description": "Official Adobe free online background remover.",
                "reason": "Official Adobe image processing engine.",
                "primary_task": "Remove image background",
                "relevance_score": 0.96,
                "tags": ["free", "trusted"],
                "category_label": "Official Adobe Tool"
            },
            {
                "name": "Photoroom",
                "domain": "photoroom.com",
                "url": "https://www.photoroom.com/tools/background-remover",
                "description": "Instant high-accuracy background removal.",
                "reason": "Fast AI background eraser.",
                "primary_task": "Remove image background",
                "relevance_score": 0.93,
                "tags": ["free", "fast"],
                "category_label": "Fast"
            }
        ]
    },
    "image-editing": {
        "category": "Image Tools",
        "sub_category": "Photo Editing",
        "primary_task": "Edit photos, crop images, or design graphics in browser",
        "input_type": "Image / PSD",
        "output_type": "Edited Graphic",
        "keywords": ["photo editor", "image editor", "photoshop online", "crop image", "photopea", "design graphics"],
        "alternatives": [
            {
                "name": "Photopea",
                "domain": "photopea.com",
                "url": "https://www.photopea.com",
                "description": "Full-featured Photoshop alternative running in browser.",
                "reason": "Supports PSD, XCF, RAW, and full layer editing.",
                "primary_task": "Edit photos and graphics",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "privacy"],
                "category_label": "Best Overall"
            },
            {
                "name": "Canva",
                "domain": "canva.com",
                "url": "https://www.canva.com",
                "description": "Online graphic design platform for social media & marketing.",
                "reason": "Trusted template-based design suite.",
                "primary_task": "Design graphics",
                "relevance_score": 0.94,
                "tags": ["free", "trusted"],
                "category_label": "Popular / Trusted"
            }
        ]
    },
    "url-shortening": {
        "category": "Web Utilities",
        "sub_category": "URL Shortener",
        "primary_task": "Shorten long web URLs and create short links",
        "input_type": "Long URL",
        "output_type": "Shortened Link",
        "keywords": ["shorten url", "link shortener", "bitly", "tinyurl", "short link", "url shortener"],
        "alternatives": [
            {
                "name": "Dub.co",
                "domain": "dub.co",
                "url": "https://dub.co",
                "description": "Modern open-source link management and URL shortener.",
                "reason": "Privacy-first, fast link shortener with custom domains.",
                "primary_task": "Shorten long URLs",
                "relevance_score": 0.97,
                "tags": ["free", "fast", "privacy"],
                "category_label": "Best Overall"
            },
            {
                "name": "Bitly",
                "domain": "bitly.com",
                "url": "https://bitly.com",
                "description": "Popular URL shortener and link analytics platform.",
                "reason": "Established, reliable short link service.",
                "primary_task": "Shorten long URLs",
                "relevance_score": 0.95,
                "tags": ["free", "trusted"],
                "category_label": "Popular / Trusted"
            },
            {
                "name": "TinyURL",
                "domain": "tinyurl.com",
                "url": "https://tinyurl.com",
                "description": "Classic online link shortening tool.",
                "reason": "Instant short link generator without mandatory sign up.",
                "primary_task": "Shorten long URLs",
                "relevance_score": 0.93,
                "tags": ["free", "fast"],
                "category_label": "Instant Free Tool"
            }
        ]
    },
    "file-transfer": {
        "category": "File Sharing",
        "sub_category": "Large File Transfer",
        "primary_task": "Send large files to recipients over the internet",
        "input_type": "Large File",
        "output_type": "Download Link",
        "keywords": ["send large files", "transfer file", "wetransfer", "share file", "upload file", "file transfer"],
        "alternatives": [
            {
                "name": "WeTransfer",
                "domain": "wetransfer.com",
                "url": "https://wetransfer.com",
                "description": "Simple online file transfer service up to 2GB free.",
                "reason": "Industry standard for quick large file sharing.",
                "primary_task": "Send large files",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "SwissTransfer",
                "domain": "swisstransfer.com",
                "url": "https://www.swisstransfer.com",
                "description": "Free secure file transfer up to 50GB hosted in Switzerland.",
                "reason": "Highly secure, 50GB free limit with strict Swiss privacy.",
                "primary_task": "Send large files",
                "relevance_score": 0.96,
                "tags": ["free", "privacy", "fast"],
                "category_label": "Privacy & 50GB Free"
            },
            {
                "name": "Wormhole",
                "domain": "wormhole.app",
                "url": "https://wormhole.app",
                "description": "End-to-end encrypted fast file sharing.",
                "reason": "End-to-end encryption for sensitive file transfers.",
                "primary_task": "Send large files",
                "relevance_score": 0.94,
                "tags": ["free", "privacy"],
                "category_label": "Encrypted Privacy"
            }
        ]
    },
    "video-editing": {
        "category": "Media Tools",
        "sub_category": "Online Video Editor",
        "primary_task": "Edit, trim, crop, or create videos in browser",
        "input_type": "Video File",
        "output_type": "Edited Video",
        "keywords": ["video editor", "edit video online", "capcut", "veed", "clipchamp", "trim video"],
        "alternatives": [
            {
                "name": "CapCut Online",
                "domain": "capcut.com",
                "url": "https://www.capcut.com",
                "description": "All-in-one online video editor with AI tools & templates.",
                "reason": "Comprehensive browser-based video editing platform.",
                "primary_task": "Edit videos online",
                "relevance_score": 0.97,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "VEED.IO",
                "domain": "veed.io",
                "url": "https://www.veed.io",
                "description": "Simple online video editor with auto subtitles & text.",
                "reason": "Fast video editing with automatic caption generator.",
                "primary_task": "Edit videos online",
                "relevance_score": 0.95,
                "tags": ["free", "fast"],
                "category_label": "Fast Auto Subtitles"
            },
            {
                "name": "Microsoft Clipchamp",
                "domain": "clipchamp.com",
                "url": "https://clipchamp.com",
                "description": "Official Microsoft online video editor.",
                "reason": "Trusted, clean video editor with high resolution export.",
                "primary_task": "Edit videos online",
                "relevance_score": 0.93,
                "tags": ["free", "trusted"],
                "category_label": "Official Microsoft Tool"
            }
        ]
    },
    "file-conversion": {
        "category": "File Tools",
        "sub_category": "Format Conversion",
        "primary_task": "Convert file formats (audio, video, document, image)",
        "input_type": "Source File",
        "output_type": "Converted File",
        "keywords": ["convert file", "file converter", "mp4 to mp3", "epub to pdf", "format converter", "cloudconvert"],
        "alternatives": [
            {
                "name": "CloudConvert",
                "domain": "cloudconvert.com",
                "url": "https://cloudconvert.com",
                "description": "Universal online file converter supporting 200+ formats.",
                "reason": "High quality conversions with strict file privacy.",
                "primary_task": "Convert file formats",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "privacy", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Convertio",
                "domain": "convertio.co",
                "url": "https://convertio.co",
                "description": "Advanced online tool that converts any file format.",
                "reason": "Fast drag-and-drop file converter.",
                "primary_task": "Convert file formats",
                "relevance_score": 0.95,
                "tags": ["free", "fast"],
                "category_label": "Fast"
            }
        ]
    },
    "code-editor": {
        "category": "Development",
        "sub_category": "Online IDE",
        "primary_task": "Write, run, and test code online in browser",
        "input_type": "Source Code",
        "output_type": "Execution Output",
        "keywords": ["online ide", "code editor", "replit", "stackblitz", "codesandbox", "run python", "run code", "code online", "developer"],
        "alternatives": [
            {
                "name": "Replit",
                "domain": "replit.com",
                "url": "https://replit.com",
                "description": "Collaborative browser-based IDE supporting 50+ languages.",
                "reason": "Instant full-stack cloud coding environment.",
                "primary_task": "Write and run code",
                "relevance_score": 0.97,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "StackBlitz",
                "domain": "stackblitz.com",
                "url": "https://stackblitz.com",
                "description": "Instant WebContainer-powered online IDE for Web apps.",
                "reason": "Instant Node.js environment running directly inside browser.",
                "primary_task": "Write and run web code",
                "relevance_score": 0.95,
                "tags": ["free", "fast", "privacy"],
                "category_label": "In-Browser WebContainers"
            }
        ]
    },
    "ai-chatbot": {
        "category": "AI Assistant",
        "sub_category": "AI Chatbot",
        "primary_task": "Conversational AI chat, answer research questions, and generate text",
        "input_type": "Prompt Text",
        "output_type": "AI Response",
        "keywords": ["chatgpt", "claude", "perplexity", "gpt", "chatbot", "ai assistant", "gemini ai", "copilot"],
        "alternatives": [
            {
                "name": "ChatGPT",
                "domain": "chatgpt.com",
                "url": "https://chatgpt.com",
                "description": "Official conversational AI model by OpenAI.",
                "reason": "Industry-leading AI assistant for research, coding, and writing.",
                "primary_task": "Conversational AI assistant",
                "relevance_score": 0.98,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Best Overall"
            },
            {
                "name": "Claude AI",
                "domain": "claude.ai",
                "url": "https://claude.ai",
                "description": "Advanced AI assistant created by Anthropic.",
                "reason": "High accuracy and privacy standards for AI research.",
                "primary_task": "Conversational AI assistant",
                "relevance_score": 0.96,
                "tags": ["free", "privacy", "trusted"],
                "category_label": "Privacy & Accuracy"
            },
            {
                "name": "Perplexity AI",
                "domain": "perplexity.ai",
                "url": "https://www.perplexity.ai",
                "description": "AI answer engine with live web sources & citations.",
                "reason": "Real-time web search and citation research.",
                "primary_task": "AI research search engine",
                "relevance_score": 0.95,
                "tags": ["free", "fast", "trusted"],
                "category_label": "Real-time Search"
            }
        ]
    }
}

# ---------------------------------------------------------------------------
# DOMAIN NORMALIZATION & VALIDATION
# ---------------------------------------------------------------------------
def normalize_domain(url_or_domain: str) -> str:
    """Extract clean domain (e.g. 'sub.example.com' -> 'example.com')"""
    if not url_or_domain:
        return ""
    text = url_or_domain.lower().strip()
    if "://" in text:
        text = urlparse(text).netloc
    text = text.split(":")[0]  # strip port
    parts = text.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return text

def validate_and_rank_alternatives(
    scanned_url: str,
    raw_alternatives: List[Dict[str, Any]],
    detected_category: str = ""
) -> List[Dict[str, Any]]:
    """Strictly validates, filters out generic AI tools if irrelevant, removes duplicates, and ranks by relevance."""
    scanned_norm = normalize_domain(scanned_url)
    is_ai_category = "ai" in detected_category.lower() or "chatbot" in detected_category.lower()
    seen_domains = set()
    cleaned = []

    for item in raw_alternatives:
        name = item.get("name", "").strip()
        url = item.get("url", "").strip()
        domain = item.get("domain", "").strip() or normalize_domain(url)
        item_norm = normalize_domain(domain)
        description = item.get("description", "").strip()
        reason = item.get("reason", "").strip()
        primary_task = item.get("primary_task", "")
        relevance_score = float(item.get("relevance_score", 0.90))
        tags = item.get("tags", [])
        category_label = item.get("category_label", "Popular / Trusted")

        # 1. Reject invalid HTTPS URLs or blank names
        if not url.startswith("https://") or not domain or len(name) < 2:
            continue

        # 2. Reject self-reference
        if item_norm == scanned_norm or item_norm in scanned_norm:
            continue

        # 3. HARD RULE: Reject generic AI chatbots (ChatGPT, Claude, Perplexity, Gemini) UNLESS site is an AI chatbot!
        if item_norm in GENERIC_AI_DOMAINS and not is_ai_category:
            print(f"[Alternatives] Hard Anti-Generic Filter REJECTED {item_norm} for non-AI category '{detected_category}'")
            continue

        # 4. Deduplicate
        if item_norm in seen_domains:
            continue
        seen_domains.add(item_norm)

        cleaned.append({
            "name": name,
            "domain": domain,
            "url": url,
            "description": description,
            "reason": reason,
            "primary_task": primary_task,
            "relevance_score": relevance_score,
            "tags": tags,
            "category_label": category_label,
            "confidence": relevance_score
        })

    # Sort strictly by task relevance score descending
    cleaned.sort(key=lambda x: x["relevance_score"], reverse=True)
    return cleaned[:4]

# ---------------------------------------------------------------------------
# PROVIDER 1: GEMINI TASK-ORIENTED RECOMMENDATION ENGINE
# ---------------------------------------------------------------------------
async def query_gemini_alternatives(
    scanned_url: str,
    page_title: str,
    page_text: str
) -> Optional[Dict[str, Any]]:
    """Queries Gemini SLM to identify the EXACT USER TASK and generate task-specific alternatives."""
    api_key = settings.GEMINI_API_KEY
    if not api_key:
        return None

    domain = normalize_domain(scanned_url)
    clean_title = re.sub(r'[\r\n\t]', ' ', page_title[:150])
    clean_text = re.sub(r'[\r\n\t]', ' ', page_text[:500])

    prompt = f"""
You are an expert security & alternative recommendation assistant for ScamShield.
Your goal is to identify the EXACT USER TASK performed by the scanned webpage and recommend 3 legitimate alternative websites that solve the SAME USER PROBLEM.

ABSOLUTE MANDATORY RULES:
1. Do NOT recommend generic popular websites.
2. Do NOT recommend ChatGPT, Claude, Perplexity, Gemini, or other AI chatbots UNLESS the scanned website's PRIMARY FUNCTION is itself an AI chatbot or AI writing assistant.
3. Identify the EXACT task the user is coming to accomplish (e.g. "Compress PDF files", "Shorten URLs", "Remove image background", "Convert file formats").
4. Alternatives MUST perform the exact same job.
5. Do NOT recommend {domain} itself.

SCANNED WEBPAGE INPUT (Untrusted data):
Domain: {domain}
Title: {clean_title}
Content Snippet: {clean_text}

Return ONLY valid JSON matching this exact schema:
{{
  "primary_task": "Exact task the user is trying to perform",
  "category": "Main Category (e.g. PDF Tools, Image Tools, Web Utilities)",
  "sub_category": "Subcategory (e.g. PDF Compression)",
  "input_type": "Input type (e.g. PDF file)",
  "output_type": "Output type (e.g. compressed PDF)",
  "alternatives": [
    {{
      "name": "Service Name",
      "domain": "example.com",
      "url": "https://www.example.com",
      "description": "Short description of what the tool does",
      "reason": "Why this is a safer alternative for this specific task",
      "primary_task": "Same user task",
      "relevance_score": 0.95,
      "tags": ["free", "fast", "privacy", "trusted"],
      "category_label": "Best Overall"
    }}
  ]
}}
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.1, "responseMimeType": "application/json"}
    }

    try:
        print(f"[Alternatives] Querying Gemini for task-first recommendations on {domain}...")
        async with httpx.AsyncClient(timeout=10.0) as client:
            res = await client.post(url, json=payload)
            if res.status_code == 200:
                data = res.json()
                raw_json_str = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                parsed = json.loads(raw_json_str)
                if isinstance(parsed, dict) and "alternatives" in parsed and len(parsed["alternatives"]) > 0:
                    print(f"[Alternatives] Gemini identified task: '{parsed.get('primary_task')}'")
                    return parsed
            elif res.status_code == 429:
                print("[Alternatives] Gemini API 429 rate-limited. Handing off to local fallback.")
    except Exception as exc:
        print(f"[Alternatives] Gemini query exception: {exc}")

    return None

# ---------------------------------------------------------------------------
# PROVIDER 2: TASK-MATCHED LOCAL FALLBACK ENGINE
# ---------------------------------------------------------------------------
def get_local_fallback_alternatives(
    scanned_url: str,
    page_title: str,
    page_text: str
) -> Dict[str, Any]:
    """Matches webpage content against curated task taxonomy with zero API calls."""
    print("[Alternatives] Executing Task-Matched Local Fallback Engine...")
    combined = f"{scanned_url} {page_title} {page_text[:500]}".lower()

    best_match = None
    max_hits = 0

    for cat_id, cat_info in CURATED_TASK_TAXONOMY.items():
        hits = sum(1 for kw in cat_info["keywords"] if kw in combined)
        if hits > max_hits:
            max_hits = hits
            best_match = cat_info

    if best_match and max_hits > 0:
        return {
            "primary_task": best_match["primary_task"],
            "category": best_match["category"],
            "sub_category": best_match.get("sub_category"),
            "input_type": best_match.get("input_type"),
            "output_type": best_match.get("output_type"),
            "alternatives": best_match["alternatives"]
        }

    # GRACEFUL EMPTY STATE (If task cannot be identified, DO NOT fabricate generic AI tools!)
    domain = normalize_domain(scanned_url) or "this website"
    return {
        "primary_task": f"Services on {domain}",
        "category": "Unknown Category",
        "sub_category": "Uncertain Purpose",
        "alternatives": []  # Empty array so UI displays polite graceful notice
    }

# ---------------------------------------------------------------------------
# COMPOSITE ORCHESTRATOR
# ---------------------------------------------------------------------------
async def get_safer_alternatives(
    page_url: str,
    page_title: str = "",
    page_text: str = "",
    db_session = None
) -> Dict[str, Any]:
    """Main orchestrator for discovering task-specific alternative recommendations."""
    domain = normalize_domain(page_url)
    start_time = time.time()

    # Priority 1: Check Database Cache
    if db_session and domain:
        try:
            from ..models import RecommendationCache
            cached_item = db_session.query(RecommendationCache).filter(RecommendationCache.domain == domain).first()
            if cached_item:
                print(f"[Alternatives] Cache hit for domain: {domain}")
                parsed_alts = json.loads(cached_item.alternatives_json)
                category_name = cached_item.category or "Web Utility"
                ranked = validate_and_rank_alternatives(page_url, parsed_alts, detected_category=category_name)
                return {
                    "primary_task": cached_item.purpose or f"Task on {domain}",
                    "category": category_name,
                    "sub_category": "Cached Result",
                    "provider_source": "cache",
                    "alternatives": ranked
                }
        except Exception as err:
            print(f"[Alternatives] Cache lookup error: {err}")

    # Priority 2: Gemini Provider
    gemini_res = await query_gemini_alternatives(page_url, page_title, page_text)
    provider_used = "gemini"

    # Priority 3: Task-Matched Local Fallback
    if not gemini_res or not gemini_res.get("alternatives"):
        gemini_res = get_local_fallback_alternatives(page_url, page_title, page_text)
        provider_used = "local_fallback"

    primary_task = gemini_res.get("primary_task", f"Services on {domain}")
    category = gemini_res.get("category", "Web Service")
    sub_category = gemini_res.get("sub_category", "")
    raw_alts = gemini_res.get("alternatives", [])

    # Priority 4: Task Validation & Anti-Generic Filter
    ranked_alts = validate_and_rank_alternatives(page_url, raw_alts, detected_category=category)

    # Save to Cache if valid alternatives found
    if db_session and domain and ranked_alts:
        try:
            from ..models import RecommendationCache
            new_cache = RecommendationCache(
                domain=domain,
                purpose=primary_task,
                category=category,
                alternatives_json=json.dumps(ranked_alts),
                provider_source=provider_used
            )
            db_session.merge(new_cache)
            db_session.commit()
            print(f"[Alternatives] Task-specific recommendations cached for: {domain}")
        except Exception as c_err:
            print(f"[Alternatives] Failed to save cache: {c_err}")

    print(f"[Alternatives] Execution finished in {int((time.time() - start_time)*1000)}ms via provider: {provider_used}")
    return {
        "primary_task": primary_task,
        "category": category,
        "sub_category": sub_category,
        "input_type": gemini_res.get("input_type"),
        "output_type": gemini_res.get("output_type"),
        "provider_source": provider_used,
        "alternatives": ranked_alts
    }


def find_safe_alternative(page_url: str = "", page_title: str = "", page_text: str = "") -> Optional[Dict[str, str]]:
    """Backwards-compatibility helper for single alt card."""
    fallback = get_local_fallback_alternatives(page_url, page_title, page_text)
    if fallback and fallback.get("alternatives"):
        top = fallback["alternatives"][0]
        return {
            "name": top["name"],
            "url": top["url"],
            "explanation": top["reason"]
        }
    return None
