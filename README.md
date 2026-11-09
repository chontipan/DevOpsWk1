# 🚀 DevOps Interactive Learning Lab (Week 1: Mindset & CALMS)

🌐 **Production URL:** [https://devopswk1.vercel.app/](https://devopswk1.vercel.app/)

เว็บแอปพลิเคชันจำลองการเรียนรู้เชิงปฏิสัมพันธ์ (Interactive Learning Simulation) สำหรับนิสิตวิชา **DevOps (คาบที่ 1: Mindset, Culture & CALMS)** 
สาขาวิชาวิศวกรรมซอฟต์แวร์ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา

---

## 🌟 จุดเด่นและระบบสนับสนุนการวิจัย (Research-Ready Features)
- 🌐 **ระบบ 2 ภาษา (Bilingual Support):** สลับภาษาไทย 🇹🇭 / English 🇬🇧 ได้ทันทีทุกส่วนของระบบ
- ⚡ **Realtime WebSocket Integration:** สตรีมข้อมูลผลคะแนนสดผ่าน Supabase PostgreSQL Realtime โดยไม่ต้องกดปุ่มรีเฟรช
- 📊 **Learning Analytics Telemetry (24 คอลัมน์):** บันทึกการตัดสินใจรายด่าน, ข้อผิดพลาดรายขั้นตอน (Cognitive Bottlenecks), เวลาเล่นจริง (Time-on-Task), และค่าความเสถียร/ขวัญกำลังใจ
- 📥 **One-Click CSV Export:** ส่งออกข้อมูลเรียงตามรหัสนิสิต พร้อมใช้งานกับ SPSS/R/Python เพื่อวิเคราะห์สถิติสำหรับตีพิมพ์วารสารนานาชาติ (Scopus Q3/Q4)
- 🖼️ **Save Slip as PNG:** บันทึกสลิปผลคะแนนความละเอียดสูง (Retina Quality) พร้อม Verification Hash
- 🔐 **Admin Dashboard:** แผงควบคุมผู้สอนพร้อมสรุปภาพรวมชั้นเรียนแบบสด (รหัสผ่าน: `227302`)
- 🛡️ **Anti-Tamper & Clean State:** ระบบรีเซ็ตค่าสะอาดทุกครั้งที่รีเฟรชหน้าเว็บ (No LocalStorage Cache Leak) และล็อกการส่งคะแนนซ้ำ

---

## 🎮 กิจกรรมการเรียนรู้ภายในแล็บ

1. **เกมที่ 1: คืนวันศุกร์สุดระทึก (Crisis Simulator)**
   - จำลองสถานการณ์วิกฤต 4 ด่าน (การรวมโค้ด, การนำขึ้นเซิร์ฟเวอร์, รับมือระบบล่มตอนค่ำ, และวัฒนธรรม Post-Mortem)
   - ปะทะกันระหว่าง **Real-world Industry Anti-patterns** กับ **DevOps Best Practices**
   - สุ่มสลับตัวเลือก (Anti-cheating) และแสดง Instant Feedback พร้อมแท็กแกน **CALMS**
   - คำนวณ Lead Time สะสม, ความเสถียรของระบบ (System Stability), และขวัญกำลังใจทีม (Team Morale)

2. **เกมที่ 2: ภารกิจหมอสายพานกู้ชีพ (DevOps Incident Doctor)**
   - จำลองปัญหาคอขวดใน Deployment Pipeline ทั้ง 4 สเตจ (Merge ➔ Test ➔ Deploy ➔ Production)
   - ให้ผู้เรียนวิเคราะห์เลือก **การ์ดทางเลือกกู้ชีพ 3 ใบ** ต่อด่าน ที่มีทั้ง Anti-pattern ลวงและทางเลือกที่ถูกต้อง
   - ปลดล็อกทักษะตามกรอบ **CALMS**:
     - สเตจ 1: **Lean** (Trunk-based Development vs Code Freeze)
     - สเตจ 2: **CI** (Continuous Integration vs Deferred Testing Debt)
     - สเตจ 3: **CD & Container** (Immutable Containers vs Manual VM Drift)
     - สเตจ 4: **Measurement & Sharing** (Observability & Blameless vs Band-aid Restart & Blame)
   - การ์ดสรุปเปรียบเทียบมาตรฐาน **DORA Metrics Benchmark**

3. **ระบบบันทึกคะแนน & แผงควบคุมผู้สอน (Admin Dashboard)**
   - บันทึกคะแนนและออกสลิปผลงานเมื่อผ่านภารกิจทั้ง 2 เกมครบถ้วน
   - สร้าง Verification Hash ป้องกันการปลอมแปลงคะแนน
   - **แผงควบคุมอาจารย์ (Admin):** สตรีมข้อมูลนิสิตสดผ่าน WebSocket, ค้นหารหัสนิสิต, และกด **Export to Excel (.csv)** ได้ในคลิกเดียว
