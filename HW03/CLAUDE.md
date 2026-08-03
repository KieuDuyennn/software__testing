# HW03 — GUI & Usability Testing on EMS (Scenario D)

Context file for future sessions. Read this before touching anything; it exists so a new session
does not have to re-derive the layout, the conventions or the rules by reading twenty files.

**Student:** Lê Phạm Kiều Duyên · 23127184 · Group 09 · branch `duyen/hw3`
**System under test:** EMS, `https://prod-dev.ems-fitus.cloud/` — the hosted instance moves; verify
the URL is live before relying on it, never assume from memory.
**Scenario D:** user files a support request, admin resolves it. Screens D1 `/complaints/new` ·
D2 `/complaints`, `/complaints/{id}` · D3 `/dashboard/admin/complaints` · D4 admin detail ·
D5 notifications · D6 attachment lightbox.

## Layout

```
docs/      every written deliverable. 01_..08_ are numbered in submission order.
           docs/checklist/          Task 1A supporting material
           docs/usability_testing/  Task 2 instruments  (00_Run_Plan.md is the entry point)
           docs/cross_platform/     Task 3 planning     (00_Run_Plan.md is the entry point)
           docs/pdf/                generated PDF exports (§15); markdown is the source of truth
reports/   generated evidence only, never hand-written prose
           evidence_task1b/ (32 real captures) · evidence_task2/ · evidence_task3/ · screenshots/ (14)
refs/      given material: refs/requirements/ (the brief, EN+VI) · refs/slides/ (course PDFs)
.claude/skills/   the seven Agent Skills built for this engagement (§8)
```

Root holds only `README.md`, this file and `.gitignore`. Keep it that way — the flat root this
folder used to have was the specific thing that got called messy.

## Conventions that are load-bearing

- **Every path reference inside a markdown file is written relative to `HW03/`** — e.g.
  `docs/05_Bug_Usability_Findings_Log.md`, `reports/evidence_task1b/D1_resting_state.jpg`. Never `../`, never a
  bare filename. A path written any other way is a bug; fix it rather than matching it.
- **Two files are deliberately exempt from path rewriting.** `docs/08_Git_Commit_Log.txt` is a
  historical export. Verbatim prompt blocks inside code fences in `docs/06_AI_Audit_Report.md` and
  `docs/checklist/Reference_Sources_and_Prompts.md` still name pre-reorganisation paths on purpose;
  a "Path note" at the top of the audit report gives the mapping. Editing those blocks falsifies
  the record — do not "fix" them.
- **Finding IDs are `D-0NN`, allocated when a finding is written, never in advance.** D-001…D-022
  are used (D-020…D-022 came from Task 3). **D-013, D-014 and D-018 are retired** (withdrawn on live re-verification) and must
  never be reused. **D-024…D-027 came from the Task 2 sessions on 2026-08-03; the next free ID is D-028.** 19 of the 24 live findings were submitted to the §7 Google Form on 2026-08-02; **D-023 and D-024…D-027 still need submitting.**
- Severity: bugs use Blocker/Critical/Major/Minor/Trivial; usability findings use the Nielsen 0-4
  scale written as `Usability 0`…`Usability 4`.
- Result cells are bare `Pass` / `Fail` / `N/A` / `Not executed` — no hedged wording. Every `N/A`
  carries a one-line reason; every not-executed cell names a cause and an owner.

## Hard rules — these are graded, not stylistic

- **Never fabricate study data.** No invented participant, session, quote, timing, SUS answer,
  cross-platform screenshot or Pass/Fail. §12 of the brief makes this grounds for voiding the task,
  the TA may phone 2 of the 5 Task 2 participants to verify them, and a fabricated result also
  poisons every conclusion drawn from it. An AI may design, score, cluster and draft; it may not be
  a participant or supply session data. Where a deliverable cannot be produced honestly, it stays a
  clearly-marked empty template — that is why several tables here read TBD.
- **The AI never enters a credential.** Every login, password and OTP is typed by the student
  herself, including each role switch. Browser automation hands the tab back at every auth step.
- **Claims get checked against the product, not against other documents.** Three findings were
  retracted in this project only after re-testing against the live EMS; explanations that merely
  made two files agree turned out to be wrong. Prefer "verify before relying on this" to a
  confident reconciliation on paper.
- §10 requires the AI Audit Report to declare which artefacts are AI-generated. Log new AI-produced
  deliverables in `docs/06_AI_Audit_Report.md`.

## Validator commands (run from `HW03/`)

```bash
python .claude/skills/findings-log/scripts/check_findings.py docs/05_Bug_Usability_Findings_Log.md --evidence-root reports/evidence_task1b --evidence-root reports/evidence_task3
python .claude/skills/gui-checklist-design/scripts/check_checklist.py docs/01_Task1A_Shared_GUI_Checklist.md --evidence-root . --expect 62
python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/results/SUS_Responses.csv --instrument sus --markdown
python .claude/skills/cross-platform-matrix/scripts/matrix_coverage.py docs/04_Task3_Cross_Platform_Matrix.md --evidence-root reports/evidence_task3
```

## State — update this section when it changes

| Task | Marks | State |
| --- | --- | --- |
| 1A shared checklist | 15 | Done. v2.0, 62 items. Open: only 5/62 from the team's own EMS experience (v2.0 added 1 genuine pillar-4 item, IA04-18; other 3 members still owe theirs); IA03-16 and IA04-18 postdate Task 1B so are unrun. |
| 1B execution D1-D6 | 15 | Done. 360 cells, **120 executed** (99 Pass / 21 Fail), 227 N/A, **13 not executed**: `IA01-07` ×6 (Slow-3G) and `IA04-11` ×6 (Offline), which now have a working CDP harness at `.claude/skills/gui-checklist-execution/scripts/network_conditions.py` and need only a signed-in browser; plus `IA01-06` on D5, which needs an account with zero notifications. 20 findings, 3 retracted on live re-verification. Read the Method section's *Instrument note* before any keyboard or coordinate-click test. |
| 2 user testing | 25 | **Done (2026-08-03).** 5 real participants, 4 universities, one screen recording each in `reports/evidence_task2/`. SUS mean 67.0, **SD 26.1**, range 27.5-97.5. Both tasks 5/5 Complete. 4 findings D-024…D-027 + user-side confirmation of D-015. Open: **no pilot ran**; time-on-task/errors/hesitations **not measured**; task outcomes are **self-reported** from participants' own written answers, not yet confirmed against the recordings. Folder is `00_Run_Plan` (plan) · `01_Session_Pack` (run a session) · `02_Participant_Handout` (the only file a participant sees) · `design/` (source of truth for wording) · `results/` (data). |
| 3 cross-platform | 25 | Done (2026-08-02). 26/28 cells — 20 Pass, 6 Fail; all 24 mandatory cells captured. Open: rows 27-28 (optional Safari-15 extension). D-020/D-021/D-022 all reproduced in a second session. |
| §7 form + log | 10 | Log complete and validated (**24 findings**). **19 submitted to the Google Form on 2026-08-02** from `lpkduyen23@clc.fitus.edu.vn`; **D-023 and D-024…D-027 outstanding — five entries.** Timestamp column is date-level, not minute-level. |
| §8 skills | 10 | Seven skills built and used; demo video links outstanding. |
| §15 formats | — | Markdown complete; PDFs in `docs/pdf/`. |

The README's §16 self-assessment table must stay consistent with this. When a task moves, update
both.
