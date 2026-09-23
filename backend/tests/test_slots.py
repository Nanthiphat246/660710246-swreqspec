import sys
import os
from datetime import date, time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure repo root is on sys.path so 'backend' package imports work when running tests
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from backend.db.models import Base, Slot
from backend.slots.service import list_slots


def test_list_slots_returns_remaining():
    """ทดสอบว่าฟังก์ชัน list_slots คืนรายการ slots พร้อมค่า remaining ตามข้อมูลใน DB

    เสร็จเมื่อ: Unit test สำหรับการคืนค่า list ของ slots พร้อม remaining ทำงานผ่าน
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    db = Session()

    # สร้างข้อมูลตัวอย่างสองช่วง
    s1 = Slot(slot_date=date(2026, 9, 24), start_time=time(9, 0), package_code="PKG-A", capacity=10, remaining=5)
    s2 = Slot(slot_date=date(2026, 9, 24), start_time=time(10, 0), package_code="PKG-A", capacity=8, remaining=0)
    db.add_all([s1, s2])
    db.commit()

    res = list_slots(db, date_from=date(2026, 9, 24), package_code="PKG-A")
    assert isinstance(res, list)
    assert len(res) == 2
    # ตรวจค่า remaining ตรงกับที่ใส่
    assert res[0]["remaining"] == 5
    assert res[1]["remaining"] == 0
