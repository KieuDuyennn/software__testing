# CLAUDE.md — Project rules for HW02 (Domain Testing on EShop)

## Project context

This repo is my individual coursework for CS423/CSC13003 Software Testing
(FIT@HCMUS). I apply the `domain-testing-bva` skill to design test cases for
selected EShop features, one project per feature under `projects/`. Every AI
interaction must be traceable for the mandatory AI Audit Report.

## Session rules (always apply)

### 1. Audit logging — every interaction

After every response in this project, trigger the `ai-audit-log` skill to
append one row to `prompt_logs.md` at the repo root, recording:

- Timestamp (current date/time)
- AI tool name: `Claude Code`
- My verbatim prompt (quote exactly, never paraphrase)
- A factual summary of your output in that turn

Verdict rules:

- For routine interactions (approvals, state updates, clarifying questions,
  file reads, commits), set Verdict to `N/A — interaction record` and
  Reasoning to a one-line factual note.
- For phase artifacts (01–04 output files), use ONLY the verdict I explicitly
  state at approval time (`VALID` / `INVALID` / `INCOMPLETE`). Never fill in
  a verdict on my behalf — if I haven't stated one yet, ask.
- Never fabricate a row for something that didn't happen in this session.

### 2. Human-in-the-loop — never skip my review

- Run ONE phase at a time. After presenting a phase artifact, STOP and wait
  for my explicit approval. Never auto-continue to the next phase, even if
  the previous phase looks complete.
- Never edit `state.json` by hand — always go through
  `.claude/skills/domain-testing-bva/scripts/update_state.py`.
- When I request a revision, edit only the affected sections of the current
  artifact; do not regenerate the whole document.

### 3. Self-critique before my review

When I ask for a self-critique of a phase artifact, list possible gaps only —
do NOT fix anything until I decide. Append the list to
`projects/<project>/gap_notes.md` as a new dated section (e.g.
"Phase 2 self-critique — 2026-07-05"); never overwrite earlier sections.

### 4. Git commits

- Commit only when I say so (normally bundled into my approval message).
- Commit message format: `test(<fr-short-name>): phase <n> <phase name>`
  — e.g. `test(fr01): phase 1 requirement analysis`.

### 5. Integrity constraints (course policy)

- Never invent business rules, thresholds, or expected behaviors not stated
  in the input Functional Requirement — flag them as Open Questions instead.
- Bug report descriptions are 100% written by me. You may run tests and show
  raw Actual-vs-Expected output when I ask, but never draft bug report text,
  verdicts, or conclusions about whether something is a bug.
- Anything you cannot verify from this session's actual context (e.g. a
  prompt that has scrolled out of view), say so — never reconstruct from
  memory.