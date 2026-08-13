import os
import re
import json
import validators
import yaml
from typing import List, Dict, Any

RULES_FILE = os.path.join(os.path.dirname(__file__), "rules.yaml")
with open(RULES_FILE, "r", encoding="utf-8") as f:
    RULES_DATA = yaml.safe_load(f)
    RULES = RULES_DATA["rules"]

URL_REGEX = re.compile(r"https?://[\w\-\.\?\#\&\=\/\%]+", re.IGNORECASE)

def extract_urls(text: str) -> List[str]:
    return [u for u in URL_REGEX.findall(text) if validators.url(u)]

def mask_sensitive(message: str) -> str:
    return re.sub(r"\b\d{4,6}\b", "****", message)

def get_risk_level(score: int) -> str:
    if score < 25:
        return "Low"
    if score < 50:
        return "Suspicious"
    if score < 75:
        return "High"
    return "Critical"

def recommendation_for(level: str) -> str:
    mapping = {
        "Low": "Message appears safe, but stay vigilant.",
        "Suspicious": "Check the sender and avoid clicking links.",
        "High": "Do NOT interact with links; verify with the sender through a trusted channel.",
        "Critical": "Strongly avoid any interaction; report as potential scam.",
    }
    return mapping.get(level, "Stay cautious.")

def evaluate_rules(message: str, urls: List[str], sender_contact: str | None) -> List[Dict[str, Any]]:
    triggered = []
    # Build context dictionary containing global helper names
    context = {
        "__builtins__": __builtins__,
        "message": message,
        "urls": urls,
        "sender_contact": sender_contact,
        "re": re,
    }
    for rule in RULES:
        try:
            # Pass context as globals so list comprehensions can access message, urls, sender_contact
            if eval(rule["condition"], context):
                triggered.append({
                    "rule": rule["name"],
                    "points": rule["points"],
                    "explanation": rule["description"],
                    "evidence": _extract_evidence(rule["condition"], message, urls, sender_contact),
                })
        except Exception:
            continue
    return triggered

def _extract_evidence(condition: str, message: str, urls: List[str], sender_contact: str | None) -> str:
    keywords = re.findall(r'"([^"]+)"', condition)
    for kw in keywords:
        if kw.lower() in message.lower():
            return f"Found '{kw}' in message"
        for u in urls:
            if kw.lower() in u.lower():
                return f"Found '{kw}' in URL {u}"
        if sender_contact and kw.lower() in sender_contact.lower():
            return f"Found '{kw}' in sender contact"
    return "Rule condition matched"

def analyze_message(message_text: str, sender: str | None, sender_contact: str | None, explicit_url: str | None = None) -> Dict[str, Any]:
    urls = extract_urls(message_text)
    if explicit_url:
        urls.append(explicit_url)

    masked_message = mask_sensitive(message_text)
    red_flags = evaluate_rules(message_text, urls, sender_contact)

    total = sum(flag["points"] for flag in red_flags)
    risk_score = min(total, 100)
    risk_level = get_risk_level(risk_score)
    verdict = {
        "Low": "Probably safe",
        "Suspicious": "Needs caution",
        "High": "Likely scam",
        "Critical": "Likely phishing",
    }[risk_level]

    recommendation = recommendation_for(risk_level)

    return {
        "masked_message": masked_message,
        "extracted_urls": urls,
        "risk_score": risk_score,
        "risk_level": risk_level,
        "verdict": verdict,
        "red_flags": red_flags,
        "recommendation": recommendation,
    }
