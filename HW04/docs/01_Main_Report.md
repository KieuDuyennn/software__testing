# HW04 — Automation Testing on EShop (Main Report)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Course:** CS423/CSC13003 — Software Testing (FIT@HCMUS) · **Exercise:** HW04-AI
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**Public repository:** _<paste the GitHub URL>_
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

No duplication with other group members: _<state how this was checked>_

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
| 3 | Externalise every case into CSV and generate one Playwright test per row. | `fr01_registration.csv` plus one branching spec for native, banner, redirect, and API channels. | Confirmed 31 CSV rows produce 93 project tests; no inline case dataset. |
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

FR-01 is data-driven in execution, not merely in storage: all 31 rows are loaded from
`automation/data/fr01_registration.csv`; each row chooses the channel and expected signal,
and the spec creates one named test from it. Runtime placeholders keep valid e-mails unique
across repeated browser runs. TC-01c is labelled diagnostic because its bypass password is
implementation-compatible rather than specification-valid.

### 3.3 Multi-browser execution (≥ 9 runs)

Every report below shows `Run by: 23127184` and an ISO timestamp (§6, §11).

| # | Feature | Browser | Started (ISO) | Tests | Pass | Fail | Report path |
|---|---|---|---|---|---|---|---|
| 1 | FR-01 | chromium | 2026-08-10T10:51:15.344Z | 31 | 17 | 14 | `reports/html/fr01/chromium/index.html` |
| 2 | FR-01 | firefox | 2026-08-10T10:57:33.665Z | 31 | 17 | 14 | `reports/html/fr01/firefox/index.html` |
| 3 | FR-01 | webkit | 2026-08-10T11:05:04.508Z | 31 | 17 | 14 | `reports/html/fr01/webkit/index.html` |
| 4 | FR-11 | chromium | 2026-08-10 | 46 | 30 | 16 | `reports/html/fr11/chromium/index.html` |
| 5 | FR-11 | firefox | 2026-08-10 | 46 | 30 | 16 | `reports/html/fr11/firefox/index.html` |
| 6 | FR-11 | webkit | 2026-08-10 | 46 | 30 | 16 | `reports/html/fr11/webkit/index.html` |
| 7 | FR-13 | chromium | 2026-08-10T11:38:45.582Z | 50 | 29 | 21 | `reports/html/fr13/all/index.html` |
| 8 | FR-13 | firefox | | | | | `reports/html/fr13/firefox/index.html` |
| 9 | FR-13 | webkit | | | | | `reports/html/fr13/webkit/index.html` |

The final FR-01 runs used `LOADTEST=1` only to disable the SUT's global 200-request/
15-minute API limiter while executing 31 independent cases. No SUT source, test data,
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

Full log: `docs/test-plan/AI_Review_Gap_Analysis.md`. Summarise the headline findings here —
what the AI got wrong, and **why** it missed it.

### 3.5 Defects found

Full detail: `docs/02_Bug_Report.md`. Each confirmed defect must also be filed as a
GitHub Issue with an issue-page screenshot; the table states the current, non-fabricated
filing status.

| Bug ID | Feature | Severity | Revealed by | GitHub Issue | Screenshot |
|---|---|---|---|---|---|
| BUG-FR01-01 | FR-01 | Major | TC-01a | Pending student filing | `reports/screenshots/BUG-FR01-01-password-valid-rejected.png` |
| BUG-FR01-02 | FR-01 | Major | BVA-02 | Pending student filing | `reports/screenshots/BUG-FR01-02-password-minimum-8-rejected.png` |
| BUG-FR01-03 | FR-01 | Major | BVA-03 | Pending student filing | `reports/screenshots/BUG-FR01-03-password-9-rejected.png` |
| BUG-FR01-04 | FR-01 | Major | TC-24 | Pending student filing | `reports/screenshots/BUG-FR01-04-weak-whitespace-password-accepted.png` |
| BUG-FR01-05 | FR-01 | Major | TC-06 | Pending student filing | `reports/screenshots/BUG-FR01-05-email-no-at-accepted.png` |
| BUG-FR01-06 | FR-01 | Major | TC-07 | Pending student filing | `reports/screenshots/BUG-FR01-06-email-no-domain-accepted.png` |
| BUG-FR01-07 | FR-01 | Major | TC-08 | Pending student filing | `reports/screenshots/BUG-FR01-07-email-no-local-accepted.png` |
| BUG-FR01-08 | FR-01 | Major | TC-09 | Pending student filing | `reports/screenshots/BUG-FR01-08-duplicate-email-accepted.png` |
| BUG-FR01-09 | FR-01 | Major | TC-03 | Pending student filing | `reports/screenshots/BUG-FR01-09-missing-name-created.png` |
| BUG-FR01-10 | FR-01 | Major | TC-05 | Pending student filing | `reports/screenshots/BUG-FR01-10-missing-email-created.png` |
| BUG-FR01-11 | FR-01 | Major | TC-11 | Pending student filing | `reports/screenshots/BUG-FR01-11-missing-password-created.png` |
| BUG-FR13-01 | FR-13 | Major | TC-02, BVA, TC-13b, TC-21 | Deferred with issue filing | `reports/json/fr13-all.json` |
| BUG-FR13-02 | FR-13 | Major | TC-13 | Deferred with issue filing | `reports/json/fr13-all.json` |
| BUG-FR13-03 | FR-13 | Critical | TC-11, API-14–17 | Deferred with issue filing | `reports/json/fr13-all.json` |
| BUG-FR13-04 | FR-13 | Critical | TC-04b, API-03/04/06/09 | Deferred with issue filing | `reports/json/fr13-all.json` |
| BUG-FR13-05 | FR-13 | Critical | API-10 | Deferred with issue filing | `reports/json/fr13-all.json` |
| BUG-FR13-06 | FR-13 | Critical | TC-19 | Deferred with issue filing | `reports/json/fr13-all.json` |

### 3.6 Test cases not automated

See the "Cases deliberately NOT automated" section in each `docs/test-plan/TC_Matrix_*.md`.

For FR-01, TC-17 and TC-23 require a Confirm Password control that the SUT does not render;
EC-34 depends on a session-expiry/reauthentication flow outside the registration form.
They are documented rather than silently converted into different tests. TC-18, TC-19,
and TC-21 do execute, but remain labelled open questions because their requirement anchors
are inferred and their red results are not counted as confirmed product defects.

To preserve all failing evidence on GitHub without overstating it, TC-18, TC-19 and TC-21
are prepared as `ISSUE-FR01-12` through `ISSUE-FR01-14` with the label
`requirement-clarification`. Together with the eleven confirmed bug entries above, the
FR-01 GitHub delivery target is fourteen issues.

---

## 4. Task 2 — Demo video (§6)

| Item | Value |
|---|---|
| YouTube link (unlisted, ≥ 5 min, Vietnamese narration) | |
| Feature demonstrated end to end | |
| Multi-browser run shown | |
| HTML report shown | |
| AI fix narrated (which one) | |
| Authorship evidence | face-cam / terminal `whoami` + `hostname` |

---

## 5. Agent Skill (§7)

| Item | Value |
|---|---|
| Skill name | `playwright-automation` (`.claude/skills/playwright-automation/`) |
| What it automates | |
| Features it was used on | |
| Demo video (YouTube) | |

---

## 6. Git commit log (§12)

≥ 8 commits over ≥ 4 days, counting only commits that change test-script files.
Exported to `docs/05_Git_Commit_Log.txt`.

| Metric | Value |
|---|---|
| Total commits | |
| Commits touching `.spec.ts` | |
| Distinct days | |
| First / last commit date | |

---

## 7. Compliance checklist (§14 required contents)

- [ ] Main report — Markdown **and** PDF
- [ ] Public GitHub repository link (scripts, data files, HTML reports)
- [ ] Multi-browser HTML reports (9 runs, each showing `Run by: 23127184`)
- [ ] Unlisted YouTube demo video link (≥ 5 min, Vietnamese)
- [ ] `docs/04_AI_Critique.md` (200–300 words) — Markdown and PDF
- [ ] `docs/03_AI_Audit_Report.md` — Markdown and PDF
- [ ] `docs/05_Git_Commit_Log.txt`
- [ ] `docs/02_Bug_Report.md` + GitHub Issues screenshots
- [ ] `README.md` with self-assessment table and test summary
- [ ] Zip named `23127184_HW04_AI_Automation_<grade>.zip`
