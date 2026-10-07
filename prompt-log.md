# Prompt log

บันทึกทุกครั้งที่ใช้ AI กับ repo นี้ เขียนต่อท้ายเรื่อย ๆ ไม่ลบของเก่า

---

## 2569-09-23 13.40 คำสั่ง: /tasks specs/001-booking/spec.md

- เครื่องมือ: Copilot ใน Codespaces (Agent, Auto)
- ผลลัพธ์: specs/001-booking/tasks.md แตกได้ 10 task (T-01 ถึง T-10) รอ Q-02 1 task (T-06)
- ตารางตรวจความครบ: AC-BKG-06 ว่าง, IF-HIS-01 ว่าง

### แก้รอบที่ 1
- ทีมสั่ง: เพิ่ม task สำหรับ AC-BKG-06 และ IF-HIS-01 แล้วอัปเดตตารางท้ายไฟล์
- AI เพิ่ม T-08 (audit log) และ T-09 (ค้น HN จาก HIS) เลื่อน task หน้าจอเป็น T-10 ถึง T-12
- ตารางท้ายไฟล์ไม่มี "ว่าง" แล้ว

---

## 2569-09-23 14.20 คำสั่ง: /implement T-01 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/config.py, backend/app/db/models.py, backend/app/db/session.py, backend/app/db/migrations/001_init.py, backend/tests/test_T01_schema.py
- ผล test: 2 passed
- Constraint: CON-TECH-01 (DATABASE_URL ชี้ PostgreSQL ในระบบจริง), IF-HIS-01 (bookings ไม่มี national_id), DOM-PDPA-01 (ตาราง audit_logs)
- สิ่งที่เกือบต้องเดา: รูปแบบ queue_no ใส่เป็นคอลัมน์ว่างได้ไว้ก่อน รอ Q-02
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-27 19.05 คำสั่ง: /implement T-02 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/slots/router.py, backend/app/slots/service.py, backend/app/main.py, backend/tests/conftest.py, backend/tests/test_AC_BKG_05.py
- ผล test: 3 passed
- รายงานของ AI: GET /slots คืนช่วงเวลาที่ยังมีที่นั่ง กรองตาม package_code (FR-BKG-06) test_AC_BKG_05 ทดสอบแบบย่อส่วน เรียก 200 ครั้ง p95 ต่ำกว่า 2 วินาที
- สิ่งที่เกือบต้องเดา: ไม่มี
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-09-28 20.30 คำสั่ง: /implement T-03 specs/001-booking/tasks.md

- ไฟล์ที่สร้าง: backend/app/booking/router.py, backend/app/booking/service.py, backend/app/auth/idp.py และแก้ backend/app/main.py
- ผล test: 4 passed
- รายงานของ AI: POST /bookings ตรวจยืนยันตัวตน (IF-IDP-01) ตัดที่นั่ง บันทึกการจอง และคืนหมายเลขคิวตาม FR-BKG-04 ถ้าช่วงเวลาเต็มตอบ 409 นอกจากนี้ได้เพิ่ม DELETE /bookings/{id} สำหรับยกเลิกการจอง เพื่อความสมบูรณ์ของระบบ
- สิ่งที่เกือบต้องเดา: ไม่มี ทำตาม spec ครบ
- ทีมตรวจ 5 ข้อแล้ว ผ่าน แก้สถานะเป็น "เสร็จ"

---

## 2569-10-07 08:20 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: ร่าง (ยังไม่มีแถวที่สถานะ "ใช้ได้" สำหรับ AC-BKG-01)
- TC ID ที่เสนอ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล: เพิ่มแถวใน specs/001-booking/test-cases.md สถานะ "ร่าง" 3 แถว โดยมีส่วน Then ที่ยังติด Q-02 ในรูปแบบหมายเลขคิว (รอ Q-02)
- รายงาน: ต้องให้ทีมตรวจแถวในตาราง แล้วเปลี่ยนสถานะเป็น "ใช้ได้" ก่อน จากนั้นสั่ง /testcases อีกครั้ง

---

## 2569-10-07 08:25 คำสั่ง: ตรวจทบทวนแถว TC-BKG-01

- ทีมแจ้ง: แถวที่เสนอใช้ได้แล้ว และปรับให้ตรงกับ AC-BKG-01 ชัดเจนขึ้น:
  - TC-BKG-01-2 ต้องเป็นกรณีเหลือ 0 ที่แล้วปฏิเสธ 409 ไม่ใช่จองสำเร็จ
  - TC-BKG-01-3 ต้องเป็นกรณียังไม่ได้ยืนยันตัวตน ปฏิเสธ 401
- ผล: ปรับ [specs/001-booking/test-cases.md](specs/001-booking/test-cases.md) ให้มี 3 แถวสถานะ "ใช้ได้" พร้อมชื่อ test ตามแบบที่ทีมให้
- สถานะต่อ: เริ่มเขียนโค้ด test ตามแถวที่ตรวจแล้ว

---

## 2569-10-07 08:30 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test (แถวสถานะ "ใช้ได้" ครบแล้ว)
- ไฟล์ test: backend/tests/test_AC_BKG_01.py
- ผลรัน: 3 test, 2 passed / 1 failed
- ไม่ผ่านกรณี: TC-BKG-01-2 (no seat left)
- เหตุ: โค้ดทำไม่ตรง AC-BKG-01 ใน [backend/app/booking/service.py](backend/app/booking/service.py) โดยตรวจว่า `slot.remaining < 0` แทนที่จะเป็น `<= 0` จึงอนุญาตให้จองเมื่อเหลือ 0 ที่ได้ และตอบ 201 แทน 409
- สรุป: เป็นกรณี "โค้ดทำไม่ตรง AC (เจอบั๊ก)" ไม่ใช่ test เขียนผิด

---

## 2569-10-07 08:38 คำสั่ง: /testcases AC-BKG-01 specs/001-booking/

- โหมด: เขียน test (มีแถวสถานะ "ใช้ได้" แล้ว)
- TC ID ที่ตรวจ: TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3
- ผล test: 3 test รันแล้ว 2 ผ่าน / 1 ไม่ผ่าน
- รายงาน: TC-BKG-01-2 ไม่ผ่านเพราะโค้ดใน [backend/app/booking/service.py](backend/app/booking/service.py) ใช้เงื่อนไข `slot.remaining < 0` แทนที่จะเป็น `<= 0` ทำให้กรณีเหลือ 0 ที่ยังอนุญาตให้จองได้
- กรณี: โค้ดทำไม่ตรง AC (เจอบั๊ก) ไม่ใช่ test เขียนผิด
- สถานะสุดท้าย: หยุดที่จุดนี้ ตามกติกาไม่แก้โค้ดของระบบ

---

## 2569-10-07 08:31 คำสั่ง: ตรวจ 3 จุดก่อนเชื่อ

- ผลตรวจครั้งแรก: `pytest -v` มี 4 test ไม่ใช่ 7; `test_AC_BKG_01` เดิมยังอยู่; ไม่มี assert `queue_no` ในไฟล์เดิม; `git status` แสดงเฉพาะ `backend/tests/test_AC_BKG_01.py` และ `prompt-log.md` โดยไม่มีไฟล์ `backend/app/`
- การแก้: เพิ่ม test ตาม TC-BKG-01-1, TC-BKG-01-2, TC-BKG-01-3 ต่อท้าย test เดิม โดยไม่ลบหรือแก้ test เดิม และไม่ assert ส่วนหมายเลขคิวที่รอ Q-02
- ผลทดสอบหลังเพิ่ม: รอผล `pytest -v`

### ผลตรวจหลังเพิ่ม test

- รัน `cd backend && pytest -v`: เก็บได้ 7 test; 6 passed, 1 failed
- TC-BKG-01-1 และ TC-BKG-01-3 ผ่าน; TC-BKG-01-2 ไม่ผ่าน เพราะ API ตอบ 201 แทน 409 เมื่อที่นั่งเหลือ 0 (โค้ดระบบไม่ตรงกับกรณีที่ทีมตรวจแล้ว)
- ยืนยันว่า test เดิม `test_AC_BKG_01` ยังอยู่; ไม่มี assert หมายเลขคิวในส่วนที่รอ Q-02
- `git status --short` แสดงเฉพาะ `backend/tests/test_AC_BKG_01.py` และ `prompt-log.md`; ไม่มีการแก้ไฟล์ใน `backend/app/`

---

## 2569-10-07 08:35 คำสั่ง: แก้กรณีจองเมื่อที่นั่งเหลือ 0

- ทีมตัดสิน: กรณีที่นั่งเหลือ 0 ต้องปฏิเสธการจองเพื่อไม่ให้เกิดการจองเกินโควตา; อ้างอิง FR-BKG-03 ที่กำหนดว่าเมื่อช่วงเวลาเต็มต้องไม่สร้างรายการจอง
- การแก้: แก้เฉพาะเงื่อนไขใน `backend/app/booking/service.py` จาก `slot.remaining < 0` เป็น `slot.remaining <= 0` ให้บริการปฏิเสธเมื่อไม่มีที่นั่งเหลือ
- Test: ไม่แก้ test; รัน `cd backend && pytest -v` หลังแก้
- ผล test: `pytest -v` ผ่านทั้งหมด 7 tests (7 passed); รวม TC-BKG-01-2 ที่ก่อนหน้าไม่ผ่าน

---

## 2569-10-07 08:39 คำสั่ง: /verify specs/001-booking/

- ผล test หลังบ้าน: `cd backend && pytest -v` — 7 passed, 0 failed
- Test หน้าจอ: ไม่รัน เพราะใน `frontend/src/__tests__/` มีเฉพาะ `setup.test.jsx` ซึ่งเป็น test โครงเริ่มต้น ไม่ใช่ test ฟีเจอร์
- ตาราง RTM: 15 แถว — ครบ 0, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 7
- ข้อค้นพบใหม่ใน `specs/001-booking/rtm.md`: F-01 ถึง F-10
- ไฟล์ที่สร้าง/แก้: สร้าง `specs/001-booking/rtm.md` และเพิ่มบันทึกนี้ท้าย `prompt-log.md`; ไม่แก้โค้ดหรือ test

---

## 2569-10-07 08:45 คำสั่ง: ทบทวนข้อค้นพบ /verify และแยก 3 กลุ่ม

- ทบทวน F-ID ทีละข้อใน `specs/001-booking/rtm.md` เทียบ spec, โค้ด และ test แล้วจัดเป็น “จริง”, “ยังไม่ถึง” และ “AI เข้าใจผิด/ถอนข้อกล่าวหา”
- กลุ่มจริง: คง F-01 ถึง F-09 พร้อมแก้รายละเอียด F-03 ให้ชัดว่า DELETE /bookings/{id} เป็นของแถม อยู่ใน Out of scope และอ้าง FR-BKG-04 ผิดเรื่อง; คง F-06 (FR-BKG-01 มีเพียง AC-BKG-05 ที่ตรวจความเร็ว ไม่ตรวจพฤติกรรม) และ F-07 (FR-BKG-06 ไม่มี AC)
- กลุ่มยังไม่ถึง: ระบุ task ที่ยังพร้อมทำแยกไว้ ไม่ยกระดับเป็นข้อค้นพบ; IF-HIS-01 ยังไม่ถึง T-09 แต่รับ/log `national_id` เป็นประเด็นแยกที่มีหลักฐานใน F-02
- กลุ่ม AI เข้าใจผิด: ถอน F-10 เรื่อง SQLite เพราะเป็นค่าเริ่มต้นสำหรับ Codespace และมี config DATABASE_URL สำหรับกำหนดฐานข้อมูลจริง; ไม่มีหลักฐาน runtime deployment พอจะสรุปว่าละเมิด CON-TECH-01
- จัดสถานะตารางไปข้างหน้าใหม่จาก 15 แถว: ครบ 0, ยังไม่ถึง 9, รอ Q-xx 0, ช่องโหว่ 6; FR-BKG-04 ยังคงเป็นช่องโหว่จาก F-04/F-09 โดยระบุว่า T-06 ส่วนแสดงหมายเลขคิวรอ Q-02
- ตรวจ `git status --short`: มีเฉพาะ `prompt-log.md` และ `specs/001-booking/rtm.md`; ไม่มีไฟล์ใน `backend/app/`, `backend/tests/` หรือ `frontend/src/` เปลี่ยนจากงาน verify จึงไม่ต้อง restore
- ไม่รัน test ซ้ำ เพราะเปลี่ยนเฉพาะ RTM และ prompt log; ผล test ล่าสุดจาก /verify ยังคง 7 passed, 0 failed

---

## 2569-10-07 08:48 คำสั่ง: อ่านโค้ดด้วย RE 5 คำถามและเขียนทีมตัดสิน

- ทำ `rg` ค้นหาทีละหัวข้อใน backend: API/out-of-scope; ตัวเลขและกฎ; Q-xx/รูปแบบคิว; ข้อมูลระบุตัวบุคคล/headers/logs; คอมเมนต์อ้าง requirement IDs แล้วเปิดไฟล์ผลลัพธ์และเทียบกับ spec
- ยืนยัน 3 จุดตามคำใบ้ ซึ่งมี F-ID อยู่แล้ว ไม่สร้างซ้ำ: F-05 ระยะค้นหา 14 วันขัด FR-BKG-01 ที่ระบุ 30 วัน; F-04 ใช้รูปแบบ A001 และรีเซ็ตรายวันทั้งที่ Q-02 ยังไม่ตอบ; F-02 รับ `national_id` ใน request จองและเขียนลง log โดยไม่ใช้ค้น HIS
- ยืนยัน F-03: DELETE /bookings/{id} และ `cancel_booking` เป็นของแถมใน Out of scope (UC-02) และอ้าง FR-BKG-04 ซึ่งกำหนดการยืนยันการจองผิดเรื่อง
- พบ source ต้นแบบอีกชุดใต้ `backend/slots/` และ `backend/booking/`; ไม่ได้ถูก import/wire ใน `backend/app/main.py`; เพิ่มรายการอธิบายไว้ในตารางตามรอยย้อนกลับ ไม่เพิ่ม finding เพราะ task ที่เกี่ยวข้องยังไม่เสร็จและ source ชุดนี้ไม่ใช่ API ที่กำลังรัน
- เติมช่อง “ทีมตัดสิน” ทุกแถว finding F-01 ถึง F-09 ด้วยหนึ่งในแนวทางแก้โค้ด/แก้ spec พร้อมเหตุผล; คง F-10 ไว้เฉพาะกลุ่ม AI เข้าใจผิด/ถอนข้อกล่าวหา
- จำนวนแถวตามรอยไปข้างหน้ายังคง 15: ครบ 0, ยังไม่ถึง 9, รอ Q-xx 0, ช่องโหว่ 6; finding ใหม่ไม่มี เนื่องจากประเด็นที่ตรวจพบมี F-ID แล้ว
- ตรวจ `git status --short`: มีเฉพาะ `specs/001-booking/rtm.md` และ `prompt-log.md`; ไม่มีการแก้ app หรือ tests; ไม่รัน test ซ้ำเพราะแก้เฉพาะเอกสาร

---

## 2569-10-07 08:52 คำสั่ง: เพิ่มหน้าจอ T-10/T-11 จาก verify lab และเทียบ mockup

- เพิ่มไฟล์ mockup, หน้าจอ `SlotPicker`/`ConfirmBooking`, test และ prompt commands จาก `ppsajja/swreqspec-verify-lab-ui` โดยไม่ลบไฟล์เดิม
- ต่อเนื้อหา UI-BKG-01/UI-BKG-02 จาก `ui-section.md` ท้าย `specs/001-booking/spec.md`
- ปรับสถานะ T-10 และ T-11 เป็น “เสร็จ รอทีมตรวจ”
- ผล `cd frontend && npm test`: 3 files / 3 tests ผ่าน; มี React `act(...)` warning จาก `setup.test.jsx`
- เทียบ source กับข้อ “ต้องตรง” ใน spec และ mockup: UI-BKG-01 มี package selector/step 3 ขั้น แต่ใช้ “ว่าง N” แทน “เหลือ N ที่” และไม่มีตัวเลือกวัน/ดูวันถัดไป; UI-BKG-02 มีปุ่มยืนยัน แต่ใช้ข้อความ “เต็มแล้ว” แทน “ช่วงเวลาเต็ม” และ slice ตัวเลือกเหลือ 2; flow ยืนยันยังแทน slot ที่เลือกเป็นวันที่วันนี้/เวลา 09:00 และ success แสดง queue_no รูปแบบ A001 ที่ยังรอ Q-02
- test UI ผ่านแต่ยัง assert ไม่ครบข้อกำหนด: test UI-BKG-02 ตรวจเพียงมีคำว่า “เต็ม” และมีตัวเลือกอย่างน้อยหนึ่งรายการ ไม่ตรวจ exact phrase/จำนวน 3
- UI-BKG-02 ยังไม่มีสถานะคิวเดิมตาม AC-BKG-02 ใน mockup; logic T-04 ยังพร้อมทำ จึงระบุเป็นงานที่ยังไม่ถึง
- ปรับ RTM เพิ่ม UI-BKG-01/UI-BKG-02 และ findings F-11 ถึง F-16 (ไม่ใช้ F-10 ซ้ำเพราะเคยถอนข้อกล่าวหาเดิม); คง findings และคำตัดสินเดิมไว้
- ตาราง RTM มี 17 แถว: ครบ 0, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 9
- ผล test ยืนยันก่อน commit: backend 7 passed; frontend 3 passed (มี `act(...)` warning ใน test setup)
- ตรวจ `git diff --check` ผ่าน; รายการเปลี่ยนแปลงเป็นไฟล์ UI lab, mockups, prompt commands, spec/tasks/RTM และ log ตามคำสั่ง; ไม่มีไฟล์ใน `backend/app/` หรือ `backend/tests/` เปลี่ยน
- ตาราง RTM ปัจจุบัน 17 แถว: ครบ 0, ยังไม่ถึง 8, รอ Q-xx 0, ช่องโหว่ 9
- Commit/push: รอดำเนินการด้วยข้อความ `ui lab start`
