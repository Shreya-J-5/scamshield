# 🛡️ ScamShield: Real Time Scam and Phishing Detection System

ScamShield is an open source security platform designed to detect suspicious SMS messages, emails, phishing links, and malicious web pages in real time. It uses a configurable rule based engine along with privacy preserving heuristics.

The project includes a FastAPI backend, a modern React web dashboard, and a Chrome Extension (Manifest V3) for scanning web pages directly from your browser.

---

## 🚀 Key Features

* 🔍 **Smart Heuristic Engine**: Scans text and URLs against 12+ security rules including urgency patterns, credential requests, shorteners, and raw IP links.
* 🛡️ **Multi Layer Protection**: Evaluates domain structures, security flags, and URL patterns.
* 🔐 **Privacy Preserving**: Sensitive numbers such as OTPs, PINs, and CVVs are automatically masked before saving or processing.
* 📊 **Cybersecurity Dashboard**: Interactive web dashboard built with React and Vite to view threat analytics, paste messages, and review scan history.
* 🧩 **Chrome Extension (Manifest V3)**: Inspect active web pages and links in one click with real time risk scores and human readable red flags.
* ⚡ **Offline Friendly**: Works completely offline out of the box using local heuristic rules.

---

## 🏗️ System Architecture

```
                      ┌──────────────────────┐
                      │    Chrome Extension  │
                      │    (Manifest V3)     │
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │    FastAPI Backend   │
                      │   (Python & SQLite)  │
                      └──────────┬───────────┘
                                 │
                                 ▼
                      ┌──────────────────────┐
                      │    Local Heuristic   │
                      │     Rule Engine      │
                      └──────────────────────┘
```

---

## 🛠️ Project Structure

```
scamshield/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── main.py           # Entry point and CORS setup
│   │   ├── config.py         # App configuration
│   │   ├── database.py       # SQLAlchemy SQLite setup
│   │   ├── models.py         # DB models
│   │   ├── schemas.py        # Pydantic validation models
│   │   ├── routes/           # API routes (analyze, scans, health)
│   │   └── services/         # Rule engine and URL checker
│   ├── tests/                # Test suite
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Environment template
├── frontend/                 # React Web Dashboard
│   ├── src/                  # React components, pages, and API service
│   ├── package.json          # Node dependencies
│   └── vite.config.js        # Vite build configuration
├── extension/                # Chrome Extension (Manifest V3)
│   ├── manifest.json         # Extension manifest
│   ├── background.js         # Service worker
│   ├── content.js            # Page extractor script
│   ├── popup.html            # Extension UI popup
│   ├── popup.css             # Extension styling
│   └── popup.js              # Popup controller script
└── README.md
```

---

## 💻 Quickstart Setup Guide

### 1. Prerequisites
* Python 3.10 or higher
* Node.js 18 or higher
* Google Chrome browser

---

### 2. Backend Setup (FastAPI)

Navigate to the `backend` folder and set up your virtual environment:

```bash
cd backend
python -m venv venv
```

Activate the environment:
* **Windows (PowerShell)**: `.\venv\Scripts\activate`
* **Linux / macOS**: `source venv/bin/activate`

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file inside the `backend` directory based on `.env.example`:
```env
DEBUG=True
DATABASE_URL=sqlite:///./scamshield.db
```

Start the FastAPI backend server:
```bash
python -m uvicorn app.main:app --reload --port 8000
```
The backend API will run at `http://127.0.0.1:8000`. You can test endpoints via Swagger docs at `http://127.0.0.1:8000/docs`.

---

### 3. Frontend Setup (React Dashboard)

In a new terminal window, navigate to the `frontend` folder:

```bash
cd frontend
npm install
npm run dev
```
The web dashboard will open at `http://localhost:5173`.

---

### 4. Chrome Extension Setup

1. Open Google Chrome and navigate to `chrome://extensions`.
2. Enable **Developer mode** in the top right corner.
3. Click **Load unpacked** in the top left.
4. Select the `scamshield/extension` directory.
5. Click the extension icon on any open web page to run a security scan.

---

## 🧪 Testing the API with Curl

Evaluate a suspicious message:
```bash
curl -X POST "http://127.0.0.1:8000/api/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "message_text": "URGENT: Your bank account will be blocked today. Click http://192.168.1.1/login to enter your OTP and PIN.",
    "sender": "HDFC Alert",
    "sender_contact": "kyc-update@suspicious.com"
  }'
```

---

## 🔒 Privacy and Security

ScamShield masks sensitive numerical patterns such as OTPs, 4 to 6 digit verification codes, and credit card numbers before saving them to the database or passing them to processing services.

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
