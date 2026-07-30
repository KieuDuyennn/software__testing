---
name: ai-audit-log
description: Record how AI was used to produce a piece of work, so the use can be declared and checked — tool and exact model, real timestamps, verbatim prompts, what the AI returned, what a human reviewed and changed, and which artefacts are AI-generated versus human-made. Use whenever an assignment, journal, employer or compliance policy requires declaring AI assistance; whenever an AI-usage appendix or a critique of where the AI was wrong must be written; and proactively after a substantial AI-assisted session on work that carries a disclosure requirement. Trigger on "AI declaration", "khai báo sử dụng AI", "khai báo phần nào do AI viết", "log this AI session", "AI usage appendix", "phụ lục AI", "which parts did AI write", "cite my use of Claude". Do NOT use to audit an AI system itself — evaluating a deployed model or feature for bias, safety, accuracy or EU AI Act conformance is an entirely different task, and this skill has nothing to offer it.
---

# AI audit log

The log has to survive someone checking it. That is the whole design constraint: every claim in it
should be independently verifiable, and anything not verifiable should be visibly marked as
pending rather than quietly asserted.

Write the entry **at the end of the session it describes**. Reconstructing one later is where audit
logs go wrong — prompts get paraphrased from memory, and timestamps become unrecoverable.

## Get the timestamp now

The single most common defect in these logs is a column of `TBD` or date-only entries where a real
time was required. It cannot be fixed afterwards.

```bash
date "+%Y-%m-%d %H:%M %Z"
```

Run it during the session and write the result down. Same for the model: record the exact
identifier, not the family name — "Claude Opus 5 (`claude-opus-5`)", not "Claude". A reviewer
comparing two entries needs to see which model produced which output.

## One entry per interaction

```markdown
### Interaction <n> — <what it was for>

| Field | Value |
| --- | --- |
| **AI tool** | <product> — <exact model id> |
| **Date / time** | 2026-07-30 14:22 +07 |
| **Task** | <which deliverable this served> |
| **Artefacts produced** | <files created or changed, with versions> |

**Prompt (verbatim):**

```
<exactly what was typed, unedited>
```

**AI output:** <what it actually did — read these files, wrote these items, ran this script,
reported these findings. Specific enough that someone can check it against the artefact.>

**Human review and action taken:** <what a person checked, what they accepted, what they
changed and why. If review has not happened: "Pending — owner: <name>".>
```

## Verbatim means verbatim

Do not tidy the prompt. Keep the original language, the typos, the missing diacritics, the casual
phrasing, the mid-sentence change of mind. Three reasons, in order of weight:

1. A cleaned-up prompt is a different prompt, so the log no longer documents what happened.
2. Where the policy asks the operator to guide the AI stepwise, the prompt chain is the *evidence*
   of how they did it. Polishing it removes the evidence.
3. The rough prompts are the informative ones. A vague prompt followed by a bad output is the
   clearest demonstration in the whole log of how prompt quality drives result quality.

If a prompt contains a secret, redact the secret and say you redacted it. Redaction is honest;
rewriting is not.

## Attribute artefacts, don't summarise them

A single sentence saying "AI helped with the report" is not an audit. Table it:

| Artefact | AI-generated | Human-generated | Human-verified |
| --- | --- | --- | --- |
| Checklist items (53) | 49 | 4 | all 53 |
| Screenshots / evidence | **none** | 14 captures | — |

The zero row matters as much as the others. Where a policy requires evidence to be real —
participants, device captures, execution results — stating plainly that AI produced none of it is
the claim being audited.

## Never assert a review that has not happened

A changelog saying "reviewed by the team" while the review table is empty is the contradiction a
reviewer finds first, and it costs more credibility than an honest gap. Write
`Pending — owner: <name>` and leave it. An audit log with open items reads as maintained; one with
fabricated completeness reads as decorative.

## Record the AI's mistakes, especially the ones it corrected itself

This is the most valuable content in the log and the most commonly omitted. For each error worth
recording, note **what the wrong claim was, what made it wrong, and what exposed it**. That last
part is the reusable lesson.

Errors worth logging, with the shape they usually take:

- **Confident factual errors** — an assertion that reads as authoritative and is simply false.
- **Instrument-mediated blindness** — the tool could not see the thing, and the tool's limit got
  written up as a fact about the product. Note the direction of the bias: selector-based inspection
  systematically under-reports what exists, so claims of *absence* deserve more suspicion than
  claims of presence.
- **Coverage illusions** — a term appearing inside another item's prose, counted as covered.
- **Plausible-but-wrong citations** — a principle attached to an item it does not support, while
  other principles go uncited.
- **Padding toward a requested number** — one rule split in two to reach a count.
- **Task-boundary overrun** — the AI answered the next question rather than the one asked, e.g.
  recording verdicts inside an artefact whose purpose was to define how to check.
- **What the AI did well** — a critique with no positives is not credible. Being able to explain
  *why it missed something* once shown the gap, and verifying structural claims by script rather
  than by assertion, are both genuinely useful and worth naming.

## Material for a critique section

If the engagement asks for a written critique, keep a *Material for the critique* section in the
log: the factual raw material, gathered as it happens. The prose must be written by the person, but
they should not have to reconstruct the facts weeks later.

The two findings that generalise past any single project, and are worth testing against your own
log:

- **Reframing the question finds different defects; changing the instrument finds a different
  class of defect.** A second pass asking "what does the spec require that this lacks?" finds real
  gaps the generating pass could not. But when the error lives in the *tool* rather than the
  reasoning, no amount of re-asking surfaces it — every pass looks through the same instrument.
- **Verify against evidence the AI did not produce.** Errors that survive several AI-run review
  passes fall in minutes against artefacts a person captured.

## Checklist before submitting

- Every interaction has a real date **and** time.
- Every prompt is verbatim, in its original language.
- Every model is named by exact identifier.
- Every "human review" cell is either filled in or explicitly marked pending with an owner.
- The artefact attribution table exists and includes the rows where AI contributed nothing.
- Entries appear in chronological order and version numbers referenced still match the artefacts.
- If AI was not used, the declaration says so plainly rather than being omitted.
