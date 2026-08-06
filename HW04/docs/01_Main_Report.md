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
| Automation framework | Playwright Test | |
| Language | TypeScript | |
| Reporter | Playwright HTML reporter | |
| AI tool(s) | | |
| Node.js | | v24.4.1 |
| OS | Windows 11 | |
| SUT deployment | | |

---

## 3. Task 1 — AI-generated automation scripts

### 3.1 How the AI was driven, step by step (§2 "AI-First strategy")

The brief rejects a single generic prompt. Record the actual step sequence used per
feature — the same sequence should be visible in `docs/03_AI_Audit_Report.md`.

| Step | What the AI was asked to do | Output | My review verdict |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### 3.2 Data-driven design

- Test data lives in `automation/data/`, never inline (§6). Loaders: `automation/utils/data-loader.ts`.
- Assertion patterns used — at least three distinct ones (§6):

| # | Pattern | Implemented in | Used by |
|---|---|---|---|
| 1 | UI state / web-first assertion | `automation/utils/assertions.ts` | |
| 2 | API / contract assertion | `automation/utils/assertions.ts` | |
| 3 | Data-integrity assertion | `automation/utils/assertions.ts` | |

### 3.3 Multi-browser execution (≥ 9 runs)

Every report below shows `Run by: 23127184` and an ISO timestamp (§6, §11).

| # | Feature | Browser | Started (ISO) | Tests | Pass | Fail | Report path |
|---|---|---|---|---|---|---|---|
| 1 | FR-01 | chromium | | | | | `reports/html/fr01/chromium/index.html` |
| 2 | FR-01 | firefox | | | | | `reports/html/fr01/firefox/index.html` |
| 3 | FR-01 | webkit | | | | | `reports/html/fr01/webkit/index.html` |
| 4 | FR-11 | chromium | | | | | `reports/html/fr11/chromium/index.html` |
| 5 | FR-11 | firefox | | | | | `reports/html/fr11/firefox/index.html` |
| 6 | FR-11 | webkit | | | | | `reports/html/fr11/webkit/index.html` |
| 7 | FR-13 | chromium | | | | | `reports/html/fr13/chromium/index.html` |
| 8 | FR-13 | firefox | | | | | `reports/html/fr13/firefox/index.html` |
| 9 | FR-13 | webkit | | | | | `reports/html/fr13/webkit/index.html` |

### 3.4 Human review and fixes

Full log: `docs/test-plan/AI_Review_Gap_Analysis.md`. Summarise the headline findings here —
what the AI got wrong, and **why** it missed it.

### 3.5 Defects found

Full detail: `docs/02_Bug_Report.md`. Each defect also filed as a GitHub Issue with a screenshot.

| Bug ID | Feature | Severity | Revealed by | GitHub Issue | Screenshot |
|---|---|---|---|---|---|
| | | | | | |

### 3.6 Test cases not automated

See the "Cases deliberately NOT automated" section in each `docs/test-plan/TC_Matrix_*.md`.

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
