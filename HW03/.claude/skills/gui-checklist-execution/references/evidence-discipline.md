# Evidence discipline

> Vendored copy. The original lives at `web-ui-survey/references/evidence-discipline.md`; this
> duplicate exists so `gui-checklist-execution` still works when installed on its own. Change both
> or neither.

Rules for making claims about a running application. Every one of these was learned from a wrong
claim that survived multiple review passes, so the failure each prevents is described concretely
rather than as a principle.

Read this before surveying an app, and again before recording any test result. It applies equally
to `web-ui-survey`, `gui-checklist-execution` and `cross-platform-matrix`.

---

## 1. A negative result describes your instrument, not the product

When a selector matches nothing, the honest statement is "my query matched nothing". Turning that
into "the product has no X" is an inference, and it is wrong often enough to be dangerous.

Three real cases, all from one survey, all wrong in the same direction:

| Query run | Concluded | Reality |
| --- | --- | --- |
| `progress, [role=progressbar]` | "no progress bar anywhere" | Five horizontal bar meters existed, built from styled `div`s with inline widths |
| text match on `"back"` | "no back control on this page" | A round icon-only `←` button sat beside the page title, with no text at all |
| `input[type=date]` census on one form | "the app uses no native date inputs" | A different screen's filter panel had two of them |

Notice the bias: **a selector-based survey systematically under-reports what exists.** Absence is
the cheap answer and the wrong one. Presence claims are comparatively safe — if you found it, it
is there.

So: **a claim of absence needs a second instrument of a different shape.** Query the DOM *and*
look at a screenshot. If they disagree, the screenshot wins, and the interesting question becomes
why the query missed it — usually because the widget is semantically generic, icon-only, or drawn
in CSS.

## 2. Scope every claim to what you actually looked at

"The app has no required-field attributes" and "the admin event form carries zero `required`
attributes" cost the same to write. The first is probably false and will be refuted; the second
is a fact and stays useful.

Generalising from one form, one page or one role to the whole product is the single most common way
a survey becomes wrong. Name the page. Name the role.

## 3. Separate interface chrome from user-generated content

`innerText` on a table returns the app's labels and the users' data as one undifferentiated
string. A date-shaped substring in that blob is more likely a title someone typed than the app's
date format.

One survey reported the app rendered timestamps as `8:07 25/07`. That string was the *title of a
support request a student had typed*. A bug report quoting it would have been closed immediately —
and worse, it concealed the genuine inconsistency, which was a different pair of formats entirely.

Before drawing conclusions from text: establish which element it came from, and whether that
element holds chrome or data.

## 4. Record volatile values as volatile

Record counts, dates, ids and totals with a timestamp, and mark them as drifting. Two failure
modes otherwise:

- A check written against a remembered number ("Pending should be 4") fails for the wrong reason
  later, or passes by coincidence.
- A dataset that fits on one page makes a pagination or count check *unfailable* — you have to
  change rows-per-page before the check means anything.

Anything a check depends on must be re-read live at execution time.

## 5. An absence you cannot reach is not an absence

If a widget is only reachable after a write you are not allowed to perform, or behind a role you
do not hold, or behind a precondition you have not satisfied (a profile field, a prior
registration), record it as **unreached** with the blocker named. Recording "not present" for
something you could not get to produces a false Fail that looks identical to a real one.

A concrete instance: a QR-code button that is disabled until the account has a member code. A
survey that stops at "the button does nothing" has found a precondition, not a defect.

## 6. Verify with evidence you did not produce

Four wrong claims in one survey survived a conformance audit, a coverage audit and two further
survey passes — every one of them agent-run. They fell within minutes once screenshots taken by a
person were used as the control.

Re-asking the same question in a new pass does not help when the error is in the instrument rather
than the reasoning, because every pass looks through the same instrument. What breaks the loop is
changing the *kind* of evidence: from queries you ran to images someone else captured, from your
own summary to the raw artefact, from your description of a file to the file.

## 7. Do not let a survey drift into judgement

Surveys inventory; executions judge. The pressure to write "and this is clearly broken" is strong
once you are looking at something odd, and it is worth resisting for two reasons beyond tidiness:

- The verdict has no evidence behind it yet. Nobody ran the check.
- If the survey is shared, everyone downstream inherits a finding they did not observe and cannot
  defend.

Write it as an **area to examine** — a place to look, not a result. Then whoever executes finds it
themselves, captures their own evidence, and describes it in their own words.

## 8. Say what you did not do

A survey with a stated coverage boundary is usable. A survey that quietly omits the roles, pages
and interactions it never touched reads as complete and misleads every stage downstream. List the
uncovered roles, the pages you could not reach, and the interactions you declined to perform.
