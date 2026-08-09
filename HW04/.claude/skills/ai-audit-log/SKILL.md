---
name: ai-audit-log
description: Append one row per AI interaction to docs/prompt_logs.md and keep docs/03_AI_Audit_Report.md in sync, recording tool name, timestamp, the verbatim prompt, the AI output and the human review outcome. Use after every response in this project, and when preparing the mandatory section 9 appendix.
---

# AI audit logging

HW04 §9 makes the audit report mandatory and names exactly four required fields per
interaction: **AI tool name, date and time, my prompt, the AI output**. This project
adds a fifth, **human review outcome**, because §2 grades review, not generation.

## After every response

Append one row to `docs/prompt_logs.md`:

| # | Timestamp | Tool | My prompt (verbatim) | AI output (factual summary) | Verdict / review note |

Rules:

- **Verbatim prompt.** Quote exactly. Never paraphrase, never tidy up.
- **Factual summary of output.** What was produced and where it landed — not a
  self-assessment of quality.
- **Verdict.** For routine turns (approvals, file reads, commits) use
  `N/A — interaction record`. For a generated artifact, use only the verdict the
  student explicitly stated. If none was stated, ask; never fill one in on their behalf.
- **Never fabricate a row** for something that did not happen in this session.
- If something cannot be verified from this session's actual context (a prompt that
  scrolled out of view), say so — do not reconstruct from memory.
- **Timestamps are observed, never estimated.** §11 lists invented timestamps as
  cheating. Read the real clock at the time of writing; if a row is written late, the
  honest value is the time it was written, not a plausible reconstruction.
- **The student can switch logging off** for a session. Honour it for that session and
  do not backfill afterwards — a batch of rows written from memory is exactly the
  fabrication §11 prohibits. The log is then simply shorter, and that is fine.
- **Prompts are often mixed Vietnamese and English.** Keep them in the language they
  were written. Translation belongs in the §9 curation step, declared as such.

## When preparing the §9 appendix

Curate `docs/prompt_logs.md` into `docs/03_AI_Audit_Report.md`: keep every substantive interaction,
collapse pure bookkeeping turns, and state at the top whether the recorded prompts are
verbatim transcripts or normalised English renderings of mixed Vietnamese/English
instructions. Both statements are acceptable; a silent normalisation is not.
