---
name: playwright-automation
description: Generate, review and run data-driven Playwright test suites across three browsers for one feature at a time. Use when converting designed test cases into automation scripts, when adding cases to an existing spec, or when preparing the multi-browser HTML reports required by HW04. Enforces external data files, three distinct assertion patterns, and a human review gate before any run.
---

# Data-driven multi-browser automation

Convert a feature's designed test cases into a Playwright suite that runs on three
browser engines and produces attributable HTML reports.

## When to use

- Converting HW02-style designed test cases into `.spec.ts` files.
- Extending an existing spec with more cases.
- Preparing the 3-feature × 3-browser run matrix and its reports.

## Non-negotiables

1. **No inline test data.** Cases come from `automation/data/*.csv` or `*.json` via
   `automation/utils/data-loader.ts`. If a case array appears inside a spec, the work is wrong.
2. **Three distinct assertion patterns**, not three spellings of one: UI state,
   API/contract, data integrity. See `automation/utils/assertions.ts`.
3. **Stop for human review** after generating each spec, before it is ever run.
4. **Never edit generated evidence** — HTML reports, JSON results, run summaries.
   If a number is wrong, re-run; do not fix the file.
5. **Never weaken an assertion to make a suite green.** A failing assertion is a
   finding until a human decides otherwise.
6. **The running SUT outranks the design documents.** Where a prior artifact and the
   live app disagree, the app is the fact and the document is the error. Record the
   correction; never quietly test the document's version of reality.

## Workflow — one feature at a time

### Step 0 — Stand the environment up, and prove it
Nothing below is meaningful against an app that is not running. Do this first, every
time — it is short, and skipping it costs an hour of misdiagnosed failures.

- Start each tier and note the **actual** port from its own output, not from memory:
  backend, customer web app, admin app. Read the ports out of the SUT's own config
  (a Vite `server.port`, a `setup_guide`), then confirm with a request.
- Check `node_modules` exists in each front-end you will drive; a fresh clone has none.
- Check the browser binaries are installed — all three engines, not just the default.
- **Confirm `baseURL` points at the front-end, not the API.** These are different
  ports on this SUT and the mistake is silent: pages 404 and every case fails
  identically, which reads like a broken suite rather than a config typo.

→ Record the verified ports somewhere the suite reads them (`.env.example`), so the
next feature does not rediscover them.

### Step 1 — Read the feature, and read the page that implements it
Load the FR text and the prior design artifact for this feature only — **then open the
SUT source for the screen itself** and read it.

This step is where the highest-value findings come from, and reading the document alone
cannot produce them. Two real examples from this project:

- A prior artifact recorded "this feature has no web UI" because it searched for a
  route by name. The feature was in fact rendered inside another route's page. Every
  downstream case had been designed at the wrong layer.
- A registration page printed "password must contain a special character" while the
  regex it actually enforced *excluded* special characters and *required* whitespace.
  The mismatch is invisible from the outside until you hit exactly the right input.

From the source, extract before writing any case: the fields that actually exist, the
literal user-visible strings, the client-side validation, and how errors are rendered
(one shared element, or one per field).

→ Stop. Get approval on the behaviour list and on any correction to a prior document.

### Step 2 — Derive the cases
Turn each behaviour into concrete cases: positive, negative, edge. Aim past the
minimum (12) — the marginal case is where defects live. Record each with a stable
`tc_id` traceable to the design artifact.

Prefer cases that close a gap the prior artifact *itself* recorded as uncovered; those
are traceable derivations. Cases invented to reach a round number are padding, and ten
variants that all fail for one root cause are one case, not ten. When a cluster of
cases will fail together, add one **diagnostic** case whose input isolates the shared
cause — it turns a wall of red into a single readable finding.

→ Stop. Get approval on the case list.

### Step 3 — Verify selectors against the live SUT
Before the data file, not after: the DOM decides which cases can exist at all. A field
the design assumed is present may simply not be there, and those cases have to move to
the "not automatable" list rather than be written and thrown away.

Write a throwaway probe script — not a spec, not evidence — that loads the page and,
for each candidate locator, prints `count()`. Require exactly 1. Also probe the
locators you expect to **fail** and keep those numbers: they are the written
justification for dropping to CSS. A useful probe reports:

- each proposed locator → count, and the tag/type it resolved to
- `getByLabel` / `getByRole` alternatives → their counts, to prove they were tried
- a fill smoke test, to prove the getters address different elements
- a structural count (e.g. total inputs in the form) that confirms what is *absent*

Selector priority: `getByRole`/`getByLabel` → `getByTestId` → `getByText` → CSS/XPath;
any CSS/XPath carries a comment saying why nothing better existed. Delete the probe
afterwards and fold what it proved into the page object's doc comment.

Watch for values the browser supplies rather than the app — native constraint
validation messages differ per engine, so assert on the boolean state, not the string.

→ Stop. Get approval on the locator set and on any case the DOM has invalidated.

### Step 4 — Write the data file
Emit `automation/data/<feature>.csv` or `.json`, one row per case, columns typed and named so a
reader can tell input from expectation. Empty string is a legitimate input — never
coerce it away. Drop any column the real page has no field for.
→ Stop. Get approval on the data file.

### Step 5 — Write the page object, then the spec
Page object holds locators and actions; the spec holds cases and assertions. The
spec iterates the loaded data and imports `test` from `automation/fixtures/test-fixtures.ts`.
→ Stop. Present the spec for human review; do not run it.

### Step 6 — Human review pass
The reviewer looks for: fragile selectors, assertions that check existence rather
than meaning, missing edge cases, `waitForTimeout`, and data that collides across
repeated runs. Every correction gets a row in `docs/test-plan/AI_Review_Gap_Analysis.md`
with **what** was wrong and **why** the AI missed it.

### Step 7 — Run all three browsers
```
$env:FEATURE='fr01'; $env:BROWSER='chromium'
npx playwright test automation/tests/fr01_account_registration --project=chromium
```
or all nine at once: `npm run runs:all`. Each run writes
`reports/html/<feature>/<browser>/index.html` showing `Run by: {StudentID}` and an
ISO timestamp.

### Step 8 — Triage failures
For each failure, decide: test defect (fix the test, log the correction) or product
defect (write it up in `docs/02_Bug_Report.md`, file a GitHub Issue with a screenshot).
Never let a third category — "made it pass" — exist.

## Output checklist per feature

- [ ] environment verified: all tiers up, ports confirmed, `baseURL` on the front-end
- [ ] page source read; any disagreement with the design artifact recorded as a correction
- [ ] ≥ 12 cases, all sourced from an external data file
- [ ] ≥ 3 distinct assertion patterns across the suite
- [ ] every locator verified against the live SUT, with the rejected alternatives' counts kept
- [ ] 3 browser runs, 3 HTML reports, each stamped `Run by: {StudentID}` + ISO time
- [ ] every AI correction logged with its cause
- [ ] non-automatable cases listed with reasons

## Pitfalls this workflow was rewritten to avoid

Each line below cost real time on this project before it became a rule.

| Symptom | Actual cause |
|---|---|
| Every case fails identically, instantly | `baseURL` pointed at the API port, not the front-end |
| Locator matches nothing despite a visible label | `<label>` has no `htmlFor` and the input no `id` — `getByLabel` cannot bind them |
| Locator is ambiguous with no accessible name | several inputs share a role; `getByRole` alone cannot separate them |
| Cases written for a field that does not exist | data file was authored before the DOM was inspected |
| A dozen red cases, one real bug | a shared client-side gate rejected them all before they reached what they tested |
| Assertion passes on one engine, fails on another | the expected string was supplied by the browser, not the app |
| Feature "has no UI" | the search was for a route name, not for the rendered feature |
