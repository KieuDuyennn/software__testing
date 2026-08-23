# HW06 - AI Critique

**Required length: 200-300 words.** Write this last, from the audit tables and
the extension phase, so the claims are backed by specific cases.

## Questions to answer

1. Where did the AI get something wrong, biased, or incomplete?
2. Why did it fail to catch the issue?
3. What principle about collaborating with AI did this assignment teach you?

## Raw material collected while working

Fill these in as you go, then compress into the final paragraph.

### Concrete misses (cite the test case id)

| # | What the AI missed or got wrong | Where it shows up | Root cause |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

### Root-cause vocabulary

- **Specification blindness.** The AI reads `api_specification.md`, which
  documents happy paths. A route that is missing its auth middleware, or a
  comparison that uses `>` where the requirement says `>=`, leaves no trace in
  the spec text.
- **Single-endpoint framing.** IDOR, privilege escalation and ownership checks
  need a second actor. A prompt scoped to one endpoint never introduces one.
- **Observed-behaviour oracles.** Ask what a response looks like and the AI
  describes what the SUT returns. A test built on that assertion passes by
  construction and can never find a defect.
- **Plausible-but-unexecuted output.** Well-formatted test cases that fail on
  the first run because a precondition was imagined rather than checked.

---

## Final critique (200-300 words)

*(Write here. Word count: ___)*
