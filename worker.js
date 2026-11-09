/**
 * Cloudflare Worker Backend for DevOps Interactive Learning Lab (Wk1)
 * URL: https://devopswk1.chontipan.workers.dev
 * 
 * Features:
 * - POST /api/submit          : Receive student telemetry (24 parameters)
 * - GET  /api/submissions     : View all submissions as JSON (PIN: 227302)
 * - GET  /api/export-csv      : One-click direct download of 24-column research CSV (PIN: 227302)
 * - GET  /api/clear           : Clear records (PIN: 227302)
 * - GET  /                    : API status and health check
 * 
 * Supported Storage Bindings:
 * - Cloudflare D1: env.DB (Automatic table creation)
 * - Cloudflare KV: env.DEVOPS_KV
 * - In-Memory Fallback
 */

const ADMIN_PIN = "227302";

const CORS_HEADERS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
  "Access-Control-Allow-Headers": "Content-Type, Authorization",
};

// In-memory fallback if KV/D1 is not yet bound (persists during active worker lifecycle)
let memoryStore = [];

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    // 1. Handle CORS preflight
    if (request.method === "OPTIONS") {
      return new Response(null, { headers: CORS_HEADERS });
    }

    // 2. POST /api/submit - Receive student telemetry
    if (url.pathname === "/api/submit" && request.method === "POST") {
      try {
        const data = await request.json();
        
        // Ensure timestamp and ID exist
        data.receivedAt = new Date().toISOString();
        const stdId = data.stdId || "unknown";
        const key = `sub_${Date.now()}_${stdId}`;

        // Save to KV if bound
        if (env && env.DEVOPS_KV) {
          try {
            await env.DEVOPS_KV.put(key, JSON.stringify(data));
          } catch (kvErr) {
            console.error("KV put error:", kvErr);
          }
        }

        // Save to D1 if bound (Auto create table if not exists)
        if (env && env.DB) {
          try {
            await env.DB.prepare(`
              CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                student_id TEXT,
                student_name TEXT,
                total_score INTEGER,
                rank_grade TEXT,
                g1_score INTEGER,
                g1_time INTEGER,
                g1_stability INTEGER,
                g1_morale INTEGER,
                g2_score INTEGER,
                g2_errors INTEGER,
                duration_sec INTEGER,
                verify_hash TEXT,
                raw_json TEXT
              )
            `).run();

            await env.DB.prepare(`
              INSERT INTO telemetry (
                timestamp, student_id, student_name, total_score, rank_grade,
                g1_score, g1_time, g1_stability, g1_morale,
                g2_score, g2_errors, duration_sec, verify_hash, raw_json
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            `).bind(
              data.time || data.receivedAt,
              data.stdId,
              data.stdName,
              data.totalScore,
              data.rankGrade,
              data.g1Score,
              data.g1TimeVal,
              data.g1Stability,
              data.g1Morale,
              data.g2Score,
              data.g2Errors,
              data.durationSec,
              data.verifyHash,
              JSON.stringify(data)
            ).run();
          } catch (d1Err) {
            console.error("D1 Insert error:", d1Err);
          }
        }

        // Always keep in memory store as fallback
        memoryStore.unshift(data);
        if (memoryStore.length > 500) memoryStore.pop();

        return new Response(JSON.stringify({
          status: "success",
          message: "Telemetry record saved successfully to Cloudflare",
          studentId: stdId,
          verifyHash: data.verifyHash,
          timestamp: data.receivedAt
        }), {
          status: 200,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json; charset=utf-8" }
        });
      } catch (err) {
        return new Response(JSON.stringify({
          status: "error",
          message: err.message
        }), {
          status: 400,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json; charset=utf-8" }
        });
      }
    }

    // 3. GET /api/submissions - Retrieve all submissions (JSON)
    if (url.pathname === "/api/submissions") {
      const pin = url.searchParams.get("pin");
      if (pin !== ADMIN_PIN) {
        return new Response(JSON.stringify({ error: "Unauthorized PIN" }), {
          status: 401,
          headers: { ...CORS_HEADERS, "Content-Type": "application/json" }
        });
      }

      const allData = await getAllSubmissions(env);
      return new Response(JSON.stringify({
        status: "success",
        count: allData.length,
        submissions: allData
      }), {
        headers: { ...CORS_HEADERS, "Content-Type": "application/json; charset=utf-8" }
      });
    }

    // 4. GET /api/export-csv - Direct download 24-column CSV
    if (url.pathname === "/api/export-csv") {
      const pin = url.searchParams.get("pin");
      if (pin !== ADMIN_PIN) {
        return new Response("Unauthorized: Invalid PIN", { status: 401, headers: CORS_HEADERS });
      }

      const list = await getAllSubmissions(env);
      const csv = generateCsv(list);

      const dateStr = new Date().toISOString().slice(0, 10);
      return new Response(csv, {
        headers: {
          ...CORS_HEADERS,
          "Content-Type": "text/csv; charset=utf-8",
          "Content-Disposition": `attachment; filename="DevOps_Class_Scores_${dateStr}.csv"`
        }
      });
    }

    // 5. GET /api/clear - Clear data
    if (url.pathname === "/api/clear") {
      const pin = url.searchParams.get("pin");
      if (pin !== ADMIN_PIN) {
        return new Response("Unauthorized", { status: 401, headers: CORS_HEADERS });
      }

      memoryStore = [];
      if (env && env.DEVOPS_KV) {
        const list = await env.DEVOPS_KV.list({ prefix: "sub_" });
        for (const k of list.keys) {
          await env.DEVOPS_KV.delete(k.name);
        }
      }
      if (env && env.DB) {
        try {
          await env.DB.prepare("DELETE FROM telemetry").run();
        } catch(e) {}
      }

      return new Response(JSON.stringify({ status: "success", message: "All records cleared" }), {
        headers: { ...CORS_HEADERS, "Content-Type": "application/json" }
      });
    }

    // 6. Default / Root health check
    return new Response(JSON.stringify({
      name: "DevOps Interactive Learning Lab - Cloudflare Telemetry API",
      status: "operational",
      version: "1.1.0",
      endpoints: {
        submit: "POST /api/submit",
        viewSubmissions: "GET /api/submissions?pin=227302",
        downloadCsv: "GET /api/export-csv?pin=227302"
      },
      kvConfigured: !!(env && env.DEVOPS_KV),
      d1Configured: !!(env && env.DB)
    }, null, 2), {
      headers: { ...CORS_HEADERS, "Content-Type": "application/json; charset=utf-8" }
    });
  }
};

/**
 * Fetch all submissions from KV, D1, or Memory
 */
async function getAllSubmissions(env) {
  if (env && env.DB) {
    try {
      const { results } = await env.DB.prepare("SELECT raw_json FROM telemetry ORDER BY id DESC").all();
      if (results && results.length > 0) {
        return results.map(r => JSON.parse(r.raw_json));
      }
    } catch (e) {
      console.error("D1 fetch error:", e);
    }
  }

  if (env && env.DEVOPS_KV) {
    try {
      const list = await env.DEVOPS_KV.list({ prefix: "sub_" });
      const records = [];
      for (const key of list.keys) {
        const val = await env.DEVOPS_KV.get(key.name, "json");
        if (val) records.push(val);
      }
      records.sort((a, b) => new Date(b.receivedAt || b.time) - new Date(a.receivedAt || a.time));
      if (records.length > 0) return records;
    } catch (e) {
      console.error("KV fetch error:", e);
    }
  }

  return memoryStore;
}

/**
 * Generate 24-column CSV with UTF-8 BOM
 */
function generateCsv(list) {
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

  let csvContent = "\uFEFF"; // UTF-8 BOM for Thai font in Excel
  csvContent += headers.map(h => `"${h}"`).join(",") + "\r\n";

  list.forEach(item => {
    const rank = item.rankGrade || (item.totalScore >= 90 ? 'Rank S' : (item.totalScore >= 80 ? 'Rank A' : (item.totalScore >= 70 ? 'Rank B' : 'Rank C')));
    const row = [
      item.time || item.receivedAt || '-',
      item.stdId || '-',
      item.stdName || '-',
      item.totalScore ?? 0,
      rank,
      item.g1Score ?? 0,
      item.g1BestChoices ?? '-',
      item.g1TimeVal ?? '-',
      item.g1Stability ?? '-',
      item.g1Morale ?? '-',
      item.g1_s1 ?? '-',
      item.g1_s2 ?? '-',
      item.g1_s3 ?? '-',
      item.g1_s4 ?? '-',
      item.g2Score ?? 0,
      item.g2Errors ?? 0,
      item.g2_s1_err ?? 0,
      item.g2_s2_err ?? 0,
      item.g2_s3_err ?? 0,
      item.g2_s4_err ?? 0,
      item.durationSec ?? '-',
      item.langUsed ?? 'TH',
      item.deviceType ?? 'Desktop',
      item.verifyHash || '-'
    ];
    csvContent += row.map(val => `"${String(val ?? '').replace(/"/g, '""')}"`).join(",") + "\r\n";
  });

  return csvContent;
}
