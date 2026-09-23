from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.db.models import Slot


# รองรับ: FR-BKG-01, FR-BKG-06, CON-TECH-01
def list_slots(
    db: Session, *, date_from: date, date_to: date = None, package_code: str | None = None
) -> List[dict]:
    """คืนรายการช่วงเวลาและที่นั่งคงเหลือสำหรับช่วงวันที่กำหนด

    รับผิดชอบตาม FR-BKG-01 (แสดงช่วงเวลาว่าง) และ FR-BKG-06 (คำนวณตามแพ็กเกจ)
    """
    if date_to is None:
        date_to = date_from

    q = db.query(Slot).filter(and_(Slot.slot_date >= date_from, Slot.slot_date <= date_to))
    if package_code:
        q = q.filter(Slot.package_code == package_code)

    results = []
    for s in q.order_by(Slot.slot_date, Slot.start_time).all():
        results.append(
            {
                "id": s.id,
                "slot_date": s.slot_date.isoformat(),
                "start_time": s.start_time.strftime("%H:%M:%S"),
                "package_code": s.package_code,
                "capacity": s.capacity,
                "remaining": s.remaining,
            }
        )
    return results
