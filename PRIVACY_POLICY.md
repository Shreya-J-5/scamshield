# Privacy Policy for ScamShield Chrome Extension

**Last Updated:** August 13, 2026

ScamShield ("we", "our", or "us") is committed to protecting your privacy. This Privacy Policy explains how our Chrome extension collects, uses, and safeguards information when you use the ScamShield extension.

---

## 1. Information We Collect

ScamShield is built with privacy-first principles. We only process data required to perform real-time security scanning and phishing analysis:

- **Webpage Content & Metadata:** When you explicitly scan an active browser tab, ScamShield extracts page metadata (such as page title, current tab URL, meta descriptions, and on-page links) to evaluate scam and phishing risk indicators.
- **No Personal Identification (PII):** ScamShield does **NOT** collect your name, email address, passwords, payment information, browsing history, or personal identity details.
- **No Keystroke / Input Logging:** ScamShield does **NOT** monitor your keystrokes, form entries, or background web activity outside of explicitly triggered or automated security tab checks.

---

## 2. How We Use Information

The data processed by ScamShield is strictly used to:
- Detect phishing, scam signals, credential harvest attempts, and malicious links.
- Identify the primary task of a scanned website to recommend safer, legitimate web alternatives when a site is determined to be dangerous or suspicious.
- Perform threat analysis using our local classification taxonomy and external API engines (such as Google Gemini).

---

## 3. Data Processing & Third-Party Services

- **Local Processing:** Security signal rules, pattern matching, and fallback recommendations are executed locally on your device or via our backend proxy server.
- **AI Analysis:** To determine webpage functionality and generate context-aware safer alternatives, anonymized webpage metadata (page URL, title, and public text snippet) may be processed by AI model endpoints (such as Google Gemini API). No personal data or private user content is ever sent to AI models.
- **No Sale of Data:** We do **NOT** sell, rent, monetize, or share your data with third-party advertisers, data brokers, or marketing networks.

---

## 4. Data Storage & Retention

- ScamShield stores temporary scan results in local extension state and in a privacy-focused backend database cache (keying non-personal domain names to recommendations).
- We do not construct user browsing profiles or track individual users across websites.

---

## 5. User Rights & Control

- You can disable or uninstall the ScamShield extension at any time directly through Chrome's Extension Management page (`chrome://extensions`).
- Upon uninstallation, all extension local storage data is automatically purged from your browser.

---

## 6. Permissions Required

- **`activeTab`**: Allows ScamShield to access the URL and content of the currently open tab only when you initiate a scan or when real-time protection is active.
- **`scripting`**: Allows the extension to extract text and links from the scanned webpage to check for security red flags.
- **`storage`**: Used to save extension configuration and scan settings locally on your device.

---

## 7. Contact Us

If you have any questions or concerns regarding this Privacy Policy, please contact us via our official project repository:
- **Repository:** [https://github.com](https://github.com)
- **Support Email:** `privacy@scamshield.org`
