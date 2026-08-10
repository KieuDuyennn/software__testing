# HW04 — Automation Testing on EShop

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Course:** CS423/CSC13003 — Software Testing (FIT@HCMUS) · **Exercise:** HW04-AI
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**Public repository:** _<paste URL>_
**AI declaration:** I use AI tools for the tasks recorded in `docs/03_AI_Audit_Report.md`.

## Features under test (§5)

The same web features selected in HW02, one per pool. HW02's FR-06 was that
assignment's Pool D (mobile) choice and is excluded here, as §5 requires.

| Pool | Feature | Spec | Data file |
|---|---|---|---|
| A | FR-01 Account registration | `automation/tests/fr01_account_registration/` | `automation/data/fr01_registration.csv` |
| B | FR-11 Order history view (user) | `automation/tests/fr11_order_history/` | `automation/data/fr11_order_history.json` |
| C | FR-13 Dashboard (admin) | `automation/tests/fr13_dashboard/` | `automation/data/fr13_dashboard.json` |

## Repository map

Four folders, one job each: **code** in `automation/`, **writing** in `docs/`,
**generated evidence** in `reports/`, **given material** in `refs/`.

```
HW04/
├── README.md               ← this file: §14 self-assessment + test summary
├── CLAUDE.md               ← project rules for the AI assistant
├── playwright.config.ts    ← 3 browser projects; stamps "Run by: 23127184" + ISO time
├── package.json · tsconfig.json · .env.example · .gitignore
│
├── automation/             ← ALL test code
│   ├── tests/              ← the automation scripts, one folder per feature
│   │   ├── fr01_account_registration/fr01.registration.spec.ts
│   │   ├── fr11_order_history/fr11.order-history.spec.ts
│   │   └── fr13_dashboard/fr13.dashboard.spec.ts
│   ├── data/               ← §6 external test-case datasets; no cases hardcoded in specs
│   ├── pages/              ← page objects (locators + actions)
│   ├── fixtures/           ← shared fixtures; stamps the Run-by annotation per test
│   ├── utils/              ← student.ts (run identity) · data-loader.ts · assertions.ts
│   └── run-all-browsers.ps1  ← runs all 9 feature × browser combinations
│
├── docs/                   ← ALL written deliverables
│   ├── 01_Main_Report.md       main report: process, results, gap analysis
│   ├── 02_Bug_Report.md        defects revealed by failing assertions
│   ├── 03_AI_Audit_Report.md   §9 mandatory appendix
│   ├── 04_AI_Critique.md       §10 mandatory, 200–300 words
│   ├── 05_Git_Commit_Log.txt   §12 commit log export
│   ├── prompt_logs.md          raw AI interaction log
│   ├── demo_links.md           Task 2 + §7 YouTube links and their checklists
│   └── test-plan/              TC_Matrix_FR01/FR11/FR13 · AI_Review_Gap_Analysis
│
├── reports/                ← ALL generated evidence (committed — never hand-edited)
│   ├── html/<feature>/<browser>/   the 9 HTML reports
│   ├── json/                       machine-readable results per run
│   ├── screenshots/                failure screenshots backing each bug
│   └── github_issues/              issue-page screenshots after GitHub filing (currently pending)
│
├── refs/                   ← given material
│   ├── requirements/           assignment brief (EN, md + pdf) + course policies
│   └── slides/                 S12 Automation testing
│
└── .claude/skills/         ← §7 Agent Skills
    ├── playwright-automation/
    └── ai-audit-log/
```

## Getting started

```powershell
# 1. install
npm install
npx playwright install          # downloads chromium, firefox, webkit

# 2. configure
copy .env.example .env          # then fill in BASE_URL and the test accounts

# 3. start the SUT (see the eshop-sut repo), then verify selectors before trusting results
npx playwright codegen $env:BASE_URL

# 4. run one feature on one browser
$env:FEATURE='fr01'; $env:BROWSER='chromium'
npx playwright test automation/tests/fr01_account_registration --project=chromium

# 5. run all 9 combinations and write reports/run-summary.txt
npm run runs:all
```

Run everything from the HW04 root. Each run writes
`reports/html/<feature>/<browser>/index.html`, whose title and metadata carry
`Run by: 23127184` and an ISO timestamp — the §11 evidence requirement.

## Test summary report (§14)

Fill from `reports/run-summary-fr01.txt`, the JSON results, and the HTML reports. Do not hand-edit the reports
themselves; if a number is wrong, re-run.

| Metric | Value |
|---|---|
| Features automated | 3 |
| FR-01 test cases automated | 31 / ≥ 12 |
| FR-01 executions | 93 (31 × 3 browsers) |
| FR-01 passed | 51 |
| FR-01 failed | 42 failed executions = 14 unique cases × 3 browsers; 11 cases support 4 confirmed bug groups and 3 are open questions |
| FR-01 browser runs | 3 / 3 |
| Confirmed FR-01 issue-level bug reports | 11 across 4 shared root causes |
| FR-01 GitHub Issues | 0 / 14 — 11 confirmed bug issues + 3 requirement-clarification issues, all pending filing |
| FR-01 cases not automatable | TC-17, TC-23; EC-34 documented as moot |
| Demo video | _<YouTube link>_ |

### Per-run results

| # | Feature | Browser | Tests | Pass | Fail | Started (ISO) | Report |
|---|---|---|---|---|---|---|---|
| 1 | FR-01 | chromium | 31 | 17 | 14 | 2026-08-10T10:51:15.344Z | `reports/html/fr01/chromium/index.html` |
| 2 | FR-01 | firefox | 31 | 17 | 14 | 2026-08-10T10:57:33.665Z | `reports/html/fr01/firefox/index.html` |
| 3 | FR-01 | webkit | 31 | 17 | 14 | 2026-08-10T11:05:04.508Z | `reports/html/fr01/webkit/index.html` |
| 4 | FR-11 | chromium | | | | | `reports/html/fr11/chromium/index.html` |
| 5 | FR-11 | firefox | | | | | `reports/html/fr11/firefox/index.html` |
| 6 | FR-11 | webkit | | | | | `reports/html/fr11/webkit/index.html` |
| 7 | FR-13 | chromium | 2026-08-10T11:38:45.582Z | 50 | 29 | 21 | `reports/html/fr13/all/index.html` |
| 8 | FR-13 | firefox | | | | | `reports/html/fr13/firefox/index.html` |
| 9 | FR-13 | webkit | | | | | `reports/html/fr13/webkit/index.html` |

## Self-assessment table (§15)

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | Task 1 — Feature A (FR-01 Account registration) | 25 | 23 |
| 1 | Task 1 — Feature B (FR-11 Order history view) | 25 | |
| 1 | Task 1 — Feature C (FR-13 Dashboard) | 25 | |
| 2 | Task 2 — Demo video | 15 | |
| 3 | Agent Skills | 10 | |
| | **Total** | **100** | |

**FR-01 self-assessment.** The feature exceeds the 12-case minimum with 31 external CSV
rows, uses three assertion patterns, and has complete reports for all three browsers with
student/timestamp metadata. Eleven confirmed issue-level reports across four shared root
causes and three inferred findings are
triaged without weakening assertions. Two points remain unclaimed because the fourteen public
GitHub Issues and their issue-page screenshots require the student to perform the real
external filing; no URL or screenshot is fabricated locally.

## Submission checklist (§14)

- [ ] `docs/01_Main_Report.md` — Markdown **and** PDF
- [ ] Public GitHub repository link
- [ ] 9 multi-browser HTML reports, each showing `Run by: 23127184` + ISO timestamp
- [ ] Unlisted YouTube demo video (≥ 5 min, Vietnamese, face-cam or `whoami`/`hostname`)
- [ ] `docs/04_AI_Critique.md` (200–300 words) — Markdown and PDF
- [ ] `docs/03_AI_Audit_Report.md` — Markdown and PDF
- [ ] `docs/05_Git_Commit_Log.txt` (≥ 8 `.spec.ts` commits over ≥ 4 days)
- [ ] `docs/02_Bug_Report.md` + GitHub Issues screenshots
- [ ] This `README.md` with the self-assessment table and the test summary
- [ ] Zip named `23127184_HW04_AI_Automation_<grade>.zip`
