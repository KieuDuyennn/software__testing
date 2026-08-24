#!/usr/bin/env node
/**
 * HW06 suite runner - shared by the local PowerShell wrapper and GitHub Actions.
 *
 *   node scripts/run-suite.js --mode gate --env ci
 *   node scripts/run-suite.js --mode full --env local
 *   node scripts/run-suite.js --mode full --only 3
 *
 * Modes
 *   gate  Runs only the folders listed in postman/config/ci-suite.json. These are the
 *         expectations the SUT currently meets, so this run must stay green;
 *         it is what the CI pipeline gates on.
 *   full  Runs every folder in every collection. Any failed assertion makes
 *         the process fail, which is the mode used by the final CI pipeline.
 *
 * Exit code: 0 when the selected scope passes, 1 when any assertion fails.
 */

const fs = require("fs");
const path = require("path");
const newman = require("newman");

const ROOT = path.resolve(__dirname, "..");

function arg(name, fallback) {
  const i = process.argv.indexOf("--" + name);
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback;
}

const mode = arg("mode", "full");
const envName = arg("env", "local");

if (!["gate", "full"].includes(mode)) {
  console.error(`Unknown --mode "${mode}" (expected gate or full)`);
  process.exit(2);
}

const envFile = path.join(ROOT, "postman", "config", `eshop-${envName}.postman_environment.json`);
if (!fs.existsSync(envFile)) {
  console.error(`No environment file at ${envFile}`);
  process.exit(2);
}

const suite = JSON.parse(fs.readFileSync(path.join(ROOT, "postman", "config", "ci-suite.json"), "utf8"));
const ALL_COLLECTIONS = [
  "API1_FR01_Register",
  "API2_FR06_ProductDetail",
  "API3_FR11_OrderHistory",
  "API4_FR13_AdminOrders",
];

// --only 3 restricts the run to API 3. Omit it to run all four.
const only = arg("only", null);
let COLLECTIONS = ALL_COLLECTIONS;
if (only !== null) {
  const index = Number(only);
  if (!Number.isInteger(index) || index < 1 || index > ALL_COLLECTIONS.length) {
    console.error(`--only must be 1..${ALL_COLLECTIONS.length}, got "${only}"`);
    process.exit(2);
  }
  COLLECTIONS = [ALL_COLLECTIONS[index - 1]];
}

for (const dir of ["reports", "evidence/newman-console"]) {
  fs.mkdirSync(path.join(ROOT, dir), { recursive: true });
}

function run(name) {
  return new Promise((resolve) => {
    // Two gate styles. A collection rendered from an explicit case list
    // (postman/config/ci-suite.json -> gate_cases) wins when it exists: once a suite is
    // written against the spec rather than against observed behaviour, the
    // passing cases no longer line up with folder boundaries, so gating per
    // folder would either be red or prove nothing. Otherwise fall back to the
    // folder list in `gate`, which is enough for the un-specced APIs.
    const gateCollection = path.join(
      ROOT, "postman", "collections", `${name}_gate.postman_collection.json`
    );
    const hasCaseGate = (suite.gate_cases || {})[name] && fs.existsSync(gateCollection);

    let folders;
    if (mode === "gate" && !hasCaseGate) {
      folders = suite.gate[name] || [];
      if (folders.length === 0) {
        console.log(`\n=== ${name}: no gate configured, skipped ===`);
        return resolve({ name, total: 0, failed: 0, skipped: true });
      }
    }

    const suffix = mode === "gate" ? "_gate" : "";
    const collectionFile =
      mode === "gate" && hasCaseGate
        ? gateCollection
        : path.join(ROOT, "postman", "collections", `${name}.postman_collection.json`);

    const style = mode === "gate" ? (hasCaseGate ? " via case list" : " via folders") : "";
    console.log(`\n=== ${name} (${mode}${style}) ===`);

    newman.run(
      {
        collection: collectionFile,
        environment: envFile,
        folder: folders,
        reporters: ["cli", "htmlextra", "json"],
        reporter: {
          htmlextra: {
            export: path.join(ROOT, "reports", `${name}${suffix}.html`),
            title: `HW06 - ${name} (${mode})`,
            browserTitle: `HW06 ${name}`,
            showEnvironmentData: true,
          },
          json: { export: path.join(ROOT, "reports", `${name}${suffix}.json`) },
        },
      },
      (err, summary) => {
        if (err) {
          console.error(`${name} failed to run:`, err.message);
          return resolve({ name, total: 0, failed: 1, error: err.message });
        }
        const s = summary.run.stats.assertions;
        resolve({ name, total: s.total, failed: s.failed });
      }
    );
  });
}

(async () => {
  const results = [];
  for (const name of COLLECTIONS) {
    results.push(await run(name));
  }

  const totalFailed = results.reduce((a, r) => a + r.failed, 0);
  const totalAsserts = results.reduce((a, r) => a + r.total, 0);

  console.log(`\n===== HW06 suite summary (mode=${mode}, env=${envName}) =====`);
  for (const r of results) {
    const status = r.skipped ? "skipped" : r.failed === 0 ? "PASS" : `${r.failed} FAILED`;
    console.log(
      `  ${r.name.padEnd(28)} ${String(r.total - r.failed).padStart(4)}/${String(r.total).padEnd(4)} passed  ${status}`
    );
  }
  console.log(`  ${"TOTAL".padEnd(28)} ${totalAsserts - totalFailed}/${totalAsserts} assertions passed`);

  fs.writeFileSync(
    path.join(ROOT, "reports", `summary_${mode}.json`),
    JSON.stringify({ mode, env: envName, generatedAt: new Date().toISOString(), results }, null, 2)
  );

  if (totalFailed > 0) {
    console.error(`\nSuite is RED: ${totalFailed} assertion(s) failed.`);
    process.exit(1);
  }
  process.exit(0);
})();
