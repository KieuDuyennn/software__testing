# HW06 - AI-assisted API Testing

Student ID: **23127184**

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
| 2 | A | FR-06 Product detail | `GET /api/products/:id` | Additional coverage; audited, extended, executed |
| 3 | B | FR-11 Order history | `GET /api/orders/my-orders` and related routes | Audited, extended, executed |
| 4 | C | FR-13 Dashboard | `GET /api/admin/orders` and status route | Audited, extended, executed |

The three graded pool slots are API 1 (A), API 3 (B), and API 4 (C). API 2 is
additional Pool-A coverage. Confirm selection uniqueness with the group and add
the date before submission.

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

- Postman Console screenshot visibly showing
  `[HW06] X-Student-Id=23127184`.
- Postman Console, Collection Runner, Monitor and Mock Server screenshots.
- Failure screenshots attached to the corresponding GitHub Issues if required.
- Group uniqueness confirmation and date.
- Generator diagram drawn by the student and exported with editable source.
- Narrated YouTube demo link.

Exact capture steps are in `evidence/REQUIRED_USER_EVIDENCE.md`.

## Self-assessment

| No. | Criterion | Maximum | Self-assessed |
|---:|---|---:|---:|
| 1 | API 1 - full pipeline | 30 | _Finalize after evidence_ |
| 2 | API 3 - full pipeline | 30 | _Finalize after evidence_ |
| 3 | API 4 - full pipeline | 30 | _Finalize after evidence_ |
| 4 | Agent Skill / generator | 10 | _Finalize after diagram/video_ |
| | **Total** | **100** | **Pending authentic evidence** |

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
- [ ] Postman Console/Runner/Monitor/Mock result evidence captured
- [ ] Self-drawn generator diagram added
- [ ] Narrated demo video URL added
- [ ] Group uniqueness and self-assessment completed
