# ScamShield Backend API

FastAPI-powered real-time detection & risk-assessment backend for messages, URLs, and webpage content.

## Setup Instructions

1. Create a virtual environment & activate it:
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the development server:
```bash
uvicorn app.main:app --reload --port 8000
```

4. Run tests:
```bash
pytest
```

## API Endpoints

- `GET /health` : Health check status
- `POST /api/analyze` : Analyze message text & extracted URLs
- `POST /api/analyze-page` : Analyze webpage content & links from Chrome extension
- `GET /api/scans` : List scan history
- `GET /api/scans/{id}` : Get single scan details
- `DELETE /api/scans/{id}` : Delete scan from database
