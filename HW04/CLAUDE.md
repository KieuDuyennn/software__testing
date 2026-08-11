# CLAUDE.md — Project rules for HW04 (Automation Testing on EShop)

## Project context

Individual coursework for CS423/CSC13003 Software Testing (FIT@HCMUS), HW04-AI.
I automate three EShop web features with Playwright + TypeScript — FR-01 (Pool A),
FR-11 (Pool B), FR-13 (Pool C) — the same web features designed in HW02. Every AI
interaction must be traceable for the mandatory AI Audit Report.

## Session rules (always apply)

### 1. Audit logging — every interaction

After every response in this project, append one row to `docs/prompt_logs.md` recording:
timestamp, tool name (`Claude Code`), my verbatim prompt, and a factual summary of
your output. Never fabricate a row for something that did not happen in this session.
`docs/03_AI_Audit_Report.md` is the curated §9 appendix; `docs/prompt_logs.md` is the raw log.

### 2. AI-first, but step by step

§2 of the brief explicitly rejects "write all the automation scripts for this feature".
Drive the technique in stages — analyse the FR, derive the cases, choose selectors,
write the data file, write the spec, review — and stop for my approval between stages.
Never auto-continue to the next feature.

### 3. Human review — never skip it

- After generating a spec, present it and STOP. I review before it is run.
- When I request a revision, edit only the affected block; do not regenerate the file.
- Every correction I make to AI-generated code gets a row in
  `docs/test-plan/AI_Review_Gap_Analysis.md`, including **why** the AI missed it.

### 4. Evidence integrity (§11 Anti-AI-Cheat)

- **Never** hand-edit a Playwright HTML report, a JSON result file, or a run summary.
  Those files are attributable execution evidence; if a number is wrong, re-run.
- Never invent a test result, a browser run, a timestamp, or a GitHub Issue link.
- Never write a bug description on my behalf. You may show raw actual-vs-expected
  output; the verdict on whether it is a defect is mine.
- If a test fails, the default assumption is that it found something — do not weaken
  or delete an assertion to make a suite green.

### 5. Test-code rules

- Test data lives in `automation/data/*.csv` / `*.json`. Inline case arrays inside a spec
  are rejected by the brief — do not write them, not even temporarily.
- Selector priority: `getByRole`/`getByLabel` → `getByTestId` → `getByText` → CSS/XPath.
  Any CSS/XPath locator needs a one-line comment saying why nothing better existed.
- No `waitForTimeout` / arbitrary sleeps. Use web-first assertions.
- Import `test` from `automation/fixtures/test-fixtures.ts`, never from `@playwright/test`, so the
  `Run by: 23127184` annotation lands on every test.
- Never commit credentials. Real accounts and passwords live in `.env` (gitignored).

### 6. Git commits

- Commit only when I say so.
- §12 counts only commits that change test-script files toward the 8-commit minimum,
  spread over ≥ 4 days. Do not batch a week of work into one commit.
- Message format: `test(fr01): <what changed>` / `chore(hw04): <what changed>`.
