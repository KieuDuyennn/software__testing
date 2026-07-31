# Task 2 — Metrics table — Scenario D

> Fill in once the 5 real sessions have run. Report **counts**, not percentages, at n = 5 — a
> percentage implies more precision than 5 data points support.

## Per-participant results (the raw table everything else is derived from)

Transcribed from the five `session_notes/Session_P<n>.md` "Task outcomes" tables — one row per
participant per task, nothing aggregated yet. The pilot is **not** a row here. Mark `Intervened`
`Y` wherever the moderator gave a task-specific hint or clicked for the participant; an intervened
run cannot count as a clean Complete and its time is excluded from the mean below
(`docs/usability_testing/Moderator_Runsheet.md` §6).

| P | Task | Result (Complete / Partial / Fail) | Time on task | Errors | Hesitations | Intervened (Y/N) | Route used to reach the response (T2) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | T1 | | | | | | — |
| P1 | T2 | | | | | | |
| P2 | T1 | | | | | | — |
| P2 | T2 | | | | | | |
| P3 | T1 | | | | | | — |
| P3 | T2 | | | | | | |
| P4 | T1 | | | | | | — |
| P4 | T2 | | | | | | |
| P5 | T1 | | | | | | — |
| P5 | T2 | | | | | | |

## Task success (aggregate — the "success rate, mean time, errors" table §6 Phase 3 asks for)

Success rate is reported as a **count out of 5**, not a percentage: at n = 5 a percentage claims
precision the sample cannot carry, and `4/5` and `80%` are the same fact with different honesty.

| Task | Success rate (Complete, of 5) | Partial | Fail | Mean time (clean Completes only) | Time range | Total errors | Total hesitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 — file the report | _/5 | _/5 | _/5 | | – | | |
| T2 — find the response | _/5 | _/5 | _/5 | | – | | |

State beneath the table how many runs were excluded from each mean and why (intervention, product
defect, aborted session) — a mean over 3 of 5 runs that is presented as a mean over 5 misreports
the study.

## SUS scores

Run: `python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/SUS_Responses.csv --instrument sus --markdown`
and paste the output table here.

| Participant | SUS score | Adjective |
| --- | --- | --- |
| P1 | | |
| P2 | | |
| P3 | | |
| P4 | | |
| P5 | | |
| **Mean** | | |

n = 5, SD = , range – . Reported descriptively — n is too small for a statistical claim.

## Interpretation note

Five participants surface most of the *findable* problems in a formative, single-user-group study,
but support no statistical claim (no significance, no confidence interval, no benchmark
comparison). Report "3 of 5 participants hit X," give the SUS mean alongside the five individual
scores, and let the severity ranking in the Usability Report carry the argument.
