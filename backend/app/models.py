from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from sqlalchemy.sql import func
from .database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(Integer, primary_key=True, index=True)
    message_text = Column(Text, nullable=False)
    sender = Column(String(255), nullable=True)
    sender_contact = Column(String(255), nullable=True)
    extracted_urls = Column(Text, nullable=True)  # Stored as JSON string list
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False)
    verdict = Column(String(100), nullable=False)
    reasons = Column(Text, nullable=True)  # JSON string of red flags
    recommendation = Column(Text, nullable=True)
    processing_time_ms = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class RecommendationCache(Base):
    __tablename__ = "recommendation_cache"

    id = Column(Integer, primary_key=True, index=True)
    domain = Column(String(255), unique=True, index=True, nullable=False)
    purpose = Column(String(255), nullable=True)
    category = Column(String(100), nullable=True)
    alternatives_json = Column(Text, nullable=False)
    provider_source = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

