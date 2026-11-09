const SUPABASE_URL = process.env.SUPABASE_URL || "https://lmvfsnxvuezkfztvrexj.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_yP3jkyIUNB5eX6Oc1JQ_pg_Bhg_qvuA";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();
  if (req.method !== "POST") return res.status(405).json({ error: "Method not allowed" });

  try {
    const d = req.body;
    
    const row = {
      student_id: String(d.stdId || "unknown"),
      student_name: String(d.stdName || "unknown"),
      total_score: Number(d.totalScore) || 0,
      rank_grade: String(d.rankGrade || "Rank C"),
      g1_score: Number(d.g1Score) || 0,
      g1_devops_count: Number(d.g1BestChoices) || 0,
      g1_time_mins: Number(d.g1TimeVal) || 0,
      g1_stability: Number(d.g1Stability) || 0,
      g1_morale: Number(d.g1Morale) || 0,
      g1_s1: String(d.g1_s1 || "-"),
      g1_s2: String(d.g1_s2 || "-"),
      g1_s3: String(d.g1_s3 || "-"),
      g1_s4: String(d.g1_s4 || "-"),
      g2_score: Number(d.g2Score) || 0,
      g2_errors: Number(d.g2Errors) || 0,
      g2_s1_err: Number(d.g2_s1_err) || 0,
      g2_s2_err: Number(d.g2_s2_err) || 0,
      g2_s3_err: Number(d.g2_s3_err) || 0,
      g2_s4_err: Number(d.g2_s4_err) || 0,
      duration_sec: Number(d.durationSec) || 0,
      lang_used: String(d.langUsed || "TH"),
      device_type: String(d.deviceType || "Desktop"),
      verify_hash: String(d.verifyHash || `UP-SE-${Date.now()}`),
      raw_json: d
    };

    const resp = await fetch(`${SUPABASE_URL}/rest/v1/telemetry`, {
      method: "POST",
      headers: {
        "apikey": SUPABASE_KEY,
        "Authorization": `Bearer ${SUPABASE_KEY}`,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
      },
      body: JSON.stringify(row)
    });

    if (!resp.ok) {
      const errText = await resp.text();
      return res.status(resp.status).json({ error: errText });
    }

    return res.status(200).json({ status: "success", message: "Recorded to Supabase", verifyHash: row.verify_hash });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
