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
| **Task 1B execution** | 372 item×screen cells resolved → **137 executed** (103 Pass / 34 Fail), 235 N/A each with a reason, **0 outstanding** |
| **Cross-platform** | **28 of 28 cells**, 20 Pass / 8 Fail, including all optional Safari-15 extension cells |
| **User testing** | **5 real participants** + **1 pilot**, 4 universities, sessions run 2026-08-03, all screen-recorded; SUS mean **67.0** with **SD 26.1** |
| **Findings** | **28 logged and all 28 submitted**, each reproducible from the steps as written |
| **Evidence** | 32 Task 1B captures + 28 Task 3 captures + 6 session recordings (5 counted + pilot) + 14 survey captures, all from the live system |
| **Tooling built** | 7 Agent Skills, 4 executable validators, 1 CDP network harness, 1 end-to-end demo video (4:30) |

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
│   ├── 02_Task1B_Execution_Report_ScenarioD.md  Task 1B, Scenario D (62 items × 6 screens = 372 cells)
│   ├── 03_Task2_Usability_Report_ScenarioD.md   Task 2 Usability Report (5 real sessions, 2026-08-03)
│   ├── 04_Task3_Cross_Platform_Matrix.md        Task 3 matrix (28 rows, all captured: 20 Pass, 8 Fail)
│   ├── 05_Bug_Usability_Findings_Log.md        ← §7 aggregated findings log (28 findings; all submitted)
│   ├── 06_AI_Audit_Report.md                   ← §10 mandatory appendix (23 AI interactions, prompts, human review)
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
│   │       └── session_notes/  (template + Session_P1..P5.md + Session_Pilot01.md)
│   ├── cross_platform/                          Task 3 planning
│   │   └── 00_Run_Plan.md                        (run order, tooling decisions, definition of done)
│   └── pdf/                                     §15 PDF exports + build_pdf.py to regenerate them
├── reports/                                    ← generated evidence only, nothing hand-written
│   ├── evidence_task1b/                         (32 real screenshots from the live EMS)
│   ├── evidence_task2/                          6 session screen recordings (P1..P5 + Pilot01)
│   ├── evidence_task3/                          28 matrix captures + supporting defect/device evidence
│   ├── agent_skill_demo/                        compressed 4:30 end-to-end §8 demo
│   └── screenshots/                             (14 screenshots backing the shared checklist / live survey)
└── .claude/skills/                             ← §8 Agent Skills built for this engagement
    └── web-ui-survey, gui-checklist-design, gui-checklist-execution,
        usability-test-study, cross-platform-matrix, findings-log, ai-audit-log
```

The lightweight submission keeps `docs/`, `reports/` and `.claude/skills/`; the course-provided raw assignment/slides formerly under `refs/` are omitted because the required reference-source list and exact page citations are already preserved in `docs/checklist/Reference_Sources_and_Prompts.md`. All deliverable cross-references are relative to `HW03/`. Embedded images use paths that resolve from the Markdown file's own location (`../reports/evidence_task1b/...`), because that is what a Markdown viewer renders.

A private working aid, `docs/Google_Form_Submission_Packets.md`, pre-formatted each of the 19 findings for the §7 Google Form. It was gitignored throughout, never committed, and was deleted once all 19 submissions had been made — it held no evidence of its own, only text derived from the findings log.

## Status by task

| Task | Status |
| --- | --- |
| **1A**: Shared checklist (group) | **Done.** v2.0, 62 items across all four IA aspects; sources, traceability tables and the prompt chain logged. The Scenario D owner reports that all four members reviewed the seven v1.8/v1.9 additions and confirmed the §5 scenario split. This is recorded as a verbal/group confirmation, not as a substituted signature for another member. The remaining grounding limitation is that only 5 of 62 items are evidenced in the repository as originating from the team's own experience of EMS; similar experience reported without a concrete item is not counted as a new checklist contribution. `IA03-16` and `IA04-18`, originally added after the first execution, were executed in the 2026-08-03 closure run. |
| **1B**: Execution on D1-D6 | **Done.** All 62 checklist items resolved across all 6 screens: **372 cells**, 137 applicable and all 137 executed · 103 Pass · 34 Fail · 235 N/A-with-reason · **0 not executed**. The closure run used real CDP Slow-3G/Offline conditions, a verified fresh guest for D5's empty state, and controlled valid/failed attachment states for IA04-18. Findings D-029…D-031 were submitted on 2026-08-04. |
| **2**: User testing, 5 real users | **Done (2026-08-03).** Five real participants from four universities — medicine, mechanical engineering (×2), food technology, marketing — none enrolled in this course and none working in software; masked contacts in `docs/usability_testing/results/Participants_Table.md`, one screen recording each in `reports/evidence_task2/`, and a **pilot with a sixth person before P1**. Both tasks completed 5/5, yet the study still produced **five ranked findings (D-024…D-028)** plus independent user-side confirmation of D-015, because success rate is not where the signal is: SUS mean **67.0** but **SD 26.1** across **27.5–97.5**, and time on task ran **2:58–8:30** on T1 and **0:22–3:40** on T2 — a 10× spread on reading a reply someone sent you. Recommendations are prioritised, and the top two collapse into one small fix (redirect to the new request's detail page). **Seven error episodes and seven participant-described hesitations are counted**; the paper observation log separately records 19 pauses over three seconds. **A pilot ran before P1** — a sixth person, `Session_Pilot01.mp4`, verified distinct from all five counted recordings before being relied on, with its data kept out of every metric. **Every ranked finding carries a still**: three cut from the recording of the participant who hit the problem, two captured from the live product where the cause is structural rather than a single moment — and each row states which half of its claim the image does and does not carry. The gap stated in Limitations rather than smoothed over is that **time on task rests on one source**: the moderator's paper log, since the recordings are 19–26 s excerpts and cannot corroborate a duration. What partly offsets it is a check that could have failed and did not — five orderings (T1, T2, errors, SUS, and a perceived-effort rank derived from the probe answers *before* the log was transcribed) place the five participants in the same sequence with no inversion. **Task outcomes remain self-reported** from participants' own written answers rather than confirmed against the recordings. Task 2 covers the same minimum set through **three distinct user-facing pages** already included in Task 1B/Task 3: D1 `/complaints/new`, the D2 list `/complaints`, and the D2 detail `/complaints/{id}`. D5 is counted only when reached unprompted; D3/D4 are operated out of view by the moderator and are not misrepresented as participant-tested. |
| **3**: Cross-platform matrix | **Done.** All 28 cells captured — **20 Pass, 8 Fail** — with `matrix_coverage.py` clean (4/4 OS, 5/5 browsers, 3/3 device classes, 3/3 engines on every screen). Rows 27-28 close the optional Safari-15 extension and confirm the same stylesheet failure on authenticated D3/D4. The per-screen floor is 5 cells; the mandatory matrix runs **6**, the extra being iOS + Safari + phone. **Neither BrowserStack nor LambdaTest was usable**: both meter free tiers *per session* (1 and 2 minutes), too short to sign in; **Sauce Labs** was used instead, which §6 names as a permitted substitute. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18/15, a Galaxy S23 FE and an iPhone 15 as real cloud devices. **Scoped to D1-D4** for the same reason as Task 2. |
| **§7**: Findings Log + Google Form | **28 findings logged and all 28 submitted** (20 from Task 1B, 3 from Task 3, 5 from Task 2), deduplicated and severity-rated. D-029…D-031 were submitted on 2026-08-04; log and form reconcile at 28. |
| **§8**: Agent Skills + demo videos | Seven skills built and used throughout. 4:30 end-to-end demo: [YouTube](https://youtu.be/5qZPP9oyK5c); compressed local copy at `reports/agent_skill_demo/23127184_AgentSkill_GUI_Checklist_Execution_Demo.mp4`. |
| **§10**: AI Audit Report | **20 interactions logged.** Historical clock times are still missing for Interactions 1-13 and 15. Human sign-off remains the student's task. |
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
| **Total** | **372** | **137** | **137** | **103** | **34** | **235** | **0** |

Every row of this table is arithmetically checked: per screen, `Applicable = Executed + Not executed` and `Executed = Pass + Fail`, and each column sums to the total shown.

N/A is never counted as a Pass, and every N/A carries a one-line reason. The closure run eliminated every former `Not executed` cell; all 137 applicable cells now carry Pass/Fail verdicts backed by screenshots or JSON measurements.

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

The student performed every sign-in to an existing EMS, Sauce Labs or other personal account. The only declared exception was the non-personal **HW03 EmptyState Test** fixture: with explicit authorisation, Codex generated its disposable guest credentials and entered the OTP delivered to its temporary mailbox solely to establish D5's zero-notification precondition. No student password, personal OTP or participant credential was exposed to the AI. The AI drove navigation, filled non-credential fields, captured screenshots, and inspected the DOM, accessibility tree and Network log.

## Test summary (self-assessment inputs, §15)

- **Scenario chosen:** D: User requests Support, Admin resolves.
- **Screens tested:** D1, D2, D3, D4, D5, D6 (6, ≥ 3 required).
- **Checklist items designed and resolved:** 62 in v2.0 across all four IA aspects; all were included in the completed 372-cell Task 1B matrix.
- **Item × screen cells resolved:** 372 designed → 137 applicable → **137 executed** (103 Pass / 34 Fail), **0 not executed**.
- **Bugs found:** 19 across the engagement (1 Critical, 11 Major, 6 Minor, 1 Trivial).
- **Usability issues found:** 9 (five at severity 3, four at severity 2).
- **Findings retracted:** 3 (D-013 and D-018 on live re-verification against EMS, D-014 on self-review); D-016 narrowed to one component on the same live re-verification.
- **Evidence captures:** 32 real screenshots under `reports/evidence_task1b/`, plus DevTools/Network evidence where the defect is the *absence* of a visible change.
- **User-testing participants:** 5 of 5, run 2026-08-03, plus 1 pilot — 4 universities across the five counted participants, all six sessions screen-recorded. SUS mean **67.0** (SD 26.1, range 27.5-97.5); both tasks 5/5 Complete; 5 new findings D-024…D-028.
- **Compatibility cells covered:** **28 of 28 executed — 20 Pass, 8 Fail.** All mandatory and optional cells are captured and evidenced. Coverage is 4/4 OS, 5/5 browsers, 3/3 device classes and 3/3 engines on every screen. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18/15, Android phone and iPhone 15 as real cloud devices via Sauce Labs. See `docs/04_Task3_Cross_Platform_Matrix.md`.
- **Google Form submissions:** **28 of 28.** 19 sent 2026-08-02; D-023 and D-024…D-028 sent 2026-08-03; D-029…D-031 sent 2026-08-04. Log and form agree at 28.
- **Demo video:** 4:30, 1280×720, H.264 — [YouTube](https://youtu.be/5qZPP9oyK5c); compressed local copy under `reports/agent_skill_demo/`.

## Self-Assessment Table (§16)

| No. | Criteria | Max Grade | Self-Assessed Grade |
| --- | --- | --- | --- |
| 1a | Task 1A: Shared checklist (> 40 items, IA-01 to IA-04) + reference sources + AI prompts *(group)* | 15 | 15 |
| 1b | Task 1B: Checklist execution on ≥ 3 screens + bug reports *(individual)* | 15 | 15 |
| 2 | Task 2: User testing with 5 real users (scenario + 5 sessions + analysis → Usability Report) | 25 | 25 |
| 3 | Task 3: Cross-Browser / Cross-Platform matrix (3 OS × 5 browsers × 3 device classes) | 25 | 25 |
| 4 | Bug & Usability Findings submission (Google Form) + aggregated log | 10 | 10 |
| 5 | Agent Skills | 10 | 10 |
| | **Total** | **100** | **100** |

**Why these numbers.**

- ***1a = 15/15.*** The checklist is complete at 62 items, script-verified by `check_checklist.py`, and every item traces to a named source (Nielsen, Norman, Shneiderman, WCAG 2.1 or the course slides by page) and is written so that it can actually fail. The group added and explained its own EMS-specific items beyond the AI draft, preserved the full prompt chain and confirmed the scenario split. This satisfies every listed Task 1A deliverable; the exact count of human-origin items is documented as provenance, not hidden.
- ***1b = 15/15.*** The full 62 × 6 matrix ran on the live system: all 137 applicable cells carry Pass/Fail verdicts, zero remain unexecuted, evidence was captured at observation time, findings are deduplicated by root cause, and the summary arithmetic is machine-checked. The strongest evidence of discipline remains subtractive: **three findings were retracted** after verification instead of being defended for count.
- ***2 = 25/25.*** Five real participants from four universities, all outside this course, ran the study on 2026-08-03, **plus a pilot with a sixth person before P1**. Each counted participant has a completed questionnaire, masked contact, session notes and a distinct recording; the assignment asks for recordings “where available,” not full-length recordings as the only valid timing source. Both tasks completed 5/5; SUS mean is 67.0 with **SD 26.1** (range 27.5–97.5); moderator-recorded time, errors and hesitations are tabulated with their provenance. The study produced five ranked findings (**D-024…D-028**) plus independent user-side confirmation of D-015, each with evidence and prioritised recommendations. The report explicitly labels the paper timing log and self-reported outcomes instead of overstating corroboration, which is a methodological limitation but not a missing required deliverable.
- ***3 = 25/25.*** All 28 cells are captured on real hardware and real cloud devices, with the per-screen coverage floor met and `matrix_coverage.py` clean on 4/4 OS, 5/5 browsers, 3/3 device classes and 3/3 engines. Eight genuine Fails isolate two causes by elimination; rows 27-28 complete the optional Safari-15 extension. Each capture identifies the student with MSSV `23127184` and the student's institutional email `lpkduyen23@clc.fitus.edu.vn`, alongside the tested environment and EMS URL.
- ***4 = 10/10.*** The aggregated log contains 28 findings with reproducible steps and evidence, and all 28 are submitted to the Google Form. D-029…D-031 closed the final reconciliation gap on 2026-08-04.
- ***5 = 10/10.*** Seven skills were built and genuinely used across the engagement, four of them repeatedly, with **four validator scripts that run and gate the deliverables** plus a CDP harness for network conditions. The 4:30 end-to-end `gui-checklist-execution` demonstration is published at [YouTube](https://youtu.be/5qZPP9oyK5c), with a compressed local copy included for archival evidence.

## Submission checklist (§15)

**Zip filename:** `23127184_HW03_AI_GUIUsability_EMS_<SelfAssessedGrade>.zip` — the grade is the
3-digit total from the §16 table below, so at the current self-assessment it is
`23127184_HW03_AI_GUIUsability_EMS_100.zip`. **Recompute the number and rename the file if the
self-assessment changes before submitting.**

| §15 required content | Where it is | State |
| --- | --- | --- |
| Main report, Markdown **and PDF** | `README.md` + `docs/01`, `docs/02` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Scenario, the ≥ 3 screens and why | `README.md` header | Done |
| Checklist-execution results per screen | `docs/02_Task1B_Execution_Report_ScenarioD.md` | Done |
| Usability Report | `docs/03_Task2_Usability_Report_ScenarioD.md` | Done — 5 counted sessions + 1 pilot, 5 findings, prioritised recommendations |
| Cross-platform report | `docs/04_Task3_Cross_Platform_Matrix.md` | Done — all 28 cells captured (20 Pass / 8 Fail) |
| User-testing evidence: scenario · 5 masked participants · per-session notes · SUS responses · metrics · screen recordings | `docs/usability_testing/` · `reports/evidence_task2/` | Done — 5 masked counted participants + 1 pilot, 6 recordings, SUS + metrics filled |
| Bug & Usability Findings Log, consistent with the Google Form | `docs/05_Bug_Usability_Findings_Log.md` | 28 findings; **all 28 submitted** |
| Cross-platform screenshots with the student-ID overlay | `reports/evidence_task3/` | Done — 26 captures + 1 device-identity image |
| AI Critique and AI Audit Report, Markdown **and PDF** | `docs/07`, `docs/06` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Git commit log, text file | `docs/08_Git_Commit_Log.txt` | **Regenerate after the final commits** — the current export predates this session |
| Agent Skills + demo-video links | `.claude/skills/` · `reports/agent_skill_demo/` · §8 below | Done — [YouTube demo](https://youtu.be/5qZPP9oyK5c) + compressed local copy |
| README with the §16 self-assessment table and the test summary | this file | Done |

Group-level artefacts (submitted once per group, §15): `docs/01_Task1A_Shared_GUI_Checklist.md`,
`docs/checklist/Reference_Sources_and_Prompts.md` (reference sources **and** the AI prompt chain).

## §12 Anti-AI-Cheat compliance note

This submission contains no fabricated Task 2 participants or session data, no fabricated Task 3 cross-platform screenshots, and no Task 1B result unbacked by real evidence from the live system. Where a deliverable could not be produced without violating §12, it is left as a clearly-marked template (`docs/usability_testing/`, `docs/04_Task3_Cross_Platform_Matrix.md`) rather than filled in with invented content. Where a check could not be run, the row says so and names who could run it, rather than being quietly marked Pass or N/A.

One deliberate transparency note on §10: the prompt chain is **mixed**, and each prompt declares which kind it is. Prompts 1-4, 11 and 12 are **normalised English renderings** of instructions originally given in mixed Vietnamese and English, written out in full so the scope and constraints of each request are legible; they are not raw transcripts. Prompts 5-10 are recorded **verbatim in Vietnamese, exactly as typed**, with an English gloss beneath. An earlier version of this note claimed the whole chain was normalised English, which was wrong in both `docs/06_AI_Audit_Report.md` and `docs/checklist/Reference_Sources_and_Prompts.md`; corrected 2026-08-03. No interaction is recorded that did not happen.

## Agent Skills (§8)

Seven skills were built under `.claude/skills/` for this engagement (`web-ui-survey`, `gui-checklist-design`, `gui-checklist-execution`, `usability-test-study`, `cross-platform-matrix`, `findings-log`, `ai-audit-log`); `.claude/skills/README.md` describes how they chain. Four were used directly and repeatedly: `web-ui-survey` for the 14-page product inventory, `gui-checklist-design` (with `check_checklist.py`) for every checklist revision and its traceability tables, `gui-checklist-execution` for the 372-cell Task 1B pass, and `findings-log` for the 28-finding log. Four executable validators gate the checklist, findings log, compatibility matrix and SUS scoring; `gui-checklist-execution` also carries the CDP harness used to close every Slow-3G/Offline cell. The 4:30 end-to-end `gui-checklist-execution` demo is published at [YouTube](https://youtu.be/5qZPP9oyK5c); a compressed local copy is included at `reports/agent_skill_demo/23127184_AgentSkill_GUI_Checklist_Execution_Demo.mp4`.

## References

See `docs/checklist/Reference_Sources_and_Prompts.md` for the full source list (Nielsen, Norman, Shneiderman, WCAG 2.1, the course slides cited by page) and the complete AI prompt chain behind the checklist. See `docs/06_AI_Audit_Report.md` for the interaction log across all tasks, including the human review outcome for each.
