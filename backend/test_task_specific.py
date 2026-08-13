import sys
import asyncio
import httpx

sys.stdout.reconfigure(encoding='utf-8')

BASE_URL = "http://127.0.0.1:8000"

GENERIC_AI_DOMAINS = {"chatgpt.com", "claude.ai", "perplexity.ai", "gemini.google.com"}

TEST_CASES = [
    {
        "name": "PDF Compression Tool",
        "url": "http://scam-pdf-compressor-free.xyz",
        "title": "Free PDF Compress & Reduce File Size Online",
        "text": "Compress your PDF file size instantly online.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["pdf", "ilovepdf", "smallpdf", "pdf24"]
    },
    {
        "name": "Image Compressor",
        "url": "http://free-image-compressor-online.top",
        "title": "Compress PNG and JPEG Images Online",
        "text": "Reduce image size without losing visual quality. Tiny PNG compressor tool.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["tinypng", "squoosh", "compress"]
    },
    {
        "name": "Background Remover",
        "url": "http://online-bg-remover-scam.xyz",
        "title": "Remove Background From Image Free",
        "text": "Cut out image backgrounds automatically in seconds.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["remove.bg", "adobe", "photoroom"]
    },
    {
        "name": "URL Shortener",
        "url": "http://suspicious-short-link-service.top",
        "title": "Shorten Long URLs Free Link Shortener",
        "text": "Create custom short links and track link clicks online.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["dub", "bitly", "tinyurl"]
    },
    {
        "name": "Large File Transfer",
        "url": "http://free-file-transfer-portal.xyz",
        "title": "Send Large Files Online Free",
        "text": "Transfer heavy files to email recipients instantly.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["wetransfer", "swisstransfer", "wormhole"]
    },
    {
        "name": "Browser Video Editor",
        "url": "http://scam-video-editor-online.top",
        "title": "Free Online Video Editor & Trimmer",
        "text": "Edit videos in browser. Add captions and trim MP4 videos.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["capcut", "veed", "clipchamp"]
    },
    {
        "name": "AI Chatbot",
        "url": "http://fake-ai-gpt-chatbot.xyz",
        "title": "Free Online AI Chatbot & Text Generator",
        "text": "Chat with AI model for writing, coding, and research.",
        "forbidden": set(),  # Here AI chatbots ARE allowed!
        "expected_kw": ["chatgpt", "claude", "perplexity"]
    },
    {
        "name": "Online Code Editor",
        "url": "http://malicious-online-ide.top",
        "title": "Write and Run Code Online - Cloud IDE",
        "text": "Run python and web code online inside browser environment.",
        "forbidden": GENERIC_AI_DOMAINS,
        "expected_kw": ["replit", "stackblitz"]
    }
]

async def run_task_test_suite():
    print("\n" + "="*75)
    print(" 🧪 SCAMSHIELD TASK-SPECIFIC RECOMMENDATION SUITE - 8 CATEGORY VERIFICATION")
    print("="*75)

    async with httpx.AsyncClient(timeout=10.0) as client:
        for idx, tc in enumerate(TEST_CASES, start=1):
            print(f"\n [{idx}/8] Testing: {tc['name']} ({tc['url']})...")
            payload = {
                "page_url": tc["url"],
                "page_title": tc["title"],
                "page_text": tc["text"],
                "links": [f"{tc['url']}/download"]  # Make it trigger risk score for testing
            }
            res = await client.post(f"{BASE_URL}/api/analyze-page", json=payload)
            data = res.json()
            alts_payload = data.get("safer_alternatives_data", {})
            alts_list = alts_payload.get("alternatives", [])
            recommended_domains = [a["domain"].lower() for a in alts_list]

            print(f"  └─ Risk Score     : {data['risk_score']} ({data['risk_level']})")
            print(f"  └─ Primary Task   : '{alts_payload.get('primary_task')}'")
            print(f"  └─ Category       : '{alts_payload.get('category')}'")
            print(f"  └─ Recommendations: {recommended_domains}")

            # 1. Verify Anti-Generic AI Filter (No ChatGPT/Claude/Perplexity on non-AI tasks!)
            if tc["forbidden"]:
                found_forbidden = tc["forbidden"].intersection(recommended_domains)
                print("  └─ Anti-Generic AI Filter Check: ", "PASSED (Zero AI Chatbots recommended)" if not found_forbidden else f"FAILED! Found {found_forbidden}")
                assert not found_forbidden, f"Generic AI domain {found_forbidden} found in non-AI category!"

            # 2. Verify Task Relevance (Must contain task-specific alternatives!)
            found_expected = any(kw in "".join(recommended_domains) for kw in tc["expected_kw"])
            print("  └─ Task Specificity Match      : ", "PASSED (Matched expected task alternatives)" if found_expected else "FAILED!")
            assert found_expected, f"Expected task alternatives {tc['expected_kw']} not found in {recommended_domains}"

    print("\n" + "="*75)
    print(" ALL 8 TASK-SPECIFIC CATEGORY TESTS PASSED PERFECTLY! ZERO GENERIC AI LEAKS!")
    print("="*75 + "\n")

if __name__ == "__main__":
    asyncio.run(run_task_test_suite())
