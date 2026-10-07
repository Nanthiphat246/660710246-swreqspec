# RTM: จองคิวตรวจสุขภาพ (Booking)
อ้างอิง: spec.md SPEC-BKG-001 Draft v2 + UI v3 | tasks.md | test-cases.md
สร้าง/ทบทวนด้วย /verify เมื่อ 2569-10-07 08:52 | test: backend 7 ผ่าน 0 ไม่ผ่าน, frontend 3 ผ่าน 0 ไม่ผ่าน

## 1. ตามรอยไปข้างหน้า (requirement ไป โค้ด ไป test)
| ID | AC | task | โค้ด (ไฟล์: ฟังก์ชัน) | test (ผล) | สถานะ |
|---|---|---|---|---|---|
| FR-BKG-01 | AC-BKG-05 (ตรวจความเร็ว ไม่ได้ตรวจรายการช่วงว่างหรือกรอบ 30 วัน) | T-02 เสร็จ; T-10 เสร็จ รอทีมตรวจ; T-12 พร้อมทำ | `backend/app/slots/router.py: get_slots`; `backend/app/slots/service.py: list_available_slots`; `frontend/src/pages/SlotPicker.jsx: SlotPicker` | `test_AC_BKG_05` ผ่าน แต่ไม่ได้ตรวจเนื้อหาหรือ 30 วัน; `SlotPicker.test.jsx` ผ่านแต่ไม่ตรวจวัน/การเรียกดูกรอบ 30 วัน | ช่องโหว่ (F-05, F-06, F-12) |
| FR-BKG-02 | AC-BKG-02 | T-04 พร้อมทำ | ยังไม่พบ logic ปฏิเสธการจองซ้ำรายวันหรือคืนคิวเดิม | ไม่มี | ยังไม่ถึง |
| FR-BKG-03 | AC-BKG-03 | T-05, T-12 พร้อมทำ; T-11 เสร็จ รอทีมตรวจ | `backend/app/booking/router.py: create_booking` ตอบ 409; `frontend/src/pages/ConfirmBooking.jsx: confirm` แสดงข้อผิดพลาด/alternatives | `AC-BKG-03.test.jsx` ผ่าน แต่ไม่ตรวจข้อความตรงตัวหรือจำนวนตัวเลือกให้ครบ 3 | ช่องโหว่ (F-13, F-14) |
| FR-BKG-04 | AC-BKG-01, AC-BKG-04 | T-03 เสร็จ; T-06 รอ Q-02; T-07 พร้อมทำ; T-11 เสร็จ รอทีมตรวจ | `backend/app/booking/service.py: create_booking, next_queue_no`; `backend/app/booking/router.py: create_booking`; `frontend/src/pages/ConfirmBooking.jsx` | `test_AC_BKG_01` ผ่านแต่ตรวจเพียง HTTP 201; TC-BKG-01 tests ผ่าน ตรวจการสร้างรายการ/ที่นั่ง/การปฏิเสธ; หน้าจอแสดง queue_no ที่สร้างด้วยรูปแบบ A001 ทั้งที่ยังรอ Q-02 | ช่องโหว่ (F-04, F-09) |
| FR-BKG-05 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่พบคิวแจ้งเตือน/ส่งซ้ำ หรือ endpoint/หน้าจอรายละเอียดการจอง | ไม่มี | ยังไม่ถึง |
| FR-BKG-06 | ไม่มี AC | T-02 เสร็จ; T-10 เสร็จ รอทีมตรวจ | `backend/app/slots/service.py: list_available_slots` กรองตามแพ็กเกจ; `frontend/src/pages/SlotPicker.jsx: SlotPicker` โหลดช่วงใหม่เมื่อแพ็กเกจเปลี่ยน | `SlotPicker.test.jsx` ผ่าน ตรวจว่ามีเวลา 10:00 หลังเปลี่ยน แต่ไม่ตรวจแทนรายการเดิม/จำนวนที่ว่าง | ช่องโหว่ (F-07) |
| NFR-PERF-01 | AC-BKG-05 | T-02 เสร็จ | `backend/app/slots/router.py: get_slots`; `backend/app/slots/service.py: list_available_slots` | `test_AC_BKG_05` ผ่าน (วัด p95 ของคำขอ 200 ครั้งแบบเรียงลำดับ ไม่ใช่ผู้ใช้พร้อมกัน 200 คน) | ช่องโหว่ (F-08) |
| NFR-SEC-01 | ไม่มี AC | ไม่มี task เฉพาะ | ไม่พบการตั้งค่า TLS ใน source ของแอป; การตั้งค่า TLS ที่ชั้น deployment ตรวจจาก repo นี้ไม่ได้ | ไม่มี | ยังไม่ถึง |
| NFR-REL-02 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่พบกลไกส่งซ้ำหรือกำหนดเวลาภายใน 5 นาที | ไม่มี | ยังไม่ถึง |
| NFR-USE-01 | ไม่มี AC | ไม่มี task เฉพาะ | ยังไม่มี flow จองบนหน้าจอที่ใช้ประเมินผู้ใช้ใหม่ | ไม่มี | ยังไม่ถึง |
| CON-TECH-01 | ไม่มี AC | T-01 เสร็จ | `backend/app/config.py: DATABASE_URL`; `backend/app/db/session.py: engine`; migration สร้าง schema ผ่าน SQLAlchemy | `test_T01_tables_created` ผ่านด้วย SQLite; config รองรับการกำหนด DATABASE_URL แต่ไม่มีหลักฐาน runtime deployment ใน repo | ยังไม่ถึง (ยืนยัน deployment ไม่ได้) |
| DOM-PDPA-01 | AC-BKG-06 | T-01 เสร็จ; T-08 พร้อมทำ | `backend/app/db/models.py: AuditLog`; ยังไม่พบการเขียน audit log หรือการบังคับเก็บอย่างน้อย 1 ปี | ไม่มี | ยังไม่ถึง |
| IF-IDP-01 | AC-BKG-01 (เงื่อนไขยืนยันตัวตน); TC-BKG-01-3 | T-03 เสร็จ | `backend/app/auth/idp.py: get_verified_hn` ตรวจเพียง prefix ใน Authorization และดึง HN จาก header; ไม่พบการตรวจผลกับ IDP | `test_TC_BKG_01_3_not_verified` ผ่านสำหรับกรณีไม่มี header เท่านั้น | ช่องโหว่ (F-01) |
| IF-HIS-01 | ไม่มี AC | T-01 เสร็จ; T-09 พร้อมทำ | ไม่มี HIS lookup; `backend/app/booking/router.py: BookingRequest, create_booking` ยังรับ `national_id` และเขียนค่าลง log; `backend/app/db/models.py: Booking` ไม่มีคอลัมน์ national_id | `test_T01_no_national_id` ผ่านเฉพาะการตรวจ schema; ไม่มี test HIS หรือการไม่เขียน national_id ลง log | ช่องโหว่ (F-02) |
| IF-NOT-01 | AC-BKG-04 | T-07 พร้อมทำ | ยังไม่พบการวางคำขอลงคิว asynchronous หรือการส่งแจ้งเตือน | ไม่มี | ยังไม่ถึง |
| UI-BKG-01 | ไม่มี AC เฉพาะ | T-10 เสร็จ รอทีมตรวจ | `frontend/src/pages/SlotPicker.jsx: SlotPicker` | `SlotPicker.test.jsx` ผ่าน แต่ข้อความจำนวนที่นั่งไม่ตรง spec และไม่มีการเลือก/เปลี่ยนวัน | ช่องโหว่ (F-11, F-12) |
| UI-BKG-02 | AC-BKG-02, AC-BKG-03; FR-BKG-04 | T-11 เสร็จ รอทีมตรวจ; FR-BKG-02 backend T-04 พร้อมทำ | `frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking, confirm` | `AC-BKG-03.test.jsx` ผ่าน แต่ข้อความและจำนวนตัวเลือกไม่ตรงข้อกำหนด; state จองซ้ำยังรอ T-04 | ช่องโหว่ (F-13, F-14) |

## 2. ตามรอยย้อนกลับ (โค้ด ไป requirement)
| โค้ด (ไฟล์: ฟังก์ชัน หรือ endpoint) | อ้าง ID | ตรงกับข้อความใน spec ไหม | หมายเหตุ |
|---|---|---|---|
| `backend/app/main.py: lifespan, app` | CON-TECH-01 | บางส่วน | สร้าง schema ด้วย `create_all`; ไม่ได้เรียก migration โดยตรง |
| `backend/app/config.py: DATABASE_URL`; `backend/app/db/session.py: engine, get_db` | CON-TECH-01 | ยังยืนยันสภาพแวดล้อมจริงไม่ได้ | SQLite ระบุไว้เป็นค่าเริ่มต้นสำหรับ Codespace; DATABASE_URL เปลี่ยนได้ตาม config การ deploy ซึ่งไม่มีใน repo จึงยังสรุปการใช้งานจริงไม่ได้ |
| `backend/app/db/models.py: Slot, Booking, AuditLog`; `backend/app/db/migrations/001_init.py: upgrade` | FR-BKG-01, FR-BKG-04, FR-BKG-06, CON-TECH-01, DOM-PDPA-01, IF-HIS-01 | บางส่วน | มี schema; bookings เก็บ HN และไม่มี national_id; ยังไม่มี retention/audit writer/HIS lookup |
| `backend/app/auth/idp.py: get_verified_hn` | IF-IDP-01 | ไม่ตรง | ตรวจ prefix จำลองแทนการรับผลยืนยันตัวตนจากระบบ IDP (F-01) |
| `backend/app/slots/router.py: GET /slots, get_slots` | FR-BKG-01, FR-BKG-06 | ไม่ครบ | ส่ง slot_id, วัน, เวลา, remaining และกรอง package_code; ไม่มี UI เปลี่ยนแพ็กเกจ |
| `backend/app/slots/service.py: list_available_slots` | FR-BKG-01, FR-BKG-06 | ไม่ตรงทั้งหมด | จำกัด 14 วันจาก date_from หรือวันนี้ แทนกรอบ 30 วัน; date_from ที่ส่งมาไม่ถูกจำกัดเทียบกับวันนี้ (F-05) |
| `backend/slots/router.py: GET /slots, get_slots`; `backend/slots/service.py: list_slots, find_nearest_available_slots` | FR-BKG-01, FR-BKG-03, FR-BKG-06 | ต้นแบบที่ยังไม่เชื่อมกับ app | อยู่คนละ package กับ `backend/app`; `app/main.py` ไม่ได้ include router นี้ จึงไม่ใช่ API ที่กำลังรัน; `list_slots` ไม่กรองเฉพาะช่วงที่เหลือที่นั่ง และใช้กรอบวันที่จาก caller; `find_nearest_available_slots` มี limit 3 และหน้าต่าง 1 วันถัดไปแต่ยังไม่มี caller/route (T-05 ยังพร้อมทำ) |
| `frontend/src/pages/SlotPicker.jsx: SlotPicker` | UI-BKG-01, FR-BKG-01, FR-BKG-06 | ไม่ตรงทั้งหมด | package selector และ step bar 3 ขั้นมี; แสดง `ว่าง N` แทนคำที่กำหนด `เหลือ N ที่`; ไม่มี control สำหรับเลือกวัน/ดูวันถัดไปในกรอบ 30 วัน (F-10, F-11) |
| `frontend/src/App.jsx: App` | UI-BKG-01, UI-BKG-02, FR-BKG-01, FR-BKG-04 | ไม่ตรงข้อมูลที่เลือก | `onNext` รับเพียง slot ID แล้วสร้างข้อมูลใหม่เป็นวันที่วันนี้และเวลา 09:00 คงที่ จึงยืนยันอาจไม่ใช่วัน/เวลาที่ผู้ใช้เลือก (F-14) |
| `frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking, confirm` | UI-BKG-02, FR-BKG-02, FR-BKG-03, FR-BKG-04 | ไม่ตรงทั้งหมด | แสดงหัวข้อ `เต็มแล้ว` ไม่ใช่ `ช่วงเวลาเต็ม`, ใช้ `.slice(0, 2)` จึงแสดงได้สูงสุด 2 ตัวเลือก; ไม่มี state คิวเดิมของ FR-BKG-02; success แสดง queue_no จริงแทน placeholder รอ Q-02 (F-04, F-12, F-13; state จองซ้ำรอ T-04) |
| `frontend/src/__tests__/SlotPicker.test.jsx: test` | UI-BKG-01, FR-BKG-06 | อ่อน | assert ว่าพบเวลา 10:00 หลังเปลี่ยน package แต่ไม่ตรวจว่าข้อมูล package เดิมหาย/ถูกแทนที่ หรือข้อความจำนวนที่นั่งตรงข้อกำหนด |
| `frontend/src/__tests__/AC-BKG-03.test.jsx: test` | UI-BKG-02, AC-BKG-03 | อ่อน | ตรวจเพียงข้อความที่มีคำว่า “เต็ม” และมีปุ่มเลือกอย่างน้อยหนึ่งปุ่ม ไม่ได้ตรวจคำตรงตัว “ช่วงเวลาเต็ม” หรือว่ามีตัวเลือก 3 รายการ (F-15) |
| `backend/app/booking/router.py: BookingRequest, POST /bookings, create_booking` | FR-BKG-02, FR-BKG-03, FR-BKG-04, IF-IDP-01, IF-HIS-01 | ไม่ครบ | มีการสร้าง booking และส่ง 409 เมื่อเต็ม; ยังไม่มี duplicate check/recommendation; รับและ log national_id โดยไม่มี HIS flow (F-02) |
| `backend/app/booking/service.py: next_queue_no` | FR-BKG-04 | ไม่ตรงกับสถานะข้อกำหนด | ใช้รูปแบบ A001 และนับใหม่รายวันทั้งที่ Q-02 ยังไม่ตอบ (F-04) |
| `backend/app/booking/service.py: create_booking` | FR-BKG-04 | บางส่วน | บันทึก booking และตัดที่นั่ง; ไม่ส่งข้อความ asynchronous; การออกเลขคิวอิงการตัดสิน Q-02 ที่ยังไม่มี |
| `backend/booking/service.py: placeholder_booking_service` | ไม่มี endpoint ที่เรียกใช้ | ไม่ได้เชื่อมกับระบบ | เป็น placeholder ที่คืน `None`; ไม่ถูก import ใน `backend/app/main.py` หรือ router จองที่ใช้งานอยู่ จึงไม่ใช่ implementation ของ FR-BKG-03/04 |
| `backend/app/booking/service.py: cancel_booking`; `backend/app/booking/router.py: DELETE /bookings/{booking_id}` | อ้าง FR-BKG-04 แต่ไม่มี FR รองรับ | ไม่ตรง — อยู่ใน Out of scope | ของแถม: endpoint ยกเลิกและคืนที่นั่งอยู่ใน Out of scope (UC-02); FR-BKG-04 กล่าวถึงการยืนยันการจอง ไม่ใช่การยกเลิก (F-03) |
| `frontend/src/App.jsx: App`; `frontend/src/main.jsx: createRoot` | ไม่มี FR ที่ทำครบ | ไม่ครบ | เป็นหน้าจอโครงเริ่มต้นเท่านั้น; ไม่มี SlotPicker, ConfirmBooking หรือ BookingResult |
| `frontend/src/api/client.js: api.getSlots, api.createBooking` | FR-BKG-01, FR-BKG-03, FR-BKG-04 | บางส่วน | มี client สำหรับค้นช่วงเวลาและยืนยัน; ไม่มี auth header, ไม่จัดการข้อผิดพลาดการค้นหา และไม่มีหน้าจอเรียกใช้ |
| `backend/tests/test_AC_BKG_05.py: test_AC_BKG_05` | NFR-PERF-01 | ไม่ครบ | ยิงคำขอเรียงลำดับ 200 ครั้ง ไม่ได้จำลอง concurrent users 200 คน (F-08) |
| `backend/tests/test_AC_BKG_01.py: test_AC_BKG_01` | FR-BKG-04, AC-BKG-01 | ไม่ครบ | ยืนยันเพียง status 201 ไม่ตรวจข้อมูลการจอง/ที่นั่ง/การแสดงหมายเลขคิว (F-09) |

## 3. ข้อค้นพบและการทบทวน
ชนิด: AC ไม่มี test / test อ่อน / โค้ดไม่มี FR / FR ไม่มี AC / เดา Q-xx / ละเมิด Constraint / ตัวเลขไม่ตรง spec / อ้าง ID ผิดเรื่อง

### จริง (มีหลักฐานใน spec/โค้ด/test)
| F-ID | ชนิด | อยู่ที่ | ขัดกับ | รายละเอียด | ทีมตัดสิน |
|---|---|---|---|---|---|
| F-01 | ละเมิด Constraint | `backend/app/auth/idp.py: get_verified_hn` | IF-IDP-01 | การตรวจเพียง prefix ใน Authorization ไม่ได้พิสูจน์ว่าได้รับผลยืนยันตัวตนจาก IDP; ผู้ส่ง header ที่ขึ้นต้นด้วย prefix จะกำหนด HN เองได้ | แก้โค้ด: ต้องตรวจ token/ผลยืนยันตัวตนจาก IDP จริง ไม่ถือ prefix ที่ผู้เรียกส่งมาเป็นหลักฐาน |
| F-02 | ละเมิด Constraint | `backend/app/booking/router.py: BookingRequest, create_booking` | IF-HIS-01 | endpoint รับ `national_id` ที่ไม่ได้ใช้ค้น HIS และเขียนค่าดังกล่าวลง log; ไม่พบ GET /patients/lookup หรือการส่งต่อไป HIS ตามสัญญา API | แก้โค้ด: เอา national_id ออกจาก request/log ของ POST /bookings และทำการค้น HIS ผ่าน flow ที่กำหนดใน T-09 |
| F-03 | โค้ดไม่มี FR | `backend/app/booking/router.py: DELETE /bookings/{booking_id}`; `backend/app/booking/service.py: cancel_booking` | Out of scope: ยกเลิก / เลื่อนคิว (UC-02); FR-BKG-04 | ของแถมที่อ้าง ID ผิดเรื่อง: มี endpoint ยกเลิกและคืนที่นั่ง ทั้งที่ UC-02 อยู่ใน Out of scope; FR-BKG-04 พูดเรื่องยืนยันการจอง ไม่ได้รองรับการยกเลิก | แก้โค้ด: ของแถม อยู่ใน Out of scope (UC-02) ลบ endpoint และ cancel_booking ออก |
| F-04 | เดา Q-02 | `backend/app/booking/service.py: next_queue_no`; `frontend/src/pages/ConfirmBooking.jsx` | Q-02, FR-BKG-04, UI-BKG-02 | backend กำหนดรูปแบบ A001 และรีเซ็ตตามวันโดยนำตัวอย่างในวงเล็บของ Q-02 มาใช้; หน้าจอแสดงหมายเลขที่สร้างตามรูปแบบนั้น ทั้งที่รูปแบบและวิธีนับยังรอคำตอบ | แก้โค้ด: งดกำหนดและแสดงรูปแบบ/วิธีนับ A001 จนกว่าเจ้าหน้าที่จะตอบ Q-02 |
| F-05 | ตัวเลขไม่ตรง spec | `backend/app/slots/service.py: DAYS_AHEAD, list_available_slots` | FR-BKG-01 | โค้ดกำหนด 14 วันแทน 30 วัน และเมื่อรับ date_from ไกลในอนาคตจะเลื่อนกรอบไปจากวันดังกล่าว ไม่ได้จำกัดกับ 30 วันข้างหน้าจากปัจจุบัน | แก้โค้ด: ใช้กรอบ 30 วันจากวันที่ปัจจุบันตาม FR-BKG-01 และไม่ให้ date_from ขยายกรอบออกนอกข้อกำหนด |
| F-06 | FR ไม่มี AC | `specs/001-booking/spec.md: AC-BKG-05; backend/tests/test_AC_BKG_05.py` | FR-BKG-01 | มี AC-BKG-05 ที่ trace ถึง FR-BKG-01 แต่ตรวจเฉพาะความเร็ว ไม่ได้ตรวจการแสดงช่วงเวลาว่างและจำนวนที่นั่งคงเหลือภายใน 30 วัน จึงไม่มี AC ที่ตรวจพฤติกรรม FR-BKG-01 โดยตรง | แก้ spec: เพิ่ม AC ที่ตรวจช่วงเวลาว่างและจำนวนที่นั่งคงเหลือภายใน 30 วัน โดยทีมกำหนด ID ตามกระบวนการ |
| F-07 | FR ไม่มี AC | `specs/001-booking/spec.md: FR-BKG-06` | FR-BKG-06 | ไม่มี AC สำหรับการเปลี่ยนแพ็กเกจแล้วคำนวณ/แสดงช่วงเวลาว่างใหม่; tasks.md และ plan.md ระบุช่องว่างนี้ด้วย | แก้ spec: เพิ่ม AC สำหรับการเปลี่ยนแพ็กเกจแล้วคำนวณช่วงเวลาว่างใหม่ โดยทีมกำหนด ID ตามกระบวนการ |
| F-08 | test อ่อน | `backend/tests/test_AC_BKG_05.py: test_AC_BKG_05` | NFR-PERF-01 | test ผ่าน p95 ≤ 2 วินาทีจาก 200 request แบบเรียงลำดับ; ไม่ทดสอบผู้ใช้พร้อมกัน 200 คนตาม NFR | แก้โค้ด: ปรับ test ประสิทธิภาพให้วัด p95 ภายใต้ผู้ใช้พร้อมกัน 200 คนตาม NFR |
| F-09 | test อ่อน | `backend/tests/test_AC_BKG_01.py: test_AC_BKG_01` | AC-BKG-01, FR-BKG-04 | test ชื่อ AC-BKG-01 ตรวจเพียง status 201 ไม่ตรวจผลการบันทึก การตัดที่นั่ง หรือการแสดงหมายเลขคิว; TC เพิ่มเติมครอบคลุมข้อมูลบางส่วน แต่ไม่มีการแสดงคิวและ T-06 ยังรอ Q-02 | แก้โค้ด: ปรับ test_AC_BKG_01 ให้ตรวจข้อมูลการจองและที่นั่ง; ส่วน assert หมายเลขคิว/หน้าจอรอคำตอบ Q-02 |
| F-11 | ข้อความ UI ไม่ตรง | `frontend/src/pages/SlotPicker.jsx: SlotPicker` | UI-BKG-01 | ต้องแสดงจำนวนที่นั่งด้วยรูปแบบ “เหลือ N ที่”; ปัจจุบันแสดง “ว่าง N” | แก้โค้ด: ใช้ข้อความ “เหลือ {N} ที่” ตาม spec |
| F-12 | UI ไม่ครบ | `frontend/src/pages/SlotPicker.jsx: SlotPicker`; `frontend/src/App.jsx: App` | UI-BKG-01, FR-BKG-01 | ไม่มี control สำหรับเลือกวัน/ดูวันถัดไป และวันถูกกำหนดจาก dateFrom ค่าเดียว จึงยังเลือกช่วงวันใน 30 วันตาม FR-BKG-01 ไม่ได้ | แก้โค้ด: เพิ่มการเลือกวัน/ดูวันถัดไปภายในกรอบที่ FR-BKG-01 กำหนด |
| F-13 | ข้อความ UI ไม่ตรง | `frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking` | UI-BKG-02, AC-BKG-03 | สถานะช่วงเต็มแสดงคำว่า “เต็มแล้ว” แทนข้อความ “ช่วงเวลาเต็ม” ที่ระบุว่าต้องตรง | แก้โค้ด: เปลี่ยน label สถานะเต็มให้ตรงกับ “ช่วงเวลาเต็ม” |
| F-14 | UI ไม่ครบ | `frontend/src/pages/ConfirmBooking.jsx: ConfirmBooking` | UI-BKG-02, FR-BKG-03 | ใช้ `.slice(0, 2)` จำกัดข้อเสนอไว้สูงสุด 2 ช่วง ทั้งที่ต้องแสดง 3 ตัวเลือกพร้อมวันและเวลา | แก้โค้ด: แสดง 3 ตัวเลือกที่ API ส่งมาและแสดงวัน/เวลาครบ |
| F-15 | ข้อมูลที่เลือกไม่ตรง | `frontend/src/App.jsx: App` | UI-BKG-01, UI-BKG-02, FR-BKG-04 | callback รับเพียง slot ID แล้วสร้าง slot ใหม่ด้วยวันที่วันนี้และเวลา 09:00 คงที่ ทำให้หน้าจอยืนยันอาจแสดงข้อมูลไม่ตรงกับช่วงที่ผู้ใช้เลือก | แก้โค้ด: ส่ง object ของช่วงเวลาที่ผู้ใช้เลือกไปยังหน้าจอยืนยันโดยไม่แทนค่าด้วยค่าคงที่ |
| F-16 | test อ่อน | `frontend/src/__tests__/AC-BKG-03.test.jsx: test` | UI-BKG-02, AC-BKG-03 | test ใช้ `toContain('เต็ม')` และตรวจจำนวนปุ่มมากกว่า 0 จึงยังผ่านได้แม้ข้อความไม่ตรงและมีตัวเลือกไม่ครบ 3 | แก้โค้ด: ปรับ assert ให้ตรวจข้อความตรงตัวและจำนวนตัวเลือกเท่ากับ 3 |

หมายเหตุสถานะ UI-BKG-02: mockup มีสถานะ “มีคิวในวันเดียวกันแล้ว” (AC-BKG-02) แต่หน้าจอยังไม่มีสถานะนี้; งาน logic ที่เกี่ยวข้อง T-04 ยังพร้อมทำ จึงติดตามเป็นงานที่ยังไม่ถึง ไม่เพิ่มเป็น finding แยกซ้ำ

### ยังไม่ถึง (ไม่จัดเป็นข้อค้นพบ)
- FR-BKG-02 / AC-BKG-02: T-04 ยังพร้อมทำ
- FR-BKG-03 / AC-BKG-03: T-05, T-11, T-12 ยังพร้อมทำ
- FR-BKG-05, NFR-REL-02, IF-NOT-01 / AC-BKG-04: T-07 ยังพร้อมทำ
- DOM-PDPA-01 / AC-BKG-06: T-08 ยังพร้อมทำ
- IF-HIS-01: T-09 ยังพร้อมทำ (แยกจากประเด็นรับและ log `national_id` ใน F-02)
- NFR-SEC-01, NFR-USE-01: ยังไม่มี task ที่ดำเนินการ
- CON-TECH-01: repo ไม่มีข้อมูล runtime deployment ให้ยืนยันฐานข้อมูล production; ค่า SQLite เป็นค่าเริ่มต้นสำหรับ Codespace จึงยังตัดสินผลระบบจริงไม่ได้

### AI เข้าใจผิด / ถอนข้อกล่าวหา
- F-10 เดิม: ข้อกล่าวหาว่า CON-TECH-01 ถูกละเมิดจากค่าเริ่มต้น SQLite ไม่มีหลักฐานรองรับ เพราะ config และ plan ระบุว่า SQLite ใช้ใน Codespace และระบบจริงกำหนด PostgreSQL ผ่าน DATABASE_URL ได้; ถอน F-10 จากข้อค้นพบ โดยไม่สรุปแทนว่า production ตั้งค่าแล้ว

## 4. แก้แล้ว
| F-ID | แก้อย่างไร | รู้ได้อย่างไร |
|---|---|---|
