from fastapi import APIRouter, Depends
from datetime import date
from typing import List
from sqlalchemy.orm import Session

from backend.db.models import Slot
from backend.slots import service
from backend.db import session as db_session  # optional DI if available

router = APIRouter()


# รองรับ: FR-BKG-01, FR-BKG-06
@router.get("/slots", response_model=List[dict])
def get_slots(date_from: date, package_code: str | None = None, db: Session = Depends(db_session.get_db)):
    """API endpoint to return available slots (list of dicts)

    รองรับ FR-BKG-01: แสดงช่วงเวลาที่ว่างพร้อมจำนวนที่นั่งคงเหลือ
    """
    return service.list_slots(db, date_from=date_from, package_code=package_code)
