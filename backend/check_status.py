import os
import sys
import time
import httpx
from dotenv import load_dotenv

load_dotenv()

# Force utf-8 encoding for stdout output on Windows
sys.stdout.reconfigure(encoding='utf-8')

print("\n" + "="*65)
print(" ***   SCAMSHIELD BACKEND & API QUOTA DIAGNOSTIC REPORT   ***")
print("="*65)

# 1. Test Local Backend
backend_url = "http://127.0.0.1:8000/health"
try:
    start = time.time()
    r = httpx.get(backend_url, timeout=3.0)
    elapsed = int((time.time() - start) * 1000)
    if r.status_code == 200:
        print(f" [+] Backend Server (Local)      : ONLINE (127.0.0.1:8000) - {elapsed}ms")
    else:
        print(f" [!] Backend Server (Local)      : HTTP {r.status_code}")
except Exception as e:
    print(f" [-] Backend Server (Local)      : OFFLINE ({e})")

# 2. Test Gemini API Key & Model
gemini_key = os.getenv("GEMINI_API_KEY")
if gemini_key:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={gemini_key}"
    payload = {"contents": [{"parts": [{"text": "Hello"}]}], "generationConfig": {"maxOutputTokens": 5}}
    try:
        start = time.time()
        r = httpx.post(url, json=payload, timeout=5.0)
        elapsed = int((time.time() - start) * 1000)
        if r.status_code == 200:
            print(f" [+] Gemini SLM (gemini-flash)   : ACTIVE (200 OK) - {elapsed}ms")
            print("     +-- Quota: 15 Requests/Min | 1,500 Requests/Day (Free Tier)")
        else:
            print(f" [!] Gemini SLM (gemini-flash)   : HTTP {r.status_code}")
    except Exception as e:
        print(f" [-] Gemini SLM (gemini-flash)   : ERROR ({e})")
else:
    print(" [!] Gemini SLM                  : KEY NOT SET")

# 3. Test Google Safe Browsing
gsb_key = os.getenv("GOOGLE_SAFE_BROWSING_API_KEY")
if gsb_key:
    url = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={gsb_key}"
    body = {
        "client": {"clientId": "scamshield", "clientVersion": "1.0"},
        "threatInfo": {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING"],
            "platformTypes": ["ANY_PLATFORM"],
            "threatEntryTypes": ["URL"],
            "threatEntries": [{"url": "http://example.com"}]
        }
    }
    try:
        start = time.time()
        r = httpx.post(url, json=body, timeout=5.0)
        elapsed = int((time.time() - start) * 1000)
        if r.status_code == 200:
            print(f" [+] Google Safe Browsing API  : ACTIVE (200 OK) - {elapsed}ms")
            print("     +-- Quota: 10,000 Queries/Day")
        else:
            print(f" [!] Google Safe Browsing API  : HTTP {r.status_code}")
    except Exception as e:
        print(f" [-] Google Safe Browsing API  : ERROR ({e})")

# 4. Test VirusTotal API
vt_key = os.getenv("VIRUSTOTAL_API_KEY")
if vt_key:
    print(f" [+] VirusTotal API Key          : CONFIGURED ({vt_key[:8]}...)")
    print("     +-- Quota: 4 Requests/Min | 500 Requests/Day")

print("="*65 + "\n")
