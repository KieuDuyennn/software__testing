# HW06 - AI-assisted API Testing

Student ID: **23127184**

Student name: **Lê Phạm Kiều Duyên**

SUT: **EShop** - <https://github.com/ttbhanh/eshop-sut>

Base URL: `http://localhost:3000`

Repository: <https://github.com/KieuDuyennn/software__testing/tree/hw6/HW06>

## Submission quick path

Use `SUBMISSION_CHECKLIST.md` as the single handoff checklist. Do not select
files manually. When the remaining authentic evidence is complete, run:

```powershell
.\scripts\New-Submission.ps1 -PreflightOnly
.\scripts\New-Submission.ps1 -Grade 100
```

The verified Moodle archive will be written to `output/`; the reviewable
folder beside it is `output/submission-ready/`.

## Scope

| API | Pool | Requirement | Endpoint | Status |
|---|---|---|---|---|
| 1 | A | FR-01 Registration | `POST /api/register` | Audited, extended, executed |
| 2 | A | FR-06 Product detail | `GET /api/products/:id` | Additional coverage; audited, extended, executed |
| 3 | B | FR-11 Order history | `GET /api/orders/my-orders` and related routes | Audited, extended, executed |
| 4 | C | FR-13 Dashboard | `GET /api/admin/orders` and status route | Audited, extended, executed |

The three graded pool slots are API 1 (Pool A), API 3 (Pool B), and API 4
(Pool C). API 2 / FR-06 is additional Pool-A coverage and is not counted as a
second graded selection.

**Group uniqueness confirmation (2026-08-24):** I, Lê Phạm Kiều Duyên
(23127184), confirm that I checked with my group and that my graded combination
consisting of FR-01 Account registration (Pool A), FR-11 Order history (Pool B),
and FR-13 Admin dashboard (Pool C), is unique within the group.

## Verified summary

The suite was executed twice against two different states of the SUT, and both
runs are part of the evidence. The SUT is reseeded before every run.

**Run 1 - defect discovery, against the SUT as delivered** (2026-08-24 00:25,
`evidence/newman-console/suite_full_20260824-002523.log`). This is the run the
bug report and the GitHub Issue screenshots were taken from.

| API | AI-generated | Student-added | Total | Passed cases | Failed cases | Assertions passed/total | Bugs found |
|---|---:|---:|---:|---:|---:|---:|---:|
| API 1 - FR-01 | 121 | 5 | 126 | 69 | 57 | 544/606 | 9 |
| API 2 - FR-06 | 83 | 5 | 88 | 54 | 34 | 390/433 | 3 |
| API 3 - FR-11 | 89 | 5 | 94 | 84 | 10 | 407/418 | 5 |
| API 4 - FR-13 | 73 | 5 | 78 | 68 | 10 | 333/345 | 2 |
| **Total / unique** | **366** | **20** | **386** | **275** | **111** | **1,674/1,802** | **16 unique bugs** |

The 128 failing assertions there are defect evidence, not broken fixtures. They
cluster into the 16 root-cause reports in `docs/bugs/BUG_REPORT.md`.

**Run 2 - regression, after the defects were fixed** (2026-08-24 14:12, commit
`73ce207`, current contents of `reports/`). The same 386 cases, unchanged, were
re-run against the patched SUT:

| API | Total cases | Passed cases | Failed cases | Assertions passed/total |
|---|---:|---:|---:|---:|
| API 1 - FR-01 | 126 | 126 | 0 | 606/606 |
| API 2 - FR-06 | 88 | 88 | 0 | 433/433 |
| API 3 - FR-11 | 94 | 94 | 0 | 418/418 |
| API 4 - FR-13 | 78 | 78 | 0 | 345/345 |
| **Total** | **386** | **386** | **0** | **1,802/1,802** |

Both numbers matter and neither replaces the other: run 1 is what the test
cases *found*, run 2 is proof that the fixes actually close those 16 defects
and that no case was quietly weakened to make the suite pass. The reports in
`reports/` are run 2; run 1 survives in the console transcripts under
`evidence/newman-console/` and in the Issue screenshots.

Audit totals across all APIs: **363 VALID, 1 INVALID and corrected, 22
INCOMPLETE with documented specification gaps**.

Regression gate: **1,802/1,802 assertions passed**. The gate is the list of
cases that pass today, so now that the defects are fixed it covers all 386.

Data-driven runs: **27 iterations, 128 assertions, 0 failed** across four
one-request collections fed from `postman/data/*.csv` (`npm run ddt:all`).

## Quick start

```powershell
npm install
npm run sut:install
.\scripts\Invoke-ApiTests.ps1
.\scripts\Invoke-ApiTests.ps1 -Mode gate
```

Data-driven runs need the SUT already up (`npm run sut:start` in another
shell):

```powershell
npm run ddt:rebuild
npm run ddt:all
```

The runner starts EShop with `LOADTEST=1`, waits for readiness, executes the
suite, writes HTML/JSON/log evidence, and stops the backend.

## Deliverables

| Item | Location |
|---|---|
| Main report | `23127184_HW06_REPORT.md` and `output/pdf/23127184_HW06_AI_API_Report.pdf` |
| Collections | `postman/collections/*.postman_collection.json` |
| Test case sources/exports | `scripts/cases/`, `testcases/*_cases.json` |
| Excel workbook | `testcases/23127184_HW06_TestCases.xlsx` |
| Audit/extend/execute registers | `docs/phases/` |
| Full and gate reports | `reports/` |
| Data-driven collections and CSVs | `postman/collections/*_ddt.postman_collection.json`, `postman/data/`, `reports/*_ddt.html` |
| Raw console transcripts | `evidence/newman-console/` |
| Bug report | `docs/bugs/BUG_REPORT.md` |
| CI/CD report | `docs/cicd/CI_CD_REPORT.md` |
| Generator design/pseudocode | `docs/design/` |
| Agent Skill | `.claude/skills/api-test-generator/` |
| AI critique/audit | `docs/AI_CRITIQUE.md`, `docs/ai-audit/AI_AUDIT.md` |

## Self-assessment

| No. | Criterion | Maximum | Self-assessed |
|---:|---|---:|---:|
| 1 | API 1 - full pipeline | 30 | **30** |
| 2 | API 3 - full pipeline | 30 | **30** |
| 3 | API 4 - full pipeline | 30 | **30** |
| 4 | Agent Skill / generator | 10 | **10** |
| | **Total** | **100** | **100** |

Self-assessment rationale: all three graded APIs include generation, a
case-by-case VALID / INVALID / INCOMPLETE audit, five student-designed
extensions, real execution results, and traceable bug evidence. The generator
deliverable includes design decisions, pseudocode, reusable implementation,
editable Mermaid/SVG sources, and a report-ready PNG. **100/100 is the
student's self-assessment, not a guarantee of the instructor's awarded grade.**

Submission filename: `23127184_HW06_AI_API_<SelfAssessedGrade>.zip`

## Submission checklist

- [x] Main report content in Markdown
- [x] Four complete Postman collections and Newman HTML/JSON reports
- [x] 386-case machine-readable exports and per-case audit registers
- [x] Five student-designed extension cases per API
- [x] Full local run and all-green local regression gate
- [x] Data-driven execution: four CSV-fed collections, 27 iterations green
- [x] Bug report with 16 root-cause defects
- [x] AI Critique (200-300 words) and AI Audit Report content
- [x] Generator implementation/design brief/pseudocode
- [x] Final Excel workbook synchronized with 386 audited/executed cases
- [x] Final PDFs regenerated and visually verified
- [x] Public GitHub branch pushed; real green/red CI URLs recorded
- [x] GitHub Issues filed; signed-in issue-page screenshots captured
- [x] Postman Cloud workspace and environment screenshots captured
- [x] Real Postman Desktop Console evidence captured with localhost, HTTP 200
  and `[HW06] X-Student-Id=23127184`
- [x] Collection Runner and completed Monitor evidence captured
- [x] Generator diagram PNG and editable Mermaid source added
- [x] Group uniqueness and self-assessment completed (2026-08-24)
