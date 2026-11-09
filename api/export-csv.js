const SUPABASE_URL = process.env.SUPABASE_URL || "https://lmvfsnxvuezkfztvrexj.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_yP3jkyIUNB5eX6Oc1JQ_pg_Bhg_qvuA";
const ADMIN_PIN = "227302";

export default async function handler(req, res) {
  const { pin } = req.query;
  if (pin !== ADMIN_PIN) {
    return res.status(401).send("Unauthorized: Invalid PIN");
  }

  try {
    const resp = await fetch(`${SUPABASE_URL}/rest/v1/telemetry?select=*&order=id.desc`, {
      headers: {
        "apikey": SUPABASE_KEY,
        "Authorization": `Bearer ${SUPABASE_KEY}`
      }
    });

    if (!resp.ok) {
      return res.status(resp.status).send(await resp.text());
    }

    const data = await resp.json();
    const headers = [
      "วัน-เวลาที่ส่ง",
      "รหัสนิสิต",
      "ชื่อ-นามสกุล",
      "คะแนนรวม (เต็ม 100)",
      "DevOps Rank",
      "คะแนนเกม 1",
      "จำนวนเลือก DevOps (เกม 1)",
      "เวลาจำลองเกม 1 (นาที)",
      "ความเสถียรคงเหลือ เกม 1 (%)",
      "ขวัญกำลังใจ เกม 1 (%)",
      "เกม1_ด่าน1_รวมโค้ด",
      "เกม1_ด่าน2_ส่งมอบ",
      "เกม1_ด่าน3_วิกฤต",
      "เกม1_ด่าน4_วัฒนธรรม",
      "คะแนนเกม 2",
      "ข้อผิดพลาดรวม เกม 2",
      "เกม2_ด่าน1_รวมโค้ด(ผิด)",
      "เกม2_ด่าน2_ทดสอบ(ผิด)",
      "เกม2_ด่าน3_ติดตั้ง(ผิด)",
      "เกม2_ด่าน4_เฝ้าระวัง(ผิด)",
      "เวลาเล่นจริงในระบบ (วินาที)",
      "ภาษาที่ใช้",
      "อุปกรณ์",
      "รหัสยืนยัน (Hash)"
    ];

    let csv = "\uFEFF"; // UTF-8 BOM
    csv += headers.map(h => `"${h}"`).join(",") + "\r\n";

    data.forEach(r => {
      const row = [
        new Date(r.created_at).toLocaleString("th-TH"),
        r.student_id,
        r.student_name,
        r.total_score,
        r.rank_grade,
        r.g1_score,
        r.g1_devops_count,
        r.g1_time_mins,
        r.g1_stability,
        r.g1_morale,
        r.g1_s1,
        r.g1_s2,
        r.g1_s3,
        r.g1_s4,
        r.g2_score,
        r.g2_errors,
        r.g2_s1_err,
        r.g2_s2_err,
        r.g2_s3_err,
        r.g2_s4_err,
        r.duration_sec,
        r.lang_used,
        r.device_type,
        r.verify_hash
      ];
      csv += row.map(v => `"${String(v ?? '').replace(/"/g, '""')}"`).join(",") + "\r\n";
    });

    const dateStr = new Date().toISOString().slice(0, 10);
    res.setHeader("Content-Type", "text/csv; charset=utf-8");
    res.setHeader("Content-Disposition", `attachment; filename="DevOps_Supabase_Scores_${dateStr}.csv"`);
    return res.status(200).send(csv);
  } catch (err) {
    return res.status(500).send(err.message);
  }
}
