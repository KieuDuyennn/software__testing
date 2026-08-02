# Task 2 — Run plan — Scenario D (user testing with 5 real users)

> **This is the operating plan, not a deliverable in itself.** It says what has to happen, in what
> order, who does it, and what "done" looks like. The graded artefact is
> `docs/03_Task2_Usability_Report_ScenarioD.md`; everything below exists to fill that file with
> real data.

**Status: not started.** 0 of 5 participants recruited, 0 sessions run. Task 2 is worth **25 of
100 marks** and is currently self-assessed at **0** in the README — it is the single largest
recoverable block of marks left in HW03.

---

## 1. What is already decided (do not redesign these)

| Decision | Value | Where it is written |
| --- | --- | --- |
| Method | Moderated think-aloud, in person or screen-shared | `docs/usability_testing/Task_Scenario_D.md` |
| Participants | 5 real + 1 pilot, all outside this class | brief §6 Task 2 |
| Screens under test | **D1** `/complaints/new`, **D2** `/complaints`, `/complaints/{id}` | `docs/usability_testing/Task_Scenario_D.md` |
| Admin side (D3/D4) | Operated by the **moderator**, never handed to a participant | same |
| Tasks | **T1** file a support request · **T2** find the official response | same, with success criteria fixed in advance |
| Instrument | **SUS** (10 items), not UEQ-S — comparable across the group's four scenario owners | same |
| Session language | **Vietnamese** — every participant-facing script is in Vietnamese | `docs/usability_testing/Recruiting_Kit.md`, `docs/usability_testing/SUS_Instrument_VI_EN.md` |
| Severity scale for findings | Nielsen **0-4**, logged as `Usability 0`…`Usability 4` | `docs/05_Bug_Usability_Findings_Log.md` |

**Scope note that must survive into the report:** Task 2 is scoped to **D1-D2**, narrower than Task
1B's D1-D6. That is deliberate — a usability participant cannot be given an admin account, so D3/D4
are driven by the moderator instead. Say this in Limitations rather than letting a reader assume the
scopes match.

**On the brief's "≥ 3 screens" rule** (§6: *"Tasks 1B, 2, and 3 all operate on the same three (or
more) screens"*): D1 and D2 are two *named* package screens but **three distinct pages** — the
participant visits `/complaints/new`, `/complaints` and `/complaints/{id}` in every session, and
some will also reach **D5** (`/notifications`) on their own while hunting for the reply. The mapping
table is in `docs/usability_testing/Task_Scenario_D.md` §"Screens under test" and repeated in the
report's §2; state it there explicitly rather than leaving a grader to count screens and come up
short. Never steer a participant toward the notification bell to manufacture D5 coverage — which
route they take is itself the result.

## 2. What you must decide before recruiting

These are yours to settle; nothing downstream can start until they are.

| # | Decision | Why it blocks | Recommendation |
| --- | --- | --- | --- |
| 1 | ~~**Participant EMS accounts**~~ — **settled** | Sign-up + OTP would eat half a session and tests a screen that is not under study | **Resolved in `docs/usability_testing/Moderator_Runsheet.md` §1:** you pre-create **6** accounts (pilot + P1-P5), each with a distinct member code so requests are told apart on the admin side without the buggy search box, and you pre-authenticate each participant's tab at T-15min. You type every password yourself; the participant never sees a login screen. Three sub-points there are marked **VERIFY BEFORE PILOT** — settle them live before the pilot. |
| 2 | **Whose device** — participant's laptop or yours? | Determines recording setup and whether their browser state contaminates the session | Yours, with a fresh profile. Simplest to record, simplest to reset. |
| 3 | **In person or remote** (Zalo/Meet screen share)? | Changes the recording method and how you observe hesitation | In person if you can — think-aloud signal is much richer. Remote is acceptable; record the shared screen. |
| 4 | **Dates for 6 slots** (~20-25 min each) | The pilot must complete and its fixes land *before* session P1 | Pilot on day 1; P1-P5 across days 2-4, max 2 per day so you can write notes between them. |
| 5 | **Which EMS host is live on the day** | The brief warns the instance moves; a dead URL kills a booked slot | Verify the morning of every session day. See `docs/usability_testing/Moderator_Runsheet.md` §1. |

## 3. The path, end to end

```
  PHASE 1 — DESIGN & PREPARE            (mostly done)
    [x] task scenario + success criteria      docs/usability_testing/Task_Scenario_D.md
    [x] metrics defined                       docs/usability_testing/Metrics_Table.md
    [x] session note template                 docs/usability_testing/session_notes/Session_Notes_TEMPLATE.md
    [x] recruiting kit + consent script       docs/usability_testing/Recruiting_Kit.md
    [x] SUS instrument (VI/EN) + probes       docs/usability_testing/SUS_Instrument_VI_EN.md
    [x] moderator run-sheet                   docs/usability_testing/Moderator_Runsheet.md
    [ ] decisions in §2 above settled                         <- YOU
    [ ] 6 people screened, invited, scheduled (+2 reserves)   <- YOU
    [ ] participant accounts pre-created, environment tested  <- YOU
    [ ] screen recorder smoke-tested end to end               <- YOU

  PHASE 2 — RUN                          (nothing here can be automated or delegated)
    [ ] PILOT session          -> fix the script, DO NOT count the data
    [ ] P1 [ ] P2 [ ] P3 [ ] P4 [ ] P5
        each: consent -> T1 -> moderator resolves -> T2 -> SUS -> probes -> notes within 10 min

  PHASE 3 — ANALYSE & REPORT             (I can do most of this once real data exists)
    [ ] 5 session notes complete            docs/usability_testing/session_notes/Session_P1..P5.md
    [ ] SUS rows entered + scored           docs/usability_testing/SUS_Responses.csv
    [ ] metrics tabulated                   docs/usability_testing/Metrics_Table.md
    [ ] observations clustered -> findings, ranked 0-4
    [ ] usability report written            docs/03_Task2_Usability_Report_ScenarioD.md
    [ ] new findings appended D-023+        docs/05_Bug_Usability_Findings_Log.md
    [ ] each new finding submitted to the Google Form (§7)
    [ ] README §16 self-assessment updated off 0
```

**The critical path is recruiting.** Everything in Phase 1 is written; nothing in Phase 2 or 3 can
start until six real people have said yes. Start there today.

## 4. Phase 3 in detail — from notes to report

Do these in order. Each step consumes only the step before it, so a mistake is cheap to redo.

### 4.1 Score the questionnaire

Enter one raw row per participant (values 1-5, **not** reverse-adjusted — the script does that) in
`docs/usability_testing/SUS_Responses.csv`, then, from `HW03/`:

```bash
python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/SUS_Responses.csv --instrument sus --markdown
```

Paste the table into `docs/usability_testing/Metrics_Table.md`. Report **all five individual
scores, the mean, and the range** — a mean of 68 from `68,68,68,68,68` and from `40,50,68,90,92`
describe different products and only the spread tells them apart.

### 4.2 Tabulate task metrics

Fill the success / time / errors table in `docs/usability_testing/Metrics_Table.md` from the five
session notes. At n = 5, report **counts** (`3/5 completed`), never percentages. A task where you
intervened is not a clean Complete — mark it Partial and say where you stepped in.

### 4.3 Cluster observations into findings

Group by **cause, not symptom**. Three participants hesitating in three different places for the
same underlying reason is **one** finding, and saying so is worth more than three thin ones.

Then apply the split:

- **Systemic design problem** — appears in **≥ 2 of 5 sessions**, *or* once with a structural cause
  you can name (control below the fold, label that means something else in Vietnamese, no feedback
  after submit). These become findings.
- **Individual slip** — one participant, once, no structural explanation. Report as an observation
  in the report body. Do **not** promote it to a finding to pad the count.

### 4.4 Rank severity 0-4

Judge frequency, impact and **persistence** together — persistence is the one people drop, and a
small friction that keeps costing every user forever outranks a dramatic one-off.

| | |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor |
| 3 | Major — high priority |
| 4 | Catastrophe — fix before release |

### 4.5 Write the report

`docs/03_Task2_Usability_Report_ScenarioD.md` already carries the required skeleton, section by
section, with the brief's rubric elements mapped in its header: the scenario (§3) · the participant
table, 5 people, masked (§5) · the metrics tables (§6, §7) · findings ranked by severity **with a
screenshot each** (§9) · the prioritised recommendation list (§11). It also holds the slots that are
easy to lose: the **pilot** and what it changed (§4), the **probe-question** responses across the
five (§8), the **observations that are not findings** (§10), **Limitations** (§12), and the
**§7 handoff table** mapping each finding to its log ID and form-submission timestamp (§13).

Fill every section; do not delete one as "not applicable". The Limitations section is pre-seeded
with the ones that already apply (n = 5, the D1-D2 participant scope with D3/D4 moderator-driven,
single browser/device, recruiting bias, moderator-is-author, known defects present during the
sessions) — add whatever the sessions as actually run add to it.

Screenshots for findings go in `reports/evidence_task2/`, named per
`docs/usability_testing/Moderator_Runsheet.md` §7.

### 4.6 Feed the findings back into §7

Genuine defects and usability improvements found in Task 2 are appended to
`docs/05_Bug_Usability_Findings_Log.md` as **D-023 onwards** (D-001…D-022 are taken — D-020…D-022
came from Task 3; D-013, D-014 and D-018 are retired and must not be reused), typed `Usability`
with the 0-4 severity, and each one **also submitted to the Google Form**. The TA may cross-check
the counts, so the log and the form must agree. Then re-run, passing **every** evidence root the
log now references (omitting one makes every finding rooted there look like missing evidence):

```bash
python .claude/skills/findings-log/scripts/check_findings.py docs/05_Bug_Usability_Findings_Log.md --evidence-root reports/evidence_task1b --evidence-root reports/evidence_task3 --evidence-root reports/evidence_task2
```

## 5. The §12 line, stated plainly

An AI can design this study, score it, cluster it and draft the report. **It cannot be a
participant, recruit one, or supply a single session's data.** Every participant, quote, timing and
SUS answer in the final report must come from a real person you actually sat with. The TA may phone
2 of the 5 to verify; impersonation is 0 for Task 2, and a fabricated study also poisons every
conclusion drawn from it.

So: the tables in `docs/usability_testing/Participants_Table.md`,
`docs/usability_testing/Metrics_Table.md`, `docs/usability_testing/SUS_Responses.csv` and the five
`Session_P*.md` files stay empty until you have run the sessions. That empty state is honest, and
it is the reason the README self-assesses Task 2 at 0 rather than guessing.

## 6. Definition of done

Task 2 is finished when all of these are true:

- [ ] 6 real people took part (1 pilot + 5 counted), all outside this class, contact details held
      unmasked privately and **masked** in `docs/usability_testing/Participants_Table.md` with
      **exactly four** middle digits hidden (`0901234567` → `090****567`), per §6/§12
- [ ] Pilot ran first, its fixes were applied before P1, and what it changed is written into
      `docs/03_Task2_Usability_Report_ScenarioD.md` §4
- [ ] 5 session-note files exist, each with consent recorded **before** recording started, screen
      (and audio where consented) captured, a timestamped observation log covering friction,
      errors, hesitations and verbalised frustration, task outcomes and SUS answers
- [ ] `docs/usability_testing/SUS_Responses.csv` has exactly 5 real rows and the scorer runs clean.
      The file currently holds **only the header row** — the worked `EXAMPLE` row lives in
      `docs/usability_testing/SUS_Instrument_VI_EN.md` §5 as a format illustration and must never be
      pasted into the CSV or scored
- [ ] `docs/usability_testing/Metrics_Table.md` filled with counts, times, errors and SUS scores
- [ ] `docs/03_Task2_Usability_Report_ScenarioD.md` complete, every section filled: method ·
      screens · scenario · pilot · participants · task metrics · SUS · probe responses ·
      severity-ranked findings **each with a screenshot** · non-finding observations · prioritised
      recommendations traced to findings · limitations · §7 handoff table
- [ ] New findings appended to `docs/05_Bug_Usability_Findings_Log.md` from D-023 and submitted to
      the Google Form, counts consistent
- [ ] The Task 2 AI interactions appended to `docs/06_AI_Audit_Report.md`, stating explicitly that
      the sessions and participants were **not** AI-produced
- [ ] README §"Status by task" and §16 self-assessment updated to the real number

## 7. Files in this folder and when each is used

| File | Used when |
| --- | --- |
| `docs/usability_testing/00_Run_Plan.md` | this file — the plan |
| `docs/usability_testing/Recruiting_Kit.md` | before booking: screener, invite text, consent script |
| `docs/usability_testing/Task_Scenario_D.md` | the study design: tasks, success criteria, probes |
| `docs/usability_testing/Moderator_Runsheet.md` | open during every session |
| `docs/usability_testing/SUS_Instrument_VI_EN.md` | at the end of every session, then for scoring |
| `docs/usability_testing/session_notes/Session_Notes_TEMPLATE.md` | copied to `Session_P<n>.md` per session |
| `docs/usability_testing/Participants_Table.md` | filled as people are recruited |
| `docs/usability_testing/SUS_Responses.csv` | one row per session, immediately after |
| `docs/usability_testing/Metrics_Table.md` | after all 5 sessions |
| `docs/03_Task2_Usability_Report_ScenarioD.md` | the graded deliverable, written last |
