#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_proposal_docx.py
สร้างเอกสารข้อเสนอโครงการวิจัย งบประมาณส่วนตัว คณะ ICT มหาวิทยาลัยพะเยา (.docx)
โดยใช้ pythainlp แทรก Zero-Width Space (ZWS) เพื่อให้ภาษาไทยตัดบรรทัดได้ถูกต้องสวยงาม
"""

import os
import re
from pythainlp import word_tokenize
import docx
from docx import Document
from docx.shared import Pt, Cm, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

ZWS = "\u200b"

def insert_zwsp(text: str) -> str:
    if not text:
        return ""
    thai_pattern = re.compile(r'([\u0E00-\u0E7F]+)')
    parts = thai_pattern.split(text)
    result = []
    for part in parts:
        if thai_pattern.fullmatch(part):
            tokens = word_tokenize(part, engine="newmm")
            result.append(ZWS.join(tokens))
        else:
            result.append(part)
    return "".join(result)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: dict(sz=12, val='single', color='CCCCCC')
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(r'<w:tcBorders %s/>' % nsdecls('w'))
    for edge in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = parse_xml(r'<%s %s w:val="%s" w:sz="%s" w:space="0" w:color="%s"/>' %
                                (tag, nsdecls('w'), edge_data.get('val', 'single'),
                                 edge_data.get('sz', '4'), edge_data.get('color', 'auto')))
            tcBorders.append(element)
    tcPr.append(tcBorders)

def set_cell_shading(cell, color_hex):
    shading_elm = parse_xml(r'<w:shd %s w:fill="%s"/>' % (nsdecls('w'), color_hex))
    cell._tc.get_or_add_tcPr().append(shading_elm)

def add_para(doc, text="", bold=False, italic=False, size_pt=16, align=WD_ALIGN_PARAGRAPH.LEFT,
             space_before=0, space_after=3, line_spacing=1.15, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = line_spacing
    
    if text:
        zw_text = insert_zwsp(text)
        run = p.add_run(zw_text)
        run.bold = bold
        run.italic = italic
        run.font.name = "TH Sarabun New"
        run.font.size = Pt(size_pt)
        if color:
            run.font.color.rgb = color
            
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(r'<w:rFonts %s w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New"/>' % nsdecls('w'))
        rPr.append(rFonts)
    return p

def add_run_to_p(p, text="", bold=False, italic=False, size_pt=16, color=None):
    zw_text = insert_zwsp(text)
    run = p.add_run(zw_text)
    run.bold = bold
    run.italic = italic
    run.font.name = "TH Sarabun New"
    run.font.size = Pt(size_pt)
    if color:
        run.font.color.rgb = color
    rPr = run._r.get_or_add_rPr()
    rFonts = parse_xml(r'<w:rFonts %s w:ascii="TH Sarabun New" w:hAnsi="TH Sarabun New" w:cs="TH Sarabun New"/>' % nsdecls('w'))
    rPr.append(rFonts)
    return run

def create_table(doc, rows, cols, col_widths=None):
    tbl = doc.add_table(rows=rows, cols=cols)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    if col_widths:
        for row in tbl.rows:
            for idx, width in enumerate(col_widths):
                row.cells[idx].width = Cm(width)
    return tbl

def format_cell(cell, text="", bold=False, size_pt=14, align=WD_ALIGN_PARAGRAPH.LEFT, bg_hex=None, border=True):
    p = cell.paragraphs[0]
    p.alignment = align
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.05
    if text:
        add_run_to_p(p, text, bold=bold, size_pt=size_pt)
    if bg_hex:
        set_cell_shading(cell, bg_hex)
    if border:
        set_cell_border(cell,
                        top=dict(sz=4, val='single', color='B0B0B0'),
                        bottom=dict(sz=4, val='single', color='B0B0B0'),
                        left=dict(sz=4, val='single', color='B0B0B0'),
                        right=dict(sz=4, val='single', color='B0B0B0'))
    cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER

def build_proposal_doc(output_path):
    doc = Document()

    # ตั้งค่าหน้ากระดาษ A4 ขอบ 2.54 ซม. (1 นิ้ว) มาตรฐาน
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(2.54)
    section.right_margin = Cm(2.54)

    # ------------------ ส่วนหัวเอกสาร ------------------
    add_para(doc, "ข้อเสนอโครงการวิจัย ประจำปี 2569", bold=True, size_pt=18, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1)
    add_para(doc, "งบประมาณส่วนตัว คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา", bold=True, size_pt=16, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    
    # เส้นคั่น
    p_line = add_para(doc, "_________________________________________________________________________________", bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=8)
    
    # ชื่อโครงการ
    p_title = add_para(doc, "ชื่อโครงการวิจัย (ภาษาไทย)\t", bold=True, size_pt=16, space_after=2)
    add_run_to_p(p_title, "การพัฒนาและประเมินผลสัมฤทธิ์ของเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบเพื่อเสริมสร้างกรอบความคิดและวัฒนธรรมเดฟออปส์สำหรับนิสิตระดับปริญญาตรี", bold=False, size_pt=16)

    p_title_en = add_para(doc, "                \t(ภาษาอังกฤษ)\t", bold=True, size_pt=16, space_after=6)
    add_run_to_p(p_title_en, "Development and Evaluation of an Interactive Scenario-Based Simulation Game to Foster DevOps Mindset and Culture for Undergraduate Students", bold=False, size_pt=16)

    # ------------------ ส่วน ก : ลักษณะโครงการวิจัย ------------------
    add_para(doc, "ส่วน ก : ลักษณะโครงการวิจัย", bold=True, size_pt=16, space_before=4, space_after=2)
    add_para(doc, "\tประเภทโครงการ", bold=True, size_pt=16, space_after=1)
    add_para(doc, "\t\t[X] โครงการวิจัยใหม่", bold=False, size_pt=16, space_after=2)
    
    add_para(doc, "\tประเภทงานวิจัย", bold=True, size_pt=16, space_after=1)
    add_para(doc, "\t[ ] พื้นฐาน (Basic Research)             [X] พัฒนาและประยุกต์ (Development)\n"
                  "\t[X] วิจัยเชิงปฏิบัติการ (Operational Research)    [ ] วิจัยทางด้านคลินิก (Clinical Trial)\n"
                  "\t[ ] วิจัยต่อยอด (Translational research)     [ ] การขยายผลงานวิจัย (Implementation)",
             bold=False, size_pt=16, space_after=6)

    # ------------------ ส่วน ข : องค์ประกอบในการจัดทำ ------------------
    add_para(doc, "ส่วน ข : องค์ประกอบในการจัดทำ", bold=True, size_pt=16, space_before=4, space_after=2)

    # 1. ผู้รับผิดชอบ
    add_para(doc, "1. ผู้รับผิดชอบ", bold=True, size_pt=16, space_after=2)
    tbl1 = create_table(doc, 2, 5, col_widths=[2.5, 4.0, 3.2, 5.2, 2.0])
    headers1 = ["คำนำหน้า", "ชื่อ-สกุล", "ตำแหน่งในโครงการ", "หน่วยงาน", "สัดส่วน (%)"]
    for i, h in enumerate(headers1):
        format_cell(tbl1.rows[0].cells[i], h, bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    
    data1 = ["นาย", "ชลติพันธ์ เปล่งวิทยา", "หัวหน้าโครงการ", "คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา", "100"]
    for i, d in enumerate(data1):
        align = WD_ALIGN_PARAGRAPH.CENTER if i in [0, 2, 4] else WD_ALIGN_PARAGRAPH.LEFT
        format_cell(tbl1.rows[1].cells[i], d, bold=False, size_pt=14, align=align)

    add_para(doc, "", space_after=4)

    # 2. สาขาที่สอดคล้อง
    add_para(doc, "2. สาขาที่สอดคล้องกับงานวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t2.1 สาขาการวิจัยหลัก OECD\t2. วิศวกรรมและเทคโนโลยี\n"
                  "\t     สาขาการวิจัยย่อย OECD\t2.2 วิศวกรรมและเทคโนโลยี : เทคโนโลยีอิเล็กทรอนิกส์ คอมพิวเตอร์และสารสนเทศ\n"
                  "\t     ด้านการวิจัย\t          \tวิทยาศาสตร์และเทคโนโลยี / การศึกษาวิศวกรรมซอฟต์แวร์ (Software Engineering Education)",
             bold=False, size_pt=16, space_after=2)
    add_para(doc, "\t2.2 สาขา ISCED\t06 Information and Communication Technologies (ICTs)\n"
                  "\t\t\t061 Information and Communication Technologies (ICTs)\n"
                  "\t\t\t0612 Database and network design and administration / Software Engineering",
             bold=False, size_pt=16, space_after=6)

    # 3. คำสำคัญ
    add_para(doc, "3. คำสำคัญ (keyword)", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\tคำสำคัญ (TH)\tเดฟออปส์, การจำลองสถานการณ์เชิงโต้ตอบ, เกมเพื่อการเรียนรู้, กรอบความคิดแบบเดฟออปส์, การศึกษาวิศวกรรมซอฟต์แวร์\n"
                  "\tคำสำคัญ (EN)\tDevOps, Interactive Simulation, Serious Games, DevOps Mindset, Software Engineering Education",
             bold=False, size_pt=16, space_after=6)

    # 4. เป้าหมายการวิจัย
    add_para(doc, "4. เป้าหมายการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t4.1 เป้าหมายเชิงปริมาณ\n"
                  "\t    1) เว็บแอปพลิเคชันเกมจำลองสถานการณ์ DevOps เชิงโต้ตอบ จำนวน 1 ระบบ (ประกอบด้วย 2 เกม: Crisis Simulator และ Pipeline Incident Doctor)\n"
                  "\t    2) กลุ่มตัวอย่างนิสิตระดับปริญญาตรี สาขาวิชาวิศวกรรมซอฟต์แวร์ / วิทยาการคอมพิวเตอร์ จำนวนไม่น้อยกว่า 30 คน\n"
                  "\t4.2 เป้าหมายเชิงคุณภาพ\n"
                  "\t    1) ผู้เรียนมีผลสัมฤทธิ์ทางการเรียนรู้และกรอบคิดด้าน DevOps (CALMS Framework) สูงขึ้นอย่างมีนัยสำคัญทางสถิติหลังการใช้นวัตกรรม\n"
                  "\t    2) เกิดการปรับเปลี่ยนกรอบคิด (Conceptual Shift) จากความเข้าใจผิดที่ยึดติดกับเครื่องมือ (Tool-Obsession) ไปสู่ความเข้าใจด้านวัฒนธรรมการทำงานร่วมกันและการรับผิดชอบร่วม (Shared Ownership & Blameless Culture)",
             bold=False, size_pt=16, space_after=6)

    # 5. ความสำคัญและที่มาของปัญหา
    add_para(doc, "5. ความสำคัญและที่มาของปัญหาที่ทำการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "ในยุคปัจจุบัน การพัฒนาและส่งมอบซอฟต์แวร์ได้ก้าวเข้าสู่วิถีของเดฟออปส์ (DevOps) ซึ่งเป็นการผสานปรัชญาวัฒนธรรม วิธีปฏิบัติ และเครื่องมือเพื่อเพิ่มขีดความสามารถขององค์กรในการส่งมอบบริการและแอปพลิเคชันได้อย่างรวดเร็ว มีเสถียรภาพ และตอบสนองต่อธุรกิจได้ทันท่วงที องค์กรชั้นนำทั่วโลกจึงมีความต้องการวิศวกรซอฟต์แวร์ที่มีความรู้และกรอบคิดด้าน DevOps สูงขึ้นอย่างก้าวกระโดด อย่างไรก็ตาม ในบริบทของการจัดการเรียนการสอนระดับอุดมศึกษา งานวิจัยด้านการศึกษาวิศวกรรมซอฟต์แวร์ระดับนานาชาติ (Ferino et al., 2021; Hobeck et al., 2021) ได้รายงานถึงความท้าทายสำคัญประการหนึ่ง คือ \"ความเข้าใจผิดที่ยึดติดกับเครื่องมือ\" (Tool-Obsession Misconception) ซึ่งผู้เรียนส่วนใหญ่มักเข้าใจว่า DevOps คือการเรียนรู้และติดตั้งซอฟต์แวร์เครื่องมือทางเทคนิค (เช่น Docker, Kubernetes, Jenkins, CI/CD Pipeline) เท่านั้น แต่มองข้ามและขาดความเข้าใจในมิติเชิงนามธรรมที่เป็นแก่นแท้ ได้แก่ วัฒนธรรมความรับผิดชอบร่วมกัน (Shared Ownership), วัฒนธรรมการไม่ชี้นิ้วหาคนผิด (Blameless Post-Mortem Culture) และแบบจำลอง CALMS (Culture, Automation, Lean, Measurement, Sharing)",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "นอกจากนี้ การจัดการเรียนรู้ด้วยการบรรยายแบบดั้งเดิม (Traditional Lecture) ในห้องเรียน ประสบข้อจำกัดอย่างยิ่งในการถ่ายทอดเนื้อหาที่เป็นนามธรรมเหล่านี้ เนื่องจากผู้เรียนไม่สามารถมองเห็นภาพหรือสัมผัสถึงความกดดัน ความสูญเสียเชิงธุรกิจ ความเสถียรของระบบ (System Stability) และขวัญกำลังใจของทีม (Team Morale) ที่เกิดขึ้นจริงเมื่อเกิดวิกฤติตอนส่งมอบงาน การบรรยายเพียงฝ่ายเดียวจึงไม่สามารถสร้างความตระหนักรู้ถึงหนี้ทางเทคนิค (Technical Debt) หรือคอขวดที่เกิดจากการทำงานแบบไซโล (Silo Mentality) ได้อย่างลึกซึ้ง (Christensen, 2016)",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "ด้วยเหตุนี้ ผู้วิจัยจึงได้พัฒนาเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบ (Interactive Scenario-Based Simulation Game) ขึ้นเพื่อเป็นเครื่องมือนวัตกรรมการเรียนรู้ โดยจำลองสถานการณ์วิกฤติในคืนวันศุกร์ (Crisis Simulator) และภารกิจกู้ชีพสายพานส่งมอบงาน (Pipeline Incident Doctor) ผ่านกลไกเกมที่มีการแสดงผลสะท้อนกลับทันที (Instant Feedback), การสลับตัวเลือกแบบสุ่มเพื่อป้องกันการลอกกัน (Dynamic Choice Randomization), ระบบเสียงสังเคราะห์ Web Audio FX, และการเชื่อมโยงผลกระทบเข้ากับตัวชี้วัด DORA Metrics ในระดับสากล เพื่อเป็นสื่อกลางที่ช่วยให้นิสิตได้สัมผัสกับผลกระทบของการตัดสินใจด้วยตนเอง และนำไปสู่การเปลี่ยนผ่านกรอบคิด DevOps ได้อย่างเป็นรูปธรรม",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "การวิจัยนี้จึงมุ่งศึกษาและประเมินผลสัมฤทธิ์ทางการเรียนรู้ พฤติกรรมการตัดสินใจ และระดับการยอมรับเทคโนโลยีของผู้เรียน เพื่อสร้างแนวปฏิบัติที่ดี (Best Practice) ในการจัดการเรียนการสอนวิศวกรรมซอฟต์แวร์ อันจะช่วยปิดช่องว่างระหว่างความรู้ในตำรากับทักษะวิชาชีพที่ภาคอุตสาหกรรมซอฟต์แวร์ต้องการอย่างแท้จริง",
             bold=False, size_pt=16, space_after=6)

    # 6. วัตถุประสงค์
    add_para(doc, "6. วัตถุประสงค์ของโครงการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t1. เพื่อพัฒนาเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบสำหรับเสริมสร้างกรอบความคิดและวัฒนธรรมเดฟออปส์ (DevOps Mindset & CALMS Framework)\n"
                  "\t2. เพื่อเปรียบเทียบผลสัมฤทธิ์ทางการเรียนรู้ของผู้เรียนก่อนและหลังการใช้งานเว็บแอปพลิเคชันเกมจำลองสถานการณ์\n"
                  "\t3. เพื่อวิเคราะห์พฤติกรรมการตัดสินใจและรูปแบบการแก้ปัญหาของผู้เรียนผ่านข้อมูลการใช้งานในระบบ (In-Game Learning Analytics)\n"
                  "\t4. เพื่อประเมินความพึงพอใจและแรงจูงใจในการเรียนรู้ของผู้เรียนต่อการใช้งานระบบนวัตกรรม",
             bold=False, size_pt=16, space_after=6)

    # 7. ขอบเขต
    add_para(doc, "7. ขอบเขตของการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t7.1 ขอบเขตด้านพื้นที่/องค์กร\n"
                  "\t\tดำเนินการ ณ คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา\n"
                  "\t7.2 ขอบเขตด้านเนื้อหา\n"
                  "\t\tมุ่งเน้นการเสริมสร้างความรู้และกรอบคิด DevOps ตามแบบจำลอง CALMS (Culture, Automation, Lean, Measurement, Sharing) และตัวชี้วัด DORA Metrics ผ่าน 2 สถานการณ์จำลอง ได้แก่ เกมคืนวันศุกร์สุดระทึก (Crisis Simulator) และเกมหมอสายพานกู้ชีพ (Incident Doctor)\n"
                  "\t7.3 ขอบเขตการเก็บรวบรวมข้อมูล (วิธีการและระยะเวลาในการเก็บข้อมูล)\n"
                  "\t\tกลุ่มเป้าหมายคือนิสิตระดับปริญญาตรี คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา ที่ลงทะเบียนเรียนในรายวิชาที่เกี่ยวข้องกับวิศวกรรมซอฟต์แวร์/ระบบคลาวด์ จำนวนไม่น้อยกว่า 30 คน เครื่องมือที่ใช้ ได้แก่ แบบทดสอบก่อน-หลังเรียน (Pre/Post-test 10 ข้อ), แบบประเมินความพึงพอใจ (10 ข้อ), ข้อมูลบันทึกพฤติกรรมในระบบ (In-Game Telemetry), และข้อความสะท้อนคิด (Reflection Logs)\n"
                  "\t7.4 ขอบเขตด้านระยะเวลา\n"
                  "\t\t12 เดือน (มกราคม 2569 – ธันวาคม 2569)\n"
                  "\t7.5 ข้อจำกัดในการวิจัย\n"
                  "\t\tการวิจัยนี้มุ่งเน้นการศึกษาในบริบทของนิสิตระดับปริญญาตรีภายในสถาบันเดียว (Single Institution) และเน้นการวัดผลการเปลี่ยนผ่านกรอบความคิดและวัฒนธรรมในระดับเริ่มต้น (Foundational DevOps Mindset) มิได้ครอบคลุมการฝึกปฏิบัติการเขียนสคริปต์โครงสร้างพื้นฐานระดับสูงในสภาพแวดล้อมจริงขององค์กรขนาดใหญ่",
             bold=False, size_pt=16, space_after=6)

    # 8. ทฤษฎี สมมุติฐาน และกรอบแนวคิด
    add_para(doc, "8. ทฤษฎี สมมุติฐาน และกรอบแนวคิดของโครงการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t8.1 ทฤษฎีที่ใช้ในการวิจัย\n"
                  "\t\t1) ทฤษฎีการเรียนรู้จากประสบการณ์ (Experiential Learning Theory ของ Kolb)\n"
                  "\t\t2) กรอบแนวคิดแบบจำลอง CALMS (Culture, Automation, Lean, Measurement, Sharing)\n"
                  "\t\t3) ทฤษฎีการยอมรับเทคโนโลยี (Technology Acceptance Model: TAM)\n"
                  "\t\t4) แบบจำลองแรงจูงใจในการจัดการเรียนรู้ (ARCS Model ของ Keller)\n"
                  "\t8.2 สมมติฐานการวิจัย\n"
                  "\t\t1) นิสิตที่เรียนรู้ผ่านเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบมีคะแนนผลสัมฤทธิ์หลังเรียน (Post-test) สูงกว่าก่อนเรียน (Pre-test) อย่างมีนัยสำคัญทางสถิติที่ระดับ .05\n"
                  "\t\t2) นิสิตมีระดับพัฒนาการการเรียนรู้ (Normalized Gain: <g>) อยู่ในระดับปานกลางขึ้นไป (>= 0.30)\n"
                  "\t\t3) ผู้เรียนมีความพึงพอใจและแรงจูงใจในการเรียนรู้ต่อการใช้งานเว็บแอปพลิเคชันเกมจำลองสถานการณ์ในระดับมากถึงมากที่สุด (ค่าเฉลี่ย >= 3.51)\n"
                  "\t8.3 กรอบแนวคิดในการวิจัย (เขียนอธิบายสั้นๆ และสรุปเป็นแผนภูมิ)\n"
                  "\t\tงานวิจัยนี้มีจุดมุ่งหมายเพื่อพัฒนาและประเมินประสิทธิภาพของเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบ เพื่อแก้ปัญหาความเข้าใจผิดเรื่องเครื่องมือของผู้เรียน โดยจำลองสถานการณ์ส่งมอบงานและการวินิจฉัยสายพาน CI/CD แล้วประเมินผลสัมฤทธิ์ทั้งมิติความรู้ (Cognitive), พฤติกรรมการตัดสินใจ (Behavioral Telemetry), และแรงจูงใจในการเรียนรู้ (Affective) ดังแสดงในแผนภูมิกรอบการวิจัย",
             bold=False, size_pt=16, space_after=3)

    # แผนภูมิกรอบแนวคิด (กล่องข้อความจัดชิดกลาง)
    diagram1_txt = (
        "ปัญหาการเรียนรู้เดิม: ขาดความเข้าใจด้าน Culture / ยึดติดเครื่องมือ (Tool-Obsession) / การบรรยายไม่เห็นภาพจริง\n"
        "                                           │\n"
        "                                           ▼\n"
        "การพัฒนานวัตกรรมการเรียนรู้: เว็บแอปพลิเคชันเกมจำลองสถานการณ์ DevOps เชิงโต้ตอบ\n"
        "  ├─ เกมที่ 1: คืนวันศุกร์สุดระทึก (Crisis Simulator: ระบบเสถียรภาพ ขวัญกำลังใจ และหนี้เทคนิค)\n"
        "  ├─ เกมที่ 2: หมอสายพานกู้ชีพ (Incident Doctor: แก้ปัญหาสายพาน CI/CD ตาม CALMS และ DORA Metrics)\n"
        "  └─ กลไกส่งเสริม: Dynamic Choice Randomization, Web Audio FX, Admin Telemetry Dashboard\n"
        "                                           │\n"
        "                                           ▼\n"
        "กระบวนการทดลองและประเมินผล: One-Group Pretest-Posttest Design ผสาน Mixed-Methods\n"
        "  ├─ เชิงปริมาณ: Pre-test vs. Post-test (10 ข้อ), Normalized Gain (<g>), Effect Size (Cohen's d)\n"
        "  ├─ การเรียนรู้เชิงพฤติกรรม: In-Game Telemetry (เวลาที่เสียไป, อัตราความผิดพลาด, สหสัมพันธ์)\n"
        "  ├─ การยอมรับและแรงจูงใจ: แบบประเมิน Likert Scale 5 ระดับ (TAM & ARCS Model)\n"
        "  └─ เชิงคุณภาพ: ข้อความสะท้อนคิด (Reflection Logs) ผ่าน Thematic Analysis\n"
        "                                           │\n"
        "                                           ▼\n"
        "ผลลัพธ์ที่คาดหวัง: ผลสัมฤทธิ์สูงขึ้นอย่างมีนัยสำคัญ, เกิด Conceptual Shift สู่ Blameless Culture, และตีพิมพ์เผยแพร่"
    )
    p_box1 = add_para(doc, diagram1_txt, bold=False, size_pt=11.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1, line_spacing=1.0)
    p_box1.paragraph_format.left_indent = Cm(0.5)
    p_box1.paragraph_format.right_indent = Cm(0.5)
    add_para(doc, "รูปแสดงแผนภูมิกรอบการวิจัย", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    # 9. การทบทวนวรรณกรรม
    add_para(doc, "9. การทบทวนวรรณกรรม/สารสนเทศ (information) ที่เกี่ยวข้อง", bold=True, size_pt=16, space_after=2)
    add_para(doc, "แนวคิดเดฟออปส์ (DevOps) ได้กลายเป็นหัวใจหลักของการพัฒนาซอฟต์แวร์ยุคใหม่ โดยมุ่งเน้นการผสานความร่วมมือระหว่างทีมพัฒนา (Development) และทีมปฏิบัติการ (Operations) เพื่อลดระยะเวลาการส่งมอบงาน (Lead Time) และเพิ่มเสถียรภาพของระบบ อย่างไรก็ดี งานวิจัยด้านการศึกษาวิศวกรรมซอฟต์แวร์ (Software Engineering Education) โดย Ferino และคณะ (2021) และ Hobeck และคณะ (2021) ระบุตรงกันว่า อุปสรรคสำคัญอันดับหนึ่งในการสอน DevOps ในระดับอุดมศึกษาคือ \"The Tool-Obsession Misconception\" ซึ่งผู้เรียนมักมองว่าการทำ DevOps คือการติดตั้งและใช้งานเครื่องมืออัตโนมัติ (เช่น Docker, Kubernetes, Jenkins) ส่งผลให้นิสิตขาดความเข้าใจในหลักการเชิงนามธรรม เช่น การแบ่งปันเป้าหมายร่วมกัน และการสื่อสารข้ามสายงาน ซึ่งสอดคล้องกับการสำรวจอย่างเป็นระบบของ Leite และคณะ (2019) ใน ACM Computing Surveys ที่ยืนยันว่า คอขวดที่แท้จริงของการนำ DevOps มาใช้ในอุตสาหกรรมไม่ได้เกิดจากเทคโนโลยี แต่เกิดจากวัฒนธรรมองค์กรที่เป็นไซโล (Silo) และวัฒนธรรมการชี้นิ้วหาคนผิดเมื่อเกิดวิกฤติ (Blame Culture)",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "นอกจากนี้ Erich, Amrit, และ Daneva (2017) ใน Journal of Systems and Software ได้ชี้ว่าปัจจัยความสำเร็จของ DevOps อยู่ที่มิติทางสังคมและมนุษย์ (Human & Social Factors) ได้แก่ ความไว้เนื้อเชื่อใจ และการไม่ผลักภาระงานข้ามแผนก (\"Throw it over the wall\") ซึ่งการเรียนการสอนแบบบรรยายในห้องเรียนแบบดั้งเดิม (Traditional Lecture) ล้มเหลวในการสร้างประสบการณ์ความเข้าอกเข้าใจนี้ Christensen (2016) ในการประชุม ACM ITiCSE จึงได้เสนอแนวทาง \"Break It, Fix It\" โดยระบุว่าผู้เรียนจะต้องได้สัมผัสกับสถานการณ์จำลองที่ระบบพังจริง และต้องเผชิญกับผลลัพธ์ของการตัดสินใจด้วยตนเอง จึงจะเกิดความเข้าใจอย่างลึกซึ้ง",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "จากการทบทวนวรรณกรรมข้างต้น ผู้วิจัยจึงได้บูรณาการกรอบแนวคิด CALMS (Humble & Molesky, 2011) และตัวชี้วัด DORA Metrics เข้ากับทฤษฎีการเรียนรู้จากประสบการณ์ (Experiential Learning Theory) ของ Kolb (1984) เพื่อพัฒนาเกมจำลองสถานการณ์ที่ผู้เรียนได้เผชิญกับวิกฤติระบบล่มในคืนวันศุกร์ และฝึกแก้ปัญหาสายพานส่งมอบงานทีละขั้นตอน ซึ่งงานวิจัยของ Krusche และคณะ (2017) ยืนยันว่าการจำลองบทบาทสมมติ (Role-playing Simulation) สามารถยกระดับความเข้าอกเข้าใจและผลสัมฤทธิ์ทางการเรียนรู้ของผู้เรียนสายวิศวกรรมซอฟต์แวร์ได้สูงกว่าการสอนแบบทฤษฎีอย่างมีนัยสำคัญ",
             bold=False, size_pt=16, space_after=6)

    # 10. วิธีการดำเนินการวิจัย
    add_para(doc, "10. วิธีการดำเนินการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, "\t10.1 พื้นที่วิจัย/องค์กร\n"
                  "\t\tคณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา โดยใช้ห้องปฏิบัติการคอมพิวเตอร์\n"
                  "\t10.2 สรุปขั้นตอนและวิธีดำเนินการวิจัย (เขียนเป็นแผนภูมิ)\n"
                  "\t\tการวิจัยนี้แบ่งกระบวนการออกเป็น 3 ระยะหลัก (Phases) ดังนี้:\n"
                  "\t\tระยะที่ 1: การเตรียมการและการพัฒนานวัตกรรม ผู้วิจัยทำการพัฒนาเว็บแอปพลิเคชันเกมจำลองสถานการณ์ DevOps (ทั้ง 2 เกม) พร้อมจัดทำแบบทดสอบก่อน-หลังเรียน (Pre/Post-test 10 ข้อ) และแบบประเมินความพึงพอใจและแรงจูงใจ (TAM/ARCS 10 ข้อ) ผ่าน Google Forms\n"
                  "\t\tระยะที่ 2: การเก็บรวบรวมข้อมูลการทดลอง ดำเนินการทดลองกับกลุ่มตัวอย่างนิสิต โดยเริ่มจากการทำ Pre-test ➔ จัดการเรียนรู้ด้วยเกมจำลองสถานการณ์เชิงโต้ตอบ ➔ กิจกรรมสะท้อนคิด (Class Debrief) นำข้อมูลจาก Admin Dashboard มาอภิปรายร่วมกัน ➔ ทำ Post-test และตอบแบบประเมินความพึงพอใจพร้อมบันทึกข้อความสะท้อนคิด (Reflection Logs)\n"
                  "\t\tระยะที่ 3: การวิเคราะห์และสรุปผล นำข้อมูลคะแนนมาวิเคราะห์ Paired-samples t-test, Normalized Gain (<g>), Effect Size (Cohen's d), วิเคราะห์ข้อมูลพฤติกรรมในระบบ (In-Game Telemetry), และถอดบทเรียนข้อความสะท้อนคิดด้วยวิธี Thematic Analysis เพื่อสรุปผลการวิจัยและจัดทำบทความตีพิมพ์ ดังแสดงในรูปวิธีดำเนินการวิจัย",
             bold=False, size_pt=16, space_after=3)

    diagram2_txt = (
        "ระยะที่ 1: การเตรียมการและพัฒนานวัตกรรม\n"
        "  ├─ 1.1 พัฒนาเว็บแอปพลิเคชัน 2 เกมจำลองสถานการณ์ DevOps\n"
        "  └─ 1.2 สร้างแบบทดสอบ Pre/Post-test (10 ข้อ) และแบบประเมินความพึงพอใจผ่าน Google Forms\n"
        "                       │\n"
        "                       ▼\n"
        "ระยะที่ 2: การเก็บรวบรวมข้อมูลการทดลอง (In-Class Implementation)\n"
        "  ├─ 2.1 ให้นิสิตทำแบบทดสอบก่อนเรียน (Pre-test 10 นาที)\n"
        "  ├─ 2.2 จัดการเรียนรู้ผ่านเกมจำลองสถานการณ์เชิงโต้ตอบ (30 นาที)\n"
        "  ├─ 2.3 กิจกรรมสะท้อนคิด (Class Debrief) อภิปรายจากหน้าจอ Admin Dashboard (15 นาที)\n"
        "  └─ 2.4 ทำแบบทดสอบหลังเรียน (Post-test) และประเมินความพึงพอใจ/ข้อความสะท้อนคิด (15 นาที)\n"
        "                       │\n"
        "                       ▼\n"
        "ระยะที่ 3: การวิเคราะห์และสรุปผล (Analysis & Dissemination)\n"
        "  ├─ 3.1 วิเคราะห์ผลสัมฤทธิ์ทางการเรียนรู้ (Paired t-test, Hake's Gain, Cohen's d)\n"
        "  ├─ 3.2 วิเคราะห์ In-Game Telemetry (สหสัมพันธ์พฤติกรรมกับการเรียนรู้) และ Thematic Analysis\n"
        "  └─ 3.3 สรุปผลการวิจัยและจัดทำต้นฉบับบทความวิจัยเพื่อส่งตีพิมพ์ (TCI 1 / Scopus)"
    )
    p_box2 = add_para(doc, diagram2_txt, bold=False, size_pt=11.5, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=1, line_spacing=1.0)
    p_box2.paragraph_format.left_indent = Cm(0.5)
    p_box2.paragraph_format.right_indent = Cm(0.5)
    add_para(doc, "รูปแสดงวิธีดำเนินการวิจัย", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=6)

    # 11. สถานที่ทำการวิจัย
    add_para(doc, "11. สถานที่ทำการวิจัย", bold=True, size_pt=16, space_after=2)
    tbl11 = create_table(doc, 3, 4, col_widths=[3.0, 3.0, 3.5, 7.5])
    headers11 = ["ในประเทศ/ต่างประเทศ", "ชื่อประเทศ/จังหวัด", "พื้นที่ที่ทำวิจัย", "ชื่อสถานที่"]
    for i, h in enumerate(headers11):
        format_cell(tbl11.rows[0].cells[i], h, bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    
    data11 = [
        ["ในประเทศ", "พะเยา", "ห้องปฏิบัติการ", "ห้องปฏิบัติการคอมพิวเตอร์ คณะ ICT มหาวิทยาลัยพะเยา"],
        ["ในประเทศ", "พะเยา", "สำนักงาน", "คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา"]
    ]
    for r_idx, row_data in enumerate(data11):
        for c_idx, val in enumerate(row_data):
            align = WD_ALIGN_PARAGRAPH.CENTER if c_idx in [0, 1, 2] else WD_ALIGN_PARAGRAPH.LEFT
            format_cell(tbl11.rows[r_idx+1].cells[c_idx], val, bold=False, size_pt=14, align=align)

    add_para(doc, "", space_after=4)

    # 12. ระยะเวลาการวิจัย
    add_para(doc, "12. ระยะเวลาการวิจัย", bold=True, size_pt=16, space_after=2)
    add_para(doc, " ระยะเวลาโครงการ        1    ปี        0         เดือน\n"
                  " วันที่เริ่มต้น 5 มกราคม 2569 - 5 มกราคม 2570\n"
                  "แผนการดำเนินงานวิจัย (ปีที่เริ่มต้น – สิ้นสุด)",
             bold=False, size_pt=16, space_after=2)

    tbl12 = create_table(doc, 6, 15, col_widths=[1.5, 4.5] + [0.8]*12 + [1.8])
    headers12 = ["ปีงบ", "กิจกรรม", "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.", "ร้อยละ"]
    for i, h in enumerate(headers12):
        format_cell(tbl12.rows[0].cells[i], h, bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")

    acts = [
        ("2569", "การพัฒนานวัตกรรมและเตรียมเครื่องมือ", [1, 2, 3], "25"),
        ("2569", "การดำเนินการทดลองและเก็บรวบรวมข้อมูล", [4, 5, 6], "25"),
        ("2569", "การวิเคราะห์ข้อมูลสถิติและ Telemetry", [7, 8, 9], "25"),
        ("2569-70", "การเขียนรายงานวิจัยและจัดทำบทความตีพิมพ์", [10, 11, 12], "25")
    ]
    for r_idx, (yr, act, months, pct) in enumerate(acts):
        row = tbl12.rows[r_idx+1]
        format_cell(row.cells[0], yr, size_pt=11, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row.cells[1], act, size_pt=12, align=WD_ALIGN_PARAGRAPH.LEFT)
        for m_idx in range(1, 13):
            mark = "X" if m_idx in months else ""
            format_cell(row.cells[m_idx+1], mark, bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
        format_cell(row.cells[14], pct, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    # รวม 100%
    row_tot = tbl12.rows[5]
    format_cell(row_tot.cells[0], "", size_pt=12)
    format_cell(row_tot.cells[1], "รวม", bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    for m in range(2, 14):
        format_cell(row_tot.cells[m], "", size_pt=12)
    format_cell(row_tot.cells[14], "100", bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)

    add_para(doc, "", space_after=4)

    # 13. งบประมาณ
    add_para(doc, "13. งบประมาณของโครงการวิจัย", bold=True, size_pt=16, space_after=2)
    tbl13 = create_table(doc, 4, 3, col_widths=[5.5, 8.5, 3.0])
    format_cell(tbl13.rows[0].cells[0], "ประเภทงบประมาณ", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    format_cell(tbl13.rows[0].cells[1], "รายละเอียด", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    format_cell(tbl13.rows[0].cells[2], "งบประมาณ (บาท)", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")

    format_cell(tbl13.rows[1].cells[0], "งบดำเนินการ : ค่าใช้สอย", bold=False, size_pt=14)
    format_cell(tbl13.rows[1].cells[1], "ค่าบริการระบบคลาวด์และโฮสติ้งสนับสนุนการวิจัย (Netlify/Domain)", bold=False, size_pt=14)
    format_cell(tbl13.rows[1].cells[2], "1,000", bold=False, size_pt=14, align=WD_ALIGN_PARAGRAPH.RIGHT)

    format_cell(tbl13.rows[2].cells[0], "", bold=False, size_pt=14)
    format_cell(tbl13.rows[2].cells[1], "ค่าวัสดุสำนักงานและจัดทำแบบประเมิน/รายงาน", bold=False, size_pt=14)
    format_cell(tbl13.rows[2].cells[2], "1,000", bold=False, size_pt=14, align=WD_ALIGN_PARAGRAPH.RIGHT)

    format_cell(tbl13.rows[3].cells[0], "รวม", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl13.rows[3].cells[1], "", bold=False, size_pt=14)
    format_cell(tbl13.rows[3].cells[2], "2,000", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.RIGHT)

    add_para(doc, "หมายเหตุ  งบประมาณของโครงการวิจัยนี้ ใช้งบประมาณส่วนตัวของผู้วิจัยเอง", bold=False, size_pt=14, space_before=1, space_after=6)

    # 14. เอกสารอ้างอิง
    add_para(doc, "14. เอกสารอ้างอิง", bold=True, size_pt=16, space_after=2)
    refs = [
        "Christensen, H. B. (2016). Teaching DevOps and Cloud Computing using a Cognitive Apprenticeship and \"Break It, Fix It\" Approach. In Proceedings of the 2016 ACM Conference on Innovation and Technology in Computer Science Education (ITiCSE '16), pp. 174–179. https://doi.org/10.1145/2899415.2899451",
        "Erich, F. M., Amrit, C., & Daneva, M. (2017). A mapping study on cooperation between information system development and operations. Journal of Systems and Software, 98, 254–265. https://doi.org/10.1016/j.jss.2014.08.032",
        "Ferino, E., et al. (2021). DevOps Education: An Interview Study of Challenges and Recommendations. In 2021 IEEE/ACM International Conference on Software Engineering: Software Engineering Education and Training (ICSE-SEET), pp. 41–50.",
        "Hobeck, R., et al. (2021). Teaching DevOps: A Tale of Two Universities. In 2021 IEEE International Conference on Software Engineering Education and Training (CSEE&T), pp. 1–10.",
        "Humble, J., & Molesky, J. (2011). Why enterprises must adopt devops to enable continuous delivery. Cutter IT Journal, 24(8), 6–12.",
        "Kolb, D. A. (1984). Experiential learning: Experience as the source of learning and development. Englewood Cliffs, NJ: Prentice-Hall.",
        "Krusche, S., et al. (2017). Introduction of Continuous Delivery in Multi-Customer Courses. In Proceedings of the 39th International Conference on Software Engineering: Software Engineering Education and Training Track (ICSE-SEET), pp. 97–106.",
        "Leite, L., Rocha, C., Kon, F., Milojicic, D., & Meirelles, P. (2019). A survey of DevOps concepts and challenges. ACM Computing Surveys (CSUR), 52(6), 1–35. https://doi.org/10.1145/3359981"
    ]
    for r in refs:
        p_ref = add_para(doc, r, bold=False, size_pt=14, space_after=2)
        p_ref.paragraph_format.left_indent = Cm(1.0)
        p_ref.paragraph_format.first_line_indent = Cm(-1.0)

    add_para(doc, "", space_after=4)

    # 15. ผลผลิต ผลลัพธ์ และผลกระทบ
    add_para(doc, "15. ผลผลิต ผลลัพธ์ และผลกระทบจากงานวิจัย (Output/Outcome/Impact)", bold=True, size_pt=16, space_after=2)
    tbl15 = create_table(doc, 2, 8, col_widths=[3.0, 3.5, 1.2, 1.2, 1.2, 1.4, 2.5, 3.0])
    headers15 = ["ผลงานที่คาดว่าจะได้รับ", "รายละเอียดของผลผลิต", "ปี 69", "ปี 70", "รวม", "หน่วยนับ", "ผลลัพธ์ที่คาดว่าจะได้รับ", "ผลกระทบที่คาดว่าจะได้รับ"]
    for i, h in enumerate(headers15):
        format_cell(tbl15.rows[0].cells[i], h, bold=True, size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")

    row15 = tbl15.rows[1]
    format_cell(row15.cells[0], "ตีพิมพ์วารสารระดับชาติ หรือ นานาชาติ", size_pt=12)
    format_cell(row15.cells[1], "ตีพิมพ์ในวารสาร TCI กลุ่ม 1 หรือ การประชุมวิชาการนานาชาติระดับ Scopus อย่างน้อย 1 เรื่อง", size_pt=12)
    format_cell(row15.cells[2], "1", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(row15.cells[3], "-", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(row15.cells[4], "1", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(row15.cells[5], "เรื่อง", size_pt=12, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(row15.cells[6], "1 แนวปฏิบัติที่ดี (Best Practice) ในการสอน DevOps", size_pt=12)
    format_cell(row15.cells[7], "1 ระบบเว็บแอปพลิเคชันเกมจำลองสถานการณ์ DevOps", size_pt=12)

    add_para(doc, "", space_after=4)

    # 16. สถานที่ใช้ประโยชน์
    add_para(doc, "16. สถานที่ใช้ประโยชน์", bold=True, size_pt=16, space_after=2)
    tbl16 = create_table(doc, 2, 3, col_widths=[3.5, 3.5, 10.0])
    format_cell(tbl16.rows[0].cells[0], "ในประเทศ/ต่างประเทศ", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    format_cell(tbl16.rows[0].cells[1], "ชื่อประเทศ/จังหวัด", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")
    format_cell(tbl16.rows[0].cells[2], "ชื่อสถานที่", bold=True, size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER, bg_hex="E2E8F0")

    format_cell(tbl16.rows[1].cells[0], "ในประเทศ", size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl16.rows[1].cells[1], "พะเยา", size_pt=14, align=WD_ALIGN_PARAGRAPH.CENTER)
    format_cell(tbl16.rows[1].cells[2], "คณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา", size_pt=14)

    add_para(doc, "", space_after=4)

    # 17. แผนการถ่ายทอดเทคโนโลยี
    add_para(doc, "17. แผนการถ่ายทอดเทคโนโลยีหรือผลการวิจัยสู่กลุ่มเป้าหมาย (ถ้ามี)", bold=True, size_pt=16, space_after=2)
    add_para(doc, "1) ในเชิงวิชาการ: เผยแพร่ผลงานวิจัยผ่านการตีพิมพ์ในวารสารวิชาการระดับชาติ (TCI กลุ่ม 1) หรือการประชุมวิชาการระดับนานาชาติ (Scopus) เพื่อเป็นต้นแบบการจัดการเรียนการสอนแก่อาจารย์ผู้สอนในสาขาวิชาวิศวกรรมซอฟต์แวร์และวิทยาการคอมพิวเตอร์\n"
                  "2) ในเชิงการศึกษา: ถ่ายทอดและนำเว็บแอปพลิเคชันเกมจำลองสถานการณ์ไปใช้เป็นสื่อการสอนมาตรฐานในรายวิชาที่เกี่ยวข้องกับกระบวนการซอฟต์แวร์ของคณะเทคโนโลยีสารสนเทศและการสื่อสาร มหาวิทยาลัยพะเยา และเปิดให้สถาบันการศึกษาเครือข่ายเข้าถึงได้แบบสาธารณะ",
             bold=False, size_pt=16, space_after=6)

    # 18. สรุปข้อเสนอโครงการวิจัย
    add_para(doc, "18. สรุปข้อเสนอโครงการวิจัย (ไม่เกิน 1 หน้ากระดาษ)", bold=True, size_pt=16, space_after=2)
    add_para(doc, "การเปลี่ยนผ่านกระบวนการพัฒนาซอฟต์แวร์สู่แนวคิดเดฟออปส์ (DevOps) ถือเป็นทักษะวิชาชีพสำคัญที่มีความต้องการสูงในอุตสาหกรรมดิจิทัล อย่างไรก็ดี การจัดการเรียนการสอนในระดับอุดมศึกษากลับเผชิญกับอุปสรรคสำคัญที่เรียกว่า \"ความเข้าใจผิดที่ยึดติดกับเครื่องมือ\" (Tool-Obsession Misconception) โดยผู้เรียนมักเข้าใจว่า DevOps คือการใช้งานเครื่องมือทางเทคนิค (เช่น Docker, CI/CD, Kubernetes) แต่มองข้ามคุณค่าเชิงนามธรรมด้านวัฒนธรรมองค์กร (Culture) การแบ่งปันความรับผิดชอบร่วมกัน (Shared Ownership) และการปรับปรุงระบบแบบไม่หาคนผิด (Blameless Post-Mortem) ซึ่งการสอนบรรยายแบบดั้งเดิมไม่สามารถสร้างประสบการณ์เสมือนจริงให้ผู้เรียนได้ตระหนักถึงผลกระทบเชิงธุรกิจและเสถียรภาพของระบบได้",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "โครงการวิจัยนี้จึงมีวัตถุประสงค์เพื่อพัฒนาและประเมินผลสัมฤทธิ์ของเว็บแอปพลิเคชันเกมจำลองสถานการณ์เชิงโต้ตอบ (Interactive Scenario-Based Simulation Game) ที่จำลองวิกฤติระบบส่งมอบงานในคืนวันศุกร์ (Crisis Simulator) และการวินิจฉัยซ่อมแซมสายพานส่งมอบงาน (Pipeline Incident Doctor) โดยผสานกลไกการสลับตัวเลือกแบบสุ่ม (Dynamic Choice Randomization), ระบบเสียงสังเคราะห์ (Web Audio FX), และการเชื่อมโยงสู่ตัวชี้วัด DORA Metrics ในระดับสากล การวิจัยดำเนินการด้วยแบบแผนการทดลอง One-Group Pretest-Posttest Design ผสานวิธีวิจัยแบบผสมผสาน (Mixed Methods) ร่วมกับกลุ่มตัวอย่างนิสิตระดับปริญญาตรี คณะ ICT มหาวิทยาลัยพะเยา ไม่น้อยกว่า 30 คน เครื่องมือที่ใช้ประกอบด้วยแบบทดสอบผลสัมฤทธิ์ก่อน-หลังเรียน, แบบประเมินความพึงพอใจและแรงจูงใจ (TAM/ARCS), ข้อมูลบันทึกพฤติกรรมในระบบ (In-Game Telemetry), และข้อความสะท้อนคิด (Reflection Logs)",
             bold=False, size_pt=16, space_after=3)
    add_para(doc, "ผลการวิจัยที่คาดว่าจะได้รับคือ นวัตกรรมการเรียนรู้เชิงโต้ตอบที่มีประสิทธิภาพในการยกระดับผลสัมฤทธิ์ทางการเรียนรู้ของผู้เรียนอย่างมีนัยสำคัญทางสถิติ ก่อให้เกิดการเปลี่ยนผ่านกรอบความคิด (Conceptual Shift) สู่การทำงานร่วมกันตามหลัก CALMS ได้อย่างแท้จริง พร้อมทั้งได้องค์ความรู้และแนวปฏิบัติที่ดีที่สามารถนำไปตีพิมพ์เผยแพร่ในวารสารวิชาการระดับชาติ (TCI กลุ่ม 1) หรือการประชุมวิชาการระดับนานาชาติ (Scopus) เพื่อยกระดับคุณภาพการศึกษาวิศวกรรมซอฟต์แวร์ต่อไป",
             bold=False, size_pt=16, space_after=6)

    # 19. ลงลายมือชื่อ
    add_para(doc, "19. ลงลายมือชื่อ หัวหน้าโครงการวิจัย พร้อมวัน เดือน ปี", bold=True, size_pt=16, space_after=4)
    add_para(doc, "\n\n", space_after=2)
    add_para(doc, "                                                                            ลงชื่อ.................................................", bold=False, size_pt=16, space_after=1)
    add_para(doc, "                                                                                      ( นายชลติพันธ์ เปล่งวิทยา )", bold=False, size_pt=16, space_after=1)
    add_para(doc, "                                                                                          หัวหน้าโครงการวิจัย", bold=False, size_pt=16, space_after=1)
    add_para(doc, "                                                                                         วันที่ 5 มกราคม 2569", bold=False, size_pt=16, space_after=6)

    doc.save(output_path)
    print("Successfully generated proposal docx")

if __name__ == '__main__':
    out1 = r"D:\DevOpsWk1\ข้อเสนอโครงการ_งบส่วนตัว_DevOps_Simulation.docx"
    out2 = r"D:\Appendix\ข้อเสนอโครงการ_งบส่วนตัว_DevOps_Simulation.docx"
    out3 = r"C:\Users\Chontipan-PC\Downloads\ข้อเสนอโครงการ_งบส่วนตัว_DevOps_Simulation.docx"
    build_proposal_doc(out1)
    build_proposal_doc(out2)
    build_proposal_doc(out3)
