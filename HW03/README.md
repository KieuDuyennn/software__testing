# HW03: GUI & Usability Testing on EMS (Scenario D)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184 · **Group:** 09
**Scenario:** **D: User requests Support, Admin resolves** (spans the user and admin sides of the support-request lifecycle)
**Screens (≥ 3 required, 6 taken):** **D1** Create Support Request (`/complaints/new`) · **D2** My Requests list + detail with official response (`/complaints`, `/complaints/{id}`) · **D3** Admin Support Requests list, Pending/Resolved, filters (`/dashboard/admin/complaints`) · **D4** Admin request detail, internal note, official response · **D5** Notifications, header bell dropdown, `/notifications` list, `/notifications/{id}` detail · **D6** Attachment image lightbox, opened from the evidence images on D1-D4

**Why six screens, not three.** D1-D4 together are what the scenario *is*: dropping either the filing half (D1/D2) or the resolving half (D3/D4) would leave only one side of a two-role flow tested. D5 and D6 were added during execution because they sit inside the same journey rather than beside it: a notification is how the requester learns that the admin acted, and the lightbox is how the admin reads the evidence the requester attached. Scenario D belongs to this member alone and shares no screen with a teammate, so extending it does not touch §5's no-duplication rule. The extension earned its place twice over: D5 produced two real defects (**D-015**, notification summaries with a permanently empty complaint title, and **D-016**, ESC failing to dismiss the bell dropdown), and D6 produced none at all once its two provisional Fails were re-tested against the live product and withdrawn.

---

## Repository map

```
HW03/
├── README.md                              ← this file
├── AI_Audit_Report.md                     ← §10 mandatory appendix (16 AI interactions, prompts, human review)
├── AI_Critique.md                         ← §11 mandatory 200-300 word critique
├── Git_Commit_Log.txt                     ← §13 mandatory commit log export (HW03-scoped)
├── checklist/                             ← Task 1 Part A, group deliverable
│   ├── Shared_GUI_Checklist.md             (60 items, IA-01 to IA-04, v1.9)
│   ├── Reference_Sources_and_Prompts.md    (sources, traceability tables, full AI prompt chain)
│   └── EMS_Live_Survey_2026-07-26.md       (widget inventory backing the checklist's EMS-grounded items)
├── task1b_execution/                      ← Task 1 Part B, individual, Scenario D, complete
│   ├── Execution_Report_ScenarioD.md       (60 items × 6 screens = 360 cells, Pass/Fail/N/A/not-executed)
│   └── evidence/                           (32 real screenshots from the live EMS)
├── findings/
│   └── Bug_Usability_Findings_Log.md       ← §7 aggregated findings log (16 findings; 3 retracted on review)
├── usability_testing/                     ← Task 2 scaffold, no real sessions run yet
│   ├── Task_Scenario_D.md
│   ├── Participants_Table.md
│   ├── Metrics_Table.md
│   ├── SUS_Responses.csv
│   ├── Usability_Report_ScenarioD.md
│   └── session_notes/Session_Notes_TEMPLATE.md
├── cross_platform/                        ← Task 3 scaffold, no cloud-lab run yet
│   └── Cross_Platform_Matrix_ScenarioD.md
├── screenshots/                            (14 screenshots backing the shared checklist / live survey)
├── refs/                                   (course PDFs: GUI testing, usability testing, compatibility testing)
├── requirments/                            (assignment brief, EN + VI, + PDF)
└── .claude/skills/                        ← §8 Agent Skills built for this engagement
    ├── web-ui-survey, gui-checklist-design, gui-checklist-execution,
    │   usability-test-study, cross-platform-matrix, findings-log, ai-audit-log
```

## Status by task

| Task | Status |
| --- | --- |
| **1A**: Shared checklist (group) | **Done.** v1.9, 60 items across all four IA aspects; sources, traceability tables and the full prompt chain logged. Two gaps stated openly rather than closed on paper: only 4 of 60 items are grounded in the team's own EMS experience (the "pillar 4" gap, retargeted to v2.0), and the 7 newest items still need sign-off from the other three members. |
| **1B**: Execution on D1-D6 | **Done.** All 60 items run against all 6 screens (360 item×screen cells), screen by screen on the live system. 136 applicable · **109 executed** · 92 Pass · 17 Fail · 224 N/A-with-reason · 27 not executed, each with a named cause and a named owner. 16 findings stand, every Fail backed by a screenshot or DevTools evidence. Three further findings were raised and then retracted after being re-tested against the live product. |
| **2**: User testing, 5 real users | **Not started.** No real participants recruited. Templates for the task scenario, participant table, SUS instrument, metrics table and report are ready in `usability_testing/`; the §12 note below explains why they cannot be filled in without real sessions. |
| **3**: Cross-platform matrix | **Not started.** No BrowserStack/LambdaTest run yet. Coverage-floor template ready in `cross_platform/`. |
| **§7**: Findings Log + Google Form | **16 findings logged**, deduplicated and severity-rated. **Google Form submission: TODO for all 16.** The log's `Form-submission timestamp` column reads `TODO` on every row because no finding has been submitted yet. The TA may cross-check counts against the form. |
| **§8**: Agent Skills + demo videos | Seven skills built and used throughout. **Demo video links: TODO.** |
| **§10**: AI Audit Report | **Done.** 17 interactions, each with tool, date/time, the prompt, the AI output and the human review outcome. |
| **§15**: report formats | Markdown is complete. **PDF versions of the main report, the AI Audit Report and the AI Critique are outstanding**; §15 asks for Markdown and PDF. |

## Task 1B results

Executed against the live EMS at `https://prod-dev.ems-fitus.cloud/` (the assignment's original ngrok URL had gone offline; the current one was supplied mid-session).

| Screen | Designed | Applicable | Executed | Pass | Fail | N/A | Not executed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| D1 | 60 | 19 | 17 | 13 | 4 | 41 | 2 |
| D2 | 60 | 22 | 20 | 16 | 4 | 38 | 2 |
| D3 | 60 | 35 | 29 | 24 | 5 | 25 | 6 |
| D4 | 60 | 28 | 20 | 19 | 1 | 32 | 8 |
| D5 | 60 | 23 | 18 | 15 | 3 | 37 | 5 |
| D6 | 60 | 9 | 5 | 5 | 0 | 51 | 4 |
| **Total** | **360** | **136** | **109** | **92** | **17** | **224** | **27** |

N/A is never counted as a Pass, and every N/A carries a one-line reason. The 27 not-executed cells are mostly one tooling gap (DevTools Network throttling and offline mode, which the browser-automation tool set cannot drive) plus a deliberate refusal to run destructive checks on a live system holding other students' data; each is listed in the report with who could run it.

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

The stage-one explanations were wrong. They were consistent with everything written down and still did not survive contact with the product. Nothing was deleted to make the files agree: the count fell from 18 to 16 because three claims could not be defended, which is the direction a real check moves the number. Full reasoning in `task1b_execution/Execution_Report_ScenarioD.md` §"Live re-verification".

### A note on how the browser automation was done

The AI never entered a password, OTP or any other credential into any field. Every login was performed by the student herself: account creation, admin login, and each re-login needed when switching roles in the same cookie-sharing browser tab. The AI was instructed to stop and hand the tab back at each authentication step. The AI drove navigation, filled non-credential fields, captured screenshots, and inspected the DOM, accessibility tree and Network log.

## Test summary (self-assessment inputs, §15)

- **Scenario chosen:** D: User requests Support, Admin resolves.
- **Screens tested:** D1, D2, D3, D4, D5, D6 (6, ≥ 3 required).
- **Checklist items designed:** 60 (group checklist, all four IA aspects).
- **Item × screen cells resolved:** 360 designed → 136 applicable → **109 executed** (92 Pass / 17 Fail), 27 not executed with named causes.
- **Bugs found:** 13 (0 Critical, 6 Major, 6 Minor, 1 Trivial).
- **Usability issues found:** 3 (two at severity 3, one at severity 2).
- **Findings retracted:** 3 (D-013 and D-018 on live re-verification against EMS, D-014 on self-review); D-016 narrowed to one component on the same live re-verification.
- **Evidence captures:** 32 real screenshots under `task1b_execution/evidence/`, plus DevTools/Network evidence where the defect is the *absence* of a visible change.
- **User-testing participants:** 0 of 5 recruited (Task 2 not started).
- **Compatibility cells covered:** 0 of the planned 12-cell matrix (Task 3 not started).
- **Google Form submissions:** 0 of 16, outstanding.
- **Demo videos:** TODO.

## Self-Assessment Table (§16)

| No. | Criteria | Max Grade | Self-Assessed Grade |
| --- | --- | --- | --- |
| 1a | Task 1A: Shared checklist (> 40 items, IA-01 to IA-04) + reference sources + AI prompts *(group)* | 15 | 13 |
| 1b | Task 1B: Checklist execution on ≥ 3 screens + bug reports *(individual)* | 15 | 14 |
| 2 | Task 2: User testing with 5 real users (scenario + 5 sessions + analysis → Usability Report) | 25 | 0 |
| 3 | Task 3: Cross-Browser / Cross-Platform matrix (3 OS × 5 browsers × 3 device classes) | 25 | 0 |
| 4 | Bug & Usability Findings submission (Google Form) + aggregated log | 10 | 4 |
| 5 | Agent Skills | 10 | 8 |
| | **Total** | **100** | **39** |

**Why these numbers.** *1a = 13*: the checklist is complete, script-verified and fully traceable, but two of its own stated standards are unmet: only 4 of 60 items come from the team's lived experience of EMS, and three members have not signed off the newest items. *1b = 14*: the full 60 × 6 matrix ran with evidence attached at the moment of observation, findings deduplicated by root cause, three findings retracted (two only after re-testing against the live product, not on paper alone) and no contradiction reconciled by inventing an explanation instead of checking it; the point off is for the 27 cells no available tool could execute. *2 and 3 = 0*: §12 makes fabricated participants and cloud-lab screenshots grounds for voiding the task, and nothing has been substituted for the real fieldwork. A zero here is a true statement, not a low one. *4 = 4/10*: the aggregated log is complete and validated, but none of the 16 findings has been submitted to the Google Form yet, and that is half of what this criterion asks for. *5 = 8*: seven skills built and genuinely used, with validator scripts that run; demo videos outstanding.

## §12 Anti-AI-Cheat compliance note

This submission contains no fabricated Task 2 participants or session data, no fabricated Task 3 cross-platform screenshots, and no Task 1B result unbacked by real evidence from the live system. Where a deliverable could not be produced without violating §12, it is left as a clearly-marked template (`usability_testing/`, `cross_platform/`) rather than filled in with invented content. Where a check could not be run, the row says so and names who could run it, rather than being quietly marked Pass or N/A.

One deliberate transparency note on §10: the prompts in `AI_Audit_Report.md` and `checklist/Reference_Sources_and_Prompts.md` are **normalised English renderings** of instructions originally given in mixed Vietnamese and English, written out in full so the scope and constraints of each request are legible. They are not raw transcripts, and both files say so at the top. No interaction is recorded that did not happen.

## Agent Skills (§8)

Seven skills were built under `.claude/skills/` for this engagement (`web-ui-survey`, `gui-checklist-design`, `gui-checklist-execution`, `usability-test-study`, `cross-platform-matrix`, `findings-log`, `ai-audit-log`); `.claude/skills/README.md` describes how they chain. Four were used directly and repeatedly: `web-ui-survey` for the 14-page product inventory, `gui-checklist-design` (with `check_checklist.py`) for every checklist revision and its traceability tables, `gui-checklist-execution` for the 360-cell Task 1B pass, and `findings-log` (with `check_findings.py`) for the 16-finding log. Demo video links: **TODO**.

## References

See `checklist/Reference_Sources_and_Prompts.md` for the full source list (Nielsen, Norman, Shneiderman, WCAG 2.1, the course slides cited by page) and the complete AI prompt chain behind the checklist. See `AI_Audit_Report.md` for the interaction log across all tasks, including the human review outcome for each.
