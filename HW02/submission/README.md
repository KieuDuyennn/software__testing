# HW02 - Domain Testing on EShop

- **Student ID:** 23127184
- **Course:** CS423/CSC13003 - Software Testing (FIT@HCMUS)
- **Assignment:** HW02-AI - Domain Testing & Boundary Value Analysis
- **SUT:** EShop (https://github.com/ttbhanh/eshop-sut)
- **Submission repository:** https://github.com/KieuDuyennn/KTPM_23127184/tree/main/HW02
- **AI declaration:** I use AI tools (Claude Code) for the tasks recorded in the AI Audit Report (`reports/AI_Audit_Report.md` and `reports/prompt_logs.md`).

## Submission contents

| Path | Content |
|---|---|
| `README.md` | This file: self-assessment table and test summary report |
| `reports/Main_Report_Domain_Testing_BVA.md` | Main report: Domain Testing report and BVA report (methodology, per-feature results, AI gap analysis) |
| `reports/AI_Audit_Report.md` | AI Audit Report (declaration and full interaction log) |
| `reports/prompt_logs.md` | Full verbatim AI interaction log (appendix to the audit report) |
| `reports/AI_Critique.md` | AI Critique (200 to 300 words) |
| `reports/Bug_Report.md` | Bug report (with links and screenshots of GitHub Issues) |
| `git_commit_log.txt` | Git commit log (one commit per phase per feature) |
| `projects/<feature>/` | Per-feature test-design workspace: FR input, 4 phase artifacts, gap notes, workflow state |
| `skills/` | Agent Skills built for this assignment (`domain-testing-bva`, `ai-audit-log`) plus project rules (`CLAUDE.md`) |

## Selected features

| Feature | Pool | Project folder | Workflow status |
|---|---|---|---|
| FR-01 Account registration | A | `projects/fr01_account_registration/` | COMPLETED (4/4 phases approved) |
| FR-06 Product detail view (Mobile) | D | `projects/fr06_product_detail_view/` | COMPLETED (4/4 phases approved) |
| FR-11 Order history view (user) | B | `projects/fr11_order_history_view/` | COMPLETED (4/4 phases approved) |
| FR-13 Dashboard | C | `projects/fr13_dashboard/` | COMPLETED (4/4 phases approved) |

## Test summary report

Counts are taken directly from the approved phase artifacts (`03_Domain_Test_Cases.md`, `04_Boundary_Value_Test_Cases.md`) of each feature. **Execution evidence:** all 73 designed cases were run against a live EShop SUT on 2026-07-07 across two passes, except FR-01 TC-17 and TC-23, which are structurally not executable because no `confirmPassword` field exists. Raw Actual-vs-Expected output is in [`reports/test_execution_log.md`](reports/test_execution_log.md) (readable summary) and [`reports/test_execution_raw.txt`](reports/test_execution_raw.txt) (the unedited console transcript, containing both pass 1 and a "PASS 2" section); screenshots are in [`reports/screenshots/`](reports/screenshots/).

**How the columns are scored.** The Passed / Failed / Conditional split reads the "Actual matches designed Expected?" column of the execution log directly: `Yes` is counted as Passed, `No` or `Partial` as Failed. A row is counted as **Conditional** when its designed expected result depends on an unresolved Open Question, or when the outcome differs by layer (the client-side check and the backend give opposite results, for example the FR-01 password rows where the client regex rejects but the backend accepts). Conditional rows are recorded factually in the execution log and are not forced into a pass or fail. Many of them do surface the confirmed defects, but the authoritative defect count is the separate **Bugs** column, which comes from the student-authored [`reports/Bug_Report.md`](reports/Bug_Report.md).

| Feature | Atomic REQs | Equivalence classes | Domain TCs | BVA TCs | Total designed | Executed | Passed | Failed | Conditional | Not yet executed | Bugs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| FR-01 Account registration | 18 | 34 | 24 | 7 | 31 | 29 | 3 | 12 | 14 | 2 | 2 |
| FR-06 Product detail view | 22 | 43 | 13 | 4 ¹ | 17 ¹ | 17 | 3 | 1 | 13 | 0 | 4 |
| FR-11 Order history view | 22 | 21 | 8 | 3 | 11 | 11 | 6 | 1 | 4 | 0 | 1 |
| FR-13 Dashboard | 17 | 22 | 8 | 6 | 14 | 14 | 5 | 4 | 5 | 0 | 2 |
| **Total** | **79** | **120** | **53** | **20** | **73** | **71** | **17** | **18** | **36** | **2** | **9** |

¹ FR-06's BVA-01 deliberately restates Phase-3 TC-04 (documented in the artifact's section 3: 13 + 3 = 16 distinct executions, not 17). The two structurally non-executable FR-01 cases (TC-17, TC-23) are the only rows not executed; the absence of a `confirmPassword` field is itself the recorded observation.

- **Number of features:** 4
- **Number of test cases designed:** 73 (53 domain + 20 boundary)
- **Executed / passed / failed / not yet executed:** 71 executed, 17 passed, 18 failed, 2 not executable (36 conditional rows recorded but not scored as pass or fail; see the note above)
- **Number of bugs:** 9 confirmed defects from 10 candidate observations (BUG-01 merges two candidates); see [`reports/Bug_Report.md`](reports/Bug_Report.md)
- **Demo videos (Agent Skills):** [YouTube link to be pasted before submission]

## Self-assessment table

| No. | Criteria | Grade | Self-Assessed Grade |
|---|---|---|---|
| 1 | Feature A (Domain + Boundary) | 25 | 25 |
| 2 | Feature B (Domain + Boundary) | 25 | 25 |
| 3 | Feature C (Domain + Boundary) | 25 | 25 |
| 4 | Feature D (Mobile, Domain + Boundary) | 15 | 15 |
| 5 | Agent Skills | 10 | 10 |
| | **Total** | **100** | **100** |
