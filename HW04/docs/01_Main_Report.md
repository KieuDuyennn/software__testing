# HW04 — Automation Testing on EShop (Main Report)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Course:** CS423/CSC13003 — Software Testing (FIT@HCMUS) · **Exercise:** HW04-AI
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**Public submission folder:** https://github.com/KieuDuyennn/software__testing/tree/main/HW04
**AI declaration:** I use AI tools for the following tasks — see `docs/03_AI_Audit_Report.md`.

---

## 1. Feature selection (§5)

This submission automates the three HW02-selected web features FR-01, FR-11 and FR-13,
one from each of Pools A–C; no Pool D/mobile feature is included.

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
| Reporter | Playwright HTML reporter | 1.50.x |
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

#### FR-11 workflow

| Step | AI proposal or task | Human verification | Accepted correction / evidence |
|---|---|---|---|
| 1 | Convert the HW02 order-history matrix to JSON and generate UI/API branches. | Traced the customer router, `Profile.jsx`, and backend order contracts before accepting routes or oracles. | Replaced the invented `/orders` route and requirement-conflicting shipping-cancel expectations. |
| 2 | Generate page-object locators and row helpers. | Counted live DOM matches and deliberately tested overlapping IDs such as `#1` and `#10`. | Added exact order-row lookup, real table-cell scoping, and numeric ID sorting. |
| 3 | Add data guards and API assertions. | Injected malformed rows, ran collection, and followed genuine red cases past their first failed status. | Moved validation to module load; prevented assertion-free rows; collected mutation/disclosure evidence before soft status assertions. |
| 4 | Run 46 cases across three engines. | Measured cumulative requests and observed worker replacement after failures rather than trusting `--list` or `beforeAll`. | Moved reusable login to `globalSetup`; ran two explicit ID groups with a disposable backend restart and merged the final evidence without disabling the limiter. |

#### FR-13 workflow

| Step | AI proposal or task | Human verification | Accepted correction / evidence |
|---|---|---|---|
| 1 | Generate a dashboard JSON dataset, page object and mixed UI/API spec. | Read the admin entry point and probed the proposed origin, route, controls and locator counts. | Navigated to the absolute admin root on `:5174`; removed invented date/table controls and anchored KPI locators to real headings. |
| 2 | Cross-check dashboard values with the orders API. | Probed authenticated and unauthenticated endpoints and compared response keys with the server schema. | Sent explicit bearer tokens, read `total_amount`, and separated UI access checks from API authorization checks. |
| 3 | Generate edge/API oracles. | Reviewed cross-row consistency, injected invalid JSON, and recalculated expected cart totals independently. | Replaced weak inequality/default-value checks with fail-loud schema validation and exact recomputation (`399000`). |
| 4 | Execute all three engines and triage failures. | Compared KPI deltas with seeded API state and preserved failures that reproduced the same mechanism. | Grouped 21 Chromium failures into six filed root causes while keeping every failing case visible in HTML/JSON evidence. |

### 3.2 Data-driven design

- Test data lives in `automation/data/`, never inline (§6). Loaders: `automation/utils/data-loader.ts`.
- Assertion patterns used — at least three distinct ones (§6):

| # | Pattern | Implemented in | Used by |
|---|---|---|---|
| 1 | UI state / web-first assertion | FR-01 spec and `RegisterPage` | Banner text, URL, form visibility, native `checkValidity()` |
| 2 | API / contract assertion | FR-01 spec and `automation/utils/assertions.ts` | Status, numeric success `id`, absence of rejection `id` |
| 3 | Data-integrity assertion | FR-01 spec plus `/api/login` probe | Claimed success must create a usable account preserving name/e-mail |
| 4 | UI state / semantic table assertion | FR-11 spec and order-history page object | Exact row identity, status badge, cancel visibility, localized-date components |
| 5 | API / authorization contract | FR-11 API branches | Refusal status plus cross-user disclosure and role-boundary checks |
| 6 | Mutation / persistence integrity | FR-11 API branches | Rejected cancel/status/checkout actions must leave the owning record unchanged |
| 7 | UI KPI/access assertion | FR-13 spec and `AdminDashboardPage` | Dashboard reachability, real KPI headings and rendered numeric values |
| 8 | API authorization/schema contract | FR-13 API branches | Token/role boundaries, status sets and required response fields |
| 9 | Independent recomputation / delta integrity | FR-13 seeded-state branches | Revenue/order deltas and exact server recomputation from `total_amount` |

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
| 4 | FR-11 | chromium | 2026-08-10T14:10:00.890Z | 46 | 30 | 16 | `reports/final/html/fr11/chromium/index.html` |
| 5 | FR-11 | firefox | 2026-08-10T12:01:52.340Z | 46 | 30 | 16 | `reports/final/html/fr11/firefox/index.html` |
| 6 | FR-11 | webkit | 2026-08-10T12:13:16.828Z | 46 | 30 | 16 | `reports/final/html/fr11/webkit/index.html` |
| 7 | FR-13 | chromium | 2026-08-10T11:38:45.582Z | 50 | 29 | 21 | `reports/final/html/fr13/chromium/index.html` |
| 8 | FR-13 | firefox | 2026-08-10T14:47:41.835Z (first split) | 50 | 30 | 20 | `reports/final/html/fr13/firefox/{tc,bva,api}/index.html` |
| 9 | FR-13 | webkit | 2026-08-10T14:53:18.599Z (first split) | 50 | 30 | 20 | `reports/final/html/fr13/webkit/{tc,bva,api}/index.html` |

The final FR-01 runs used `LOADTEST=1` only to disable the SUT's global 200-request/
15-minute API limiter while executing 43 independent cases. No SUT source, test data,
or expectation was changed; normal rate limiting was restored after the run. Exit code 1
is expected because the reports preserve product divergences as failed assertions.

### 3.4 Human review and fixes

For each feature, the AI produced the first scaffold and data-driven branches; my
acceptance gate was source tracing → live DOM/API probes → type-check and collection →
three-browser execution → evidence-led correction. The sections below distinguish the
AI proposal from my human decisions.

#### FR-01 — Account registration

For FR-01, human review corrected the guessed success status from 201 to the documented
200, replaced fragile label locators after inspecting the actual DOM, and added runtime-
unique e-mails for repeatability. Most importantly, the initial happy path used a password
accepted only by the implementation; TC-01a now uses the requirement-valid `Password123!`
and correctly fails, while TC-01c is explicitly diagnostic and proves redirect plus account
persistence with the implementation-compatible gate. Native browser validity is checked
as state rather than browser-specific prose, and rejected API responses must not return an
`id`. A historical Firefox teardown symptom did not reproduce in the two final reruns. No
assertion was weakened to turn a product divergence green.

#### FR-11 — Order history

The AI first converted the HW02 matrix into external JSON and generated the FR-11
Playwright scaffold. I did not accept it by inspection alone: I traced the customer
router and `Profile.jsx`, counted live locator matches, exercised overlapping order IDs,
injected malformed data, and ran genuine red cases on all three engines. The review found
an invented `/orders` route, guessed locators, substring row matching (`#1` also matching
`#10`–`#19`), localized dates parsed with Node `Date.parse`, and contradictory shipping-
cancel oracles derived from the current build rather than the requirement. Hard status
assertions also stopped before recording disclosure/mutation evidence, while per-test
authentication exhausted the SUT's global API limit. A first `beforeAll` repair still
repeated whenever Playwright replaced a worker after a failed test.

I corrected the route and DOM locators, exact row lookup and numeric ordering; moved JSON
validation to module load so malformed or assertion-free rows fail collection; compared
dates using browser-context year/month/day parts; collected state evidence before soft
status assertions; and moved reusable authentication to `globalSetup`. Because 46 valid
cases still exceed the limiter, the final workflow executes two explicit ID groups with a
disposable backend restart and merges their evidence without disabling the limiter. The AI
missed these points because it reasoned from common SPA conventions and one case at a time,
not from this SUT's router, DOM, worker lifecycle, cumulative request budget, or accumulated
database state. Evidence: FR-11 spec; gap-analysis findings 8–11 and 28–39; commits
`1cee595`, `99d9b9f`, `c078366`; and `reports/final/{html,json}/fr11/`.

#### FR-13 — Admin dashboard

The AI generated a JSON-driven dashboard scaffold with UI/API branches. I reviewed it by
reading the admin entry point and backend contracts, probing every proposed locator and
endpoint with and without tokens, injecting invalid data rows, and comparing KPI values
with independently seeded API state. This exposed an invented `/admin/dashboard` path on
the customer origin even though the admin app is a route-less root on port 5174; guessed
landmarks/test IDs and controls that do not exist; use of `total` instead of
`total_amount`; and an assumption that Playwright's request context inherited browser
authentication. The scaffold also confused a passing client-side role gate with API
authorization, used weak negative oracles, keyed behavior to `tc_id`, and trusted a
volatile JSON file without collection-time validation.

I changed navigation to the absolute admin origin, anchored KPI locators to real headings,
removed nonexistent controls, sent explicit bearer tokens, and tested authorization at the
API tier. Defensive `?? 0` defaults became fail-loud schema checks; behavior dispatch now
uses data columns rather than case IDs; currency matching is anchored; and whole-file
validation covers IDs, enums, numeric fields, status lists and declared case count. The
checkout oracle now populates a known cart and requires the exact recomputed total
`399000`. The AI missed these defects because it modeled a conventional dashboard instead
of this build and treated defensive defaults/negative assertions as safe. Evidence: FR-13
spec; gap-analysis findings 12–27; commits `9ce554b`, `c078366`, `68c1f3b`; and
`reports/final/{html,json}/fr13/`.

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
| BUG-FR13-01 | FR-13 | Major | TC-02, BVA, TC-13b, TC-21 | Filed as GitHub #15; reproduced in final run | `reports/evidence/github-issues/fr13/issue-15-BUG-FR13-01.png` |
| BUG-FR13-02 | FR-13 | Major | TC-13 | Filed as GitHub #38; reproduced in final run | `reports/evidence/github-issues/fr13/issue-38-BUG-FR13-02.png` |
| BUG-FR13-03 | FR-13 | Critical | TC-11, API-14–17 | Filed as GitHub #34; reproduced in final run | `reports/evidence/github-issues/fr13/issue-34-BUG-FR13-03.png` |
| BUG-FR13-04 | FR-13 | Critical | TC-04b, API-03/04/06/09 | Filed as GitHub #14; reproduced in final run | `reports/evidence/github-issues/fr13/issue-14-BUG-FR13-04.png` |
| BUG-FR13-05 | FR-13 | Critical | API-10 | Filed as GitHub #36; reproduced in final run | `reports/evidence/github-issues/fr13/issue-36-BUG-FR13-05.png` |
| BUG-FR13-06 | FR-13 | Critical | TC-19 | Filed as GitHub #37; reproduced in final run | `reports/evidence/github-issues/fr13/issue-37-BUG-FR13-06.png` |

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
| YouTube link (unlisted, ≥ 5 min, Vietnamese narration) | [https://youtu.be/krqH7ua7CNA](https://youtu.be/krqH7ua7CNA) |
| Duration / visibility verified | 10:06; unlisted |
| What the current recording proves | The reusable Agent Skill, its three-browser command, approval prompts, and an FR-13 agent invocation are visible. |
| Missing Task 2 evidence | No completed multi-browser execution or opened HTML report is visible before the recording ends. |
| Authorship evidence | No face-cam or completed `whoami` + `hostname` evidence was observed in the reviewed frames. |
| Submission decision | **Replace this recording before Moodle submission.** The URL is retained only as an honest process artifact. |

---

## 5. Agent Skill (§7)

| Item | Value |
|---|---|
| Primary skill | `playwright-automation` (`.claude/skills/playwright-automation/`) |
| Supporting skill | `ai-audit-log` (`.claude/skills/ai-audit-log/`) |
| Invocation contract | Requires explicit feature/requirement/design paths, application URLs, spec/data paths, browser projects, student ID and report destination; unresolved authoritative input produces `BLOCKED`, never a guessed default |
| Human gates | `BLOCKED` → `READY_FOR_REVIEW` → quoted human approval → `APPROVED_TO_RUN` → evidence-triaged `COMPLETE` |
| Oracle discipline | Requirement/API contract defines expected behavior; source/live DOM defines reachability, locators and observed behavior. Current build behavior is never copied into an expected result. |
| Deterministic validator | `playwright-automation/scripts/validate-feature.ps1` checks ≥12 unique external cases, data loading, fixed waits, report attribution, ISO timestamps and entry points |
| Output contract | A Feature Run Manifest records discovered inputs, validation commands/exit codes, approval quote, per-browser counts/paths and every red case's disposition |
| Features it was used on | Exercised/refined on FR-01; conventions applied and validated on FR-11 and FR-13 |
| Validation evidence | `docs/test-plan/Agent_Skill_Validation.md`: FR-01/FR-11 validator `PASS`; FR-13 `PASS_WITH_REVIEW_ITEMS`. All remain historically `READY_FOR_REVIEW` because approval quotes/manifests were not retained; no evidence was backfilled. |
| Demo video (YouTube) | [https://youtu.be/krqH7ua7CNA](https://youtu.be/krqH7ua7CNA) — partial process demonstration; a complete end-to-end replacement is still required |

The revision is based on observed project failures rather than generic advice. In
particular, the skill now forbids using the live build as the oracle (the cause of the
contradictory FR-11 shipping-cancel expectations), validates branch-specific data at
collection time (preventing silent skipped assertions), preserves downstream evidence
before a hard status check, and accounts for global request budgets and Playwright worker
replacement. The audit skill separately preserves prompts in their original language,
maps every raw interaction ID into the appendix, and marks incomplete logging honestly.
Commit `ef2b70f` additionally records the actual Playwright `browserName` on every FR-13
case and corrects a misleading order-ID failure message. TypeScript validation and a
50-case Chromium collection both pass after this change.

---

## 6. Git commit log (§12)

The course's former four-day threshold was removed. The submitted log therefore records
the actual HW04 history without asserting a minimum-day condition. Exported to
`docs/05_Git_Commit_Log.txt`.

| Metric | Value |
|---|---|
| Total HW04 commits at pre-export validation | 87 (the final documentation commit is added after export) |
| Commits touching `.spec.ts` | 8 |
| Distinct `.spec.ts` commit dates | 2 (reported for transparency; no longer a grading threshold) |
| First / last commit date | 2026-08-06 / 2026-08-11 |

---

## 7. Compliance checklist (§14 required contents)

- [x] Main report — `docs/01_Main_Report.md` and `output/pdf/01_Main_Report.pdf`
- [x] Public submission folder is merged under `main/HW04`
- [x] 9 browser combinations (13 HTML entry points), all showing `Run by: 23127184` + ISO timestamp
- [ ] Replace the current [unlisted 10:06 process recording](https://youtu.be/krqH7ua7CNA) with the complete Task 2 evidence required by §6 and §11
- [x] `docs/04_AI_Critique.md` (263 words) and `output/pdf/04_AI_Critique.pdf`
- [x] `docs/03_AI_Audit_Report.md` and `output/pdf/03_AI_Audit_Report.pdf`
- [x] `docs/05_Git_Commit_Log.txt`
- [x] `docs/02_Bug_Report.md` + GitHub Issues screenshots
- [x] `README.md` with self-assessment table and test summary
- [x] One Moodle-safe ZIP prepared as `23127184_HW04_AI_Automation_100.zip`
  (large trace/video attachments are available in the public repository, not duplicated in the ZIP)
