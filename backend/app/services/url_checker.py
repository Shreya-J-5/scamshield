from abc import ABC, abstractmethod
from typing import List, Dict, Any
import httpx
import re
from ..config import settings

class URLReputationProvider(ABC):
    @abstractmethod
    async def check_url(self, url: str) -> Dict[str, Any]:
        """Check a single URL and return dict: {"is_malicious": bool, "details": str, "provider": str}"""
        pass

from urllib.parse import urlparse

TRUSTED_DOMAINS = {
    "chatgpt.com", "openai.com", "google.com", "github.com", "microsoft.com",
    "apple.com", "amazon.com", "youtube.com", "linkedin.com", "twitter.com",
    "x.com", "stackoverflow.com", "wikipedia.org", "reddit.com", "netflix.com",
    "cloudflare.com", "zoom.us", "slack.com", "notion.so", "figma.com",
    "canva.com", "dropbox.com", "spotify.com", "huggingface.co"
}

def is_trusted_domain(url: str) -> bool:
    try:
        netloc = urlparse(url).netloc.lower().split(":")[0]
        for td in TRUSTED_DOMAINS:
            if netloc == td or netloc.endswith("." + td):
                return True
    except Exception:
        pass
    return False

class LocalHeuristicURLChecker(URLReputationProvider):
    SUSPICIOUS_TLDS = [".xyz", ".top", ".club", ".work", ".info", ".kim", ".gq", ".cf", ".tk", ".ml", ".ga"]
    SHORTENERS = ["bit.ly", "tinyurl.com", "t.co", "goo.gl", "is.gd", "buff.ly", "ow.ly", "rb.gy"]

    async def check_url(self, url: str) -> Dict[str, Any]:
        url_lower = url.lower()
        reasons = []

        # Skip heuristic flags if URL belongs to a verified trusted domain
        if is_trusted_domain(url):
            return {
                "is_malicious": False,
                "details": "Verified Official Trusted Domain",
                "provider": "LocalHeuristics"
            }

        # Check for IP address host
        if re.search(r"https?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", url_lower):
            reasons.append("URL uses raw IP address instead of domain name")

        # Check for HTTP instead of HTTPS
        if url_lower.startswith("http://"):
            reasons.append("URL uses unencrypted HTTP protocol")

        # Check for shorteners
        if any(shortener in url_lower for shortener in self.SHORTENERS):
            reasons.append("URL uses a known link shortening service")

        # Check for suspicious TLDs
        if any(url_lower.endswith(tld) or f"{tld}/" in url_lower for tld in self.SUSPICIOUS_TLDS):
            reasons.append("URL uses a high-risk top-level domain")

        # Check for suspicious keywords in domain/path
        suspicious_keywords = ["login", "verify", "secure", "banking", "update-account", "free-claim", "kyc"]
        if any(kw in url_lower for kw in suspicious_keywords):
            reasons.append("URL contains security or credential target keywords")

        is_malicious = len(reasons) > 0
        details = "; ".join(reasons) if reasons else "No obvious heuristic red flags found in URL string"

        return {
            "is_malicious": is_malicious,
            "details": details,
            "provider": "LocalHeuristics"
        }


class GoogleSafeBrowsingProvider(URLReputationProvider):
    async def check_url(self, url: str) -> Dict[str, Any]:
        api_key = settings.GOOGLE_SAFE_BROWSING_API_KEY
        if not api_key:
            return {"is_malicious": False, "details": "Google Safe Browsing API key not configured", "provider": "GoogleSafeBrowsing"}

        endpoint = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}"
        payload = {
            "client": {"clientId": "ScamShield", "clientVersion": "1.0.0"},
            "threatInfo": {
                "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
                "platformTypes": ["ANY_PLATFORM"],
                "threatEntryTypes": ["URL"],
                "threatEntries": [{"url": url}]
            }
        }

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.post(endpoint, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    matches = data.get("matches", [])
                    if matches:
                        threats = [m.get("threatType") for m in matches]
                        return {
                            "is_malicious": True,
                            "details": f"Flagged by Google Safe Browsing: {', '.join(threats)}",
                            "provider": "GoogleSafeBrowsing"
                        }
        except Exception:
            pass  # Fallback gracefully on API errors or timeouts

        return {"is_malicious": False, "details": "Clean according to Google Safe Browsing", "provider": "GoogleSafeBrowsing"}

class VirusTotalProvider(URLReputationProvider):
    async def check_url(self, url: str) -> Dict[str, Any]:
        api_key = settings.VIRUSTOTAL_API_KEY
        if not api_key:
            return {"is_malicious": False, "details": "VirusTotal API key not configured", "provider": "VirusTotal"}

        # VirusTotal URL lookup requires base64 URL identifier without padding
        import base64
        url_id = base64.urlsafe_b64encode(url.encode()).decode().strip("=")
        endpoint = f"https://www.virustotal.com/api/v3/urls/{url_id}"
        headers = {"x-apikey": api_key}

        try:
            async with httpx.AsyncClient(timeout=3.0) as client:
                response = await client.get(endpoint, headers=headers)
                if response.status_code == 200:
                    data = response.json()
                    stats = data.get("data", {}).get("attributes", {}).get("last_analysis_stats", {})
                    malicious = stats.get("malicious", 0)
                    suspicious = stats.get("suspicious", 0)
                    if malicious > 0 or suspicious > 0:
                        return {
                            "is_malicious": True,
                            "details": f"VirusTotal detected {malicious} malicious & {suspicious} suspicious vendor reports",
                            "provider": "VirusTotal"
                        }
        except Exception:
            pass

        return {"is_malicious": False, "details": "No malicious reports on VirusTotal", "provider": "VirusTotal"}

class CompositeURLChecker:
    def __init__(self):
        self.providers: List[URLReputationProvider] = [
            LocalHeuristicURLChecker(),
            GoogleSafeBrowsingProvider(),
            VirusTotalProvider()
        ]

    async def check_urls(self, urls: List[str]) -> List[Dict[str, Any]]:
        results = []
        for u in urls[:10]:  # Limit URL checks to top 10 for performance
            for provider in self.providers:
                res = await provider.check_url(u)
                if res["is_malicious"]:
                    results.append({"url": u, **res})
                    break  # Stop checking this URL once flagged
        return results
