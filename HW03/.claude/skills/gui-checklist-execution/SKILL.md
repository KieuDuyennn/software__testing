---
name: gui-checklist-execution
description: Run an existing GUI checklist against named screens of a live web application, recording Pass / Fail / N/A per item with evidence that shows the state being claimed, and producing an execution report plus a set of defensible findings. Use once screens have been chosen and a checklist or heuristic evaluation must actually be carried out against them, and when an existing execution report needs auditing for unsupported results, missing evidence, or items marked N/A without justification. Trigger on "run the checklist", "chạy checklist", "kiểm tra màn hình … theo checklist", "đánh giá heuristic cho các màn hình này", "GUI review of these pages", "evaluate these screens against the checklist", "fill in the Pass/Fail column". Do NOT use to write or audit the checklist itself (gui-checklist-design), to inventory an app before any checklist exists (web-ui-survey), or to run the same screen across several browsers and devices (cross-platform-matrix).
---

# GUI checklist execution

Execution turns an instrument into evidence. The output is one result per (item × screen), each
Fail backed by a capture someone can reproduce from.

Two failure modes dominate, and they are opposites. **False Fails** come from concluding absence
from a query that was blind to the widget, or from a precondition you never satisfied — they waste
a reviewer's time and get refuted in seconds. **Silent skips** come from marking N/A because an
item looked awkward. Both are avoidable with the discipline below.

Read `references/evidence-discipline.md` first. Sections 1, 3 and 5 are the ones that bite hardest
during execution.

## Before you start

- **Get the checklist and freeze it.** Do not reword items while executing. If an item is
  genuinely unexecutable, record that as feedback on the instrument — do not quietly reinterpret
  it, because then your results are not comparable with anyone else's.
- **Name the screens** and why they were chosen, against whatever scope rules the engagement has.
- **Confirm the account and role** for each screen. Role-conditional UI means a result recorded
  under the wrong role is meaningless.
- **Read the survey**, if one exists, for the URL map, volatile values and areas to examine.
- **Settle write permission.** Some items need a destructive or state-changing action
  (delete-confirmation dialogs, unsaved-changes warnings, offline submission). On a shared system,
  ask first, and prefer acting on a record you created yourself.

## Work screen by screen, not item by item

Open a screen, run every applicable item against it, then move on. Iterating item-first means
re-navigating for every one of them, and re-navigation is where state gets lost and results drift.

Take a full-page capture of each screen in its resting state before you start. It costs one action
and it is the reference you will want when a later item is ambiguous.

## Recording a result

| Result | Requirement |
| --- | --- |
| **Pass** | The item applies and the expected behaviour was observed. |
| **Fail** | The item applies, expected behaviour absent. **Screenshot + a Notes line saying what was expected and what happened instead.** |
| **N/A** | The widget genuinely does not exist on this screen. **One-line reason, mandatory.** |

N/A without a reason is an unexecuted item wearing a costume. Never count N/A as a pass; report
*applicable / executed / passed / failed* separately from the designed total.

### Before recording any Fail

1. **Cross-check the instrument.** If your evidence is a selector that matched nothing, look at
   the screen. Icon-only controls, bar meters built from styled `div`s and CSS-drawn markers are
   invisible to the obvious query. A Fail from a DOM query alone is a coin flip.
2. **Check the preconditions.** A disabled control may be gated on state you have not created — a
   missing profile field, no prior record, an expired window. That is a precondition, not a defect,
   though *whether the disabled state explains itself* is a legitimate separate finding.
3. **Re-read the live values.** Never test against a number remembered from a survey. And notice
   when the current data makes an item unfailable: if the whole dataset fits on one page, a
   pagination or count check cannot fail until you lower rows-per-page.
4. **Rule out a legitimate platform difference.** A native control rendering its own locale format,
   a platform scrollbar, a system font substitution — these are the platform behaving correctly.
5. **Reproduce it once.** If it does not reproduce, say so in Notes and treat it as intermittent
   rather than dropping it; intermittent is a real category.

### One item can hide two independent failures

When an item contains two claims that can fail separately — *this label is arithmetically correct*
and *the five lists agree with each other* — score and report them separately. Collapsing them into
one Fail loses which one broke, and a fix for one will not fix the other.

Conversely, one root cause showing on three screens is **one finding with three instances**, not
three findings. See `findings-log`.

## Items an agent must not execute

Some items depend on the physical or perceptual world. Executing them by inference produces a
result that looks identical to a real one, which is worse than leaving them blank:

- whether a QR or barcode **physically scans** with a phone camera
- what a **screen reader announces** (you can verify `role`/`aria-live` are present; you cannot
  verify the announcement)
- how something **renders on a real device** — see `cross-platform-matrix`
- whether text is *comfortably* readable, or a colour pairing is pleasant

For each, either hand it to a person and record who executed it and when, or mark it
**not executed** with the reason. Contrast ratios are the useful counter-example: measurable, so
measure them and record the number rather than an impression.

## Output

```markdown
# Execution report — <scope> — <name>
Checklist version: <vX.Y, N items>   Environment: <URL>   Dates: <range>
Screens: <S1 (role) · S2 (role) · S3 (role)>  — and why these

## Summary
| Screen | Applicable | Executed | Pass | Fail | N/A |
Designed: N. Never counting N/A as a pass.

## Results — <screen 1>
| Item ID | Result | Notes | Evidence |
| IA02-01 | Fail | Three required fields carry no `required`; asterisk is CSS-drawn so absent from the accessibility tree. Expected: requirement exposed programmatically. | S1_IA02-01_required.png |
| IA02-05 | N/A  | No rich-text editor on this screen. | — |

## Items not executed
| Item ID | Screen | Why | Who should execute it |

## Findings raised
Ids into the findings log, so the two artefacts reconcile.
```

Name evidence files `<Screen>_<ItemID>_<slug>.png`, and make sure each capture shows the URL and
the state being claimed. A screenshot that does not show what the Notes assert is not evidence.

## Notes that survive review

A Fail note needs three things: **what was expected, what happened, and the measurement**. "Looks
wrong" is not reviewable. "The bar renders full-width while its own label reads `0 (0%)`" is —
and it survives the dataset changing underneath it.

Quote the app's own strings exactly, including language and punctuation. Paraphrased UI text makes
a finding unreproducible, and it is the first thing a developer checks.

## Handing off

Every Fail becomes a record in `findings-log`. If AI assisted, log the session with
`ai-audit-log` — and record which results the agent produced versus which a person produced,
because the distinction is what makes the report auditable.
