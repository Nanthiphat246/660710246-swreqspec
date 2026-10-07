# test ของ T-03: จองคิวสำเร็จ
# AC-BKG-01 (FR-BKG-04)
from tests.conftest import AUTH


def test_AC_BKG_01(client, make_slot):
    """AC-BKG-01: ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง จองแล้วต้องสำเร็จ"""
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201


from app.db.models import Booking


# Given ยืนยันตัวตนแล้ว และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
# When ยืนยันการจองช่วง 09.00 น.
# Then บันทึกสำเร็จ มีการจอง 1 รายการ; ที่นั่งว่างของช่วงนั้นเป็น 0;
# แสดงหมายเลขคิว (รอ Q-02) — ยังไม่ตรวจเพราะรอ Q-02
def test_TC_BKG_01_1_last_seat(client, db, make_slot):
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 201
    assert db.query(Booking).count() == 1
    db.refresh(slot)
    assert slot.remaining == 0


# Given ยืนยันตัวตนแล้ว และช่วง 09.00 น. เหลือ 0 ที่ (มีคนจองที่สุดท้ายไปแล้ว)
# When ยืนยันการจองช่วง 09.00 น.
# Then ปฏิเสธ และตอบ 409; ไม่มีการจองใหม่; ที่นั่งว่างยังเป็น 0 และไม่ติดลบ
def test_TC_BKG_01_2_no_seat_left(client, db, make_slot):
    slot = make_slot(start="09:00", remaining=0)

    res = client.post("/bookings", json={"slot_id": slot.id}, headers=AUTH)

    assert res.status_code == 409
    assert db.query(Booking).count() == 0
    db.refresh(slot)
    assert slot.remaining == 0


# Given ยังไม่ได้ยืนยันตัวตน และช่วง 09.00 น. มีที่นั่งว่าง 1 ที่
# When ยืนยันการจองช่วง 09.00 น.
# Then ปฏิเสธ และตอบ 401; ไม่มีการจอง; ที่นั่งว่างยังเป็น 1
def test_TC_BKG_01_3_not_verified(client, db, make_slot):
    slot = make_slot(start="09:00", remaining=1)

    res = client.post("/bookings", json={"slot_id": slot.id})

    assert res.status_code == 401
    assert db.query(Booking).count() == 0
    db.refresh(slot)
    assert slot.remaining == 1
