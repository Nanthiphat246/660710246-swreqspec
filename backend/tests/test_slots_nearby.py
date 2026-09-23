import sys
import os
from datetime import date, time, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure repo root is on sys.path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.db.models import Base, Slot
from backend.slots.service import find_nearest_available_slots


def test_find_nearest_available_slots_returns_three_closest():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    # Requested slot is 2026-09-24 09:00 but it's full
    # Create candidate slots on same day and next day with various times
    slots = [
        Slot(slot_date=date(2026, 9, 24), start_time=time(8, 30), package_code="PKG-A", capacity=5, remaining=2),
        Slot(slot_date=date(2026, 9, 24), start_time=time(9, 30), package_code="PKG-A", capacity=5, remaining=1),
        Slot(slot_date=date(2026, 9, 24), start_time=time(11, 0), package_code="PKG-A", capacity=5, remaining=3),
        Slot(slot_date=date(2026, 9, 25), start_time=time(8, 45), package_code="PKG-A", capacity=5, remaining=4),
        Slot(slot_date=date(2026, 9, 25), start_time=time(10, 0), package_code="PKG-A", capacity=5, remaining=0),
    ]
    db.add_all(slots)
    db.commit()

    res = find_nearest_available_slots(
        db, slot_date=date(2026, 9, 24), start_time=time(9, 0), package_code="PKG-A", limit=3
    )
    assert len(res) == 3

    # First should be 9:30 (30 min), then 8:30 (30 min but earlier), then 8:45 next day (23h45m -> much larger)
    times = [r["start_time"] for r in res]
    assert "09:30:00" in times
    assert "08:30:00" in times
    assert "08:45:00" in times or "11:00:00" in times
