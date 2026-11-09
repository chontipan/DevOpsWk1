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
    const cleanStdId = String(d.stdId || "unknown").trim().toUpperCase();
    const cleanHash = String(d.verifyHash || `UP-SE-${Date.now()}`).trim();
    
    // Check if this submission was already recorded to prevent duplicate counting
    try {
      const checkResp = await fetch(`${SUPABASE_URL}/rest/v1/telemetry?verify_hash=eq.${encodeURIComponent(cleanHash)}&select=id`, {
        headers: {
          "apikey": SUPABASE_KEY,
          "Authorization": `Bearer ${SUPABASE_KEY}`
        }
      });
      if (checkResp.ok) {
        const existing = await checkResp.json();
        if (existing && existing.length > 0) {
          return res.status(200).json({ status: "success", message: "Record already exists", verifyHash: cleanHash, duplicate: true });
        }
      }
    } catch(checkErr) {
      console.warn("Duplicate check error:", checkErr);
    }

    const row = {
      student_id: cleanStdId,
      student_name: String(d.stdName || "unknown").trim(),
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
      verify_hash: cleanHash,
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
