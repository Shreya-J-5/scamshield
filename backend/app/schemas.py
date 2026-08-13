# Pydantic schemas for ScamShield
from typing import List, Optional
from pydantic import BaseModel, Field, validator

class AnalyzeRequest(BaseModel):
    message_text: str = Field(..., description="Full message body")
    sender: Optional[str] = Field(None, description="Sender name or identifier")
    sender_contact: Optional[str] = Field(None, description="Email or phone number of sender")
    url: Optional[str] = Field(None, description="Optional URL supplied separately")

    @validator("message_text")
    def not_empty(cls, v):
        if not v.strip():
            raise ValueError("message_text cannot be empty")
        return v

class AnalyzePageRequest(BaseModel):
    page_title: Optional[str] = Field("", description="Title of the scanned webpage")
    page_url: str = Field(..., description="URL of the scanned webpage")
    page_text: Optional[str] = Field("", description="Extracted visible text from webpage")
    links: Optional[List[str]] = Field(default_factory=list, description="Extracted anchor links")

class RedFlag(BaseModel):
    rule: str
    points: int
    explanation: str
    evidence: str

class AnalyzeResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    verdict: str
    red_flags: List[RedFlag]
    recommendation: str
    processing_time_ms: int

class ScanOut(BaseModel):
    id: int
    message_text: str
    sender: Optional[str]
    sender_contact: Optional[str]
    extracted_urls: Optional[List[str]]
    risk_score: int
    risk_level: str
    verdict: str
    reasons: Optional[List[RedFlag]]
    recommendation: Optional[str]
    created_at: str

    class Config:
        from_attributes = True
