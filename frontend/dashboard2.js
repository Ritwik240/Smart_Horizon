// ============================================================
//  dashboard2.js  —  FULL FIXED VERSION
//
//  Reads from localStorage "pipeline_result" (set by dashboard1.js).
//  Exact backend structure (from orchestrator.py via server.py):
//  {
//    status: "success",
//    pipeline_output: {
//      total_time: N,
//      agent_outputs: {
//        agent1: [ ...16 field records ],
//        agent2: {
//          agent2_output: { risks:[...], disease, risk_score, status },
//          input_used: { crop, temperature, humidity, soil_moisture, ndvi }
//        },
//        agent3: {
//          agent, strategy_used, priority, budget, water, llm_reason,
//          plan: { actions:[{type,cost_inr,water_liters,start,end,notes},...],
//                  status, total_cost, total_risk_reduction }
//        }
//      },
//      final_output: <same as agent_outputs.agent3>
//    }
//  }
//  Additionally "pipeline_inputs" stores { soil_moisture, temperature, humidity }
// ============================================================

// ── Helpers ──────────────────────────────────────────────────
function setText(el, val) {
    if (el && val !== undefined && val !== null) el.textContent = String(val);
}
function setHTML(el, html) {
    if (el && html !== undefined && html !== null) el.innerHTML = String(html);
}

// ── Last-Updated ticker ───────────────────────────────────────
(function () {
    const el = document.getElementById("lastUpdated");
    if (!el) return;
    let secs = 0;
    setInterval(() => {
        secs++;
        el.textContent = secs < 60
            ? secs + "s ago"
            : Math.floor(secs / 60) + "m " + (secs % 60) + "s ago";
    }, 1000);
})();

// ── Risk Chart (Agent 2) ──────────────────────────────────────
function drawRiskChart() {
    const canvas = document.getElementById("riskChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const water = [1.2,1.5,2.1,1.8,2.4,2.0,1.7,1.9,2.3,2.8,2.1,1.6];
    const heat  = [0.8,1.0,0.7,1.3,1.8,2.2,1.9,1.4,1.1,1.5,1.8,2.0];
    const maxV  = 3.5;
    const pad   = { l:8, r:8, t:6, b:4 };
    const cW = W - pad.l - pad.r, cH = H - pad.t - pad.b;
    const sx = i => pad.l + (i / (water.length - 1)) * cW;
    const sy = v => pad.t + cH - (v / maxV) * cH;
    ctx.clearRect(0, 0, W, H);
    function dl(pts, color, fill) {
        ctx.beginPath();
        ctx.moveTo(sx(0), sy(pts[0]));
        pts.forEach((v, i) => { if (i > 0) ctx.lineTo(sx(i), sy(v)); });
        ctx.lineTo(sx(pts.length - 1), H); ctx.lineTo(sx(0), H); ctx.closePath();
        ctx.fillStyle = fill; ctx.fill();
        ctx.beginPath();
        ctx.moveTo(sx(0), sy(pts[0]));
        pts.forEach((v, i) => { if (i > 0) ctx.lineTo(sx(i), sy(v)); });
        ctx.strokeStyle = color; ctx.lineWidth = 2; ctx.stroke();
    }
    dl(water, "#1565c0", "rgba(21,101,192,0.10)");
    dl(heat,  "#e53935", "rgba(229,57,53,0.08)");
}

// ── Performance Chart (Agent 4) ───────────────────────────────
function drawPerfChart() {
    const canvas = document.getElementById("perfChart");
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    const perf = [68,72,74,76,80,85];
    const maxV = 100, minV = 60;
    const pad  = { l:6, r:6, t:6, b:6 };
    const cW = W - pad.l - pad.r, cH = H - pad.t - pad.b;
    const sx = i => pad.l + (i / (perf.length - 1)) * cW;
    const sy = v => pad.t + cH - ((v - minV) / (maxV - minV)) * cH;
    ctx.clearRect(0, 0, W, H);
    const g = ctx.createLinearGradient(0, 0, 0, H);
    g.addColorStop(0, "rgba(45,106,45,0.25)");
    g.addColorStop(1, "rgba(45,106,45,0)");
    ctx.beginPath();
    ctx.moveTo(sx(0), sy(perf[0]));
    perf.forEach((v, i) => { if (i > 0) ctx.lineTo(sx(i), sy(v)); });
    ctx.lineTo(sx(perf.length - 1), H); ctx.lineTo(sx(0), H); ctx.closePath();
    ctx.fillStyle = g; ctx.fill();
    ctx.beginPath();
    ctx.moveTo(sx(0), sy(perf[0]));
    perf.forEach((v, i) => { if (i > 0) ctx.lineTo(sx(i), sy(v)); });
    ctx.strokeStyle = "#2d6a2d"; ctx.lineWidth = 2.5; ctx.stroke();
    perf.forEach((v, i) => {
        const isLast = i === perf.length - 1;
        ctx.beginPath();
        ctx.arc(sx(i), sy(v), isLast ? 5 : 3, 0, Math.PI * 2);
        ctx.fillStyle = "#2d6a2d"; ctx.fill();
        if (isLast) {
            ctx.beginPath();
            ctx.arc(sx(i), sy(v), 5, 0, Math.PI * 2);
            ctx.strokeStyle = "#fff"; ctx.lineWidth = 2; ctx.stroke();
        }
    });
}

// ── Main dashboard update ─────────────────────────────────────
function updateDashboard(serverResp, inputs) {
    const po    = serverResp.pipeline_output || {};
    const ao    = po.agent_outputs           || {};

    // ── Agent 1 data (sensor inputs the user set) ─────────────
    // We use pipeline_inputs (saved separately) for exact user values
    const soil = inputs?.soil_moisture ?? null;
    const temp = inputs?.temperature   ?? null;
    const hum  = inputs?.humidity      ?? null;

    const envVals = document.querySelectorAll(".env-value");
    // env-value order in HTML: soil, temperature, humidity, reliability
    if (envVals[0] && soil !== null) envVals[0].textContent = soil + "%";
    if (envVals[1] && temp !== null) envVals[1].textContent = temp + "°C";
    if (envVals[2] && hum  !== null) envVals[2].textContent = hum  + "%";
    // envVals[3] is reliability — leave as-is

    // ── Agent 2 ────────────────────────────────────────────────
    const a2wrap    = ao.agent2         || {};
    const a2out     = a2wrap.agent2_output || a2wrap;
    const riskScore = Number(a2out.risk_score ?? 2);
    const riskLabel = a2out.status || (riskScore > 5 ? "HIGH" : riskScore > 2 ? "ALERT" : "LOW");

    // ── Agent 3 / final ───────────────────────────────────────
    const a3    = ao.agent3         || {};
    const final = po.final_output   || a3;

    const budget       = final.budget         || a3.budget         || "—";
    const water        = final.water          || a3.water          || "—";
    const stratUsed    = final.strategy_used  || a3.strategy_used  || "—";
    const priority     = final.priority       || a3.priority       || "balanced";
    const llmReason    = final.llm_reason     || a3.llm_reason     || "";
    const planActions  = final.plan?.actions  || a3.plan?.actions  || [];
    const planStatus   = final.plan?.status   || a3.plan?.status   || "—";
    const totalCost    = final.plan?.total_cost            || a3.plan?.total_cost   || "—";
    const riskReduc    = final.plan?.total_risk_reduction  || a3.plan?.total_risk_reduction || "—";

    // ── KPI Cards ─────────────────────────────────────────────
    // Overall Success = 100 - (risk_score * 10), clamped 0-100
    const successPct = Math.max(0, Math.min(100, Math.round(100 - riskScore * 10)));
    setText(document.querySelector(".kpi-value.green"), successPct + "%");
    setText(document.querySelector(".kpi-value.blue"),
        riskScore > 5 ? "HIGH" : riskScore > 2 ? "MODERATE" : "MILD");
    // Yield: keep static unless backend returns it
    // setText(document.querySelector(".kpi-value.gold"), "+18.4%");

    // ── Action Cards ──────────────────────────────────────────
    const actionNames = document.querySelectorAll(".action-name");
    if (planActions.length > 0) {
        const a0 = planActions[0];
        if (typeof a0 === "object" && a0 !== null) {
            // Clean name
            const name = (a0.name || a0.type || "Scouting");
            if (actionNames[0]) actionNames[0].textContent =
                name.charAt(0).toUpperCase() + name.slice(1);
            // Show notes in meta
            const meta0 = document.getElementById("action-meta-0");
            if (meta0 && a0.notes) {
                meta0.innerHTML = "NOTES &nbsp; <strong>" + a0.notes + "</strong>";
            } else if (meta0 && a0.cost_inr) {
                meta0.innerHTML = "COST &nbsp; <strong>₹" + a0.cost_inr + "</strong>";
            }
        } else if (actionNames[0]) {
            actionNames[0].textContent = String(a0);
        }
    }

    // ── Reasoning Bar ─────────────────────────────────────────
    if (llmReason) {
        const rb = document.querySelector(".reasoning-bar span:last-child");
        if (rb) setHTML(rb,
            "<strong>Agent 3 Reasoning:</strong> " + llmReason);
    }

    // ── System Status Badge ───────────────────────────────────
    const statusVal = document.querySelector(".status-value");
    if (statusVal) statusVal.textContent = riskScore > 5 ? "CAUTION" : "OPTIMAL";

    // ── Show total pipeline time in meta if available ─────────
    const totalTime = po.total_time;
    if (totalTime) {
        const metaEl = document.querySelector(".report-meta");
        if (metaEl) {
            // Append pipeline time without breaking the "last updated" span
            const existing = metaEl.innerHTML;
            if (!existing.includes("Pipeline")) {
                metaEl.innerHTML += ` &bull; Pipeline: ${totalTime}s`;
            }
        }
    }
}

// ── Apply / Dismiss buttons ───────────────────────────────────
const applyBtn   = document.getElementById("applyBtn");
const dismissBtn = document.getElementById("dismissBtn");
if (applyBtn) {
    applyBtn.addEventListener("click", () => {
        applyBtn.textContent = "✔ Applied";
        applyBtn.style.background = "#1b5e20";
        applyBtn.disabled = true;
    });
}
if (dismissBtn) {
    dismissBtn.addEventListener("click", () => {
        dismissBtn.closest(".future-card")?.remove();
    });
}

// ── Boot ─────────────────────────────────────────────────────
drawRiskChart();
drawPerfChart();

// Load and apply stored pipeline result
try {
    const raw    = localStorage.getItem("pipeline_result");
    const rawIn  = localStorage.getItem("pipeline_inputs");
    if (raw) {
        const data   = JSON.parse(raw);
        const inputs = rawIn ? JSON.parse(rawIn) : null;
        updateDashboard(data, inputs);
    }
} catch (e) {
    console.error("dashboard2: localStorage parse error", e);
}
