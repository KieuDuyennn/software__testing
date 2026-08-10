# HW04 — Automation Testing on EShop (Main Report)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Course:** CS423/CSC13003 — Software Testing (FIT@HCMUS) · **Exercise:** HW04-AI
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**Public repository:** https://github.com/KieuDuyennn/software__testing
**AI declaration:** I use AI tools for the following tasks — see `docs/03_AI_Audit_Report.md`.

---

## 1. Feature selection (§5)

The three web features are the same ones selected in HW02, one from each of Pools A, B, C.
HW02's fourth feature, FR-06 Product detail view, was that assignment's **Pool D (mobile)**
choice and is therefore excluded here, as §5 requires.

| Pool | Feature | HW02 artifact | HW04 spec | Data file |
|---|---|---|---|---|
| A | FR-01 Account registration | `HW02/submission/projects/fr01_account_registration/` | `automation/tests/fr01_account_registration/fr01.registration.spec.ts` | `automation/data/fr01_registration.csv` |
| B | FR-11 Order history view (user) | `HW02/submission/projects/fr11_order_history_view/` | `automation/tests/fr11_order_history/fr11.order-history.spec.ts` | `automation/data/fr11_order_history.json` |
| C | FR-13 Dashboard | `HW02/submission/projects/fr13_dashboard/` | `automation/tests/fr13_dashboard/fr13.dashboard.spec.ts` | `automation/data/fr13_dashboard.json` |

**Student declaration:** this FR-01 / FR-11 / FR-13 selection was carried forward
unchanged from the Group 09 HW02 allocation and does not duplicate another member's
assigned Pool A, B, or C feature.

---

## 2. Tooling and environment (§8)

| Item | Choice | Version |
|---|---|---|
| Automation framework | Playwright Test | 1.50.x |
| Language | TypeScript | 5.7.x |
| Reporter | Playwright HTML reporter | |
| AI tool(s) | Claude Code; OpenAI Codex | See `docs/03_AI_Audit_Report.md` |
| Node.js | | v24.4.1 |
| OS | Windows 11 | |
| SUT deployment | Local: customer UI `:5173`, API `:3000` | EShop checked out locally |

---

## 3. Task 1 — AI-generated automation scripts

### 3.1 How the AI was driven, step by step (§2 "AI-First strategy")

The brief rejects a single generic prompt. Record the actual step sequence used per
feature — the same sequence should be visible in `docs/03_AI_Audit_Report.md`.

| Step | What the AI was asked to do | Output | My review verdict |
|---|---|---|---|
| 1 | Trace HW02 FR-01 cases to the written SUT requirement; identify unreachable Confirm Password cases. | 31-row coverage plan and explicit exclusions. | Preserved designed cases; rejected invented fields and undocumented certainty. |
| 2 | Inspect `Register.jsx` and probe the live page before writing locators. | Verified three inputs, missing label associations, one error banner, and the actual password regex. | Replaced non-matching `getByLabel` guesses with label-text-anchored locators. |
| 3 | Externalise every case into CSV and generate one Playwright test per row. | `fr01_registration.csv` plus one branching spec for native, banner, redirect, and API channels. | Confirmed 43 CSV rows produce 129 project tests; no inline case dataset. |
| 4 | Run all browsers, triage red cases against the requirement and API specification. | HTML/JSON reports, screenshots, traces, and `FR01_Failure_Evidence.md`. | Corrected the AI's guessed success status from 201 to documented 200; kept genuine divergences red. |
| 5 | Re-review the happy path and negative API evidence. | TC-01a now uses `Password123!`; TC-01c isolates downstream plumbing; rejected API responses assert no returned `id`. | Removed the false-green happy-path claim and exposed stronger server-creation evidence. |

### 3.2 Data-driven design

- Test data lives in `automation/data/`, never inline (§6). Loaders: `automation/utils/data-loader.ts`.
- Assertion patterns used — at least three distinct ones (§6):

| # | Pattern | Implemented in | Used by |
|---|---|---|---|
| 1 | UI state / web-first assertion | Playwright locators and native validity checks | FR-01 banner text, URL, form visibility, `checkValidity()` |
| 2 | API / contract assertion | `automation/utils/assertions.ts` and FR-01 spec | FR-01 status, numeric success `id`, absence of rejection `id` |
| 3 | Data-integrity assertion | FR-01 spec plus `/api/login` probe | FR-01 claimed success must be usable and preserve submitted name/e-mail; observable rejection must leave no usable account |

FR-01 is data-driven in execution, not merely in storage: all 43 rows are loaded from
`automation/data/fr01_registration.csv`; each row chooses the channel and expected signal,
and the spec creates one named test from it. Runtime placeholders keep valid e-mails unique
across repeated browser runs. TC-01c is labelled diagnostic because its bypass password is
implementation-compatible rather than specification-valid.

### 3.3 Multi-browser execution (≥ 9 runs)

Every report below shows `Run by: 23127184` and an ISO timestamp (§6, §11).

| # | Feature | Browser | Started (ISO) | Tests | Pass | Fail | Report path |
|---|---|---|---|---|---|---|---|
| 1 | FR-01 | chromium | 2026-08-10T12:06:09.635Z | 43 | 17 | 26 | `reports/final/html/fr01/chromium/index.html` |
| 2 | FR-01 | firefox | 2026-08-10T14:28:58.633Z | 43 | 17 | 26 | `reports/final/html/fr01/firefox/index.html` |
| 3 | FR-01 | webkit | 2026-08-10T14:55:13.862Z | 43 | 17 | 26 | `reports/final/html/fr01/webkit/index.html` |
| 4 | FR-11 | chromium | 2026-08-10 | 46 | 30 | 16 | `reports/final/html/fr11/chromium/index.html` |
| 5 | FR-11 | firefox | 2026-08-10 | 46 | 30 | 16 | `reports/final/html/fr11/firefox/index.html` |
| 6 | FR-11 | webkit | 2026-08-10 | 46 | 30 | 16 | `reports/final/html/fr11/webkit/index.html` |
| 7 | FR-13 | chromium | 2026-08-10T11:38:45.582Z | 50 | 29 | 21 | `reports/final/html/fr13/chromium/index.html` |
| 8 | FR-13 | firefox | 2026-08-10 | 50 | 30 | 20 | `reports/final/html/fr13/firefox/{tc,bva,api}/index.html` |
| 9 | FR-13 | webkit | 2026-08-10 | 50 | 30 | 20 | `reports/final/html/fr13/webkit/{tc,bva,api}/index.html` |

The final FR-01 runs used `LOADTEST=1` only to disable the SUT's global 200-request/
15-minute API limiter while executing 43 independent cases. No SUT source, test data,
or expectation was changed; normal rate limiting was restored after the run. Exit code 1
is expected because the reports preserve product divergences as failed assertions.

### 3.4 Human review and fixes

For FR-01, human review corrected the guessed success status from 201 to the documented
200, replaced fragile label locators after inspecting the actual DOM, and added runtime-
unique e-mails for repeatability. Most importantly, the initial happy path used a password
accepted only by the implementation; TC-01a now uses the requirement-valid `Password123!`
and correctly fails, while TC-01c is explicitly diagnostic and proves redirect plus account
persistence with the implementation-compatible gate. Native browser validity is checked
as state rather than browser-specific prose, and rejected API responses must not return an
`id`. A historical Firefox teardown symptom did not reproduce in the two final reruns. No
assertion was weakened to turn a product divergence green.

The full correction log is in `docs/test-plan/AI_Review_Gap_Analysis.md`. Its recurring
causes were unverified UI assumptions, implementation-derived oracles, missing
cross-row consistency checks, and fail-soft guards that could silently skip assertions.

### 3.5 Defects found

Full detail: `docs/02_Bug_Report.md`. FR-01 findings are filed as GitHub Issues #39–#64,
with issue-page screenshots stored under `reports/evidence/github-issues/fr01/`. All 26 issues have their
matching failure image attached directly in GitHub.

| Bug ID | Feature | Severity | Revealed by | GitHub Issue | Screenshot |
|---|---|---|---|---|---|
| BUG-FR01-01→11 | FR-01 | Major | Original 11 confirmed cases | [#39–#49](https://github.com/KieuDuyennn/software__testing/issues) | See per-issue paths in `docs/02_Bug_Report.md` |
| BUG-FR01-15→26 | FR-01 | Major | API-01→API-12 | [#53–#64](https://github.com/KieuDuyennn/software__testing/issues) | See per-issue paths in `docs/02_Bug_Report.md` |
| BUG-FR13-01 | FR-13 | Major | TC-02, BVA, TC-13b, TC-21 | Fixed and tracked in GitHub #15 | `reports/final/json/fr13-chromium.json` |
| BUG-FR13-02 | FR-13 | Major | TC-13 | Fixed and tracked in GitHub #38 | `reports/final/json/fr13-chromium.json` |
| BUG-FR13-03 | FR-13 | Critical | TC-11, API-14–17 | Fixed and tracked in GitHub #34 | `reports/final/json/fr13-chromium.json` |
| BUG-FR13-04 | FR-13 | Critical | TC-04b, API-03/04/06/09 | Fixed and tracked in GitHub #14 | `reports/final/json/fr13-chromium.json` |
| BUG-FR13-05 | FR-13 | Critical | API-10 | Fixed and tracked in GitHub #36 | `reports/final/json/fr13-chromium.json` |
| BUG-FR13-06 | FR-13 | Critical | TC-19 | Fixed and tracked in GitHub #37 | `reports/final/json/fr13-chromium.json` |

### 3.6 Test cases not automated

See the "Cases deliberately NOT automated" section in each `docs/test-plan/TC_Matrix_*.md`.

For FR-01, TC-17 and TC-23 require a Confirm Password control that the SUT does not render;
EC-34 depends on a session-expiry/reauthentication flow outside the registration form.
They are documented rather than silently converted into different tests. TC-18, TC-19,
and TC-21 do execute, but remain labelled open questions because their requirement anchors
are inferred and their red results are not counted as confirmed product defects.

To preserve all failing evidence on GitHub without overstating it, TC-18, TC-19 and TC-21
are filed as `ISSUE-FR01-12` through `ISSUE-FR01-14` ([#50–#52](https://github.com/KieuDuyennn/software__testing/issues))
with the `question` label. Together with the twenty-three confirmed bug entries above,
the FR-01 GitHub delivery contains twenty-six issues.

---

## 4. Task 2 — Demo video (§6)

| Item | Value |
|---|---|
| YouTube link (unlisted, ≥ 5 min, Vietnamese narration) | **Pending student upload** |
| Feature demonstrated end to end | Planned: FR-01 Account registration |
| Multi-browser run shown | Planned: Chromium, Firefox, WebKit |
| HTML report shown | Planned: final FR-01 report with student ID and ISO timestamp |
| AI fix narrated (which one) | Planned: replacing guessed locators and separating requirement-valid from implementation-compatible passwords |
| Authorship evidence | Planned: terminal `whoami` + `hostname` |

---

## 5. Agent Skill (§7)

| Item | Value |
|---|---|
| Skill name | `playwright-automation` (`.claude/skills/playwright-automation/`) |
| What it automates | A staged workflow for external test data, verified selectors, page objects, three assertion classes, multi-browser runs, report attribution, and failure triage |
| Features it was used on | Exercised and refined during FR-01; its shared project conventions and report workflow support FR-01, FR-11, and FR-13 |
| Demo video (YouTube) | Pending student upload |

---

## 6. Git commit log (§12)

The course's former four-day threshold was removed. The submitted log therefore records
the actual HW04 history without asserting a minimum-day condition. Exported to
`docs/05_Git_Commit_Log.txt`.

| Metric | Value |
|---|---|
| Total HW04 commits before final documentation export | 82 |
| Commits touching `.spec.ts` | 7 |
| Distinct `.spec.ts` commit dates | 2 (reported for transparency; no longer a grading threshold) |
| First / last commit date | 2026-08-06 / 2026-08-11 |

---

## 7. Compliance checklist (§14 required contents)

- [x] Main report — `docs/01_Main_Report.md` and `output/pdf/01_Main_Report.pdf`
- [ ] Public GitHub repository link is filled; push the final local `duyen/hw4` commit before submission
- [x] Multi-browser HTML reports (9 runs, each showing `Run by: 23127184`)
- [ ] Unlisted YouTube demo video link (≥ 5 min, Vietnamese)
- [x] `docs/04_AI_Critique.md` (263 words) and `output/pdf/04_AI_Critique.pdf`
- [x] `docs/03_AI_Audit_Report.md` and `output/pdf/03_AI_Audit_Report.pdf`
- [x] `docs/05_Git_Commit_Log.txt`
- [x] `docs/02_Bug_Report.md` + GitHub Issues screenshots
- [x] `README.md` with self-assessment table and test summary
- [ ] Zip named `23127184_HW04_AI_Automation_<grade>.zip`
