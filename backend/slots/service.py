from typing import List
from datetime import date, datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_

from backend.db.models import Slot
from datetime import timedelta
from sqlalchemy import func


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


# รองรับ: FR-BKG-03
def find_nearest_available_slots(
    db: Session,
    *,
    slot_date: date,
    start_time: datetime.time,
    package_code: str | None = None,
    limit: int = 3,
) -> List[dict]:
    """ค้นหาช่วงเวลาที่ว่างใกล้เคียงกับ `slot_date`/`start_time` ภายในวันเดียวกันและวันถัดไป

    Returns up to `limit` slots ordered by absolute time difference (closest first).
    รองรับ FR-BKG-03: เสนอ 3 ตัวเลือกที่ใกล้ที่สุดภายในวันเดียวกันและวันถัดไป
    """
    # date window: slot_date and slot_date + 1
    date_to = slot_date + timedelta(days=1)

    q = db.query(Slot).filter(Slot.slot_date >= slot_date, Slot.slot_date <= date_to, Slot.remaining > 0)
    if package_code:
        q = q.filter(Slot.package_code == package_code)

    # compute absolute time difference in seconds; SQLite may not support direct time arithmetics via SQLAlchemy
    # So load candidates and sort in Python for portability in tests
    candidates = q.all()

    def time_diff_seconds(s: Slot) -> int:
        # compute seconds difference between candidate slot and requested datetime
        dt_candidate = datetime.combine(s.slot_date, s.start_time)
        dt_requested = datetime.combine(slot_date, start_time)
        return abs(int((dt_candidate - dt_requested).total_seconds()))

    sorted_candidates = sorted(candidates, key=time_diff_seconds)
    results = []
    for s in sorted_candidates[:limit]:
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
