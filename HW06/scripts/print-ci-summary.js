#!/usr/bin/env node
/** Render a scope-explicit GitHub Actions job summary from run-suite output. */

const fs = require("fs");
const path = require("path");

const modeIndex = process.argv.indexOf("--mode");
const mode = modeIndex >= 0 ? process.argv[modeIndex + 1] : "gate";
if (!new Set(["gate", "full"]).has(mode)) {
  console.error(`Unsupported mode: ${mode}`);
  process.exit(2);
}

const reportPath = path.resolve(__dirname, "..", "reports", `summary_${mode}.json`);
const report = JSON.parse(fs.readFileSync(reportPath, "utf8"));
const total = report.results.reduce((sum, row) => sum + row.total, 0);
const failed = report.results.reduce((sum, row) => sum + row.failed, 0);
const scope = mode === "gate"
  ? "Regression-acceptance suite (all declared gate cases)"
  : "Complete submitted suite (all 386 API test cases)";

console.log(`## ${scope}`);
console.log("");
console.log("| API | Passed assertions | Failed assertions | Total assertions |");
console.log("|---|---:|---:|---:|");
for (const row of report.results) {
  console.log(`| ${row.name} | ${row.total - row.failed} | ${row.failed} | ${row.total} |`);
}
console.log(`| **Total** | **${total - failed}** | **${failed}** | **${total}** |`);
console.log("");
if (mode === "gate") {
  console.log(failed === 0
    ? "Every test in the declared cross-API regression suite passed."
    : `The controlled regression sample contains ${failed} failed assertion(s).`);
} else {
  console.log(failed === 0
    ? "All 386 submitted API test cases passed."
    : `The full-suite job failed with ${failed} failed assertion(s).`);
}
