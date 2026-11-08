/**
 * ==============================================================================
 * สคริปต์สร้าง Google Forms แบบทดสอบอัตโนมัติ (Google Apps Script)
 * วิชา: วิศวกรรมซอฟต์แวร์ / DevOps (Week 1: Mindset & CALMS Framework)
 * 
 * วิธีใช้งาน:
 * 1. เปิดเว็บเบราว์เซอร์ แล้วพิมพ์ลิงก์: https://script.new (หรือเข้า script.google.com)
 * 2. ลบโค้ดเดิมออกทั้งหมด แล้ววาง (Paste) โค้ดด้านล่างนี้ลงไป
 * 3. กดปุ่มไอคอน "บันทึก" (รูปแผ่นดิสก์) แล้วกดปุ่ม "เรียกใช้" (Run) ด้านบน
 * 4. กดยอมรับสิทธิ์ (Review permissions -> เลือกบัญชี Google -> Advanced -> Go to Untitled project)
 * 5. ระบบจะสร้าง Google Forms ข้อสอบ 10 ข้อพร้อมเฉลยใน Google Drive ของอาจารย์ทันที!
 *    ดูลิงก์ฟอร์มที่สร้างเสร็จได้ที่ช่อง "บันทึกการดำเนินการ" (Execution Log) ด้านล่าง
 * ==============================================================================
 */

function createDevOpsQuiz() {
  // 1. สร้างแบบฟอร์ม
  var form = FormApp.create('แบบทดสอบความรู้และกรอบคิด DevOps (Pre-test / Post-test)');
  form.setDescription('วิชา: วิศวกรรมซอฟต์แวร์ / DevOps (Week 1: Mindset & CALMS Framework)\nคำชี้แจง: ให้นิสิตเลือกคำตอบที่ถูกต้องที่สุดเพียงข้อเดียว (ข้อละ 1 คะแนน รวม 10 คะแนน)');
  
  // 2. ตั้งค่าให้เป็นแบบทดสอบ (Quiz) และเก็บคะแนนอัตโนมัติ
  form.setIsQuiz(true);
  form.setAllowResponseEdits(false);
  form.setCollectEmail(false);
  
  // 3. ส่วนข้อมูลผู้สอบ
  form.addTextItem().setTitle('รหัสนิสิต (Student ID)').setRequired(true);
  form.addTextItem().setTitle('ชื่อ - นามสกุล (Full Name)').setRequired(true);
  
  // 4. ตัวเลือกประเภทแบบทดสอบ (ก่อนเรียน หรือ หลังเรียน)
  var testType = form.addMultipleChoiceItem();
  testType.setTitle('รอบการทำแบบทดสอบ')
          .setChoices([
            testType.createChoice('แบบทดสอบก่อนเรียน (Pre-test)'),
            testType.createChoice('แบบทดสอบหลังเรียน (Post-test)')
          ])
          .setRequired(true);

  // 5. รายการข้อสอบ 10 ข้อ
  var questions = [
    {
      q: "1. ปัญหา 'Works on my machine!' (โค้ดรันบนเครื่องนักพัฒนาผ่าน แต่รันบนเซิร์ฟเวอร์จริงพัง) ในมุมมองของ DevOps เกิดจากสาเหตุใดเป็นหลัก?",
      choices: [
        { text: "ก. นักพัฒนาเขียนโค้ดไม่ตรงตามมาตรฐานไวยากรณ์ (Syntax Error)", correct: false },
        { text: "ข. ความแตกต่างของสภาพแวดล้อมระบบ (Environment Parity) ระหว่างเครื่อง Dev และ Production", correct: true },
        { text: "ค. เซิร์ฟเวอร์จริงมีหน่วยความจำ (RAM) ไม่เพียงพอ", correct: false },
        { text: "ง. ทีม Ops จงใจติดตั้งซอฟต์แวร์คนละเวอร์ชันเพื่อกลั่นแกล้งทีม Dev", correct: false }
      ],
      fb: "เฉลย: ข. | เสริมความรู้: DevOps แก้ปัญหานี้ด้วยการใช้ Containerization (เช่น Docker) และ IaC เพื่อให้สภาพแวดล้อมเหมือนกันทุกระดับ"
    },
    {
      q: "2. แนวคิด 'Trunk-based Development' ในข้อใดสอดคล้องกับหลักการ Lean ของ DevOps มากที่สุด?",
      choices: [
        { text: "ก. ดองโค้ดไว้ใน Branch ส่วนตัวเป็นสัปดาห์ แล้วค่อยรวมโค้ดก่อนส่งมอบ", correct: false },
        { text: "ข. ซอยงานให้เป็นชิ้นเล็กและทยอยรวมโค้ดเข้า Branch กลางอย่างสม่ำเสมอทุกวัน", correct: true },
        { text: "ค. ห้ามรวมโค้ดเด็ดขาดหากยังเขียนฟีเจอร์ไม่เสร็จครบ 100%", correct: false },
        { text: "ง. ให้หัวหน้าทีมเป็นผู้ตรวจสอบและรวมโค้ดของทุกคนเพียงคนเดียว", correct: false }
      ],
      fb: "เฉลย: ข. | เสริมความรู้: การซอยงานเล็ก (Small Batches) ช่วยลดโอกาสเกิด Merge Conflict มหาศาลและลด Lead Time"
    },
    {
      q: "3. เมื่อระบบบน Production เกิดปัญหาหน้าชำระเงินค้างในคืนวันศุกร์ แนวทางรับมือแบบใดที่สะท้อนกรอบคิด DevOps ที่ดีที่สุด?",
      choices: [
        { text: "ก. สั่งให้ทุกคนรีโมตเข้าไปพิมพ์คำสั่งแก้โค้ดสด ๆ บน Production Server ทันที", correct: false },
        { text: "ข. ปิดเซิร์ฟเวอร์หนีกลับบ้าน แล้วรอเช้าวันจันทร์ค่อยมาเปิดล็อกไฟล์ไล่ดูทีละบรรทัด", correct: false },
        { text: "ค. สุ่มเดาจุดผิดและเขียนโค้ดแก้ร้อนรนแล้วพุชทับขึ้นไปใหม่", correct: false },
        { text: "ง. ตรวจสอบจากระบบ Monitoring และกด 1-Click Rollback ย้อนเวอร์ชันเดิมที่เสถียรในทันที", correct: true }
      ],
      fb: "เฉลย: ง. | เสริมความรู้: เป้าหมายอันดับแรกคือฟื้นฟูระบบให้ผู้ใช้บริการได้ปกติ (MTTR ต่ำ) ก่อน แล้วจึงค่อยสืบหาต้นตออย่างเป็นระบบ"
    },
    {
      q: "4. วัฒนธรรม 'Blameless Post-Mortem' มีเป้าหมายสำคัญที่สุดคืออะไร?",
      choices: [
        { text: "ก. ค้นหาตัวบุคคลที่เขียนโค้ดบรรทัดที่พัง เพื่อดำเนินการตัดเงินเดือน", correct: false },
        { text: "ข. ตรวจสอบช่องโหว่ของกระบวนการและระบบ แล้วเขียน Automated Test เพื่อไม่ให้บั๊กเดิมหลุดรอดอีก", correct: true },
        { text: "ค. การยกเลิกการปล่อยฟีเจอร์ใหม่ทั้งหมดในอนาคตเพื่อความปลอดภัย", correct: false },
        { text: "ง. การสร้างเอกสารอนุมัติขั้นตอนการทำงานให้หนาขึ้นและเพิ่มขั้นตอนการเซ็นชื่อ", correct: false }
      ],
      fb: "เฉลย: ข. | เสริมความรู้: ความผิดพลาดถือเป็นโอกาสในการเรียนรู้ มุ่งเน้นการปรับปรุงระบบ (Systemic improvement) ไม่ใช่การลงโทษบุคคล"
    },
    {
      q: "5. ตัวอักษร 'C' ในแบบจำลอง CALMS Framework หมายถึงข้อใด และมีความสำคัญอย่างไร?",
      choices: [
        { text: "ก. Cloud – การย้ายเซิร์ฟเวอร์ทั้งหมดขึ้นระบบคลาวด์เพื่อลดต้นทุน", correct: false },
        { text: "ข. Coding – การบังคับให้โปรแกรมเมอร์ทุกคนเขียนโค้ดด้วยภาษาเดียวกัน", correct: false },
        { text: "ค. Culture – การปรับวัฒนธรรมการทำงานร่วมกัน ความไว้เนื้อเชื่อใจ และการรับผิดชอบร่วม", correct: true },
        { text: "ง. Container – การบังคับให้ทุกระบบต้องรันด้วย Docker", correct: false }
      ],
      fb: "เฉลย: ค. | เสริมความรู้: DevOps มีรากฐานสำคัญที่สุดคือ 'วัฒนธรรม' ก่อนที่จะนำเครื่องมืออัตโนมัติมาเสริม"
    },
    {
      q: "6. การส่งมอบงานแบบดั้งเดิม (Traditional Silo) ที่ Dev เขียนงานเสร็จแล้ว 'โยนข้ามกำแพง' ให้ Ops ดูแล มักนำไปสู่วิกฤตใด?",
      choices: [
        { text: "ก. การผลักภาระ ขาดความรับผิดชอบร่วม และทะเลาะเบาะแว้งเมื่อระบบพัง", correct: true },
        { text: "ข. งานเสร็จเร็วเกินไปจนลูกค้าใช้งานไม่ทัน", correct: false },
        { text: "ค. ทีม Ops มีเวลาว่างมากเกินไปจนเบื่องาน", correct: false },
        { text: "ง. ระบบมีความเสถียรสูงจนไม่จำเป็นต้องมีการตรวจสอบ", correct: false }
      ],
      fb: "เฉลย: ก. | เสริมความรู้: การแบ่งแยกทีม (Silo) สร้างกำแพงแห่งความสับสน (Wall of Confusion) ระหว่างความต้องการเปลี่ยนแปลง (Dev) กับความต้องการระบบนิ่ง (Ops)"
    },
    {
      q: "7. สิ่งใดต่อไปนี้ 'ไม่ใช่' บทบาทหน้าที่ของระบบ Automated CI (Continuous Integration)?",
      choices: [
        { text: "ก. คอมไพล์และบิลด์โค้ดอัตโนมัติทุกครั้งที่มีการ Commit", correct: false },
        { text: "ข. รัน Unit Test อัตโนมัติเพื่อตรวจจับบั๊กตั้งแต่เนิ่น ๆ", correct: false },
        { text: "ค. โทรไปต่อว่าโปรแกรมเมอร์ที่เขียนโค้ดไม่ผ่านแบบส่วนตัว", correct: true },
        { text: "ง. รายงานผลการทดสอบทันทีเพื่อสร้าง Feedback Loop ที่รวดเร็ว", correct: false }
      ],
      fb: "เฉลย: ค. | เสริมความรู้: CI คือระบบอัตโนมัติที่ช่วยให้ข้อมูลสะท้อนกลับ (Feedback Loop) แก่นักพัฒนาอย่างรวดเร็วและเป็นกลาง"
    },
    {
      q: "8. ตัวชี้วัด 'Lead Time for Changes' ตามมาตรฐาน DORA Metrics หมายถึงข้อใด?",
      choices: [
        { text: "ก. เวลาตั้งแต่เริ่มพิมพ์โค้ดบรรทัดแรกจนถึงเวลาพักเที่ยง", correct: false },
        { text: "ข. เวลาตั้งแต่โค้ดถูก Commit จนกระทั่งโค้ดนั้นขึ้นไปทำงานบน Production ได้สำเร็จอย่างปลอดภัย", correct: true },
        { text: "ค. เวลาที่ใช้ในการประชุมวางแผนของทีมบริหาร", correct: false },
        { text: "ง. จำนวนวันที่เซิร์ฟเวอร์หยุดทำงานในรอบหนึ่งปี", correct: false }
      ],
      fb: "เฉลย: ข. | เสริมความรู้: ทีม DevOps ชั้นนำมี Lead Time ต่ำระดับนาทีหรือชั่วโมง เทียบกับระบบเดิมที่ใช้เวลาเป็นสัปดาห์หรือเป็นเดือน"
    },
    {
      q: "9. การที่ทีมตัดสินใจ 'แก้โค้ดสด ๆ บน Production Server เพื่อความรวดเร็ว (Hotfix on Prod)' มักก่อให้เกิดผลเสียระยะยาวที่เรียกว่าอะไร?",
      choices: [
        { text: "ก. การประหยัดทรัพยากรเซิร์ฟเวอร์", correct: false },
        { text: "ข. หนี้ทางเทคนิค (Technical Debt) และการขาดการบันทึกประวัติความเปลี่ยนแปลงที่ตรวจสอบได้", correct: true },
        { text: "ค. การเพิ่มขึ้นของโบนัสพนักงาน", correct: false },
        { text: "ง. ความเสถียรของระบบระดับสูงสุด", correct: false }
      ],
      fb: "เฉลย: ข. | เสริมความรู้: การแก้สดทำให้โค้ดบนเครื่องกับบน Server ไม่ตรงกัน เกิดบาปสูงสุดที่กู้คืนยากมาก"
    },
    {
      q: "10. ข้อความใดสะท้อนแก่นแท้ของคำว่า 'DevOps' ได้ถูกต้องสมบูรณ์ที่สุด?",
      choices: [
        { text: "ก. DevOps คือการติดตั้งซอฟต์แวร์ Jenkins และ Kubernetes ให้ครบทุกเครื่อง", correct: false },
        { text: "ข. DevOps คือตำแหน่งพนักงานไอทีคนหนึ่งที่คอยแก้ปัญหาตอนดึก", correct: false },
        { text: "ค. DevOps คือการผสมผสานปรัชญาวัฒนธรรม วิธีปฏิบัติ และเครื่องมือเพื่อเพิ่มขีดความสามารถในการส่งมอบระบบอย่างรวดเร็วและมีเสถียรภาพ", correct: true },
        { text: "ง. DevOps คือการบังคับให้นักพัฒนาต้องไปเป็นผู้ดูแลระบบแทนทีม Ops ทั้งหมด", correct: false }
      ],
      fb: "เฉลย: ค. | เสริมความรู้: สอดคล้องกับนิยามสากลของ AWS, DORA และนิยามวิชาการระดับสากล"
    }
  ];

  // 6. วนลูปสร้างข้อสอบแต่ละข้อ
  questions.forEach(function(itemData) {
    var item = form.addMultipleChoiceItem();
    item.setTitle(itemData.q)
        .setPoints(1)
        .setRequired(true);
    
    var choices = [];
    itemData.choices.forEach(function(c) {
      choices.push(item.createChoice(c.text, c.correct));
    });
    item.setChoices(choices);

    // กำหนด Feedback เฉลย
    var feedback = FormApp.createFeedback()
      .setText(itemData.fb)
      .build();
    item.setFeedbackForCorrect(feedback);
    item.setFeedbackForIncorrect(feedback);
  });

  // 7. พิมพ์ลิงก์ออกมาที่ Execution Log
  Logger.log('=====================================================');
  Logger.log('🎉 สร้าง Google Form ข้อสอบ DevOps สำเร็จแล้ว!');
  Logger.log('👉 ลิงก์สำหรับอาจารย์แก้ไขฟอร์ม: ' + form.getEditUrl());
  Logger.log('👉 ลิงก์สำหรับส่งให้นิสิตทำข้อสอบ: ' + form.getPublishedUrl());
  Logger.log('=====================================================');
}
