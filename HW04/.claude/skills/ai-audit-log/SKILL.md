---
name: ai-audit-log
description: Append one row per AI interaction to docs/prompt_logs.md and keep docs/03_AI_Audit_Report.md in sync, recording tool name, timestamp, the verbatim prompt, the AI output and the human review outcome. Use after every response in this project, and when preparing the mandatory section 9 appendix.
---

# AI audit logging

HW04 §9 makes the audit report mandatory and names exactly four required fields per
interaction: **AI tool name, date and time, my prompt, the AI output**. This project
adds a fifth, **human review outcome**, because §2 grades review, not generation.

## Interaction contract

At the start of each substantive interaction, capture the observed timestamp, tool/model
and exact prompt before transforming it. At the end, append one numbered record to
`docs/prompt_logs.md`. Use a fenced block rather than a Markdown table whenever the prompt
contains newlines, pipes or code so the original bytes remain readable.

Each record contains:

- stable interaction ID;
- observed timestamp and timezone;
- tool and model when observable;
- prompt verbatim in its original language;
- factual output summary plus artifact paths/commit;
- verdict: `PENDING`, `ACCEPTED`, `REJECTED`, or `REVISED`;
- the student's verdict quote when one exists.

Rules:

- **Verbatim prompt.** Quote exactly. Never paraphrase, never tidy up.
- **Factual summary of output.** What was produced and where it landed — not a
  self-assessment of quality.
- **Verdict.** Use `PENDING` until the student explicitly accepts, rejects or revises the
  artifact. Never infer acceptance from silence. Preserve the student's decision as a
  quote and link a later decision back to the original interaction ID.
- **Never fabricate a row** for something that did not happen in this session.
- If something cannot be verified from this session's actual context (a prompt that
  scrolled out of view), say so — do not reconstruct from memory.
- **Timestamps are observed, never estimated.** §11 lists invented timestamps as
  cheating. Read the real clock at the time of writing; if a row is written late, the
  honest value is the time it was written, not a plausible reconstruction.
- **The student can switch logging off** for a session. Honour it and do not backfill from
  memory, but mark the audit `INCOMPLETE — logging disabled for part of the process`; never
  describe a knowingly shortened log as complete.
- **Prompts are often mixed Vietnamese and English.** Keep them in the language they
  were written. Translation belongs in the §9 curation step, declared as such.

## When preparing the §9 appendix

Curate `docs/prompt_logs.md` into `docs/03_AI_Audit_Report.md` while preserving a mapping
from every raw interaction ID. Do not silently collapse records: list every omitted ID and
the reason (for example, read-only bookkeeping). Keep the original prompt verbatim. If a
translation helps the marker, add it as a separate labelled field beside the original;
never replace the source prompt with normalized English.

Before export, verify:

1. IDs are unique and ordered.
2. Every substantive interaction is included or explicitly mapped as omitted.
3. Every artifact path and commit exists.
4. Human verdicts are quoted or remain `PENDING`.
5. Historical normalized summaries are disclosed as limitations, not reconstructed as
   verbatim transcripts.

The appendix status is `COMPLETE` only when all five checks pass; otherwise state
`INCOMPLETE` and name the missing evidence.
