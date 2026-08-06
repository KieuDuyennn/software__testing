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

## Workflow — one feature at a time

### Step 1 — Read the feature, not the whole app
Load the FR text and the HW02 design artifact for this feature only. List the
observable behaviours. Do not propose test cases yet.
→ Stop. Get approval on the behaviour list.

### Step 2 — Derive the cases
Turn each behaviour into concrete cases: positive, negative, edge. Aim past the
minimum (12) — the marginal case is where defects live. Record each with a stable
`tc_id` traceable to the HW02 artifact.
→ Stop. Get approval on the case list.

### Step 3 — Write the data file
Emit `automation/data/<feature>.csv` or `.json`, one row per case, columns typed and named so a
reader can tell input from expectation. Empty string is a legitimate input — never
coerce it away.
→ Stop. Get approval on the data file.

### Step 4 — Verify selectors against the live SUT
Open the real pages. Confirm every locator the page object will use. Selector
priority: `getByRole`/`getByLabel` → `getByTestId` → `getByText` → CSS/XPath, and
any CSS/XPath needs a comment saying why nothing better existed. This step is not
skippable — a spec built on guessed selectors produces meaningless pass/fail.

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

- [ ] ≥ 12 cases, all sourced from an external data file
- [ ] ≥ 3 distinct assertion patterns across the suite
- [ ] every locator verified against the live SUT
- [ ] 3 browser runs, 3 HTML reports, each stamped `Run by: {StudentID}` + ISO time
- [ ] every AI correction logged with its cause
- [ ] non-automatable cases listed with reasons
