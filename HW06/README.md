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
.\scripts\New-Submission.ps1 -Grade 100 -VideoUrl https://youtu.be/VIDEO_ID
```

The verified Moodle archive will be written to `output/`; the reviewable
folder beside it is `output/submission-ready/`.

## Scope

| API | Pool | Requirement | Endpoint | Status |
|---|---|---|---|---|
| 1 | A | FR-01 Registration | `POST /api/register` | Audited, extended, executed |
| 2 | D | FR-06 Product detail | `GET /api/products/:id` | Additional coverage; audited, extended, executed |
| 3 | B | FR-11 Order history | `GET /api/orders/my-orders` and related routes | Audited, extended, executed |
| 4 | C | FR-13 Dashboard | `GET /api/admin/orders` and status route | Audited, extended, executed |

The three graded pool slots are API 1 (Pool A), API 3 (Pool B), and API 4
(Pool C). API 2 / FR-06 is additional Pool-D coverage under the class allocation
confirmed by the student.

**Group uniqueness confirmation (2026-08-24):** I, Lê Phạm Kiều Duyên
(23127184), confirm that I checked with my group and that my graded combination
— FR-01 Account registration (Pool A), FR-11 Order history (Pool B), and FR-13
Admin dashboard (Pool C) — is unique within the group.

## Verified summary

Final local full run: **2026-08-23**. The SUT is reseeded before each run.

| API | AI-generated | Student-added | Total | Passed cases | Failed cases | Assertions passed/total | Bugs touched |
|---|---:|---:|---:|---:|---:|---:|---:|
| API 1 - FR-01 | 121 | 5 | 126 | 69 | 57 | 544/606 | 9 |
| API 2 - FR-06 | 83 | 5 | 88 | 54 | 34 | 390/433 | 3 |
| API 3 - FR-11 | 89 | 5 | 94 | 84 | 10 | 407/418 | 5 |
| API 4 - FR-13 | 73 | 5 | 78 | 68 | 10 | 333/345 | 2 |
| **Total / unique** | **366** | **20** | **386** | **275** | **111** | **1,674/1,802** | **16 unique bugs** |

Failed assertions are defect evidence, not broken fixtures. They are clustered
into 16 root-cause reports in `docs/bugs/BUG_REPORT.md`.

Audit totals across all APIs: **363 VALID, 1 INVALID and corrected, 22
INCOMPLETE with documented specification gaps**.

Regression gate: **1,262/1,262 assertions passed**.

## Quick start

```powershell
npm install
npm run sut:install
.\scripts\Invoke-ApiTests.ps1
.\scripts\Invoke-ApiTests.ps1 -Mode gate
```

The runner starts EShop with `LOADTEST=1`, waits for readiness, executes the
suite, writes HTML/JSON/log evidence, and stops the backend.

## Deliverables

| Item | Location |
|---|---|
| Main report | `23127184_HW06_REPORT.md` and `output/pdf/23127184_HW06_AI_API_Report.pdf` |
| Collections | `collections/*.postman_collection.json` |
| Test case sources/exports | `scripts/cases/`, `testcases/*_cases.json` |
| Excel workbook | `testcases/23127184_HW06_TestCases.xlsx` |
| Audit/extend/execute registers | `docs/phases/` |
| Full and gate reports | `reports/` |
| Raw console transcripts | `evidence/newman-console/` |
| Bug report | `docs/bugs/BUG_REPORT.md` |
| CI/CD report | `docs/cicd/CI_CD_REPORT.md` |
| Generator design/pseudocode | `docs/design/` |
| Agent Skill | `.claude/skills/api-test-generator/` |
| AI critique/audit | `docs/AI_CRITIQUE.md`, `docs/ai-audit/AI_AUDIT.md` |

## Evidence still requiring the student

These items cannot be generated or invented by an AI agent:

- Collection Runner and Monitor result screenshots.
- A successful Mock Server example response; the server and call log already
  exist, but the example response still needs to be attached to the request.
- Failure screenshots attached to the corresponding GitHub Issues if required.
- Generator diagram drawn by the student and exported with editable source.
- Narrated YouTube demo link.

Exact capture steps are in `evidence/REQUIRED_USER_EVIDENCE.md`.

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
- [x] Bug report with 16 root-cause defects
- [x] AI Critique (200-300 words) and AI Audit Report content
- [x] Generator implementation/design brief/pseudocode
- [ ] Final Excel workbook synchronized and visually verified
- [x] Final PDFs regenerated and visually verified
- [x] Public GitHub branch pushed; real green/red CI URLs recorded
- [x] GitHub Issues filed; signed-in issue-page screenshots captured
- [x] Postman Cloud workspace and environment screenshots captured
- [x] Real Postman Desktop Console evidence captured with localhost, HTTP 200
  and `[HW06] X-Student-Id=23127184`
- [ ] Collection Runner/Monitor and successful Mock response evidence captured
- [x] Generator diagram PNG and editable Mermaid source added
- [ ] Student reviewed/adapted the diagram and can explain every design choice
- [ ] Narrated demo video URL added
- [x] Group uniqueness and self-assessment completed (2026-08-24)
