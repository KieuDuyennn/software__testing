# Bug & Usability Findings Log — Scenario D (Lê Phạm Kiều Duyên, 23127184)

> **§7 mandatory aggregated file.** Every finding here must also be submitted to the Google Form
> (https://forms.gle/CJQFQCAXcsDbXDMM9) using the student-ID email, and the two must stay
> consistent — the TA may cross-check counts.
>
> **Status: 1 finding logged so far (2026-07-30), from a first live Task 1B pass.** Task 2 / Task 3
> have not run yet. This file is validated by `.claude/skills/findings-log/scripts/check_findings.py`;
> run it again after adding rows:
>
> ```bash
> python .claude/skills/findings-log/scripts/check_findings.py findings/Bug_Usability_Findings_Log.md --evidence-root .
> ```
>
> **Never add a row for something that was not actually observed and not actually submitted to
> the form.** A finding invented to fill this table is worse than an empty one — see
> `.claude/skills/findings-log/SKILL.md` §"What not to log".

## Totals (keep in sync with the table below)

| Source | Bug — Blocker | Bug — Critical | Bug — Major | Bug — Minor | Bug — Trivial | Usability 4 | Usability 3 | Usability 2 | Usability 1 | Usability 0 | Total |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Task 1B (checklist execution) | 0 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 |
| Task 2 (usability sessions) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Task 3 (cross-platform) | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| **Grand total** | **0** | **0** | **1** | **0** | **0** | **0** | **0** | **0** | **0** | **0** | **1** |

## Findings

| ID | Scenario/Screen | Type | Description | Steps/Heuristic | Severity | Suggested fix | Screenshot ref | Form-submission timestamp |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| D-001 | D1 — `/complaints/new` | Bug | Selecting a value in the "Request type" dropdown and then clicking elsewhere within roughly the next second intermittently discards the selection (reverting to the placeholder and showing "Vui lòng chọn một mục trong danh sách") or silently swaps it for a different option the user never clicked — without the user reopening the dropdown or taking any dropdown action. | 1. Log in as a student, go to `/complaints/new`. 2. Click the "Request type" combobox, click "Support". 3. Immediately (within ~0.5 s) click into the "Issue requiring support" field below. 4. Observe: Request type reverts to the unselected placeholder and the required-field error appears (or the value silently changes to a different option), even though no dropdown interaction occurred in step 3. Reproduced twice this way; did not reproduce when a ~2 s pause was inserted between steps 2 and 3 — consistent with the dropdown's closing/blur transition still intercepting the next click for a short window. Related checklist items IA02-01 (required-field marking) and IA02-09 (submit blocked with a clear summary), though neither is a clean match — see `task1b_execution/Execution_Report_ScenarioD.md` §"Findings raised" for why this is logged standalone. | Major | Ensure the dropdown's option list is not pointer-interactive (or has released focus/blur handling) during its close transition, so a click immediately after selection lands on the intended next element rather than being absorbed by the closing listbox; and make sure the selected value is committed to form state synchronously on click, not after an animation-dependent timeout. | D1_IA02-01_requesttype_selected_before_blur.jpg, D1_IA02-01_requesttype_reset_after_blur.jpg | TODO |

### Column guide (§7 required columns)

- **ID** — stable, never reused. Use `D-001`, `D-002`, … (scope-prefixed with `D` since this is the
  Scenario-D log; keeps IDs distinguishable from teammates' A-/B-/C- logs if merged at group level).
- **Scenario/Screen** — `D1` / `D2` / `D3` / `D4`, or the usability-session task / cross-platform
  cell it came from.
- **Type** — `Bug` (behaves contrary to spec or breaks) or `Usability` (works, but costs the user).
  Different severity scale each — see below.
- **Description** — one or two sentences, quoting the app's own strings exactly.
- **Steps/Heuristic** — for a `Bug`: numbered repro steps from a known state (URL, account, role,
  precondition). For a `Usability` finding: the heuristic or checklist item it violates (e.g.
  `IA04-14`, `Nielsen H1`).
- **Severity** — **Bug**: Blocker / Critical / Major / Minor / Trivial. **Usability**: 0–4
  (Nielsen). Never blend the two scales in one column.
- **Suggested fix** — concrete enough to argue with, not "improve UX."
- **Screenshot ref** — a filename that actually exists under `task1b_execution/evidence/`,
  `usability_testing/evidence/`, or `cross_platform/evidence/`.
- **Form-submission timestamp** — fill in only after the finding has actually been submitted to
  the Google Form; leave `TODO` until then, never a fabricated timestamp.

### Severity scales (do not mix)

**Bug** — impact on function:

| | Meaning |
| --- | --- |
| Blocker | Core flow cannot be completed; no workaround |
| Critical | Major function broken or data lost; workaround is painful |
| Major | Function impaired, workaround exists |
| Minor | Small deviation, easily worked around |
| Trivial | Cosmetic, no functional effect |

**Usability** — Nielsen 0–4, judged on frequency + impact + persistence together:

| | Meaning |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor — low priority |
| 3 | Major — important to fix, high priority |
| 4 | Catastrophe — imperative to fix before release |

An accessibility defect that removes the *only* path for a group of users (e.g. a modal that
ignores ESC for a keyboard-only user) is rated Major/3 at minimum, regardless of how few people it
"functionally" blocks — see `.claude/skills/findings-log/SKILL.md` §"Accessibility findings are
rated from the barrier, not from the flow".

## Cross-cutting causes

_(Fill in once findings exist: which two or more findings share one underlying root cause, so a
reviewer sees the few structural fixes behind the list rather than N unrelated rows.)_
