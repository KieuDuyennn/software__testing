---
name: ai-audit-log
description: Log an AI-assisted artifact for an academic AI-usage audit trail / disclosure requirement. Triggers whenever an AI-assisted artifact (test cases, script, document, analysis) has just been produced or approved and needs to be recorded for coursework AI-usage disclosure.
allowed-tools: Read, Write, Edit
---

# AI Audit Log

## Purpose

Append a disclosure record to `prompt_logs.md` at the repository root whenever an
AI-assisted artifact has just been produced or approved, so the coursework has a
verifiable AI-usage audit trail.

## Behavior

On trigger, append one row to `prompt_logs.md` at the repository root with these
columns:

| Timestamp | AI tool name | Verbatim prompt | AI output summary | Verdict | Reasoning | Student fix (if any) |
|---|---|---|---|---|---|---|

- **Timestamp**: current date/time.
- **AI tool name**: the assistant/tool actually used in this conversation.
- **Verbatim prompt**: the user's actual prompt text that led to the artifact —
  quote it exactly, do not paraphrase or reconstruct it from memory.
- **AI output summary**: a factual, concise summary of what was actually produced
  in this conversation — do not describe an idealized or intended output.
- **Verdict**: one of `VALID` / `INVALID` / `INCOMPLETE`. If the user has not
  stated a verdict, **ask them which applies** — never guess or default to `VALID`.
- **Reasoning**: the stated basis for the verdict (from the user, or your own
  factual observation of what happened — not speculation).
- **Student fix (if any)**: describe any correction the student/user made to the
  AI output. Write "None" if no fix was made — never leave the cell blank.

If `prompt_logs.md` does not exist yet at the repository root, create it with a
header row before appending the first entry.

## Constraints

- Never fabricate a prompt or output that wasn't actually part of this conversation.
  Every logged row must correspond to something that genuinely happened in this
  session.
- Never invent a verdict on the user's behalf — ask if it's not already stated.
- This skill only appends rows to `prompt_logs.md`. It does not modify or create
  any other files.
