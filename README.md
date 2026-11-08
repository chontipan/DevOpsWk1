# 🚀 DevOps Interactive Learning Lab (Week 1: Mindset & CALMS)

เว็บแอปพลิเคชันจำลองการเรียนรู้เชิงปฏิสัมพันธ์ (Interactive Learning Simulation) สำหรับนิสิตวิชา **DevOps (คาบที่ 1: Mindset, Culture & CALMS)** 
สาขาวิชาวิศวกรรมซอฟต์แวร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา

---

## 🎮 กิจกรรมการเรียนรู้ภายในแล็บ

1. **เกมที่ 1: คืนวันศุกร์สุดระทึก (Crisis Simulator)**
   - จำลองสถานการณ์วิกฤต 4 ด่าน (การรวมโค้ด, การนำขึ้นเซิร์ฟเวอร์, รับมือระบบล่มตอนค่ำ, และวัฒนธรรม Post-Mortem)
   - **ระบบนับเวลาถอยหลัง 60 วินาทีต่อข้อ** เพื่อกระตุ้นการตัดสินใจในภาวะกดดัน
   - คำนวณ Lead Time สะสม, ความเสถียรของระบบ (System Stability), และขวัญกำลังใจทีม (Team Morale)

2. **เกมที่ 2: ภารกิจหมอสายพานกู้ชีพ (DevOps Incident Doctor)**
   - จำลองปัญหาคอขวดใน Deployment Pipeline ทั้ง 4 สเตจ (Merge ➔ Test ➔ Deploy ➔ Production)
   - ให้ผู้เรียนวิเคราะห์เลือก **การ์ดทางเลือกกู้ชีพ 3 ใบ** ต่อด่าน (มีมุกตลก/ข้อผิดพลาดจริง vs แนวคิด DevOps สากล)
   - ปลดล็อกทักษะตามกรอบ **CALMS**:
     - สเตจ 1: **Lean** (ซอยงานเล็ก Trunk-based Development)
     - สเตจ 2: **CI** (Continuous Integration & Automated Test Bot)
     - สเตจ 3: **CD & Container** (Docker & Script Deployment อัตโนมัติ)
     - สเตจ 4: **Measurement & Sharing** (Real-time Monitoring, 1-Click Rollback & Blameless Culture)

3. **ระบบสรุปผลคะแนน & แผงควบคุมผู้สอน (Admin Dashboard)**
   - ปลดล็อกสร้างการ์ดคะแนนเมื่อผ่านภารกิจทั้ง 2 เกมครบถ้วน (กรอกเพียงรหัสนิสิตและชื่อ-นามสกุล)
   - สร้าง Verification Hash ป้องกันการแก้ไขคะแนน
   - **แผงควบคุมอาจารย์ (Admin):** ล็อกอินดูรายชื่อคะแนนนิสิตแบบเรียลไทม์ และกด **Export to Excel (.csv)** ได้ในคลิกเดียว
   - รองรับการเก็บข้อมูลอัตโนมัติผ่าน **Netlify Forms** ในตัว
