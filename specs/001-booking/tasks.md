# Tasks: จองคิวตรวจสุขภาพ (Booking)
Feature: จองคิวตรวจสุขภาพ
Spec ID: SPEC-BKG-001
อ้างอิง: plan.md
วันที่: 2569-09-23

สรุป: แยกรายการงานเป็น 20 tasks, มีกี่งานรอ Open Questions: 2 งาน (รอ Q-02)

### T-01 สร้างตารางและ migration
- รองรับ: CON-TECH-01, DOM-PDPA-01, IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-01
- ไฟล์ที่แตะ: backend/db/models.py, backend/db/migrations/001_init.py
- ต้องทำหลัง: ไม่มี
- เสร็จเมื่อ: สคริปต์ migration `upgrade(engine)` สร้างตาราง `slots`, `bookings`, `audit_logs` สำเร็จและรันผ่านใน SQLite memory
- สถานะ: พร้อมทำ
 - เสร็จเมื่อ: สคริปต์ migration `upgrade(engine)` สร้างตาราง `slots`, `bookings`, `audit_logs` สำเร็จและรันผ่านใน SQLite memory
 - สถานะ: เสร็จ รอทีมตรวจ

### T-02 สร้าง model `slots` และ service คำนวณช่วงว่าง
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ (ฟังก์ชันพื้นฐาน) แต่คือฐานให้ T-18
- ไฟล์ที่แตะ: backend/db/models.py, backend/slots/service.py, backend/slots/router.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: Unit test สำหรับการคืนค่า list ของ slots พร้อม remaining ทำงานผ่าน
- สถานะ: พร้อมทำ
 - เสร็จเมื่อ: Unit test สำหรับการคืนค่า list ของ slots พร้อม remaining ทำงานผ่าน
 - สถานะ: เสร็จ รอทีมตรวจ

### T-03 สร้าง POST /bookings พื้นฐาน (บันทึกการจองและตัด remaining)
- รองรับ: FR-BKG-04, IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-14
- ไฟล์ที่แตะ: backend/booking/service.py, backend/booking/router.py
- ต้องทำหลัง: T-01, T-02
- เสร็จเมื่อ: POST /bookings สร้าง record ใน `bookings` และลด `slots.remaining` เมื่อเรียกใน test
- สถานะ: พร้อมทำ

### T-04 กันจองซ้ำสำหรับวันเดียวกัน (logic และ DB check)
- รองรับ: FR-BKG-02
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-15
- ไฟล์ที่แตะ: backend/booking/service.py, backend/db/models.py, backend/tests/test_duplication.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: เมื่อมีการเรียกจองซ้ำระบบปฏิเสธ (409) และไม่สร้าง booking ใหม่ใน unit test
- สถานะ: พร้อมทำ

### T-05 ค้นช่วงเวลาใกล้เคียง (เสนอ 3 ตัวเลือก)
- รองรับ: FR-BKG-03
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-16 (และ UI T-11)
- ไฟล์ที่แตะ: backend/slots/service.py, backend/booking/service.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: ฟังก์ชันที่ให้ 3 ช่วงที่ใกล้ที่สุด คืนค่าตามเงื่อนไขใน unit test
- สถานะ: พร้อมทำ

### T-06 ระบบคิวส่งข้อความและนโยบาย retry
- รองรับ: FR-BKG-05, IF-NOT-01, NFR-REL-02, ASM-03
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-17
- ไฟล์ที่แตะ: backend/notify/queue.py, backend/notify/worker.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: งานส่งข้อความถูกวางลงคิวแบบ asynchronous และมี logic ส่งซ้ำภายใน 5 นาที ตาม ASM-03
- สถานะ: พร้อมทำ

### T-07 เพิ่ม audit middleware เพื่อบันทึกการเข้าถึง
- รองรับ: DOM-PDPA-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ แต่เป็นพื้นฐานให้ T-19
- ไฟล์ที่แตะ: backend/audit/middleware.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ทุก API ที่แตะข้อมูลการจองเรียก middleware และเขียน `audit_logs` ใน unit test
- สถานะ: พร้อมทำ

### T-08 สร้าง HIS client (GET /patients/lookup)
- รองรับ: IF-HIS-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-08
- ไฟล์ที่แตะ: backend/his/client.py, backend/his/router.py
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: client mock ส่งคืน `hn` และ API คืนค่า `hn` ใน unit test
- สถานะ: พร้อมทำ

### T-09 ออกแบบนโยบาย `queue_no` (รอคำตอบ Q-02)
- รองรับ: FR-BKG-04 (ส่วนที่เกี่ยวกับ `queue_no`)
- ตรวจด้วย: ไม่มี -- รอคำตอบ Q-02
- ไฟล์ที่แตะ: backend/db/models.py (column `queue_no`), design note ใน specs/001-booking/
- ต้องทำหลัง: T-01
- เสร็จเมื่อ: ได้ข้อสรุปจากเจ้าหน้าที่เวชระเบียนว่า `queue_no` รีเซ็ตหรือรันต่อเนื่อง และมีรูปแบบ ตัวอย่าง เช่น A001 หรือ 0001
- สถานะ: รอ Q-02

### T-10 หน้า SlotPicker (frontend) กับ API จำลอง
- รองรับ: FR-BKG-01, FR-BKG-06
- ตรวจด้วย: ไม่มี AC ตรง ๆ เป็นงานพื้นฐานของ T-11
- ไฟล์ที่แตะ: frontend/src/pages/SlotPicker.jsx, frontend/src/api/client.js
- ต้องทำหลัง: ไม่มี (ใช้ API จำลองได้เลย ตามกฎ plan)
- เสร็จเมื่อ: หน้าจอโหลดและแสดงรายการช่วงเวลาจาก API จำลอง ใน UI snapshot test
- สถานะ: พร้อมทำ

### T-11 หน้า ConfirmBooking (แสดง 409 และ 3 ช่วงใกล้เคียง)
- รองรับ: FR-BKG-03
- ตรวจด้วย: AC-BKG-03 (ผ่าน UI test `AC-BKG-03.test.jsx`)
- ไฟล์ที่แตะ: frontend/src/pages/ConfirmBooking.jsx, frontend/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-10, T-05
- เสร็จเมื่อ: เมื่อ API จำลองคืน 409 พร้อม 3 ช่วง หน้าจอแสดงข้อความ "ช่วงเวลาเต็ม" และปุ่ม 3 ตัวเลือก ตาม UI test
- สถานะ: พร้อมทำ

### T-12 หน้า BookingResult (แสดงหมายเลขคิว แม้ส่งข้อความไม่สำเร็จ)
- รองรับ: FR-BKG-04, FR-BKG-05
- ตรวจด้วย: AC-BKG-01, AC-BKG-04 (UI test และ integration test)
- ไฟล์ที่แตะ: frontend/src/pages/BookingResult.jsx, frontend/__tests__/AC-BKG-01.test.jsx
- ต้องทำหลัง: T-03, T-06, T-09 (ถ้าต้องการรูปแบบหมายเลขเฉพาะ)
- เสร็จเมื่อ: หลังจองสำเร็จ หน้าจอแสดง `queue_no` แม้ระบบส่งข้อความล้มเหลว ใน UI test
- สถานะ: รอ Q-02

### T-13 ต่อหน้าจอกับ API จริง (เชื่อม frontend → backend)
- รองรับ: FR-BKG-01, FR-BKG-03, FR-BKG-04
- ตรวจด้วย: ไม่มี AC ตรง ๆ (integration step)
- ไฟล์ที่แตะ: frontend/src/api/client.js, Vite proxy config, backend main app
- ต้องทำหลัง: T-02, T-03, T-10, T-11
- เสร็จเมื่อ: หน้าแอปจริงเรียก API หลังบ้านและทำงาน end-to-end ใน integration smoke test
- สถานะ: พร้อมทำ

### T-14 ทดสอบ AC-BKG-01 (test_AC_BKG_01)
- รองรับ: AC-BKG-01 (FR-BKG-04)
- ตรวจด้วย: AC-BKG-01
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_01.py
- ต้องทำหลัง: T-03
- เสร็จเมื่อ: test_AC_BKG_01 ผ่าน (สร้างช่วง 09.00 เหลือ 1 ที่ ยืนยันแล้ว remaining เป็น 0 และแสดงหมายเลขคิว)
- สถานะ: พร้อมทำ

### T-15 ทดสอบ AC-BKG-02 (test_AC_BKG_02)
- รองรับ: AC-BKG-02 (FR-BKG-02)
- ตรวจด้วย: AC-BKG-02
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_02.py
- ต้องทำหลัง: T-04
- เสร็จเมื่อ: test_AC_BKG_02 ผ่าน (มีคิวเดิมปฏิเสธการจองซ้ำและคืนหมายเลขเดิม)
- สถานะ: พร้อมทำ

### T-16 ทดสอบ AC-BKG-03 (backend + UI)
- รองรับ: AC-BKG-03 (FR-BKG-03)
- ตรวจด้วย: AC-BKG-03 (ทั้ง backend test และ `frontend/__tests__/AC-BKG-03.test.jsx`)
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_03.py, frontend/__tests__/AC-BKG-03.test.jsx
- ต้องทำหลัง: T-05, T-11
- เสร็จเมื่อ: test AC-BKG-03 ทั้ง backend และ UI ผ่าน (409 + 3 ช่วง ใกล้ 09.00 น.)
- สถานะ: พร้อมทำ

### T-17 ทดสอบ AC-BKG-04 (notify retry)
- รองรับ: AC-BKG-04 (FR-BKG-05, NFR-REL-02)
- ตรวจด้วย: AC-BKG-04
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_04.py, backend/notify/queue.py
- ต้องทำหลัง: T-06
- เสร็จเมื่อ: test จำลองการส่งไม่สำเร็จ ตรวจว่าการจองถูกบันทึก และมีงานส่งซ้ำกำหนดภายใน 5 นาที
- สถานะ: พร้อมทำ

### T-18 ทดสอบ AC-BKG-05 (performance p95 ของ GET /slots)
- รองรับ: AC-BKG-05 (NFR-PERF-01)
- ตรวจด้วย: AC-BKG-05
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_05_performance.py, backend/slots/service.py
- ต้องทำหลัง: T-02
- เสร็จเมื่อ: การทดสอบแบบย่อส่วนใน Codespace วัด p95 <= 2s สำหรับโหลดจำลอง (200 concurrent แบบย่อส่วน)
- สถานะ: พร้อมทำ

### T-19 ทดสอบ AC-BKG-06 (audit log)
- รองรับ: AC-BKG-06 (DOM-PDPA-01)
- ตรวจด้วย: AC-BKG-06
- ไฟล์ที่แตะ: backend/tests/test_AC_BKG_06.py, backend/audit/middleware.py
- ต้องทำหลัง: T-07
- เสร็จเมื่อ: เปิดดูการจองแล้วมีบันทึก `audit_logs` ที่มี actor_id, accessed_at และ hn
- สถานะ: พร้อมทำ

### T-20 เพิ่ม middleware/endpoint ตรวจผลยืนยันตัวตน (IF-IDP-01)
- รองรับ: IF-IDP-01
- ตรวจด้วย: ไม่มี AC ตรง ๆ แต่เป็นข้อจำเป็นก่อนใช้งาน endpoints
- ไฟล์ที่แตะ: backend/auth/idp.py, backend/app/main.py (dependency injection)
- ต้องทำหลัง: ไม่มี (แต่ต้องทำก่อนเปิด API ให้ผู้ใช้จริง)
- เสร็จเมื่อ: unit test ที่ mock IDP คืนสถานะยืนยันตัวตน ทำให้ endpoint ยอมรับคำขอ
- สถานะ: พร้อมทำ

## ตารางตรวจความครบ

AC ID | task ที่ตรวจ AC นี้
---|---
AC-BKG-01 | T-14
AC-BKG-02 | T-15
AC-BKG-03 | T-16
AC-BKG-04 | T-17
AC-BKG-05 | T-18
AC-BKG-06 | T-19

Constraint ID | task ที่ทำให้เป็นจริง
---|---
CON-TECH-01 | T-01, T-03
DOM-PDPA-01 | T-01, T-07, T-19
IF-IDP-01 | T-20, (T-03 uses it)
IF-HIS-01 | T-08
IF-NOT-01 | T-06

## สิ่งที่ยังไม่ทำ (Open Questions)
- Q-02: รูปแบบหมายเลขคิว (`queue_no`) — ยังไม่ได้คำตอบจากเจ้าหน้าที่เวชระเบียน.
  - งานที่รอคำตอบ: T-09 (ออกแบบ `queue_no`), T-12 (ถ้าต้องการรูปแบบเฉพาะ)

---
หมายเหตุ: ทุก AC ใน spec ถูกแมปไปยัง task ทดสอบเฉพาะ ถ้าทีมต้องการเปลี่ยนลำดับหรือแยกงานให้เล็กลงบอกได้เลย
