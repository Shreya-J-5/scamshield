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

class SafeAlternative(BaseModel):
    name: str
    url: str
    explanation: str

class AlternativeCard(BaseModel):
    name: str
    domain: str
    url: str
    description: str
    reason: str
    primary_task: Optional[str] = None
    relevance_score: Optional[float] = 1.0
    tags: List[str] = Field(default_factory=list)
    category_label: Optional[str] = "Popular / Trusted"
    confidence: Optional[float] = 1.0

class AlternativesPayload(BaseModel):
    primary_task: str
    category: str
    sub_category: Optional[str] = None
    input_type: Optional[str] = None
    output_type: Optional[str] = None
    provider_source: str
    alternatives: List[AlternativeCard] = Field(default_factory=list)

class AnalyzeResponse(BaseModel):
    risk_score: int = Field(..., ge=0, le=100)
    risk_level: str
    verdict: str
    red_flags: List[RedFlag]
    recommendation: str
    processing_time_ms: int
    safe_alternative: Optional[SafeAlternative] = None
    safer_alternatives_data: Optional[AlternativesPayload] = None

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
