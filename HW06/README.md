# HW06 — AI-assisted API Testing

Student ID: **23127184**
SUT: **EShop** — <https://github.com/ttbhanh/eshop-sut> (vendored under `eshop/`)
Base URL: `http://localhost:3000`
Public repository: <https://github.com/KieuDuyennn/software__testing/tree/hw6/HW06>
Uniqueness: FR-01 / FR-06 / FR-11 / FR-13 — *confirm with your group and record the date here.*

## APIs under test

| # | Pool | Requirement | Endpoint | Collection |
|---|---|---|---|---|
| 1 | A | FR-01 Account registration | `POST /api/register` | `API1_FR01_Register` |
| 2 | A | FR-06 Product detail | `GET /api/products/:id` | `API2_FR06_ProductDetail` |
| 3 | B | FR-11 Order history (user) | `GET /api/orders/my-orders` (+ `GET /api/orders/:id`) | `API3_FR11_OrderHistory` |
| 4 | C | FR-13 Dashboard | `GET /api/admin/orders` | `API4_FR13_AdminOrders` |

The brief asks for three APIs, one per pool. Four are covered because FR-01 and
FR-06 both sit in Pool A; the three graded slots are filled by one API from each
pool and the fourth is additional coverage.

## Test summary

*Update these numbers from `testcases/23127184_HW06_TestCases.xlsx` before
submitting. They must match the workbook and the main report exactly.*

| Metric | Value |
|---|---|
| APIs tested | 4 |
| Test cases generated with AI | |
| Test cases added by the student | |
| Total test cases | |
| Executed | |
| Passed | |
| Failed | |
| Bugs found | |
| Bugs filed as GitHub Issues | |

### Per-API breakdown

| API | Generated | Added | Total | Executed | Passed | Failed | Bugs |
|---|---:|---:|---:|---:|---:|---:|---:|
| API1 — FR-01 Register | | | | | | | |
| API2 — FR-06 Product detail | | | | | | | |
| API3 — FR-11 Order history | | | | | | | |
| API4 — FR-13 Admin dashboard | | | | | | | |
| **Total** | | | | | | | |

## Quick start

```powershell
cd HW06
npm install                        # Newman + reporters
npm run sut:install                # EShop backend dependencies
.\scripts\Invoke-ApiTests.ps1      # start SUT, run all four collections, stop SUT
```

Reports land in `reports/`, console transcripts in `evidence/newman-console/`.
Full details in [`docs/runbooks/LOCAL_RUN.md`](docs/runbooks/LOCAL_RUN.md).

> The backend **must** run with `LOADTEST=1` — it rate-limits `/api` to 200
> requests per 15 minutes, which a full suite exceeds. The scripts set it for
> you.

## Deliverables

| Item | Location |
|---|---|
| Main report | `23127184_HW06_REPORT.md` (+ PDF in `output/pdf/`) |
| Postman collections | `collections/*.postman_collection.json` |
| Environments and globals | `config/` |
| Newman HTML reports | `reports/` |
| Postman features used | `docs/postman/POSTMAN_FEATURES.md` |
| Per-API pipeline documents | `docs/phases/` |
| Bug report | `docs/bugs/BUG_REPORT.md` |
| CI/CD report | `docs/cicd/CI_CD_REPORT.md` |
| Pipeline definition | `../.github/workflows/hw06-api-tests.yml` |
| Test generator design + pseudocode | `docs/design/` |
| Self-drawn diagram | `docs/design/diagram/` |
| Agent Skill | `.claude/skills/api-test-generator/` |
| AI audit report | `docs/ai-audit/AI_AUDIT.md` |
| AI critique | `docs/AI_CRITIQUE.md` |
| Excel test cases + summary | `testcases/23127184_HW06_TestCases.xlsx` |
| Git commit log | `evidence/git-commit-log.txt` |
| Screenshots | `evidence/screenshots/`, `evidence/postman-cloud/` |

Demo video (Agent Skill generating tests for one API): **_TODO — YouTube link_**

## Self-assessment

| No. | Criterion | Maximum | Self-assessed |
|---:|---|---:|---:|
| 1 | API 1 — full pipeline (generate + audit + extend + execute + bugs) | 30 | |
| 2 | API 2 — full pipeline | 30 | |
| 3 | API 3 — full pipeline | 30 | |
| 4 | Agent Skills (AI-driven test generator) | 10 | |
| | **Total** | **100** | |

Submission filename: `23127184_HW06_AI_API_<SelfAssessedGrade>.zip`

## Submission checklist

- [ ] Main report in Markdown **and** PDF
- [ ] Public GitHub repository link included
- [ ] Postman collection `.json` + Newman HTML report
- [ ] List of Postman features used
- [ ] CI/CD report with both pipeline runs (one green, one red), screenshots and links
- [ ] Excel test cases and test summary
- [ ] Generator diagram (**self-drawn**) and pseudocode
- [ ] Bug report + GitHub Issues with screenshots
- [ ] AI Critique (200–300 words) and AI Audit Report, Markdown + PDF
- [ ] Git commit log as a text file
- [ ] This README with the self-assessment table and test summary filled in
- [ ] Postman console screenshot showing `X-Student-Id` (Section 11 evidence)
