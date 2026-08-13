# ScamShield

ScamShield is a web security and scam/phishing analysis Chrome extension backed by an asynchronous FastAPI analysis engine and a modern React web dashboard. It inspects active web pages in real-time, extracts threat signals, calculates explainable risk scores, and automatically suggests task-specific safer alternatives when a scanned website is suspicious or dangerous.

---

## Overview

ScamShield provides instant, transparent webpage risk assessments directly in your browser:
- **Webpage & Message Scanning:** Analyzes active web pages, extracted links, titles, and text for phishing indicators, credential harvesting requests, urgency patterns, and raw IP links.
- **Explainable Risk Scoring:** Computes a transparent 0–100 risk score, categorized into clear risk levels (`Low`, `Suspicious`, `High`, `Critical`), accompanied by itemized red flags.
- **Task-First Safe Alternative Engine:** When a scanned website is determined to be high risk or suspicious, ScamShield identifies the website's primary functional purpose (e.g., PDF compression, URL shortening, file transfer) and recommends safer, verified web tools so users can accomplish their goals securely without risking malware or data theft.
- **Privacy-First Design:** Masks sensitive verification numbers (OTPs, PINs, card numbers) locally before logging, and operates without tracking personal browsing history.

*Note: ScamShield provides automated security risk assessments based on available signals and heuristics. No automated tool can guarantee 100% detection of every malicious website.*

---

## Features

- **Real-Time Webpage Scanner:** Scan the current active tab with a single click.
- **Explainable Security Signals:** View granular red flags (e.g. credential requests, prize promises, suspicious TLDs, IP-based URLs).
- **Risk Score & Meter:** Visual progress meter and risk level badge (`Low`, `Suspicious`, `High`, `Critical`).
- **Task-First Safer Alternatives:** Recommends verified alternatives matched by primary functional task (e.g. PDF compression, video editing, URL shortening) with zero-latency local fallback.
- **Hard Anti-Generic AI Filter:** Excludes generic AI chatbots when recommending alternatives for specialized web tools.
- **Interactive React Dashboard:** Manage scan history, view aggregated threat analytics, and run manual message analysis.
- **FastAPI Backend Service:** Asynchronous backend providing REST API endpoints for security scanning, reputation checks, and task discovery.

---

## Architecture

```text
Chrome Extension (Manifest V3)
        │
        │ HTTPS (JSON API)
        ▼
FastAPI Backend (Python)
        │
        ├──► Security & Reputation Services (Google Safe Browsing, VirusTotal)
        ├──► AI & Task Discovery Engine (Google Gemini API)
        ├──► Local Fallback Engine (Curated Task Taxonomy)
        └──► SQLite Database (Scans & Recommendation Cache)

React Web Dashboard
        │
        ▼
FastAPI Backend (JSON API)
```

---

## Project Structure

```text
scamshield/
├── backend/                  # FastAPI Application
│   ├── app/
│   │   ├── main.py           # Entry point and CORS setup
│   │   ├── config.py         # Application settings & environment variables
│   │   ├── database.py       # SQLAlchemy SQLite configuration
│   │   ├── models.py         # DB models (Scans & Cache)
│   │   ├── schemas.py        # Pydantic data validation models
│   │   ├── routes/           # API endpoints (analyze, scans, health)
│   │   └── services/         # Security rules, URL checker, alternatives engine
│   ├── tests/                # Test suite
│   ├── check_status.py       # API status checker
│   ├── test_task_specific.py # 8-category task recommendation test suite
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Backend environment template
├── extension/                # Chrome Extension (Manifest V3)
│   ├── manifest.json         # Extension manifest V3
│   ├── background.js         # Background service worker
│   ├── content.js            # Page content extractor script
│   ├── popup.html            # Dark-theme popup interface
│   ├── popup.css             # Cybersecurity theme stylesheet
│   ├── popup.js              # Popup interaction controller
│   └── icons/                # Extension branding icons
├── frontend/                 # React Web Dashboard (Vite)
│   ├── src/                  # React components, pages, and API service
│   ├── package.json          # Frontend Node dependencies
│   └── vite.config.js        # Vite build configuration
├── .env.example              # Global environment template
├── .gitignore                # Git ignore configuration
├── PRIVACY_POLICY.md         # Official Privacy Policy
├── privacy_policy.html       # Hosted Privacy Policy page
└── README.md                 # Project documentation
```

---

## Technology Stack

### Backend
- **Python 3.10+**
- **FastAPI** (Asynchronous web framework)
- **SQLAlchemy** (ORM)
- **SQLite** (Development database)
- **Pydantic** (Data validation)

### Browser Extension
- **Chrome Manifest V3**
- **Vanilla JavaScript & CSS3** (Dark cybersecurity design system)
- **Service Workers & Content Scripts**

### Frontend
- **React 18**
- **Vite**
- **Tailwind CSS**
- **Lucide React** (Iconography)

---

## Backend Setup

1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create your local environment configuration:
   - **Windows:**
     ```cmd
     copy .env.example .env
     ```
   - **Linux / macOS:**
     ```bash
     cp .env.example .env
     ```

6. Open `backend/.env` and fill in your API keys (optional for basic local testing).

---

## Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DEBUG` | No | Enables debug logging (`True` / `False`) |
| `DATABASE_URL` | Yes | SQLite or PostgreSQL database connection string |
| `GOOGLE_SAFE_BROWSING_API_KEY` | Optional | API key for Google Safe Browsing URL threat checks |
| `VIRUSTOTAL_API_KEY` | Optional | API key for VirusTotal domain reputation scanning |
| `GEMINI_API_KEY` | Optional | API key for Google Gemini task discovery & explanations |

---

## Running the Backend

Start the FastAPI development server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will run at `http://localhost:8000`. API documentation is available at `http://localhost:8000/docs`.

---

## Frontend Setup

1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev
   ```

The dashboard will run at `http://localhost:5173`.

---

## Chrome Extension Setup

1. Open Google Chrome and navigate to `chrome://extensions`.
2. Enable **Developer mode** using the toggle in the top-right corner.
3. Click **Load unpacked** in the top-left corner.
4. Select the `extension` folder inside this repository (`scamshield/extension`).
5. Open any webpage in Chrome.
6. Click the **ScamShield** icon in the extension toolbar.
7. Click **Scan Active Page** to run a real-time security analysis.

---

## Production Deployment

In a production environment:
- The **Chrome Extension** is published on the Chrome Web Store and communicates via HTTPS with your hosted backend API.
- The **FastAPI Backend** is deployed to a cloud provider (e.g. Render, AWS, GCP, Railway) with environment variables securely set in the host settings.
- All private API keys (Gemini, VirusTotal, Safe Browsing) remain on the backend and are never exposed to the client or browser extension.

---

## Security

- Private API credentials must be stored strictly in environment variables on the server.
- `.env` files, local database files (`*.db`), and build artifacts are excluded via `.gitignore`.
- The Chrome Extension contains zero private provider keys or database secrets.
- In production, always use HTTPS for backend communications.

---

## Privacy

ScamShield processes webpage content and extracted URLs only when a user initiates a scan or when real-time protection is active. Sensitive numerical strings (such as OTPs, PINs, and payment card numbers) are masked before data processing. ScamShield does not collect browsing history or personal identity information.

---

## Testing

Run the automated task-specific category test suite:

```bash
cd backend
python test_task_specific.py
```

---

## Chrome Web Store Publishing

When packaging the extension for the Chrome Web Store:
- Create a `.zip` archive containing **only** the contents of the `extension/` folder (`manifest.json`, `background.js`, `content.js`, `popup.html`, `popup.css`, `popup.js`, `icons/`).
- Do **NOT** include `backend/`, `frontend/`, `node_modules/`, `.env`, or local database files.

---

## License

License has not yet been specified.

---

## Disclaimer

ScamShield provides security risk assessments based on available signals and automated analysis. No automated security tool can guarantee that every website or message is completely safe or malicious. Always exercise caution when sharing sensitive information online.
