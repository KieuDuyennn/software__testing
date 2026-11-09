#!/usr/bin/env python3
"""Render phase 2-4 Markdown from audited cases and the latest Newman run."""

from __future__ import annotations

import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_cases import audit_counts, enrich_cases  # noqa: E402

MODULES = {
    1: "cases/api1_fr01_register.py",
    2: "cases/api2_fr06_product_detail.py",
    3: "cases/api3_fr11_order_history.py",
    4: "cases/api4_fr13_admin_orders.py",
}
REPORTS = {
    1: "API1_FR01_Register.json",
    2: "API2_FR06_ProductDetail.json",
    3: "API3_FR11_OrderHistory.json",
    4: "API4_FR13_AdminOrders.json",
}


def load_api(api):
    path = Path(__file__).resolve().parent / MODULES[api]
    spec = importlib.util.spec_from_file_location("phase_api%d" % api, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    enrich_cases(module.CASES)
    return module


def esc(value):
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def run_data(api):
    report_path = ROOT / "reports" / REPORTS[api]
    run = json.loads(report_path.read_text(encoding="utf-8"))["run"]
    failures = defaultdict(list)
    for failure in run.get("failures", []):
        source = failure.get("source") or {}
        name = source.get("name", "")
        if " | " not in name:
            continue
        case_id = name.split(" | ", 1)[0]
        message = ((failure.get("error") or {}).get("message") or "assertion failed")
        if message not in failures[case_id]:
            failures[case_id].append(message)

    stats = run.get("stats", {})
    assertions = stats.get("assertions", {})
    requests = stats.get("requests", {})
    return {
        "failures": failures,
        "assertions": assertions.get("total", 0),
        "failed_assertions": assertions.get("failed", 0),
        "requests": requests.get("total", 0),
        "failed_requests": requests.get("failed", 0),
        "report": report_path.name,
    }


def bug_for(case_id):
    n = int(case_id.split("-")[-1]) if case_id.split("-")[-1].isdigit() else 0
    if case_id.startswith("A1-"):
        if case_id.startswith("A1-DP-") and 19 <= n <= 28 or case_id in {"A1-HR-001", "A1-HR-002"}:
            return "BUG-01"
        if case_id in {"A1-SEC-001", "A1-SEC-003", "A1-SEC-004"}:
            return "BUG-02"
        if case_id.startswith("A1-DP-") and n in set(range(2, 6)) | {10, 11, 15, 16, 17, 18, 35, 36, 39, 40, 41, 63, 68, 69, 72, 74} or case_id in {"A1-ST-008", "A1-SCH-007", "A1-HR-003"}:
            return "BUG-07"
        if case_id.startswith("A1-DP-") and n in set(range(42, 50)) | {57, 58, 59, 60}:
            return "BUG-08"
        if case_id in {"A1-DP-033", "A1-DP-034", "A1-SCH-010"}:
            return "BUG-09"
        if case_id in {"A1-DP-066", "A1-DP-067", "A1-HR-005"}:
            return "BUG-10"
        if case_id == "A1-DP-071":
            return "BUG-11"
        if case_id == "A1-SCH-012":
            return "BUG-12"
        if case_id == "A1-SEC-013":
            return "BUG-06"
    if case_id.startswith("A2-"):
        if case_id.startswith("A2-SEC-") and 11 <= n <= 15:
            return "BUG-13"
        if case_id in {"A2-ST-003", "A2-ST-006", "A2-ST-010", "A2-SCH-002", "A2-SCH-004", "A2-SCH-007", "A2-SCH-009"}:
            return "BUG-04"
        return "BUG-03"
    if case_id == "A3-DP-009":
        return "BUG-14"
    if case_id in {"A3-ST-008", "A3-HR-001"}:
        return "BUG-15"
    if case_id == "A3-ST-020":
        return "BUG-16"
    if case_id in {"A3-SEC-001", "A3-SEC-002", "A3-SEC-003", "A3-SEC-004"}:
        return "BUG-05"
    if case_id in {"A3-SEC-008", "A3-SEC-009"}:
        return "BUG-06"
    if case_id.startswith("A4-"):
        if case_id == "A4-ST-016":
            return "BUG-16"
        return "BUG-06"
    return "UNMAPPED"


def render_audit(module, data, out_dir):
    cases = module.CASES
    counts = audit_counts(cases)
    lines = [
        "# %s - Phase 2: Audit (human review)" % module.META["collection_name"],
        "",
        "> Every case was checked against `refs/spec/api_specification.md`, the selected FR, and SEC-01..SEC-07. "
        "Audit labels assess the *test design*, not whether the SUT passed it.",
        "",
        "## Audit summary",
        "",
        "| Label | Cases | Meaning |",
        "|---|---:|---|",
        "| VALID | %d | Correct precondition, input, traceability and oracle. |" % counts["VALID"],
        "| INVALID | %d | Generated design was wrong/duplicate and was replaced before final execution. |" % counts["INVALID"],
        "| INCOMPLETE | %d | Useful partition, but the specification cannot justify a single strong oracle. |" % counts["INCOMPLETE"],
        "| **Total** | **%d** | Every case has a decision and reason. |" % len(cases),
        "",
        "## Case-by-case decision register",
        "",
        "| ID | Origin | Dimension | Label | Audit reasoning | Correction | Final run |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in cases:
        failed = data["failures"].get(case["id"])
        result = "FAIL - %s" % failed[0] if failed else "PASS"
        lines.append("| %s | %s | %s | **%s** | %s | %s | %s |" % (
            esc(case["id"]), esc(case["origin"]), esc(case["dim"]),
            esc(case["audit_label"]), esc(case["audit_reason"]),
            esc(case["correction"]), esc(result),
        ))
    lines += [
        "",
        "## Review conclusion",
        "",
        "VALID and INVALID describe test quality, not the final execution result. A failed VALID case shows "
        "that the implementation violated its requirement-based oracle. An INCOMPLETE case does not prove a "
        "defect unless another FR/SEC invariant supplies the missing oracle. The INVALID generated case remains "
        "in the audit trail with its replacement recorded.",
        "",
    ]
    (out_dir / "02-audit.md").write_text("\n".join(lines), encoding="utf-8")


def render_extend(module, data, out_dir):
    cases = [c for c in module.CASES if c["origin"] == "Student-designed"]
    lines = [
        "# %s - Phase 3: Extend" % module.META["collection_name"],
        "",
        "> Five cases designed after the human audit cover omitted encodings, post-conditions, "
        "metamorphic consistency, and atomicity.",
        "",
        "## Added test cases",
        "",
        "| ID | Dimension | Title | Why the AI missed it | Expected | Final run | Bug |",
        "|---|---|---|---|---|---|---|",
    ]
    for case in cases:
        failed = data["failures"].get(case["id"])
        result = "FAIL - %s" % failed[0] if failed else "PASS"
        bug = bug_for(case["id"]) if failed else "-"
        lines.append("| %s | %s | %s | %s | %s | %s | %s |" % (
            esc(case["id"]), esc(case["dim"]), esc(case["title"]),
            esc(case.get("rationale")), esc(case.get("expected")), esc(result), bug,
        ))
    lines += [
        "",
        "## Extension quality check",
        "",
        "- Exactly five cases are marked `Student-designed`; they are not included in the AI-generated count.",
        "- Every added case is executable in the same Postman collection and inherits the mandatory `X-Student-Id` harness.",
        "- Each rationale identifies a concrete generation blind spot, not the generic claim that 'AI missed it'.",
        "- Failures are linked to an existing root-cause bug where appropriate, preventing duplicate issue inflation.",
        "",
    ]
    (out_dir / "03-extend.md").write_text("\n".join(lines), encoding="utf-8")


def render_execute(module, data, out_dir):
    cases = module.CASES
    failed_ids = sorted(data["failures"])
    clusters = defaultdict(list)
    for case_id in failed_ids:
        clusters[bug_for(case_id)].append(case_id)
    summary = json.loads((ROOT / "reports" / "summary_full.json").read_text(encoding="utf-8"))
    generated_at = summary["generatedAt"]
    lines = [
        "# %s - Phase 4: Execute" % module.META["collection_name"],
        "",
        "## Reproducible command",
        "",
        "```powershell",
        ".\\scripts\\Invoke-ApiTests.ps1 -Api %d" % module.META["api"],
        "```",
        "",
        "The runner starts a freshly seeded backend with `LOADTEST=1`, executes Newman, writes JSON/HTML/raw "
        "console evidence, and stops the backend.",
        "",
        "## Verified result",
        "",
        "| Metric | Value |",
        "|---|---:|",
        "| Generated at | `%s` |" % generated_at,
        "| Cases in collection | %d |" % len(cases),
        "| Cases fully passing | %d |" % (len(cases) - len(failed_ids)),
        "| Cases with at least one failed assertion | %d |" % len(failed_ids),
        "| Newman assertions | %d |" % data["assertions"],
        "| Failed assertions | %d |" % data["failed_assertions"],
        "| Request transport failures | %d |" % data["failed_requests"],
        "| HTML report | `reports/%s` |" % data["report"].replace(".json", ".html"),
        "| JSON report | `reports/%s` |" % data["report"],
        "",
        "## Failure triage by root cause",
        "",
        "| Bug | Failing cases |",
        "|---|---|",
    ]
    for bug, ids in sorted(clusters.items()):
        lines.append("| %s | %s |" % (bug, ", ".join("`%s`" % i for i in ids)))
    if not clusters:
        lines.append("| - | No failed cases |")
    lines += [
        "",
        "## Evidence integrity",
        "",
        "- The HTML and JSON files above were generated by the same local run.",
        "- `reports/summary_full.json` is the machine-readable cross-API assertion summary.",
        "- The corresponding timestamped console transcript is under `evidence/newman-console/`.",
        "- The regression gate is separate from the defect-revealing full suite; a green gate does not hide documented SUT defects.",
        "- Screenshot evidence and GitHub Issue URLs remain user-captured evidence and are not fabricated here.",
        "",
    ]
    (out_dir / "04-execute.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    for api in sorted(MODULES):
        module = load_api(api)
        data = run_data(api)
        out_dir = ROOT / "docs" / "phases" / module.META["slug"]
        render_audit(module, data, out_dir)
        render_extend(module, data, out_dir)
        render_execute(module, data, out_dir)
        print("API %d: %d cases, %d failed cases -> %s" % (
            api, len(module.CASES), len(data["failures"]), out_dir.relative_to(ROOT)))


if __name__ == "__main__":
    main()
