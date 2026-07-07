# AI Audit Report — HW02 Domain Testing on EShop

- **Student ID:** 23127184
- **Course:** CS423/CSC13003 — Software Testing (FIT@HCMUS)
- **Assignment:** HW02-AI

## Declaration

**I use AI tools for the following tasks:**

| AI tool | Role in this assignment |
|---|---|
| Claude Code (models: claude-sonnet-5, claude-opus-4-8, claude-fable-5) | Executing the 4-phase `domain-testing-bva` Agent Skill under my phase-by-phase direction: requirement decomposition drafts, equivalence-class derivation drafts, domain/BVA test-case drafts, checklist-driven self-critiques, targeted revisions I specified, workflow state updates, git commits, audit-log bookkeeping, and assembly of this submission package |
| Claude (claude.ai) | Independent cross-review of selected phase artifacts (recorded in the log rows marked "cross-review, per user report") |

I did **not** use AI to: choose verdicts on phase artifacts (all VALID / INVALID /
INCOMPLETE verdicts are my own decisions, stated explicitly at approval time),
decide which self-critique findings were real (each finding was dispositioned by me
as APPLIED / DEFERRED / REJECTED), or write bug reports and their conclusions.

## Logging mechanism

Logging was automated with a dedicated Agent Skill (`ai-audit-log`, included under
`../skills/`): after every interaction, one row is appended to the log with the
timestamp, tool name, **verbatim prompt**, factual output summary, my verdict, the
reasoning, and the student fix (if any). Routine interactions (approvals, state
updates, file reads, commits) carry the verdict `N/A — interaction record`;
phase artifacts carry only the verdict I stated explicitly at approval time.

## Full interaction log

The complete log (53+ rows, 2026-07-05 → 2026-07-07, covering all four features'
phases plus revision cycles and this submission-package assembly) is in
[`prompt_logs.md`](prompt_logs.md), kept verbatim as required.

Summary of phase-artifact verdicts:

| Feature | Phase 1 | Phase 2 | Phase 3 | Phase 4 |
|---|---|---|---|---|
| FR-01 Account registration | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved |
| FR-06 Product detail view | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved |
| FR-11 Order history view | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved |
| FR-13 Dashboard | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved | INCOMPLETE → fixed → approved |

(No first draft was approved as-is; every phase went through at least one
self-critique + user-directed-fix cycle. Details per row in `prompt_logs.md` and
per finding in each feature's `gap_notes.md`.)
