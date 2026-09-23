from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    DateTime,
    ForeignKey,
    func,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# รองรับ: CON-TECH-01, FR-BKG-01, FR-BKG-06
class Slot(Base):
    __tablename__ = "slots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    slot_date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    package_code = Column(String(50), nullable=False)
    capacity = Column(Integer, nullable=False, default=0)
    remaining = Column(Integer, nullable=False, default=0)


# รองรับ: FR-BKG-04, IF-HIS-01, CON-TECH-01
# หมายเหตุ: ห้ามเก็บ national_id ตาม IF-HIS-01 — เก็บเฉพาะ `hn`
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    hn = Column(String(64), nullable=False)  # เก็บ HN ตาม IF-HIS-01
    slot_id = Column(Integer, ForeignKey("slots.id"), nullable=False)
    booking_date = Column(DateTime, nullable=False, default=func.now())
    queue_no = Column(String(32), nullable=True)  # รูปแบบยังรอ Q-02
    status = Column(String(32), nullable=False, default="confirmed")
    created_at = Column(DateTime, nullable=False, default=func.now())

    slot = relationship("Slot")


# รองรับ: DOM-PDPA-01
class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    actor_id = Column(String(128), nullable=False)
    action = Column(String(128), nullable=False)
    hn = Column(String(64), nullable=True)
    accessed_at = Column(DateTime, nullable=False, default=func.now())
