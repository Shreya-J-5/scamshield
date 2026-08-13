# 🛡️ ScamShield

> **Your AI-Powered Cybersecurity Companion for the Web**  
> Real-time phishing scanner, security risk analyzer, and task-first safe alternative recommendation engine.

ScamShield protects you from shady websites, credential harvest traps, and malicious links before they can steal your data. Backed by a high-performance FastAPI backend, a sleek Chrome extension, and an intuitive React dashboard, ScamShield gives you instant security peace of mind while you browse.

---

## 🌟 Overview

ScamShield gives you instant, transparent webpage security assessments right inside your browser:

- 🔍 **Smart Webpage & Link Scanning:** Automatically inspects active web pages, titles, external links, and text for phishing indicators, urgency triggers, and raw IP addresses.
- 📊 **Clear & Explainable Risk Scores:** Calculates a transparent 0–100 risk score with human-readable red flags and clear risk badges (`Low`, `Suspicious`, `High`, `Critical`).
- 💡 **Task-First Safe Alternatives:** Found a shady PDF converter, video editor, or file transfer site? ScamShield detects what you were trying to do and automatically suggests verified, safe alternatives so you can finish your job securely.
- 🔐 **Privacy-First Core:** Automatically masks sensitive numeric patterns (OTPs, PINs, card numbers) locally on your device. We never track your personal browsing history.

> 💡 *Note: ScamShield provides automated risk assessments based on smart security heuristics. While it catches most online threats, no automated tool can guarantee 100% detection—always stay vigilant online!*

---

## ✨ Key Features

- ⚡ **Instant Webpage Scanner:** Scan any open tab in 1 click from your Chrome toolbar.
- 🎯 **Task-Matched Alternatives:** Automatically recommends trusted tools tailored to your exact task (PDF, video, images, file sharing, URL shortening).
- 🛡️ **Zero-Latency Fallback Engine:** Built-in curated taxonomy ensures safe alternative suggestions even when offline or rate-limited.
- 🚫 **Anti-Generic AI Filter:** Keeps generic AI chatbots out of your recommendations when you're looking for specialized web tools.
- 🖥️ **Interactive Security Dashboard:** Review your scan history, view threat analytics, and manually analyze suspicious text messages or links.
- 🚀 **Asynchronous Python Backend:** Powered by FastAPI for lightning-fast analysis and external threat intelligence lookup.

---

## 🏗️ Architecture Overview

```text
 Chrome Extension (Manifest V3)
        │
        │ 🌐 HTTPS API Request
        ▼
 FastAPI Backend (Python 3.10+)
        │
        ├──► 🛡️ Security Reputation (Google Safe Browsing, VirusTotal)
        ├──► 🧠 AI Task Engine (Google Gemini API)
        ├──► ⚡ Local Fallback Engine (Curated Task Taxonomy)
        └──► 💾 Database Cache (SQLite / PostgreSQL)

 React Web Dashboard
        │
        ▼
 FastAPI Backend (JSON API)
```

---

## 📁 Project Structure

```text
scamshield/
├── ⚙️ backend/                 # FastAPI Application & Security Engine
│   ├── app/
│   │   ├── main.py           # API routes & CORS middleware
│   │   ├── config.py         # Environment configuration
│   │   ├── database.py       # SQLAlchemy SQLite setup
│   │   ├── models.py         # DB models (Scan History & Cache)
│   │   ├── schemas.py        # Pydantic data validation
│   │   ├── routes/           # Security endpoints (analyze, scans, health)
│   │   └── services/         # Security rules, URL checker, alternatives engine
│   ├── tests/                # Test suite
│   ├── check_status.py       # API status health checker
│   ├── test_task_specific.py # 8-category task recommendation test suite
│   ├── requirements.txt      # Python dependencies
│   └── .env.example          # Backend environment template
├── 🧩 extension/               # Chrome Extension (Manifest V3)
│   ├── manifest.json         # Extension manifest V3
│   ├── background.js         # Service worker
│   ├── content.js            # Page text extractor
│   ├── popup.html            # Dark-theme popup interface
│   ├── popup.css             # Cybersecurity design system
│   ├── popup.js              # Popup controller logic
│   └── icons/                # Extension branding icons
├── 💻 frontend/                # React Web Dashboard (Vite + Tailwind)
│   ├── src/                  # Components, pages, and API service
│   ├── package.json          # Frontend dependencies
│   └── vite.config.js        # Vite build config
├── 🖼️ store_assets/           # Chrome Web Store graphics & screenshots
├── .env.example              # Global environment template
├── .gitignore                # Git ignore configuration
├── PRIVACY_POLICY.md         # Official Privacy Policy
├── privacy_policy.html       # Web-formatted Privacy Policy page
└── README.md                 # Project documentation
```

---

## 💻 Tech Stack

### 🐍 Backend
- **Python 3.10+** & **FastAPI**
- **SQLAlchemy** & **SQLite**
- **Pydantic** validation
- **Google Gemini API** & **VirusTotal API**

### 🧩 Chrome Extension
- **Chrome Manifest V3**
- **Vanilla JavaScript & Modern CSS3** (Dark Studio Aesthetic)
- **Service Workers & Content Scripts**

### ⚛️ Frontend
- **React 18** & **Vite**
- **Tailwind CSS**
- **Lucide React** icons

---

## ⚙️ Backend Setup

1. 📂 Navigate to the backend folder:
   ```bash
   cd backend
   ```

2. 🐍 Create a virtual environment:
   ```bash
   python -m venv venv
   ```

3. ⚡ Activate the environment:
   - **Windows (PowerShell):**
     ```powershell
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     source venv/bin/activate
     ```

4. 📦 Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. 🔑 Setup environment variables:
   - **Windows:**
     ```cmd
     copy .env.example .env
     ```
   - **Linux / macOS:**
     ```bash
     cp .env.example .env
     ```

6. Open `backend/.env` and add your API keys (optional for basic local heuristic scanning).

---

## 🔑 Environment Variables

| Variable | Required | Description |
|---|---|---|
| `DEBUG` | No | Enable debug mode (`True` / `False`) |
| `DATABASE_URL` | Yes | SQLite or PostgreSQL connection string |
| `GOOGLE_SAFE_BROWSING_API_KEY` | Optional | Google Safe Browsing threat lookup |
| `VIRUSTOTAL_API_KEY` | Optional | VirusTotal domain reputation scanning |
| `GEMINI_API_KEY` | Optional | Google Gemini task discovery & explanations |

---

## 🏃‍♂️ Running the Backend

Start the FastAPI server:

```bash
python -m uvicorn app.main:app --reload --port 8000
```

The API will be live at `http://localhost:8000`. Test endpoints anytime via the interactive Swagger Docs at `http://localhost:8000/docs` 🚀!

---

## 🔌 Frontend Setup

1. Navigate to the frontend folder:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the dev server:
   ```bash
   npm run dev
   ```

Your dashboard will open at `http://localhost:5173` 🎨!

---

## 🧩 Chrome Extension Setup

1. Open Google Chrome and go to `chrome://extensions`.
2. Turn ON **Developer mode** (top right toggle).
3. Click **Load unpacked** (top left).
4. Select the `extension/` folder in this repository.
5. Open any website and click the **ScamShield** icon in your toolbar to scan! 🛡️

---

## 🌐 Production Deployment

- The **Chrome Extension** runs on the client's browser and communicates via secure HTTPS with your hosted backend API.
- The **FastAPI Backend** can be deployed to Render, AWS, GCP, or Railway with environment variables set in your deployment portal.
- All private API keys stay 100% on the server and are never exposed to the browser.

---

## 🔒 Security & Privacy

- 🛡️ All API keys and secrets stay safely inside server environment variables.
- 🙈 Sensitive numbers (OTPs, PINs, card numbers) are automatically masked before processing.
- 🚫 We don't track your personal web history or sell user data.
- 📑 Read our complete [Privacy Policy](PRIVACY_POLICY.md).

---

## 🧪 Testing

Run the automated task-specific recommendation test suite:

```bash
cd backend
python test_task_specific.py
```

---

## 📄 License

License has not yet been specified.

---

## ⚠️ Disclaimer

ScamShield provides security risk assessments based on automated signal analysis and heuristic rules. No automated security tool can guarantee 100% detection of every online scam or malicious site. Always practice safe browsing habits! 🛡️
