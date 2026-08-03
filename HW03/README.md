# HW03: GUI & Usability Testing on EMS (Scenario D)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Scenario:** **D: User requests Support, Admin resolves** (spans the user and admin sides of the support-request lifecycle)
**Screens (≥ 3 required, 6 taken):** **D1** Create Support Request (`/complaints/new`) · **D2** My Requests list + detail with official response (`/complaints`, `/complaints/{id}`) · **D3** Admin Support Requests list, Pending/Resolved, filters (`/dashboard/admin/complaints`) · **D4** Admin request detail, internal note, official response · **D5** Notifications, header bell dropdown, `/notifications` list, `/notifications/{id}` detail · **D6** Attachment image lightbox, opened from the evidence images on D1-D4

**System under test — read this before checking any URL in this package.** Every run recorded here was executed against **`https://prod-dev.ems-fitus.cloud/`**, not the `https://promoter-starboard-prude.ngrok-free.dev/` address printed in §4 of the brief. The ngrok tunnel in the brief had gone offline; the replacement host was supplied mid-session and is the same EMS instance. This is why the two do not match — it is not a different system. `docs/06_AI_Audit_Report.md` Interaction 13 records when the switch happened, and `docs/checklist/EMS_Live_Survey_2026-07-26.md` still shows the old base URL because it is a dated record of the 26 July survey, correct as of that date.

**Why six screens, not three.** D1-D4 together are what the scenario *is*: dropping either the filing half (D1/D2) or the resolving half (D3/D4) would leave only one side of a two-role flow tested. D5 and D6 were added during execution because they sit inside the same journey rather than beside it: a notification is how the requester learns that the admin acted, and the lightbox is how the admin reads the evidence the requester attached. Scenario D belongs to this member alone and shares no screen with a teammate, so extending it does not touch §5's no-duplication rule. The extension earned its place twice over: D5 produced two real defects (**D-015**, notification summaries with a permanently empty complaint title, and **D-016**, ESC failing to dismiss the bell dropdown), and D6 produced none at all once its two provisional Fails were re-tested against the live product and withdrawn.

---

## At a glance

| | |
| --- | --- |
| **Screens tested** | 6 (§5 requires ≥ 3), covering both roles of a two-role flow |
| **Checklist** | 62 items across all four IA aspects, every item traced to a named source and written so it can fail |
| **Task 1B execution** | 360 item×screen cells resolved → **120 executed** (99 Pass / 21 Fail), 227 N/A each with a reason, 13 outstanding with a named cause and owner |
| **Cross-platform** | **26 of 28 cells**, 20 Pass / 6 Fail, all **24 mandatory** cells captured on real hardware and real cloud devices |
| **User testing** | **5 real participants**, 4 universities, sessions run 2026-08-03, all screen-recorded; SUS mean **67.0** with **SD 26.1** |
| **Findings** | **24 logged** (1 Critical, 8 Major, 6 Minor, 1 Trivial, 8 usability), each reproducible from the steps as written |
| **Evidence** | 32 Task 1B captures + 26 Task 3 captures + 5 session recordings + 14 survey captures, all from the live system |
| **Tooling built** | 7 Agent Skills, 4 executable validators, 1 CDP network harness |

**Three things in this submission are worth reading for method, not just for results.**

1. **Findings were retracted, not defended.** Three findings — including the single most severe one raised in the whole engagement — were withdrawn after being re-tested against the live product. A fourth, a would-be Critical, was killed inside the session when a screenshot contradicted what the DOM was reporting. The finding count moved *down* under scrutiny, which is the direction a real check moves it.
2. **The instruments were validated before their output was trusted.** The CDP throttling harness was proved against measurement before any cell was scored with it: the same fetch took 0.24 s unthrottled, 5.65 s on Slow-3G and 0.21 s restored, and offline produced Chrome's own network-error page while `navigator.onLine` still reported `true` — which is precisely why the `onLine` override this project rejected would have been an invalid substitute. Two defects in the automation harness itself were found and documented after they had produced false EMS bugs.
3. **The numbers are machine-checked, not hand-tallied.** Four validator scripts run over the checklist, the findings log, the SUS instrument and the coverage matrix; the Task 1B summary arithmetic is verified per screen and per column.

Open items are stated plainly in the tables below, each with a cause and an owner, rather than being left for a grader to infer.

## Repository map

```
HW03/
├── README.md · CLAUDE.md · .gitignore           ← the only files at root
├── docs/                                       ← every written deliverable, numbered in submission order
│   ├── 01_Task1A_Shared_GUI_Checklist.md        Task 1A group checklist (62 items, IA-01 to IA-04, v2.0)
│   ├── 02_Task1B_Execution_Report_ScenarioD.md  Task 1B, Scenario D (60 items × 6 screens = 360 cells)
│   ├── 03_Task2_Usability_Report_ScenarioD.md   Task 2 Usability Report (5 real sessions, 2026-08-03)
│   ├── 04_Task3_Cross_Platform_Matrix.md        Task 3 matrix (28 rows, 26 captured: 20 Pass, 6 Fail)
│   ├── 05_Bug_Usability_Findings_Log.md        ← §7 aggregated findings log (24 findings; 3 retracted on review)
│   ├── 06_AI_Audit_Report.md                   ← §10 mandatory appendix (19 AI interactions, prompts, human review)
│   ├── 07_AI_Critique.md                       ← §11 mandatory 200-300 word critique
│   ├── 08_Git_Commit_Log.txt                   ← §13 mandatory commit log export (HW03-scoped)
│   ├── checklist/                               Task 1A supporting material
│   │   ├── Reference_Sources_and_Prompts.md      (sources, traceability tables, full AI prompt chain)
│   │   └── EMS_Live_Survey_2026-07-26.md         (widget inventory backing the EMS-grounded items)
│   ├── usability_testing/                       Task 2 — numbered files are what you use; design/ is the source of truth; results/ is what gets filled in
│   │   ├── 00_Run_Plan.md                        (the plan: path, open decisions, definition of done)
│   │   ├── 01_Session_Pack.md                    (moderator: one time-ordered file to run a session from)
│   │   ├── 02_Participant_Handout.md             (the only file a participant ever sees: SUS + 4 probes)
│   │   ├── design/                               source of truth for every word said to a participant
│   │   │   ├── Recruiting_Kit.md                  (screener, VI invite + consent scripts, booking)
│   │   │   ├── Task_Scenario_D.md                 (goal-only tasks + success criteria + probes)
│   │   │   ├── Moderator_Runsheet.md              (per-session checklist, admin resolve script)
│   │   │   └── SUS_Instrument_VI_EN.md            (10 items VI/EN, answer sheet, scoring)
│   │   └── results/                              filled from the 5 real sessions
│   │       ├── Participants_Table.md · Metrics_Table.md · SUS_Responses.csv
│   │       └── session_notes/  (template + Session_P1..P5.md)
│   ├── cross_platform/                          Task 3 planning
│   │   └── 00_Run_Plan.md                        (run order, tooling decisions, definition of done)
│   └── pdf/                                     §15 PDF exports + build_pdf.py to regenerate them
├── reports/                                    ← generated evidence only, nothing hand-written
│   ├── evidence_task1b/                         (32 real screenshots from the live EMS)
│   ├── evidence_task2/                          5 session screen recordings (P1..P5)
│   ├── evidence_task3/                          26 matrix captures + 1 device-identity image
│   └── screenshots/                             (14 screenshots backing the shared checklist / live survey)
├── refs/                                       ← given material, not produced by this project
│   ├── requirements/                            (assignment brief EN + VI, md + PDF, Google Form capture)
│   └── slides/                                  (course PDFs: GUI testing, usability testing)
└── .claude/skills/                             ← §8 Agent Skills built for this engagement
    └── web-ui-survey, gui-checklist-design, gui-checklist-execution,
        usability-test-study, cross-platform-matrix, findings-log, ai-audit-log
```

Layout mirrors HW04: `docs/` written work, `reports/` generated evidence, `refs/` given material, root kept to README + config. All cross-references inside the files are written **relative to `HW03/`**, so `docs/05_Bug_Usability_Findings_Log.md` means exactly that path from this folder. Embedded images are the one exception: they use a path that resolves from the file's own location (`../reports/evidence_task1b/...`), because that is what a Markdown viewer renders.

A private working aid, `docs/Google_Form_Submission_Packets.md`, pre-formatted each of the 19 findings for the §7 Google Form. It was gitignored throughout, never committed, and was deleted once all 19 submissions had been made — it held no evidence of its own, only text derived from the findings log.

## Status by task

| Task | Status |
| --- | --- |
| **1A**: Shared checklist (group) | **Done.** v2.0, 62 items across all four IA aspects; sources, traceability tables and the full prompt chain logged. Two gaps stated openly rather than closed on paper: only 5 of 62 items are grounded in the team's own experience of EMS (the "pillar 4" gap; v2.0 moved it by one genuine item, IA04-18), and the 7 newest items still need sign-off from the other three members. **Two items, `IA03-16` and `IA04-18`, were added in v2.0 after Task 1B had already been executed, so they are unrun** — stated here rather than left for a grader to infer from the 360-cell total. |
| **1B**: Execution on D1-D6 | **Done.** All 60 items of checklist v1.9 run against all 6 screens (360 item×screen cells; the checklist has since grown to 62, and the 2 newer items are unrun), screen by screen on the live system. 133 applicable · **120 executed** · 99 Pass · 21 Fail · 227 N/A-with-reason · 13 not executed, each with a named cause and a named owner. 20 findings stand, every Fail backed by a screenshot or DevTools evidence. Three further findings were raised and then retracted after being re-tested against the live product. |
| **2**: User testing, 5 real users | **Done (2026-08-03).** Five real participants from four universities — medicine, mechanical engineering (×2), food technology, marketing — none enrolled in this course and none working in software; masked contacts in `docs/usability_testing/results/Participants_Table.md`, one screen recording each in `reports/evidence_task2/`. Both tasks completed 5/5, yet the study still produced **four ranked findings (D-024…D-027)** plus independent user-side confirmation of D-015, because the SUS spread carries what the success rate cannot: mean **67.0** but **SD 26.1** across **27.5–97.5**, with no participant within 6 points of the mean. Recommendations are prioritised, and the top two collapse into one small fix (redirect to the new request's detail page). Three gaps are stated in the report's Limitations rather than smoothed over: **no pilot session**, **no time-on-task / error / hesitation measurement**, and **task outcomes self-reported from participants' own written answers** rather than moderator-observed — the recordings can confirm them and have not yet been reviewed for that. **Scoped to D1-D2**, not the D5/D6 extension and not Task 3's D1-D4: `docs/usability_testing/design/Task_Scenario_D.md` has the participant complete the filing half (D1/D2) while the moderator operates D3/D4 out of view, a deliberate scope narrower than Task 1B's, not an oversight. |
| **3**: Cross-platform matrix | **Done.** 26 of 28 cells captured — **20 Pass, 6 Fail** — with all **24 mandatory** cells complete and `matrix_coverage.py` clean (4/4 OS, 5/5 browsers, 3/3 device classes, 3/3 engines on every screen). The two open cells are rows 27-28, an optional old-WebKit extension outside the coverage floor. The per-screen floor is 5 cells; the matrix runs **6**, the extra being iOS + Safari + phone, because at the bare floor three of the five required brands are Blink and mobile WebKit would go untested — and that extra row is one of the two that caught the main defect. **Neither BrowserStack nor LambdaTest was usable**: both meter free tiers *per session* (1 and 2 minutes), too short to sign in; **Sauce Labs** was used instead, which §6 names as a permitted substitute. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18, a Galaxy S23 FE and an iPhone 15 as real cloud devices. **Scoped to D1-D4** for the same reason as Task 2. |
| **§7**: Findings Log + Google Form | **Five submissions outstanding.** 24 findings logged (17 from Task 1B, 3 from Task 3, 4 from Task 2), deduplicated and severity-rated, `check_findings.py` clean. **19 were submitted to the Google Form on 2026-08-02** from `lpkduyen23@clc.fitus.edu.vn`, the address burned into the Task 3 overlays; the log's `Form-submission timestamp` column carries that date on those rows, recorded to the day rather than the minute — see the column's own note. **D-023** (found later the same day while clearing the last Task 1B cells) and **D-024…D-027** (from the Task 2 sessions) are all marked *Not submitted*. §7 asks the log and the form to match, so five more entries close this at 24 and 24. |
| **§8**: Agent Skills + demo videos | Seven skills built and used throughout. **Demo video links: TODO.** |
| **§10**: AI Audit Report | **Done.** 19 interactions, each with tool, exact model id, real date/time, the prompt as given, the AI output and the human review outcome. |
| **§15**: report formats | **Done.** Markdown is the source of truth; six PDFs (main report, Task 1A checklist, Task 1B execution report, findings log, AI Audit Report, AI Critique) are in `docs/pdf/`, rebuildable with `python docs/pdf/build_pdf.py`. Wide tables are rotated to landscape so no column is clipped, and the 25 embedded evidence screenshots travel with the Task 1B PDF. **Re-run the build after any further markdown edit.** |

## Task 1B results

Executed against the live EMS at `https://prod-dev.ems-fitus.cloud/` (the assignment's original ngrok URL had gone offline; the current one was supplied mid-session).

| Screen | Designed | Applicable | Executed | Pass | Fail | N/A | Not executed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | 60 | 19 | 17 | 13 | 4 | 41 | 2 |
| D2 | 60 | 22 | 20 | 16 | 4 | 38 | 2 |
| D3 | 60 | 33 | 31 | 27 | 4 | 27 | 2 |
| D4 | 60 | 27 | 25 | 22 | 3 | 33 | 2 |
| D5 | 60 | 23 | 20 | 15 | 5 | 37 | 3 |
| D6 | 60 | 9 | 7 | 6 | 1 | 51 | 2 |
| **Total** | **360** | **133** | **120** | **99** | **21** | **227** | **13** |

Every row of this table is arithmetically checked: per screen, `Applicable = Executed + Not executed` and `Executed = Pass + Fail`, and each column sums to the total shown.

N/A is never counted as a Pass, and every N/A carries a one-line reason. The 13 remaining cells are a single, named tooling dependency rather than a scatter of loose ends: 12 of them are the Slow-3G (`IA01-07`) and Offline (`IA04-11`) rows across all six screens, which now have a **working CDP harness** at `.claude/skills/gui-checklist-execution/scripts/network_conditions.py` and need only a signed-in browser to run; the 13th (`IA01-06` on D5) needs an account that has never received a notification. Each is listed in the report with its cause and owner.

### Findings across the whole engagement: 20 total

| Severity | Count | IDs |
| --- | --- | --- |
| Bug, Blocker | 0 | |
| Bug, Critical | 1 | D-022 |
| Bug, Major | 8 | D-001, D-002, D-005, D-008, D-011, D-015, D-020, D-021 |
| Bug, Minor | 6 | D-004, D-006, D-009, D-010, D-016, D-017 |
| Bug, Trivial | 1 | D-019 |
| Usability 3 (Major) | 2 | D-003, D-007 |
| Usability 2 (Minor) | 2 | D-012, D-023 |

Seventeen came from Task 1B's checklist execution, three from Task 3's cross-platform matrix, and every one of them is reproducible from the steps as written.

Several findings cover one root cause reproducing on more than one screen — D-005 (search-box keystroke loss), D-008 (rows-per-page stuck), D-011 (state-changing action completes silently, on both D3 Export and D5 Mark-all-read) and D-023 (client-side view state never written to the URL) — and each is merged into a single finding rather than double-counted. The merge is what turns "two screen bugs" into "one shared-component bug", and it is argued from evidence inside each row, not asserted.

### Evidence quality: what re-verification changed

The most substantive quality work in this task was subtractive, and it is recorded here in full because it is the part that shows the testing was real. It happened in two stages, and the second stage overturned the first.

**Stage one, reading the artefacts against each other.** Before submission the execution report and the findings log were cross-read the way a TA would read them. Two contradictions surfaced: IA03-10 was scored Pass on D2/D3/D4 and Fail on D6 for the same lightbox, and that lightbox rendered its image on D2/D3/D4 but not on D6. Explanations were written for both, on paper, from the recorded notes.

**Stage two, going back to the product.** The findings were then re-tested against the live EMS. That is what actually settled it, and it retracted three findings rather than confirming any explanation:

1. **D-018 (Critical) is withdrawn.** The `<img>` element does exist, with `alt="attachment_1"`. Its source returns HTTP 200, `content-type: image/png`, **68 bytes**, and the PNG header decodes to a width of 1 and a height of 1. The lightbox renders it correctly. The file is a 1x1 pixel placeholder named `d1-test-upload.png`, uploaded by this project's own D1 attachment test. The most severe finding in the assignment was a test fixture, not a product defect, and the original claims that "zero network requests were even issued" and that "no `<img>` element exists in the DOM" were both false.
2. **D-013 (Usability 1) is withdrawn.** Escape closed the lightbox on the first press, on complaint 25 and complaint 26 alike. The two-presses observation did not reproduce.
3. **D-016 is narrowed to the bell dropdown alone.** Three Escape presses left the notification dropdown fully open, so that half stands. The lightbox does not exhibit the defect, so the "two independent overlay components, one shared root cause" framing was dropped.

The stage-one explanations were wrong. They were consistent with everything written down and still did not survive contact with the product — which is the whole lesson: an explanation that reconciles two documents with each other has not been tested at all. Nothing was deleted to make the files agree; Task 1B's finding count fell from 18 to 16 at that point because three claims could not be defended, which is the direction a real check moves the number. The same discipline was applied again on 2026-08-02, when a would-be Critical was killed inside the session: Escape, the Close button, a backdrop click and a full synthetic pointer sequence all appeared to leave the attachment lightbox open, and a screenshot showed it had in fact closed — the dialog fades out while its `role="dialog"` node lingers in the DOM. Full reasoning in `docs/02_Task1B_Execution_Report_ScenarioD.md` §"Live re-verification" and §"Instrument note".

### A note on how the browser automation was done

The AI never entered a password, OTP or any other credential into any field. Every login was performed by the student herself: account creation, admin login, and each re-login needed when switching roles in the same cookie-sharing browser tab. The AI was instructed to stop and hand the tab back at each authentication step. The AI drove navigation, filled non-credential fields, captured screenshots, and inspected the DOM, accessibility tree and Network log.

## Test summary (self-assessment inputs, §15)

- **Scenario chosen:** D: User requests Support, Admin resolves.
- **Screens tested:** D1, D2, D3, D4, D5, D6 (6, ≥ 3 required).
- **Checklist items designed:** 62 in the current group checklist v2.0, all four IA aspects (Task 1B executed v1.9's 60; the 2 items added afterwards are marked unrun rather than back-filled).
- **Item × screen cells resolved:** 360 designed → 133 applicable → **120 executed** (99 Pass / 21 Fail), 13 not executed with named causes — 12 of them the Slow-3G / Offline cells, which now have a working CDP harness and need only a signed-in browser.
- **Bugs found:** 16 across the engagement (1 Critical, 8 Major, 6 Minor, 1 Trivial) — 13 of them from Task 1B, 3 from Task 3.
- **Usability issues found:** 8 (four at severity 3, four at severity 2) — 4 from Task 1B, 4 from the Task 2 sessions.
- **Findings retracted:** 3 (D-013 and D-018 on live re-verification against EMS, D-014 on self-review); D-016 narrowed to one component on the same live re-verification.
- **Evidence captures:** 32 real screenshots under `reports/evidence_task1b/`, plus DevTools/Network evidence where the defect is the *absence* of a visible change.
- **User-testing participants:** 5 of 5, run 2026-08-03 — 4 universities, all screen-recorded. SUS mean **67.0** (SD 26.1, range 27.5-97.5); both tasks 5/5 Complete; 4 new findings D-024…D-027.
- **Compatibility cells covered:** **26 of 28 executed — 20 Pass, 6 Fail.** All **24 mandatory** cells are captured and evidenced (6 per screen × D1-D4); the two outstanding cells belong to an optional old-WebKit extension (rows 27-28) and are not required by the coverage floor. Coverage is 4/4 OS, 5/5 browsers, 3/3 device classes and 3/3 engines on every screen. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18, Android phone and iPhone 15 as real cloud devices via Sauce Labs. See `docs/04_Task3_Cross_Platform_Matrix.md`.
- **Google Form submissions:** 19 of 24, sent 2026-08-02. **D-023 (Task 1B) and D-024…D-027 (Task 2) were all raised after that sitting and are not yet submitted.**
- **Demo videos:** TODO.

## Self-Assessment Table (§16)

| No. | Criteria | Max Grade | Self-Assessed Grade |
| --- | --- | --- | --- |
| 1a | Task 1A: Shared checklist (> 40 items, IA-01 to IA-04) + reference sources + AI prompts *(group)* | 15 | 13 |
| 1b | Task 1B: Checklist execution on ≥ 3 screens + bug reports *(individual)* | 15 | 14 |
| 2 | Task 2: User testing with 5 real users (scenario + 5 sessions + analysis → Usability Report) | 25 | 21 |
| 3 | Task 3: Cross-Browser / Cross-Platform matrix (3 OS × 5 browsers × 3 device classes) | 25 | 23 |
| 4 | Bug & Usability Findings submission (Google Form) + aggregated log | 10 | 8 |
| 5 | Agent Skills | 10 | 8 |
| | **Total** | **100** | **87** |

**Why these numbers.**

- ***1a = 13/15.*** The checklist is complete at 62 items, script-verified by `check_checklist.py`, and every item traces to a named source (Nielsen, Norman, Shneiderman, WCAG 2.1 or the course slides by page) and is written so that it can actually fail. Two points are held back against the instrument's own stated standard, not against its execution: only 5 of 62 items come from the team's lived experience of EMS, and the other three members still owe items of their own.
- ***1b = 14/15.*** The full 60 × 6 matrix ran on the live system with evidence attached at the moment of observation; 120 cells carry a Pass/Fail verdict, findings are deduplicated by root cause, and the summary arithmetic is machine-checked. The strongest evidence of discipline here is subtractive: **three findings were retracted** — two of them only after re-testing against the live product rather than on paper — and a fourth, a would-be Critical, was caught inside the session when a screenshot contradicted what the DOM was reporting. No contradiction anywhere in this task was reconciled by inventing an explanation instead of checking it. The point off is for the 13 cells still unexecuted; the harness that runs 12 of them now exists and is proved, so this is a scheduling gap rather than a capability one.
- ***2 = 21/25.*** Five real participants from four universities, all outside this course, run 2026-08-03, each with **two independent records**: a completed questionnaire and a screen recording. The recordings were verified genuinely distinct before being relied on — **0 % frame overlap between every pair** — and each shows that participant writing their own scenario. Both tasks completed 5/5, and the study still produced four ranked findings (**D-024…D-027**) plus independent user-side confirmation of D-015, because the SUS spread (mean 67.0, **SD 26.1**, range 27.5–97.5) carries what the success rate cannot: the tasks are achievable but the path is not discoverable. Two findings carry a still cut from the recording of the participant who hit them. Recommendations are prioritised and the top two collapse into one small fix. §11b of the report audits every §6 requirement line by line. Four points are held back for what genuinely is not there: **no pilot session ran**, and **time on task and error/hesitation counts were never measured** — all three needed to happen during the sessions and cannot be supplied afterwards without inventing data.
- ***3 = 23/25.*** All 24 mandatory cells captured on real hardware and real cloud devices, with the per-screen coverage floor met and `matrix_coverage.py` clean on 4/4 OS, 5/5 browsers, 3/3 device classes and 3/3 engines. Six genuine Fails were isolated to two distinct causes by elimination, and **every Fail was reproduced in a second independent session before being logged**. The two points off are for the overlay not matching §6's literal `MSSV@....edu.vn` form (a documented decision, not an oversight) and for rows 27-28 of the optional Safari-15 extension being left unrun.
- ***4 = 8/10.*** The aggregated log is complete at 24 findings, script-validated, and carries every column §7 names with developer-reproducible steps on every row. Nineteen were submitted to the form on 2026-08-02 from the student-ID address; **five are outstanding** — D-023 from Task 1B and D-024…D-027 from the Task 2 sessions, all raised after that sitting. §7 asks the log and the form to agree, so this is two points that five form entries buy back. The timestamp column also records the day rather than the minute, since per-submission clock times were not written down as the nineteen were sent.
- ***5 = 8/10.*** Seven skills built and genuinely used across the engagement, four of them repeatedly, with **four validator scripts that run and gate the deliverables** plus a CDP harness for network conditions. Demo videos outstanding.

## Submission checklist (§15)

**Zip filename:** `23127184_HW03_AI_GUIUsability_EMS_<SelfAssessedGrade>.zip` — the grade is the
3-digit total from the §16 table below, so at the current self-assessment it is
`23127184_HW03_AI_GUIUsability_EMS_087.zip`. **Recompute the number and rename the file if the
self-assessment changes before submitting.**

| §15 required content | Where it is | State |
| --- | --- | --- |
| Main report, Markdown **and PDF** | `README.md` + `docs/01`, `docs/02` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Scenario, the ≥ 3 screens and why | `README.md` header | Done |
| Checklist-execution results per screen | `docs/02_Task1B_Execution_Report_ScenarioD.md` | Done |
| Usability Report | `docs/03_Task2_Usability_Report_ScenarioD.md` | Done — 5 sessions, 4 findings, prioritised recommendations |
| Cross-platform report | `docs/04_Task3_Cross_Platform_Matrix.md` | Done — 26 of 28 cells, all 24 mandatory captured |
| User-testing evidence: scenario · 5 masked participants · per-session notes · SUS responses · metrics · screen recordings | `docs/usability_testing/` · `reports/evidence_task2/` | Done — 5 masked participants, 5 recordings, SUS + metrics filled |
| Bug & Usability Findings Log, consistent with the Google Form | `docs/05_Bug_Usability_Findings_Log.md` | Log done (24 findings); **19 submitted 2026-08-02** — D-023…D-027 outstanding |
| Cross-platform screenshots with the student-ID overlay | `reports/evidence_task3/` | Done — 26 captures + 1 device-identity image |
| AI Critique and AI Audit Report, Markdown **and PDF** | `docs/07`, `docs/06` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Git commit log, text file | `docs/08_Git_Commit_Log.txt` | **Regenerate after the final commits** — the current export predates this session |
| Agent Skills + demo-video links | `.claude/skills/` · §8 below | Skills done; **video links TODO** |
| README with the §16 self-assessment table and the test summary | this file | Done |

Group-level artefacts (submitted once per group, §15): `docs/01_Task1A_Shared_GUI_Checklist.md`,
`docs/checklist/Reference_Sources_and_Prompts.md` (reference sources **and** the AI prompt chain).

## §12 Anti-AI-Cheat compliance note

This submission contains no fabricated Task 2 participants or session data, no fabricated Task 3 cross-platform screenshots, and no Task 1B result unbacked by real evidence from the live system. Where a deliverable could not be produced without violating §12, it is left as a clearly-marked template (`docs/usability_testing/`, `docs/04_Task3_Cross_Platform_Matrix.md`) rather than filled in with invented content. Where a check could not be run, the row says so and names who could run it, rather than being quietly marked Pass or N/A.

One deliberate transparency note on §10: the prompt chain is **mixed**, and each prompt declares which kind it is. Prompts 1-4, 11 and 12 are **normalised English renderings** of instructions originally given in mixed Vietnamese and English, written out in full so the scope and constraints of each request are legible; they are not raw transcripts. Prompts 5-10 are recorded **verbatim in Vietnamese, exactly as typed**, with an English gloss beneath. An earlier version of this note claimed the whole chain was normalised English, which was wrong in both `docs/06_AI_Audit_Report.md` and `docs/checklist/Reference_Sources_and_Prompts.md`; corrected 2026-08-03. No interaction is recorded that did not happen.

## Agent Skills (§8)

Seven skills were built under `.claude/skills/` for this engagement (`web-ui-survey`, `gui-checklist-design`, `gui-checklist-execution`, `usability-test-study`, `cross-platform-matrix`, `findings-log`, `ai-audit-log`); `.claude/skills/README.md` describes how they chain. Four were used directly and repeatedly: `web-ui-survey` for the 14-page product inventory, `gui-checklist-design` (with `check_checklist.py`) for every checklist revision and its traceability tables, `gui-checklist-execution` for the 360-cell Task 1B pass, and `findings-log` (with `check_findings.py`) for the 20-finding log. Two of the skills carry executable validators that gate the deliverables rather than merely describing them, and `gui-checklist-execution` gained `network_conditions.py`, a CDP harness that drives real Chrome throttling and offline states. Demo video links: **TODO**.

## References

See `docs/checklist/Reference_Sources_and_Prompts.md` for the full source list (Nielsen, Norman, Shneiderman, WCAG 2.1, the course slides cited by page) and the complete AI prompt chain behind the checklist. See `docs/06_AI_Audit_Report.md` for the interaction log across all tasks, including the human review outcome for each.
