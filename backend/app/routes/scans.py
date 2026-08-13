from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
import json

from ..database import get_db
from ..models import Scan
from ..schemas import ScanOut, RedFlag

router = APIRouter()

def _format_scan(scan: Scan) -> ScanOut:
    extracted_urls = json.loads(scan.extracted_urls) if scan.extracted_urls else []
    reasons_raw = json.loads(scan.reasons) if scan.reasons else []
    reasons = [RedFlag(**rf) for rf in reasons_raw]
    
    return ScanOut(
        id=scan.id,
        message_text=scan.message_text,
        sender=scan.sender,
        sender_contact=scan.sender_contact,
        extracted_urls=extracted_urls,
        risk_score=scan.risk_score,
        risk_level=scan.risk_level,
        verdict=scan.verdict,
        reasons=reasons,
        recommendation=scan.recommendation,
        created_at=scan.created_at.isoformat() if scan.created_at else "",
    )

@router.get("/scans", response_model=List[ScanOut], tags=["Scans"])
async def list_scans(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    scans = db.query(Scan).order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()
    return [_format_scan(s) for s in scans]

@router.get("/scans/{scan_id}", response_model=ScanOut, tags=["Scans"])
async def get_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    return _format_scan(scan)

@router.delete("/scans/{scan_id}", tags=["Scans"])
async def delete_scan(scan_id: int, db: Session = Depends(get_db)):
    scan = db.query(Scan).filter(Scan.id == scan_id).first()
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    db.delete(scan)
    db.commit()
    return {"status": "deleted", "scan_id": scan_id}
