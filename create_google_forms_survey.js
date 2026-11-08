/**
 * ==============================================================================
 * สคริปต์สร้าง Google Forms แบบประเมินความพึงพอใจและแรงจูงใจอัตโนมัติ (Google Apps Script)
 * วิชา: วิศวกรรมซอฟต์แวร์ / DevOps (Week 1: Mindset & CALMS Framework)
 * 
 * วิธีใช้งาน:
 * 1. เปิดเว็บเบราว์เซอร์ แล้วพิมพ์: https://script.new
 * 2. ลบโค้ดเดิมออกทั้งหมด แล้ววาง (Paste) โค้ดด้านล่างนี้ลงไป
 * 3. กดบันทึก (แผ่นดิสก์) แล้วกดปุ่ม "เรียกใช้" (Run)
 * 4. ระบบจะสร้าง Google Forms แบบประเมินความพึงพอใจ 10 ข้อ (มาตรวัด Likert 5 ระดับ) 
 *    พร้อมเปิดลิงก์ให้ใน Execution Log ทันที!
 * ==============================================================================
 */

function createDevOpsSurvey() {
  // 1. สร้างแบบฟอร์ม
  var form = FormApp.create('แบบประเมินความพึงพอใจและแรงจูงใจในการเรียนรู้ (DevOps Gamification Lab)');
  form.setDescription(
    'คำชี้แจง: แบบประเมินนี้มีวัตถุประสงค์เพื่อประเมินความพึงพอใจและแรงจูงใจในการเรียนรู้ของนิสิตต่อการใช้งานเว็บแอปพลิเคชันเกมจำลองสถานการณ์ DevOps\n' +
    'เกณฑ์การประเมิน: 5 = เห็นด้วยอย่างยิ่ง, 4 = เห็นด้วย, 3 = ปานกลาง, 2 = ไม่เห็นด้วย, 1 = ไม่เห็นด้วยอย่างยิ่ง'
  );
  
  form.setAllowResponseEdits(false);
  form.setCollectEmail(false);

  // 2. ข้อมูลทั่วไปของผู้ตอบ
  form.addTextItem().setTitle('รหัสนิสิต (Student ID)').setRequired(true);
  form.addTextItem().setTitle('ชื่อ - นามสกุล (Full Name)').setRequired(false);

  // 3. หมวดที่ 1: ด้านเนื้อหาและความเข้าใจ (Cognitive & Learning Value)
  form.addPageBreakItem().setTitle('หมวดที่ 1: ด้านเนื้อหาและคุณค่าการเรียนรู้ (Learning Value)');

  var q1 = form.addScaleItem();
  q1.setTitle('1. เกมจำลองสถานการณ์ช่วยให้เห็นภาพผลกระทบของการทำงานแบบ Silo และการแก้ผ้าเอาหน้ารอดได้ชัดเจนขึ้น')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q2 = form.addScaleItem();
  q2.setTitle('2. ผู้เรียนเข้าใจความหมายและหัวใจสำคัญของ CALMS Framework ชัดเจนขึ้นกว่าการฟังบรรยายเพียงอย่างเดียว')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q3 = form.addScaleItem();
  q3.setTitle('3. เกมช่วยให้เข้าใจคุณค่าของการทำ Automation (CI/CD) และการซอยงานเล็ก (Trunk-based) อย่างเป็นรูปธรรม')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q4 = form.addScaleItem();
  q4.setTitle('4. ผู้เรียนตระหนักถึงความสำคัญของวัฒนธรรมการไม่ชี้นิ้วหาคนผิด (Blameless Post-Mortem) ในการทำงานจริง')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  // 4. หมวดที่ 2: ด้านความน่าสนใจและแรงจูงใจ (Engagement & Motivation)
  form.addPageBreakItem().setTitle('หมวดที่ 2: ด้านความน่าสนใจและแรงจูงใจ (Engagement & Motivation)');

  var q5 = form.addScaleItem();
  q5.setTitle('5. สถานการณ์จำลองและบทสนทนา (NPC Dialogue) มีความสมจริงและกระตุ้นให้อยากติดตามแก้ปัญหา')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q6 = form.addScaleItem();
  q6.setTitle('6. ระบบเสียงเอฟเฟกต์ (Audio FX) ช่วยเพิ่มความตื่นเต้นและสร้างบรรยากาศการเรียนรู้ที่สนุกสนาน')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q7 = form.addScaleItem();
  q7.setTitle('7. ระบบฉายาตอนจบ (Badges) และการ์ดรายงานผล ทำให้รู้สึกท้าทายและอยากพัฒนาทักษะการตัดสินใจ')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  // 5. หมวดที่ 3: ด้านการออกแบบและการใช้งาน (Usability & Design)
  form.addPageBreakItem().setTitle('หมวดที่ 3: ด้านการออกแบบและการใช้งาน (Usability & Design)');

  var q8 = form.addScaleItem();
  q8.setTitle('8. ระบบใช้งานง่าย เข้าถึงได้สะดวกผ่านเว็บเบราว์เซอร์ และทำงานได้ราบรื่น')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q9 = form.addScaleItem();
  q9.setTitle('9. การแสดง Feedback เหตุผลอธิบายผลลัพธ์ทันทีหลังกดเลือก ช่วยให้เข้าใจข้อผิดพลาดได้ตรงจุด')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  var q10 = form.addScaleItem();
  q10.setTitle('10. โดยภาพรวม ผู้เรียนพึงพอใจและต้องการให้มีเกมนวัตกรรมเช่นนี้ในหัวข้อการเรียนรู้อื่น ๆ ต่อไป')
    .setBounds(1, 5)
    .setLabels('ไม่เห็นด้วยอย่างยิ่ง', 'เห็นด้วยอย่างยิ่ง')
    .setRequired(true);

  // 6. ข้อเสนอแนะเพิ่มเติม
  var feedbackItem = form.addParagraphTextItem();
  feedbackItem.setTitle('ข้อเสนอแนะเพิ่มเติม หรือสิ่งที่อยากให้ปรับปรุงในเกม')
              .setRequired(false);

  // 7. พิมพ์ลิงก์ออกมาที่ Execution Log
  Logger.log('=====================================================');
  Logger.log('🎉 สร้าง Google Form แบบประเมินความพึงพอใจสำเร็จแล้ว!');
  Logger.log('👉 ลิงก์สำหรับอาจารย์แก้ไขฟอร์ม: ' + form.getEditUrl());
  Logger.log('👉 ลิงก์สำหรับส่งให้นิสิตทำแบบประเมิน: ' + form.getPublishedUrl());
  Logger.log('=====================================================');
}
