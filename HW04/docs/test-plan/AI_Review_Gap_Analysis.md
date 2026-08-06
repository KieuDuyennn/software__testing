# AI review & gap analysis — what the AI got wrong in the generated scripts

This file is the evidence for the "Review and fix (human review)" bullet of Task 1.
The brief asks for two things per finding, and the second is where the marks are:
**what** the AI got wrong or missed, and **why** it missed it (prompt quality,
model limitation, or a characteristic of the feature).

Fill one row per correction you actually made. A row you cannot point to in a diff
does not belong here.

## Corrections log

| # | Feature | File / line | What the AI produced | Why it is wrong | What I changed it to | Why the AI missed it |
|---|---|---|---|---|---|---|
| 1 | | | | | | |
| 2 | | | | | | |
| 3 | | | | | | |

### Categories the brief names explicitly

Use these as prompts for your own review pass — but only record what you actually found.

- **Fragile selectors** — CSS/XPath tied to generated class names, nth-child chains,
  text matching that breaks under the SUT's Vietnamese UI.
- **Weak or missing assertions** — asserting an element exists rather than that it
  says the right thing; asserting a success toast without checking the server agreed.
- **Missing edge cases** — boundary values the AI skipped because they were not in
  the prompt; the AI tends to generate the happy path plus one obvious negative.
- **Flaky waits** — `waitForTimeout`, arbitrary sleeps, or racing an animation
  instead of using a web-first assertion.
- **Wrong-by-construction data** — hardcoded emails that collide on the second run,
  fixtures that mutate shared state so run 2 of 9 behaves differently from run 1.

## Cross-browser differences observed

Nine runs across three engines will not behave identically. Record real differences
here; do not file browser-engine differences as SUT bugs unless the SUT is genuinely
broken on that engine.

| Feature | Browser | Difference observed | SUT defect or engine behaviour? | Evidence |
|---|---|---|---|---|
| | | | | |

## Cases that could not be automated

Aggregated from the three TC matrices, with reasons.

| TC ID | Feature | Why not automatable | Who/what could run it |
|---|---|---|---|
| | | | |
