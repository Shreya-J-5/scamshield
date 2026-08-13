import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .database import engine, Base
from .routes import health, analyze, scans

# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ScamShield Backend",
    version="1.0.0",
    description="Real-time explainable scam & phishing detection API"
)

# Robust production-ready CORS configuration
origins = [
    "http://localhost",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"chrome-extension://.*",
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)

# Include API routers
app.include_router(health.router)
app.include_router(analyze.router, prefix="/api")
app.include_router(scans.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
