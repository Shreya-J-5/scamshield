from app.services.analyzer import analyze_message, extract_urls, mask_sensitive

def test_extract_urls():
    text = "Check out https://bit.ly/3xYz and http://192.168.1.1/login for details"
    urls = extract_urls(text)
    assert len(urls) == 2
    assert "https://bit.ly/3xYz" in urls

def test_mask_sensitive():
    text = "Your OTP is 482910 and CVV is 123"
    masked = mask_sensitive(text)
    assert "****" in masked
    assert "482910" not in masked

def test_analyze_scam_message():
    message = "URGENT! Your bank account will be blocked today. Click https://bit.ly/verify-kyc to enter your OTP and PIN."
    res = analyze_message(message, sender="Bank", sender_contact="alert@suspicious.com")
    assert res["risk_score"] > 50
    assert res["risk_level"] in ["High", "Critical"]
    assert len(res["red_flags"]) >= 3

def test_analyze_safe_message():
    message = "Hey team, the project meeting is scheduled for tomorrow at 10 AM. See you there!"
    res = analyze_message(message, sender="Colleague", sender_contact="colleague@gmail.com")
    assert res["risk_score"] < 25
    assert res["risk_level"] == "Low"
    assert res["verdict"] == "Probably safe"
