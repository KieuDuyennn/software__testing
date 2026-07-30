---
name: web-ui-survey
description: Inventory what a running web application actually contains — its pages, URL scheme, widgets, controls and accessibility properties — by inspecting the live DOM, so later test design rests on observed facts rather than assumptions. Use before writing GUI checks, test cases or a UI test plan against a real deployed app; when answering "does this app have X?" without guessing; and when an earlier survey, a test result, or a claim that some widget is absent needs verifying. Produces a durable survey document so later work need not re-browse. Trigger on "survey the app", "khảo sát ứng dụng", "khảo sát giao diện", "inventory the UI", "what widgets does this page have", "app có nút … không", "list the pages and URLs", "check whether the app has". Do NOT use for a questionnaire that people fill in — a "bảng khảo sát", SUS or UEQ-S form is usability-test-study. Do NOT use to apply a checklist to screens (gui-checklist-execution) or to compare browsers and devices (cross-platform-matrix).
---

# Web UI survey

A survey answers one question: **what does this application actually contain?** It records no
verdicts. Getting this stage right is what stops every later stage from testing widgets that do
not exist and missing widgets that do.

The failure mode this skill exists to prevent is specific and common: an agent queries the DOM,
matches nothing, and writes "the product has no X". Read
`references/evidence-discipline.md` before you begin — it is short, and it is the whole point.

## Before you touch the app

Establish these, because a survey that omits them is not interpretable later:

- **Base URL and environment.** A tunnel, a staging box and production render differently.
- **Account and role.** UI is role-conditional. A survey run as an administrator describes the
  administrator's UI and nothing else. If the app has multiple roles, either survey each one or
  state plainly which roles are uncovered.
- **Credentials handling.** Ask the person to log in themselves. Do not accept or type
  credentials — you do not need them to observe, and an audit trail is cleaner without them.
- **Write permission.** Decide up front whether you may create, modify or delete anything. On a
  shared or production system the default is no. See *Not mutating shared state* below.

## How to observe

Use two instruments in parallel, because they fail differently:

| Instrument | Sees | Blind to |
| --- | --- | --- |
| DOM / accessibility tree query | attributes, roles, semantics, exact counts | anything built out of styled generic elements; anything you did not think to query |
| Screenshot read by eye | visual affordances, icon-only controls, layout, bar fills | attributes, ARIA, timing, what happens on interaction |

Browser automation tooling (Claude in Chrome, Playwright) gives you both. Prefer DOM queries for
counting and for attributes — they are cheap and exact. Prefer screenshots whenever the question
is "is there a control here?", because that question is visual and a selector cannot answer it.

For each page record: URL, page title, the role you were signed in as, and then the widgets.

## What to inventory

Work through this list per page rather than free-associating, or the survey will mirror whatever
you happened to notice first:

- **Structure** — layout regions, navigation (menu, sidebar, tabs, breadcrumb), page heading.
- **Data display** — tables (column count and names), lists, cards, empty states, pagination
  controls and the exact wording of any count label.
- **Inputs** — text fields, textareas, selects, checkboxes, radios, switches, date/time controls
  (note native vs custom — this matters, they behave differently), file uploads with their stated
  constraints, rich-text editors.
- **Feedback** — toasts and their container's ARIA role, badges, status pills, confirmation
  dialogs, progress indicators and bar meters, inline validation.
- **Accessibility properties** — presence of `required` / `aria-required`, accessible names on
  icon-only controls, `alt` on images, `aria-live` regions, focus visibility.
- **URL scheme** — how a detail record is addressed. Inconsistency here (one area using a query
  parameter, another a path segment) is worth recording; it constrains deep-link testing later.
- **Absences** — but only those you verified with two instruments, and worded as scoped claims.

## Not mutating shared state

Registering, submitting, deleting and publishing all write to a system other people are using. A
survey does not need any of them: forms can be inspected without submission, and validation
behaviour belongs to the execution stage where the person running it owns the consequences.

Stop at inspection. Where a widget can only be reached by writing something, record it as
**unreached, with the write it would require**, and ask before proceeding. Reaching a page by
performing a destructive action and then reporting the page is a bad trade.

## Output

Write a dated survey file — `UI_Survey_<app>_<YYYY-MM-DD>.md` — structured so later stages can
plan against it without opening a browser:

```markdown
# UI survey — <app> — <date>
Environment: <base URL>   Account/role surveyed: <account> (<role>)
Instruments: <e.g. Chrome via extension; DOM queries + screenshots>
Roles NOT covered: <list, or "none">

## URL map
| Path | Purpose | Requires role |

## Per-page inventory
### <path>
| Widget | Observed | How verified | Note |

## Verified absences
| Claimed absent | Instrument 1 | Instrument 2 | Scope of the claim |

## Volatile values (as at <timestamp>)
Counts, dates and record ids that will drift. Never build a check that hardcodes these.

## Areas to examine
Neutral list of places where something looked worth a closer look during execution.
No verdicts — see below.

## Reusable snippets
Any DOM query worth re-running, so the next survey is a diff rather than a rerun.
```

## Two things to keep out of the survey

**Verdicts.** The moment you write "this is a bug", the survey stops being an inventory and starts
being an unevidenced result. Note it as an *area to examine* and let whoever executes the check
find it, with their own evidence and in their own words. This is not pedantry: a suspected defect
recorded before anyone ran the check is not an observation, and if the survey is shared, everyone
downstream inherits a finding they did not make.

**User-generated content read as interface.** `innerText` returns chrome and data in one string. A
date-shaped string inside a table cell is very likely something a user typed, not the app's date
format. Before drawing any conclusion from text, establish which part of the page it came from.

## Handing off

`gui-checklist-design` consumes the inventory to write checks that name real widgets.
`gui-checklist-execution` consumes the URL map, the volatile-values warning and the areas to
examine. Log the session with `ai-audit-log` if the engagement requires an audit trail.
