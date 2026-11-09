const SUPABASE_URL = process.env.SUPABASE_URL || "https://lmvfsnxvuezkfztvrexj.supabase.co";
const SUPABASE_KEY = process.env.SUPABASE_ANON_KEY || "sb_publishable_yP3jkyIUNB5eX6Oc1JQ_pg_Bhg_qvuA";
const ADMIN_PIN = "227302";

export default async function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET, OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");

  if (req.method === "OPTIONS") return res.status(200).end();

  const { pin } = req.query;
  if (pin !== ADMIN_PIN) {
    return res.status(401).json({ error: "Unauthorized: Invalid PIN" });
  }

  try {
    const resp = await fetch(`${SUPABASE_URL}/rest/v1/telemetry?select=*&order=id.desc`, {
      headers: {
        "apikey": SUPABASE_KEY,
        "Authorization": `Bearer ${SUPABASE_KEY}`
      }
    });

    if (!resp.ok) {
      const err = await resp.text();
      return res.status(resp.status).json({ error: err });
    }

    const data = await resp.json();
    const submissions = data.map(r => ({
      time: new Date(r.created_at).toLocaleString("th-TH"),
      stdId: r.student_id,
      stdName: r.student_name,
      totalScore: r.total_score,
      rankGrade: r.rank_grade,
      g1Score: r.g1_score,
      g1BestChoices: r.g1_devops_count,
      g1TimeVal: r.g1_time_mins,
      g1Stability: r.g1_stability,
      g1Morale: r.g1_morale,
      g1_s1: r.g1_s1,
      g1_s2: r.g1_s2,
      g1_s3: r.g1_s3,
      g1_s4: r.g1_s4,
      g2Score: r.g2_score,
      g2Errors: r.g2_errors,
      g2_s1_err: r.g2_s1_err,
      g2_s2_err: r.g2_s2_err,
      g2_s3_err: r.g2_s3_err,
      g2_s4_err: r.g2_s4_err,
      durationSec: r.duration_sec,
      langUsed: r.lang_used,
      deviceType: r.device_type,
      verifyHash: r.verify_hash
    }));

    return res.status(200).json({ status: "success", count: submissions.length, submissions });
  } catch (err) {
    return res.status(500).json({ error: err.message });
  }
}
