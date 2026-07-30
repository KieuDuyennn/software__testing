---
name: gui-checklist-design
description: Author or audit a GUI checklist as a reusable instrument — items traceable to recognised heuristics (Nielsen, Norman, Shneiderman), WCAG, a product survey and team experience, each item written so it can actually fail. Use to create, extend or renumber a checklist, define interface-quality criteria, or audit one for coverage gaps, dead citations, unfailable items, or traceability drift. About the checklist itself, never any particular screen. Trigger on "GUI checklist", "xây checklist giao diện", "bộ tiêu chí đánh giá giao diện", "checklist của mình thiếu gì", "rà soát checklist", "audit my checklist", "does my checklist cover". Do NOT use once a checklist exists and the request is to apply it to screens and record Pass/Fail — that is gui-checklist-execution, including "đánh giá heuristic" for named screens.
---

# GUI checklist design

A checklist is an **instrument**: it says how to check and what good looks like. It records no
results. Keeping that boundary is what makes it reusable across screens, across people, and across
projects.

Two things make a checklist good, and they pull in opposite directions: **authority** (every item
traces to a source, so nobody can dismiss it as opinion) and **executability** (someone can
actually run all of it in the time available). Design for both from the start; retrofitting either
one is expensive.

## The four grounding pillars

An item that traces to none of these is an opinion in checklist clothing.

| Pillar | What it supplies | Who can supply it |
| --- | --- | --- |
| **Standards** | Objective thresholds — WCAG success criteria with their real numbers (contrast 4.5:1, status messages, focus visible, non-text content) | Agent, from the spec |
| **Heuristics** | Vocabulary and authority — Nielsen's 10, Norman's 6, Shneiderman's 8, plus any course or house material | Agent |
| **The real product** | Items that name widgets that exist, in the words the UI uses | Agent, via `web-ui-survey` |
| **Team experience** | What actually annoyed real users of *this* app — things no framework predicts | **Only humans** |

Pillar 4 is the one to be explicit about. Everything else is derivable from a document or an
observation, which means an agent can reproduce it and it carries no evidence of judgement. Ask
the people who use the app for one or two items each, ask *why* no framework would have produced
them, and record the answer. If you are the agent, do not invent pillar-4 items — say the pillar is
thin and hand it back.

## Sequence

**1. Survey the product first.** Run `web-ui-survey`, or read an existing survey. Writing items
before knowing what the app contains produces items for widgets that do not exist — a carousel
where there is a static hero, a date picker where there is a custom control — and each one costs a
rewrite later or produces a false result.

**2. Enumerate the coverage dimensions before writing any item.** Take whatever the engagement
defines as its aspects (general UI standards / forms / navigation / feedback-and-state is a
serviceable default) and list, in the specification's own words, every element named under each.
That word list is the thing you check coverage against later. Skipping it is the root cause of the
most common gap: an agent grounded in screenshots and heuristics covers what it was pointed at and
reports full coverage of everything else.

**3. Generate a first pass.** For each aspect, write items in a fixed shape:

| Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |

- **Verification Rule** — what to do, concretely enough that two people do the same thing. Name
  the screen, the control, the setting ("DevTools → Network → Slow 3G", "lower rows-per-page to
  the smallest value the dropdown offers").
- **Expected Behavior** — what counts as a pass, stated so a fail is unambiguous.

**4. Verify in a separate pass, against different grounding.** This is not optional polish; it is
where most real defects in a checklist are found. See below.

**5. Reduce to something executable.** A 66-item checklist that nobody finishes is worse than a
53-item one that gets run. When cutting, protect items that are the sole carrier of a framework
citation or of a specification-named element, then renumber contiguously and publish an old→new
ID map so work in flight can be rebased.

## The verification pass

The first pass asked "what checks follow from these materials?". The second must ask a
*differently-shaped* question, or it will find nothing:

> What does the specification require that this checklist lacks?

Concretely:

- **Build the conformance map** — a table of every element the spec names → the items covering it.
  Building the table is what exposes gaps; reading the checklist does not. Empty rows are your
  missing items.
- **Hunt coverage illusions.** A word appearing inside another item's prose is not coverage. "and/or
  upload progress" tucked into an expected-behaviour cell does not cover progress indicators. Search
  the checklist for each spec term and check whether it heads an item or merely appears.
- **Check the citations rather than trusting them.** Run `scripts/check_checklist.py`. It reports
  principles cited zero times (a suspicious gap — if a whole aspect is about feedback, a
  feedback-related principle uncited is a signal) and principles cited by many items, which is
  usually one principle being used as a catch-all. Plausible-looking citations are the norm from a
  first pass and they read as authoritative.
- **Look for the missing dimension, not just missing items.** The highest-value gap found in
  practice was structural: every feedback item concerned actions that *succeeded*, and none
  concerned what the user sees when an action *fails*. Screenshot-grounded work is systematically
  biased to the happy path, because nobody screenshots a 500 error. Ask what whole category of
  state is absent — failure, empty, loading, offline, unauthorised, mid-transition.
- **Test each item for failability.** "No function should be buried more than one level deep" is a
  design opinion; two testers will disagree. "Simulate a scan" is undefined. Rewrite anything where
  two competent people could record different results from the same screen.
- **Check the arithmetic.** An item asserting that a summary count equals the rows displayed is
  false for any paginated table, and would generate a confident false bug report.

## Do not pad to a number

Asked for exactly N items, it is tempting to split one rule in two. That inflates the count and
adds no coverage — and it is visible to anyone who reads the pair. If the material yields fewer
than N genuine items, say so and say what would have to be split.

## Sharing one checklist across scopes

When several people run the same checklist against different screens, some items address widgets
absent from a given screen. Marking those Pass is false; Fail invents a defect. Define three
results up front:

- **Pass** — applies here, expected behaviour observed.
- **Fail** — applies here, expected behaviour not observed. Evidence required.
- **N/A** — the widget is absent from this screen. **A one-line reason is mandatory**, otherwise
  N/A becomes a place to hide unexecuted items. Never count N/A as a pass.

Report *designed / applicable / executed / passed / failed* separately. And keep the item wording
identical for everyone — per-person edits destroy comparability, which is the reason to share an
instrument at all.

## Deliverables

1. **The checklist** — items in the five-column shape, plus the conformance map, a per-widget
   coverage map, and a framework-coverage table. These three tables are what make coverage
   auditable instead of asserted.
2. **Sources and traceability** — every source with the specific sections used, and source → item
   tables. **Regenerate these with `scripts/check_checklist.py --emit-traceability`, never by
   hand.** Hand-maintained traceability goes stale the first time items are renumbered, and stale
   tables pointing at item IDs that no longer exist discredit the whole artefact.
3. **The prompt chain**, if AI was used — see `ai-audit-log`.
4. **"Items added beyond the AI output, and why the AI missed them"** — one row per item, with a
   root cause, not a restatement. Good root causes are mechanical: *focus state leaves no trace in
   a still image*; *`alt` lives in the source, not in rendered pixels*; *reordering is a gesture and
   has no static appearance*; *the spec's own element list was never in the prompt*. This table is
   usually the most useful thing in the deliverable, because it is where the method gets examined
   rather than the output.

## Keeping results out

Whatever you notice while surveying, do not write it into the checklist as a verdict. Two reasons
beyond tidiness: it has no evidence behind it, and in a shared instrument it forces everyone
downstream to inherit a finding they did not make. Put it in a neutral *areas to examine* list and
let execution produce the result.

## Validate before you ship

```bash
python .claude/skills/gui-checklist-design/scripts/check_checklist.py <checklist.md>
python .claude/skills/gui-checklist-design/scripts/check_checklist.py <checklist.md> --emit-traceability
```

Verify structure by script rather than by assertion. Item counts, duplicate and missing IDs, and
citation coverage are exactly the claims that quietly rot as a checklist is revised — and the
claims a reviewer can check in seconds.
