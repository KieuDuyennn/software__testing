# HW03: GUI & Usability Testing on EMS (Scenario D)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Scenario:** **D: User requests Support, Admin resolves** (spans the user and admin sides of the support-request lifecycle)
**Screens (≥ 3 required, 6 taken):** **D1** Create Support Request (`/complaints/new`) · **D2** My Requests list + detail with official response (`/complaints`, `/complaints/{id}`) · **D3** Admin Support Requests list, Pending/Resolved, filters (`/dashboard/admin/complaints`) · **D4** Admin request detail, internal note, official response · **D5** Notifications, header bell dropdown, `/notifications` list, `/notifications/{id}` detail · **D6** Attachment image lightbox, opened from the evidence images on D1-D4

**System under test — read this before checking any URL in this package.** Every run recorded here was executed against **`https://prod-dev.ems-fitus.cloud/`**, not the `https://promoter-starboard-prude.ngrok-free.dev/` address printed in §4 of the brief. The ngrok tunnel in the brief had gone offline; the replacement host was supplied mid-session and is the same EMS instance. This is why the two do not match — it is not a different system. `docs/06_AI_Audit_Report.md` Interaction 13 records when the switch happened, and `docs/checklist/EMS_Live_Survey_2026-07-26.md` still shows the old base URL because it is a dated record of the 26 July survey, correct as of that date.

**Why six screens, not three.** D1-D4 together are what the scenario *is*: dropping either the filing half (D1/D2) or the resolving half (D3/D4) would leave only one side of a two-role flow tested. D5 and D6 were added during execution because they sit inside the same journey rather than beside it: a notification is how the requester learns that the admin acted, and the lightbox is how the admin reads the evidence the requester attached. Scenario D belongs to this member alone and shares no screen with a teammate, so extending it does not touch §5's no-duplication rule. The extension earned its place twice over: D5 produced two real defects (**D-015**, notification summaries with a permanently empty complaint title, and **D-016**, ESC failing to dismiss the bell dropdown), and D6 produced none at all once its two provisional Fails were re-tested against the live product and withdrawn.

---

## Repository map

```
HW03/
├── README.md · CLAUDE.md · .gitignore           ← the only files at root
├── docs/                                       ← every written deliverable, numbered in submission order
│   ├── 01_Task1A_Shared_GUI_Checklist.md        Task 1A group checklist (60 items, IA-01 to IA-04, v1.9)
│   ├── 02_Task1B_Execution_Report_ScenarioD.md  Task 1B, Scenario D (60 items × 6 screens = 360 cells)
│   ├── 03_Task2_Usability_Report_ScenarioD.md   Task 2 report (template, no real sessions run yet)
│   ├── 04_Task3_Cross_Platform_Matrix.md        Task 3 matrix (template, no cloud-lab run yet)
│   ├── 05_Bug_Usability_Findings_Log.md        ← §7 aggregated findings log (19 findings; 3 retracted on review)
│   ├── 06_AI_Audit_Report.md                   ← §10 mandatory appendix (13 AI interactions, prompts, human review)
│   ├── 07_AI_Critique.md                       ← §11 mandatory 200-300 word critique
│   ├── 08_Git_Commit_Log.txt                   ← §13 mandatory commit log export (HW03-scoped)
│   ├── checklist/                               Task 1A supporting material
│   │   ├── Reference_Sources_and_Prompts.md      (sources, traceability tables, full AI prompt chain)
│   │   └── EMS_Live_Survey_2026-07-26.md         (widget inventory backing the EMS-grounded items)
│   ├── usability_testing/                       Task 2 instruments — start at 00_Run_Plan.md
│   │   ├── 00_Run_Plan.md                        (the plan: path, open decisions, definition of done)
│   │   ├── Recruiting_Kit.md                     (screener, VI invite + consent scripts, booking)
│   │   ├── Task_Scenario_D.md                    (goal-only tasks + success criteria + probes)
│   │   ├── Moderator_Runsheet.md                 (per-session checklist, admin resolve script)
│   │   ├── SUS_Instrument_VI_EN.md               (10 items VI/EN, answer sheet, scoring)
│   │   ├── Participants_Table.md · Metrics_Table.md · SUS_Responses.csv
│   │   └── session_notes/Session_Notes_TEMPLATE.md
│   ├── cross_platform/                          Task 3 planning
│   │   └── 00_Run_Plan.md                        (24-cell plan, run order, screenshot rule)
│   └── pdf/                                     §15 PDF exports + build_pdf.py to regenerate them
├── reports/                                    ← generated evidence only, nothing hand-written
│   ├── evidence_task1b/                         (32 real screenshots from the live EMS)
│   ├── evidence_task2/                          (empty: Task 2 not run)
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

One file on disk is deliberately absent from the map and from the submission: `docs/Google_Form_Submission_Packets.md`, a private working aid that pre-formats each of the 19 findings for the §7 Google Form. It is listed in `.gitignore`, so it is not committed and not part of the graded package.

## Status by task

| Task | Status |
| --- | --- |
| **1A**: Shared checklist (group) | **Done.** v1.9, 60 items across all four IA aspects; sources, traceability tables and the full prompt chain logged. Two gaps stated openly rather than closed on paper: only 4 of 60 items are grounded in the team's own EMS experience (the "pillar 4" gap, retargeted to v2.0), and the 7 newest items still need sign-off from the other three members. |
| **1B**: Execution on D1-D6 | **Done.** All 60 items run against all 6 screens (360 item×screen cells), screen by screen on the live system. 136 applicable · **108 executed** · 92 Pass · 16 Fail · 224 N/A-with-reason · 28 not executed, each with a named cause and a named owner. 16 findings stand, every Fail backed by a screenshot or DevTools evidence. Three further findings were raised and then retracted after being re-tested against the live product. |
| **2**: User testing, 5 real users | **Designed, not run.** Phase 1 is complete and Phase 2 is blocked on recruiting: 0 of 5 participants found, 0 sessions run. `docs/usability_testing/00_Run_Plan.md` holds the end-to-end plan, the five decisions still owed and the definition of done; the task scenario, recruiting/consent kit, bilingual SUS instrument, moderator run-sheet, session-note template, participant table, metrics table and report skeleton are all ready in `docs/usability_testing/`. Every result table stays empty — the §12 note below explains why they cannot be filled in without real sessions. **Scoped to D1-D2**, not the D5/D6 extension and not Task 3's D1-D4: `docs/usability_testing/Task_Scenario_D.md` has the participant complete the filing half (D1/D2) while the moderator operates D3/D4 out of view, a deliberate scope narrower than Task 1B's, not an oversight. |
| **3**: Cross-platform matrix | **Done.** 26 of 28 cells captured — **20 Pass, 6 Fail** — with all **24 mandatory** cells complete and `matrix_coverage.py` clean (4/4 OS, 5/5 browsers, 3/3 device classes, 3/3 engines on every screen). The two open cells are rows 27-28, an optional old-WebKit extension outside the coverage floor. The per-screen floor is 5 cells; the matrix runs **6**, the extra being iOS + Safari + phone, because at the bare floor three of the five required brands are Blink and mobile WebKit would go untested — and that extra row is one of the two that caught the main defect. **Neither BrowserStack nor LambdaTest was usable**: both meter free tiers *per session* (1 and 2 minutes), too short to sign in; **Sauce Labs** was used instead, which §6 names as a permitted substitute. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18, a Galaxy S23 FE and an iPhone 15 as real cloud devices. **Scoped to D1-D4** for the same reason as Task 2. |
| **§7**: Findings Log + Google Form | **19 findings logged** (16 from Task 1B, 3 from Task 3), deduplicated and severity-rated. **Google Form submission: TODO for all 19.** The log's `Form-submission timestamp` column reads `TODO` on every row because no finding has been submitted yet. The TA may cross-check counts against the form. |
| **§8**: Agent Skills + demo videos | Seven skills built and used throughout. **Demo video links: TODO.** |
| **§10**: AI Audit Report | **Done.** 13 interactions, each with tool, date/time, the prompt, the AI output and the human review outcome. |
| **§15**: report formats | **Done.** Markdown is the source of truth; six PDFs (main report, Task 1A checklist, Task 1B execution report, findings log, AI Audit Report, AI Critique) are in `docs/pdf/`, rebuildable with `python docs/pdf/build_pdf.py`. Wide tables are rotated to landscape so no column is clipped, and the 25 embedded evidence screenshots travel with the Task 1B PDF. **Re-run the build after any further markdown edit.** |

## Task 1B results

Executed against the live EMS at `https://prod-dev.ems-fitus.cloud/` (the assignment's original ngrok URL had gone offline; the current one was supplied mid-session).

| Screen | Designed | Applicable | Executed | Pass | Fail | N/A | Not executed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | 60 | 19 | 17 | 13 | 4 | 41 | 2 |
| D2 | 60 | 22 | 20 | 16 | 4 | 38 | 2 |
| D3 | 60 | 35 | 28 | 24 | 4 | 25 | 7 |
| D4 | 60 | 28 | 20 | 19 | 1 | 32 | 8 |
| D5 | 60 | 23 | 18 | 15 | 3 | 37 | 5 |
| D6 | 60 | 9 | 5 | 5 | 0 | 51 | 4 |
| **Total** | **360** | **136** | **108** | **92** | **16** | **224** | **28** |

N/A is never counted as a Pass, and every N/A carries a one-line reason. The 28 not-executed cells are mostly one tooling gap (DevTools Network throttling and offline mode, which the browser-automation tool set cannot drive) plus a deliberate refusal to run destructive checks on a live system holding other students' data; each is listed in the report with who could run it.

### Findings: 16 total

| Severity | Count | IDs |
| --- | --- | --- |
| Bug, Blocker | 0 | |
| Bug, Critical | 0 | |
| Bug, Major | 6 | D-001, D-002, D-005, D-008, D-011, D-015 |
| Bug, Minor | 6 | D-004, D-006, D-009, D-010, D-016, D-017 |
| Bug, Trivial | 1 | D-019 |
| Usability 3 (Major) | 2 | D-003, D-007 |
| Usability 2 (Minor) | 1 | D-012 |

Two findings each cover one root cause reproducing on two screens (D-005 search-box keystroke loss, D-008 rows-per-page stuck), merged into one finding apiece rather than double-counted. The merge is what turns "two screen bugs" into "one shared-component bug", and it is argued from evidence in each row.

### What review and re-verification changed

This happened in two stages, and the second stage overturned the first.

**Stage one, reading the artefacts against each other.** Before submission the execution report and the findings log were cross-read the way a TA would read them. Two contradictions surfaced: IA03-10 was scored Pass on D2/D3/D4 and Fail on D6 for the same lightbox, and that lightbox rendered its image on D2/D3/D4 but not on D6. Explanations were written for both, on paper, from the recorded notes.

**Stage two, going back to the product.** The findings were then re-tested against the live EMS. That is what actually settled it, and it retracted three findings rather than confirming any explanation:

1. **D-018 (Critical) is withdrawn.** The `<img>` element does exist, with `alt="attachment_1"`. Its source returns HTTP 200, `content-type: image/png`, **68 bytes**, and the PNG header decodes to a width of 1 and a height of 1. The lightbox renders it correctly. The file is a 1x1 pixel placeholder named `d1-test-upload.png`, uploaded by this project's own D1 attachment test. The most severe finding in the assignment was a test fixture, not a product defect, and the original claims that "zero network requests were even issued" and that "no `<img>` element exists in the DOM" were both false.
2. **D-013 (Usability 1) is withdrawn.** Escape closed the lightbox on the first press, on complaint 25 and complaint 26 alike. The two-presses observation did not reproduce.
3. **D-016 is narrowed to the bell dropdown alone.** Three Escape presses left the notification dropdown fully open, so that half stands. The lightbox does not exhibit the defect, so the "two independent overlay components, one shared root cause" framing was dropped.

The stage-one explanations were wrong. They were consistent with everything written down and still did not survive contact with the product. Nothing was deleted to make the files agree: the count fell from 18 to 16 because three claims could not be defended, which is the direction a real check moves the number. Full reasoning in `docs/02_Task1B_Execution_Report_ScenarioD.md` §"Live re-verification".

### A note on how the browser automation was done

The AI never entered a password, OTP or any other credential into any field. Every login was performed by the student herself: account creation, admin login, and each re-login needed when switching roles in the same cookie-sharing browser tab. The AI was instructed to stop and hand the tab back at each authentication step. The AI drove navigation, filled non-credential fields, captured screenshots, and inspected the DOM, accessibility tree and Network log.

## Test summary (self-assessment inputs, §15)

- **Scenario chosen:** D: User requests Support, Admin resolves.
- **Screens tested:** D1, D2, D3, D4, D5, D6 (6, ≥ 3 required).
- **Checklist items designed:** 60 (group checklist, all four IA aspects).
- **Item × screen cells resolved:** 360 designed → 136 applicable → **108 executed** (92 Pass / 16 Fail), 28 not executed with named causes.
- **Bugs found:** 13 (0 Critical, 6 Major, 6 Minor, 1 Trivial).
- **Usability issues found:** 3 (two at severity 3, one at severity 2).
- **Findings retracted:** 3 (D-013 and D-018 on live re-verification against EMS, D-014 on self-review); D-016 narrowed to one component on the same live re-verification.
- **Evidence captures:** 32 real screenshots under `reports/evidence_task1b/`, plus DevTools/Network evidence where the defect is the *absence* of a visible change.
- **User-testing participants:** 0 of 5 recruited (Task 2 not started).
- **Compatibility cells covered:** **26 of 28 executed — 20 Pass, 6 Fail.** All **24 mandatory** cells are captured and evidenced (6 per screen × D1-D4); the two outstanding cells belong to an optional old-WebKit extension (rows 27-28) and are not required by the coverage floor. Coverage is 4/4 OS, 5/5 browsers, 3/3 device classes and 3/3 engines on every screen. Environments: Windows 11 (Edge 151, Firefox 153) and an Android tablet as real local devices; macOS Safari 18, Android phone and iPhone 15 as real cloud devices via Sauce Labs. See `docs/04_Task3_Cross_Platform_Matrix.md`.
- **Google Form submissions:** 0 of 19, outstanding — the 16 from Task 1B plus the three from Task 3 (D-020, D-021, D-022).
- **Demo videos:** TODO.

## Self-Assessment Table (§16)

| No. | Criteria | Max Grade | Self-Assessed Grade |
| --- | --- | --- | --- |
| 1a | Task 1A: Shared checklist (> 40 items, IA-01 to IA-04) + reference sources + AI prompts *(group)* | 15 | 13 |
| 1b | Task 1B: Checklist execution on ≥ 3 screens + bug reports *(individual)* | 15 | 14 |
| 2 | Task 2: User testing with 5 real users (scenario + 5 sessions + analysis → Usability Report) | 25 | 0 |
| 3 | Task 3: Cross-Browser / Cross-Platform matrix (3 OS × 5 browsers × 3 device classes) | 25 | 23 |
| 4 | Bug & Usability Findings submission (Google Form) + aggregated log | 10 | 4 |
| 5 | Agent Skills | 10 | 8 |
| | **Total** | **100** | **62** |

**Why these numbers.** *1a = 13*: the checklist is complete, script-verified and fully traceable, but two of its own stated standards are unmet: only 4 of 60 items come from the team's lived experience of EMS, and three members have not signed off the newest items. *1b = 14*: the full 60 × 6 matrix ran with evidence attached at the moment of observation, findings deduplicated by root cause, three findings retracted (two only after re-testing against the live product, not on paper alone) and no contradiction reconciled by inventing an explanation instead of checking it; the point off is for the 28 cells no available tool could execute. *2 = 0*: §12 makes fabricated participants grounds for voiding the task, and nothing has been substituted for the real fieldwork — no participant has been recruited, so there is nothing to score. A zero here is a true statement, not a low one. *3 = 23/25*: all 24 mandatory cells captured on real hardware and real cloud devices with the coverage floor met per screen, six genuine Fails isolated to two distinct causes by elimination; the two points off are for the overlay not matching §6's literal `MSSV@....edu.vn` form (a documented decision, not an oversight) and for rows 27-28 of the optional Safari-15 extension being left unrun. Every Fail was reproduced in a second independent session before being logged. *4 = 4/10*: the aggregated log is complete and validated, but none of the 19 findings has been submitted to the Google Form yet, and that is half of what this criterion asks for. *5 = 8*: seven skills built and genuinely used, with validator scripts that run; demo videos outstanding.

## Submission checklist (§15)

**Zip filename:** `23127184_HW03_AI_GUIUsability_EMS_<SelfAssessedGrade>.zip` — the grade is the
3-digit total from the §16 table below, so at the current self-assessment it is
`23127184_HW03_AI_GUIUsability_EMS_062.zip`. **Recompute the number and rename the file if the
self-assessment changes before submitting.**

| §15 required content | Where it is | State |
| --- | --- | --- |
| Main report, Markdown **and PDF** | `README.md` + `docs/01`, `docs/02` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Scenario, the ≥ 3 screens and why | `README.md` header | Done |
| Checklist-execution results per screen | `docs/02_Task1B_Execution_Report_ScenarioD.md` | Done |
| Usability Report | `docs/03_Task2_Usability_Report_ScenarioD.md` | **Skeleton only — sessions not run** |
| Cross-platform report | `docs/04_Task3_Cross_Platform_Matrix.md` | **Matrix planned, 0 cells captured** |
| User-testing evidence: scenario · 5 masked participants · per-session notes · SUS responses · metrics · screen recordings | `docs/usability_testing/` · `reports/evidence_task2/` | **Instruments ready, all result tables empty** |
| Bug & Usability Findings Log, consistent with the Google Form | `docs/05_Bug_Usability_Findings_Log.md` | Log done; **0 of 19 submitted to the form** |
| Cross-platform screenshots with the student-ID overlay | `reports/evidence_task3/` | **Empty** |
| AI Critique and AI Audit Report, Markdown **and PDF** | `docs/07`, `docs/06` · `docs/pdf/` | Markdown done; PDF in `docs/pdf/` |
| Git commit log, text file | `docs/08_Git_Commit_Log.txt` | **Regenerate after the final commits** — the current export predates this session |
| Agent Skills + demo-video links | `.claude/skills/` · §8 below | Skills done; **video links TODO** |
| README with the §16 self-assessment table and the test summary | this file | Done |

Group-level artefacts (submitted once per group, §15): `docs/01_Task1A_Shared_GUI_Checklist.md`,
`docs/checklist/Reference_Sources_and_Prompts.md` (reference sources **and** the AI prompt chain).

## §12 Anti-AI-Cheat compliance note

This submission contains no fabricated Task 2 participants or session data, no fabricated Task 3 cross-platform screenshots, and no Task 1B result unbacked by real evidence from the live system. Where a deliverable could not be produced without violating §12, it is left as a clearly-marked template (`docs/usability_testing/`, `docs/04_Task3_Cross_Platform_Matrix.md`) rather than filled in with invented content. Where a check could not be run, the row says so and names who could run it, rather than being quietly marked Pass or N/A.

One deliberate transparency note on §10: the prompt chain is **mixed**, and each prompt declares which kind it is. Prompts 1-4, 11 and 12 are **normalised English renderings** of instructions originally given in mixed Vietnamese and English, written out in full so the scope and constraints of each request are legible; they are not raw transcripts. Prompts 5-10 are recorded **verbatim in Vietnamese, exactly as typed**, with an English gloss beneath. An earlier version of this note claimed the whole chain was normalised English, which was wrong in both `docs/06_AI_Audit_Report.md` and `docs/checklist/Reference_Sources_and_Prompts.md`; corrected 2026-08-01. No interaction is recorded that did not happen.

## Agent Skills (§8)

Seven skills were built under `.claude/skills/` for this engagement (`web-ui-survey`, `gui-checklist-design`, `gui-checklist-execution`, `usability-test-study`, `cross-platform-matrix`, `findings-log`, `ai-audit-log`); `.claude/skills/README.md` describes how they chain. Four were used directly and repeatedly: `web-ui-survey` for the 14-page product inventory, `gui-checklist-design` (with `check_checklist.py`) for every checklist revision and its traceability tables, `gui-checklist-execution` for the 360-cell Task 1B pass, and `findings-log` (with `check_findings.py`) for the 19-finding log. Demo video links: **TODO**.

## References

See `docs/checklist/Reference_Sources_and_Prompts.md` for the full source list (Nielsen, Norman, Shneiderman, WCAG 2.1, the course slides cited by page) and the complete AI prompt chain behind the checklist. See `docs/06_AI_Audit_Report.md` for the interaction log across all tasks, including the human review outcome for each.
