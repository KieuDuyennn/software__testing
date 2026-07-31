# Usability Report — EMS Scenario D (Support requests) — Lê Phạm Kiều Duyên, 23127184

> **Status: NOT YET RUN. 0 of 5 participants recruited, 0 sessions held.** Every table below is an
> empty template. No number, quote, timing, participant or SUS answer in this file may be written
> from anything except a real session actually held with a real person — §12 of the brief makes a
> fabricated participant grounds for **0 on Task 2**, and the TA may telephone up to 2 of the 5 to
> verify them. An AI can design, score, cluster and draft this study; it cannot be a participant,
> recruit one, or supply one session's data.
>
> Fill each section only from `docs/usability_testing/session_notes/Session_P1..P5.md`, scored via
> `docs/usability_testing/SUS_Responses.csv` and tabulated in
> `docs/usability_testing/Metrics_Table.md`. If a section is still empty at submission time, leave
> it empty and say so — an honest gap costs less than an invented fact.

**Section map against the brief.** §6 Task 2 Phase 3 requires the report to contain: the scenario
(§3 below) · the participant table, 5 people, masked (§5) · the metrics table (§6) · the findings
ranked by severity **with a screenshot each** (§8) · a prioritised list of concrete recommendations
(§10). §7 of the brief requires genuine bugs to be logged through the findings channel (§12 below).
Nothing here may be deleted as "not applicable"; each one is separately marked in the rubric.

---

## 1. Method and what was measured

| | |
| --- | --- |
| Method | Moderated think-aloud, one participant at a time |
| Participants | **n = 5** counted, all outside this class, **+ 1 pilot** (not counted) |
| Session length | ~20–25 minutes per participant |
| Session language | Vietnamese (all participant-facing wording; this report is in English) |
| Mode / device | TBD — in person or remote screen-share; participant's or moderator's machine |
| Dates | TBD |
| Instrument | **SUS**, 10 items, administered after both tasks and **before** the probe questions |
| Recording | Screen recording, plus audio where the participant consented; consent captured before recording started |
| Moderator | Lê Phạm Kiều Duyên |

Measures collected, the minimum set named in §6 Task 2 Phase 1:

| Measure | Definition used | Where it lands |
| --- | --- | --- |
| Task success | Complete / Partial / Fail against criteria fixed **before** the sessions (§3) | §6 |
| Time on task | From the participant beginning to act on the prompt until the success criterion; intervened runs excluded from means | §6 |
| Errors | Wrong actions requiring recovery | §6 |
| Hesitations | Pauses of roughly 3 s or more, backtracking, re-reading | §6 |
| SUS | 10 items, 1–5, reverse-scored at positions 2/4/6/8/10 by `score_sus.py` | §7 |
| Open probes | Four fixed questions: clarity · error recovery · speed · trust | §8 |

## 2. Screens under test

| Page the participant reaches | Route | Package screen | Reached in |
| --- | --- | --- | --- |
| Create Support Request form | `/complaints/new` | **D1** | Task 1 |
| My Requests list | `/complaints` | **D2** (list) | Task 2 |
| Request detail with the official response | `/complaints/{id}` | **D2** (detail) | Task 2 |
| Notifications bell / list / detail | `/notifications`, `/notifications/{id}` | **D5** | Only where a participant went there unprompted — record which did |

Three distinct user-facing pages across the same package screens tested in Task 1B
(`docs/02_Task1B_Execution_Report_ScenarioD.md`), plus a fourth reached only by participants who
chose that route. **D3** and **D4** (admin list and admin detail) are operated by the moderator to
resolve each request mid-session and are never shown to a participant — exercised, not user-tested.
See §11.

## 3. Task scenario

Full design, success criteria and moderator script: `docs/usability_testing/Task_Scenario_D.md`.
Goal-oriented, no click path given, and deliberately avoiding EMS's own vocabulary so the task
tests findability rather than reading comprehension.

**Task 1 (verbatim, as spoken):**

> *"Bạn hãy tưởng tượng là bạn đã đăng ký tham gia một sự kiện trên trang web này, nhưng tới hôm
> diễn ra sự kiện, lúc bạn check-in thì hệ thống lại báo là bạn chưa hề đăng ký. Bạn muốn chuyện
> này được xử lý. Bạn hãy dùng trang web để báo lại vấn đề đó, theo cách nào bạn thấy là đúng — các
> thông tin chi tiết (tên sự kiện, ngày bạn đăng ký, v.v.) thì bạn cứ tự nghĩ ra thoải mái nhé."*

English gloss: *"Imagine you registered for an event here, but on the day the check-in said you
were never registered. You want it fixed. Use the platform to report the problem, however you think
is right — invent whatever details you need."*

*Success:* a support request submitted with a request type, a description, and at least one image
attached. *Partial:* submitted but missing the image, or with an unclear description. *Fail:* could
not submit, or gave up.

**Task 2 (verbatim, handed over after the moderator has quietly resolved the request):**

> *"Cái vụ lúc nãy bạn báo đó, giờ bạn thử xem có ai trả lời lại chưa, rồi đọc cho mình nghe họ
> nói gì nhé."*

English gloss: *"That thing you reported earlier — check whether anyone has replied, and read me
what they said."*

*Success:* the participant finds their own request without being told the menu name and reads the
official response back correctly. *Partial:* finds the request but misses or misreads the response.
*Fail:* cannot find where the request went.

## 4. Pilot

Required by §6 Task 2 Phase 1: one extra person, run before the counted sessions, to catch unclear
wording or a broken flow. **Pilot data never enters §6, §7 or §8.**

| | |
| --- | --- |
| Pilot run on | TBD |
| Problems the pilot exposed | TBD |
| Changes made to the script/setup before P1 | TBD — or state explicitly "none needed" if that is what happened |

## 5. Participants

Five real people, all outside this class, contacts masked per §12 (middle four digits). The
unmasked list is held privately by the moderator and is **not** in this repository or the
submission zip. Source of record: `docs/usability_testing/Participants_Table.md` — keep the two
copies identical.

| P | Name (or initials) | Profile | Outside this class | Contact (masked) | Session date | Consent: screen / audio |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | TBD | TBD | TBD | TBD | TBD | TBD / TBD |
| P2 | TBD | TBD | TBD | TBD | TBD | TBD / TBD |
| P3 | TBD | TBD | TBD | TBD | TBD | TBD / TBD |
| P4 | TBD | TBD | TBD | TBD | TBD | TBD / TBD |
| P5 | TBD | TBD | TBD | TBD | TBD | TBD / TBD |

Recruiting channel and screener: `docs/usability_testing/Recruiting_Kit.md` §1–§4. Masking format:
`0901234567` → `090****567`, exactly four digits hidden.

## 6. Metrics — task success, time, errors

Copied from `docs/usability_testing/Metrics_Table.md` once the five sessions are tabulated.
Reported as counts out of 5, not percentages.

| Task | Success rate (Complete, of 5) | Partial | Fail | Mean time (clean Completes only) | Time range | Total errors | Total hesitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 — file the report | _/5 | _/5 | _/5 | | – | | |
| T2 — find the response | _/5 | _/5 | _/5 | | – | | |

Runs excluded from either mean, and why: TBD.

Per-participant breakdown (the table above is derived from this one, in
`docs/usability_testing/Metrics_Table.md` §"Per-participant results"): TBD.

## 7. Metrics — SUS

Scored with
`python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/SUS_Responses.csv --instrument sus --markdown`.
Report all five individual scores, the mean **and** the range — a mean alone cannot distinguish
five participants who agreed from five who were split.

| Participant | SUS score | Adjective |
| --- | --- | --- |
| P1 | | |
| P2 | | |
| P3 | | |
| P4 | | |
| P5 | | |
| **Mean** | | |

n = 5, SD = , range – . Descriptive only: no confidence interval, no significance claim, no
"above/below the industry average" stated as a measurement.

## 8. Probe question responses

Asked after the SUS, same wording every session (Vietnamese wording in
`docs/usability_testing/SUS_Instrument_VI_EN.md` §4). Summarise across the five participants and
quote verbatim where a quote carries the point; attribute each quote to P1–P5 and to a timestamp in
that session's notes.

| Probe | What the five said | Quotes (attributed, verbatim) | Feeds finding # |
| --- | --- | --- | --- |
| **Clarity** — unsure what the platform wanted, or what would happen next | TBD | TBD | |
| **Error recovery** — noticing a mistake and getting back on track | TBD | TBD | |
| **Speed** — anything slower or more effortful than it should be | TBD | TBD | |
| **Trust** — confidence that the report went through and someone would see it | TBD | TBD | |

## 9. Findings, ranked by severity

Severity scale (Nielsen 0–4, as required by §6 Task 2 Phase 3):

| | |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor |
| 3 | Major — high priority |
| 4 | Catastrophe — fix before release |

Rules applied when turning observations into the rows below, per
`docs/usability_testing/00_Run_Plan.md` §4.3:

- Group by **cause, not symptom** — three participants stumbling in three places for one underlying
  reason is **one** finding.
- **Systemic** (a finding): hit in **≥ 2 of 5** sessions, *or* once with a structural cause that can
  be named. **Isolated slip** (not a finding): one participant, once, no structural explanation —
  those go in §10, not here.
- Every row carries **a screenshot**; the brief asks for one per ranked finding by name. Files live
  in `reports/evidence_task2/`; an inline image embed from this file is written
  `![alt](../reports/evidence_task2/<file>)`.
- Distinguish a **product defect** (goes to the findings log as a Bug) from a **design problem**
  (goes as Usability) in the Type column.

| # | Severity (0–4) | Type (Bug / Usability) | Finding | Participants affected (of 5) | Evidence: quote + session timestamp | Screenshot (`reports/evidence_task2/`) | Root cause | Recommendation | Log ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| _(none yet — no sessions run)_ | | | | | | | | | |

## 10. Observations that are not findings

Single-participant slips with no structural cause, and anything interesting that does not meet the
bar in §9. Recorded so the evidence is complete, explicitly **not** counted as findings and not
ranked — padding the finding count with these is how a small study starts overclaiming.

| Observation | Participant | Why it is not promoted to a finding |
| --- | --- | --- |
| _(none yet)_ | | |

## 11. Prioritised recommendations

Concrete and actionable — name the screen, the control, and the change. Ordered by severity first,
then by cost to fix, so the top of the list is what to do on Monday morning. Each row must trace
back to a finding number in §9; a recommendation with no finding behind it is an opinion.

| Priority | From finding # | Screen / control | Concrete change | Severity addressed | Est. effort (S/M/L) |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |

## 12. Limitations

- **n = 5** supports discovery, not measurement. Five was set by the brief, not chosen from a
  cost–benefit curve; no percentage, confidence interval or significance claim is made anywhere in
  this report.
- **Scope is narrower than Task 1B.** Participants exercise D1 and D2 (and D5 only if they went
  there themselves). **D3/D4 are driven by the moderator**, because a usability participant cannot
  be handed an admin account — so the admin side has checklist coverage (Task 1B) but no
  user-testing coverage.
- **Single environment.** One browser, one device class, one network, per §1 — cross-platform
  behaviour is Task 3's evidence (`docs/04_Task3_Cross_Platform_Matrix.md`), not this report's.
- **Recruiting bias.** Participants came from the moderator's own network (see
  `docs/usability_testing/Recruiting_Kit.md` §2), which skews younger and more digitally literate
  than the full EMS population; findability results are therefore, if anything, optimistic.
- **The moderator is also the report's author**, so the observation and the analysis are not
  independent. Mitigated by fixing the success criteria and the probe wording before the first
  session, not after seeing the data.
- **Known defects were present during the sessions** (`docs/usability_testing/Moderator_Runsheet.md`
  §4). Where one caused a task failure, the failure is the product's and is recorded as such — but
  it also means task times are not a clean measure of the intended design.
- TBD — add anything specific to the sessions as actually run: outages, a rescheduled participant, a
  failed recording, a task not reached.

## 13. Handoff — findings channel (§7) and evidence

Every genuine defect and every usability improvement from these sessions is logged in
`docs/05_Bug_Usability_Findings_Log.md` from **D-020 onwards** (D-001…D-019 are taken; D-013, D-014
and D-018 are retired and must not be reused), typed `Bug` or `Usability` with the 0–4 severity, and
**each one also submitted to the Google Form** named in §7 of the brief. The log and the form must
agree — the TA may cross-check the counts.

| Finding # (§9) | Findings-log ID | Submitted to the form (timestamp) |
| --- | --- | --- |
| | | |

**Evidence index.** Session recordings and screenshots are in `reports/evidence_task2/`, named
`P<n>_<task>_<what-it-shows>.<ext>` per `docs/usability_testing/Moderator_Runsheet.md` §7. Raw
session notes are in `docs/usability_testing/session_notes/`; raw SUS answers in
`docs/usability_testing/SUS_Responses.csv`.

AI assistance on this report (study design, scoring, clustering, drafting) is declared in
`docs/06_AI_Audit_Report.md`, which states explicitly that **the sessions, the participants and the
session data were not AI-produced**.
