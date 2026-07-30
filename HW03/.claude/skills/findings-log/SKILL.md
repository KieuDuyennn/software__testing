---
name: findings-log
description: Maintain one normalised log of defects and usability findings a testing engagement has already produced — stable IDs, developer-reproducible steps, Bug or Usability severity on the correct scale, suggested fix, evidence references — deduplicated and reconciled against whatever tracker they were submitted to. Use to collect observations into findings, merge or dedupe them, rate severity, write bug reports, or check against what was actually submitted elsewhere. Trigger on "bug report", "findings log", "tổng hợp lỗi", "báo cáo lỗi", "xếp severity cho các lỗi", "deduplicate findings", "đối chiếu với Jira", "viết lại lỗi này cho dev reproduce được", or after any test execution produced failures. Do NOT use to produce the findings in the first place — that is gui-checklist-execution, cross-platform-matrix or usability-test-study, each of which ranks its own observations; this skill begins once a finding is already rated and consolidates across sources.
---

# Findings log

One file, one row per defect, every row reproducible by someone who was not there. A findings log
is read by two audiences with different needs: a developer who must reproduce and fix, and a
reviewer who must confirm the work was real. Both need the same thing — specificity.

## The record

| Field | Rule |
| --- | --- |
| **ID** | Stable and never reused. `F-001`, or scope-prefixed (`D-001`) when several people merge logs. |
| **Scope / screen** | Where it lives — the screen name and the URL, so it can be found. |
| **Type** | `Bug` (behaves contrary to spec or breaks) or `Usability` (works, but costs the user). Keep them distinct; they have different severity scales and different fixes. |
| **Description** | What is wrong, in one or two sentences. Quote the app's own strings exactly. |
| **Steps to reproduce** *(Bug)* | Numbered, starting from a known state: URL, account and role, any precondition. |
| **Heuristic / rule violated** *(Usability)* | The principle or checklist item it fails, so it is a finding rather than a preference. |
| **Expected vs actual** | Both, explicitly. A description of the actual alone is an observation, not a defect. |
| **Severity** | See below. |
| **Suggested fix** | Concrete enough to argue with. "Improve UX" is not a suggestion. |
| **Evidence** | Filename that exists on disk, showing the claimed state and the URL. |
| **Source** | Which activity found it — checklist item id, usability session number, matrix cell. |
| **Submitted at** | Timestamp, if there is an external channel. |

## Severity: use one scale per type and say which

**Bugs** — impact on function:

| | Meaning |
| --- | --- |
| Blocker | Core flow cannot be completed; no workaround |
| Critical | Major function broken or data lost; workaround is painful |
| Major | Function impaired, workaround exists |
| Minor | Small deviation, easily worked around |
| Trivial | Cosmetic, no functional effect |

**Usability** — Nielsen's 0–4:

| | Meaning |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor — low priority |
| 3 | Major — important to fix, high priority |
| 4 | Catastrophe — imperative to fix before release |

Rate a usability finding on three factors together — **frequency** (how many users hit it),
**impact** (how hard to get past), **persistence** (does it keep costing them after they learn the
workaround). A one-off annoyance that everyone hits every time outranks a dramatic problem one
person hit once.

Do not blend the scales into one column. A reviewer cannot tell whether "3" means Major-bug or
Major-usability, and the two prioritise differently.

### Accessibility findings are rated from the barrier, not from the flow

Choosing a scale must never change how bad something is. Splitting Bug from Usability introduces a
specific trap, and it has been observed in practice: an accessibility defect gets filed as a Bug,
then rated on functional impact — "nothing is broken, the form still blocks an empty submit, no data
is lost" — and lands at Minor. That reasoning omits the users the defect actually affects. The
function that broke is the one assistive technology depends on.

Two rules keep it honest:

- **A finding that removes the only path for a group of users is Major / severity 3 at least**, even
  when everyone else completes the flow. A keyboard-only user facing a modal that ignores ESC has no
  non-pointer exit; a screen-reader user given a CSS-drawn asterisk and no `aria-required` is told
  nothing at all.
- **Where the finding fails a normative criterion, cite it and let its conformance level set the
  floor.** A WCAG Level A failure is not Minor, whichever scale you filed it under. Naming the
  criterion also makes the severity arguable on evidence rather than on taste.

Be wary of "users learn the workaround" as an argument for low persistence. For the group actually
blocked, there is nothing to learn — they pay the cost on every encounter.

## Look for cross-cutting causes after logging

Once the rows exist, read them together and ask which *different* findings share one underlying
cause. Two inconsistent date formats and two inconsistent pagination labels are separate defects
with separate fixes, but both are symptoms of presentation logic duplicated per view — and one
architectural change prevents recurrence of both.

This is not the merge rule, which applies to one defect appearing in several places. This is a short
closing section that gives the reader the two or three structural changes behind a long list, and it
is usually the part a development team acts on first.

## Deduplication

**Merge when the root cause is the same.** One inconsistent date format appearing on five screens
is one finding with five instances — a single fix resolves all of them. Log it once and list the
instances.

**Split when the causes differ**, even inside one checklist item. "The count label is arithmetically
wrong" and "the five lists disagree with each other" are two defects with two fixes; one row for
both means one of them never gets fixed.

The test: *would one change fix all of it?* Yes → one finding. No → split.

## Reproducibility is the bar

Write the steps, then read them as a stranger. Would you land in the same state? The usual gaps:

- Starting mid-flow without saying how you got there.
- Omitting the account and role, when the UI is role-conditional.
- Omitting a precondition — a record that must already exist, a profile field, an open window.
- Depending on data that has since changed. Say what the data was *and* what property mattered
  ("a table with more rows than one page holds"), so the finding survives the dataset.
- Paraphrasing UI text. Quote it.

## Reconciling with an external channel

When findings are also submitted somewhere else — a form, a tracker — the two must agree, and
someone will check the counts.

- Submit first, then log with the returned id or the submission timestamp.
- Never log something that was not submitted, and never submit something not in the log.
- If a finding is withdrawn, keep the row and mark it withdrawn with a reason. Deleting rows makes
  the counts disagree and destroys the audit trail.
- State the total in the log header, so a mismatch is visible without counting.

## Validate before you ship

```bash
python .claude/skills/findings-log/scripts/check_findings.py <log.md> --evidence-root <dir>
```

Checks IDs unique, required fields non-empty, severity values legal, evidence files present on
disk, and prints the counts by type and severity. Missing evidence is the most common defect in a
findings log and the one that most damages its credibility — a finding whose screenshot is not
there reads as a finding that was never observed.

## What not to log

- Anything you did not observe yourself. A note from a survey or someone's suspicion is a *place
  to look*, not a finding.
- Platform behaviour working as designed — native controls following the browser locale, system
  fonts, platform scrollbars. Log the *inconsistency* if the app mixes native and custom controls;
  do not log the platform being itself.
- Feature requests. If it is not a defect against a rule or a real user cost, it belongs somewhere
  else, and mixing it in dilutes the log.
