/**
 * baseline.js — Step 1/2: measure single-user latency per endpoint.
 *
 * Why this exists: every thread count, ramp-up and think-time in a load profile
 * should trace back to a measured service time. Without a baseline you are
 * choosing round numbers and calling them a design. With one you can say "this
 * endpoint costs 45 ms of server time, so a single-threaded target tops out near
 * 22 req/s, so N virtual users at 2 s think time will demand N/2 req/s" — and
 * every later number inherits that reasoning instead of a guess.
 *
 * It sends requests one at a time, never concurrently. Concurrency is what the
 * actual scenarios measure; mixing it in here would contaminate the reference
 * point they are compared against.
 *
 * Usage:
 *   node baseline.js --spec baseline-spec.json
 *   node baseline.js --spec baseline-spec.json --base http://localhost:3000 --requests 10
 *   node baseline.js --spec baseline-spec.json --out docs/phases/baseline.md
 *
 * Spec file — an array of requests, executed in order:
 *   [
 *     { "name": "login", "method": "POST", "path": "/api/login",
 *       "body": { "email": "perf001@eshop.com", "password": "Perf1234!" },
 *       "capture": { "token": "token" } },
 *     { "name": "search products", "method": "GET", "path": "/api/products?search=iPhone" },
 *     { "name": "add to cart", "method": "POST", "path": "/api/cart",
 *       "auth": true, "body": { "id": 1, "name": "X", "price": 100, "quantity": 1 } }
 *   ]
 *
 * "capture" maps a response JSON field to a variable name. "auth": true sends
 * the captured `token` as a Bearer header. Any {{var}} inside a path or body
 * string is substituted from captured variables, so a workflow that depends on
 * an earlier response can still be measured step by step.
 */

const fs = require("fs");
const path = require("path");

function arg(flag, dflt) {
  const i = process.argv.indexOf(flag);
  if (i !== -1 && i + 1 < process.argv.length) return process.argv[i + 1];
  return dflt;
}

const SPEC_PATH = arg("--spec", null);
const BASE = (arg("--base", "http://localhost:3000") || "").replace(/\/$/, "");
const REQUESTS = parseInt(arg("--requests", "7"), 10);
const OUT = arg("--out", null);

if (!SPEC_PATH) {
  console.error("usage: node baseline.js --spec <spec.json> [--base URL] [--requests N] [--out FILE]");
  process.exit(1);
}

const vars = {};

/** Replaces {{name}} with a captured variable, in strings at any depth. */
function substitute(value) {
  if (typeof value === "string") {
    return value.replace(/\{\{(\w+)\}\}/g, (whole, key) =>
      Object.prototype.hasOwnProperty.call(vars, key) ? vars[key] : whole,
    );
  }
  if (Array.isArray(value)) return value.map(substitute);
  if (value && typeof value === "object") {
    const out = {};
    for (const [k, v] of Object.entries(value)) out[k] = substitute(v);
    return out;
  }
  return value;
}

/** One request. Returns elapsed ms plus the response body, or throws. */
async function once(step) {
  const url = BASE + substitute(step.path);
  const headers = {};
  const init = { method: step.method || "GET", headers };

  if (step.body !== undefined) {
    headers["Content-Type"] = "application/json";
    init.body = JSON.stringify(substitute(step.body));
  }
  if (step.auth && vars.token) {
    headers["Authorization"] = `Bearer ${vars.token}`;
  }

  const started = process.hrtime.bigint();
  const res = await fetch(url, init);
  const text = await res.text(); // read the body fully — a latency figure that
  // stops at the response headers understates any endpoint with a large payload
  const elapsedMs = Number(process.hrtime.bigint() - started) / 1e6;

  return { elapsedMs, status: res.status, bytes: Buffer.byteLength(text), text };
}

function percentileish(sorted, fraction) {
  if (sorted.length === 0) return 0;
  const idx = Math.min(sorted.length - 1, Math.floor(sorted.length * fraction));
  return sorted[idx];
}

async function main() {
  const spec = JSON.parse(fs.readFileSync(path.resolve(SPEC_PATH), "utf8"));
  const rows = [];

  for (const step of spec) {
    // One discarded warm-up call. The first request to a cold route pays for
    // connection setup and JIT, and reporting that as the service time would
    // inflate every capacity estimate derived from it.
    let warm;
    try {
      warm = await once(step);
    } catch (err) {
      console.error(`[baseline] ${step.name}: ${err.message}`);
      process.exit(1);
    }

    if (step.capture) {
      let parsed = null;
      try {
        parsed = JSON.parse(warm.text);
      } catch {
        parsed = null;
      }
      for (const [varName, field] of Object.entries(step.capture)) {
        if (parsed && parsed[field] !== undefined) {
          vars[varName] = parsed[field];
        } else {
          console.error(
            `[baseline] ${step.name}: cannot capture "${field}" (status ${warm.status}) — ` +
              "later steps depending on it will fail",
          );
        }
      }
    }

    const samples = [];
    let lastStatus = warm.status;
    let lastBytes = warm.bytes;

    for (let i = 0; i < REQUESTS; i++) {
      const r = await once(step);
      samples.push(r.elapsedMs);
      lastStatus = r.status;
      lastBytes = r.bytes;
    }

    samples.sort((a, b) => a - b);
    const avg = samples.reduce((s, v) => s + v, 0) / samples.length;

    rows.push({
      name: step.name,
      method: step.method || "GET",
      path: step.path,
      status: lastStatus,
      avg,
      min: samples[0],
      max: samples[samples.length - 1],
      median: percentileish(samples, 0.5),
      bytes: lastBytes,
    });

    const flag = lastStatus >= 400 ? `  <-- status ${lastStatus}` : "";
    console.error(`[baseline] ${step.name.padEnd(24)} ${avg.toFixed(1)} ms${flag}`);
  }

  const lines = [];
  lines.push("## Single-user baseline");
  lines.push("");
  lines.push(`Base URL \`${BASE}\` · ${REQUESTS} measured requests per endpoint, ` +
             "one warm-up discarded, no concurrency.");
  lines.push("");
  lines.push("| Endpoint | Method | Status | avg ms | min | median | max | Response size | Est. ceiling |");
  lines.push("|---|---|---|---|---|---|---|---|---|");

  for (const r of rows) {
    const kb = (r.bytes / 1024).toFixed(1);
    // 1/service_time is an upper bound for a single-threaded server handling this
    // endpoint alone. Labelled an estimate because it ignores queueing, GC and
    // any work the endpoint shares with others.
    const ceiling = r.avg > 0 ? (1000 / r.avg).toFixed(0) : "n/a";
    lines.push(
      `| ${r.name} | ${r.method} | ${r.status} | ${r.avg.toFixed(1)} | ${r.min.toFixed(1)} | ` +
        `${r.median.toFixed(1)} | ${r.max.toFixed(1)} | ${kb} KB | ~${ceiling} req/s |`,
    );
  }

  const workflowCost = rows.reduce((s, r) => s + r.avg, 0);
  lines.push("");
  lines.push(`Full workflow costs **${workflowCost.toFixed(1)} ms** of server time per iteration ` +
             `(~${(1000 / workflowCost).toFixed(1)} iterations/s upper bound if run back to back).`);
  lines.push("");
  lines.push("Little's Law for sizing: `N = target_rate × (service_time + think_time)`.");

  const text = lines.join("\n") + "\n";

  if (OUT) {
    fs.mkdirSync(path.dirname(path.resolve(OUT)), { recursive: true });
    fs.writeFileSync(OUT, text, "utf8");
    console.error(`[baseline] written: ${OUT}`);
  } else {
    console.log(text);
  }
}

main().catch((err) => {
  console.error("[baseline] failed:", err.message);
  process.exit(1);
});
