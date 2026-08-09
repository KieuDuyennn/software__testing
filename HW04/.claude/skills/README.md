# Agent Skills — HW04 (§7)

| Skill | Purpose | Used on |
|---|---|---|
| `playwright-automation` | Drive the data-driven, multi-browser automation workflow step by step: FR analysis → case derivation → data file → page object → spec → review → 9-run execution | FR-01, FR-11, FR-13 |
| `ai-audit-log` | Append each interaction to `docs/prompt_logs.md` and keep `docs/03_AI_Audit_Report.md` in sync | all sessions |

§7 asks for the skill **plus** a YouTube demo showing it used end to end on a complete
feature. Record the link in `docs/demo_links.md`.

## Revision history

These skills are maintained against real execution, not written once and left alone.
`playwright-automation` was revised after FR-01 was set up and its selectors verified:

| Change | What forced it |
|---|---|
| Added Step 0 (environment) | The SUT was not running, a front-end had no `node_modules`, no browser engines were installed, and `baseURL` pointed at the API port |
| Step 1 now reads the page source, not only the FR text | Reading the source is what exposed a prior artifact's wrong "this feature has no UI" conclusion, and a validation regex that contradicted its own error message |
| Selector verification moved ahead of the data file | The live DOM lacked a field the design assumed, so two designed cases had to be reclassified — writing the data file first would have wasted them |
| Step 3 now specifies *how* to verify | "Verify selectors" without a method is unactionable; the probe technique (count each candidate, keep the counts of the rejected alternatives) makes it repeatable |
| Added a pitfalls table | Each row is a failure mode that actually cost time here |

`ai-audit-log` gained rules on observed-vs-estimated timestamps, honouring a
logging-off instruction without backfilling, and keeping mixed-language prompts intact.
