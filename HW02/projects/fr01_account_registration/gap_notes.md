# Gap Notes — fr01_account_registration

## 2026-07-05 — Phase 1 self-critique

Re-reading `output/01_Requirements_Breakdown.md` against the FR text before approval.
Findings only — nothing fixed yet.

1. **REQ-04 conflates a stated rule with an unstated inference.** §3.1 only says the
   Confirm Password field "MUST also be present in the registration form (UI-level)."
   My REQ-04 statement adds "and by extension must be provided/required" — that
   extension isn't explicitly in the text; it's an inference (supported indirectly by
   REQ-13/14, but not the same claim). This should probably be split into a plain
   "field must be present" REQ plus a separate Assumption for the "must be filled in"
   part, instead of folding the inference into a REQ classified as "Functional
   Requirement."

2. **REQ-16 bundles two independently-testable output facts into one REQ.** The
   success response has (a) an exact message string `"User registered successfully"`
   and (b) a numeric `id`. These are separable equivalence classes for Phase 2
   (e.g., "id is present and numeric" vs "message text matches exactly") but are
   currently merged into a single REQ-16, which risks under-covering one of the two
   facts later.

3. **REQ-18 over-bundles the API contract Observation.** It merges the endpoint path,
   HTTP method, and all three request body field-name mappings (`name`, `email`,
   `password`) into one row. The `name` ↔ "Full Name" mapping specifically overlaps
   with ASM-01 and would be cleaner traced as its own item rather than buried inside
   REQ-18's prose.

4. **Missing Open Question: email uniqueness case-sensitivity/normalization.** §3.2
   says email must be unique but doesn't say whether comparison is case-sensitive
   (e.g., is `Test@x.com` a duplicate of `test@x.com`?) or whether the email is
   normalized before the uniqueness check. Not captured anywhere in the current
   artifact.

5. **Missing Open Question: whitespace/trimming behavior.** The FR doesn't say
   whether leading/trailing whitespace on Full Name or Email is trimmed before
   validation. This affects what "must not be empty" means for Full Name (e.g., is
   a string of only spaces empty?) and isn't currently flagged despite touching two
   existing REQs (REQ-01, REQ-05).

6. **Missing Open Question: is the special-character set exclusive or just a
   minimum-inclusion rule?** §3.3 says the password must contain "at least 1 special
   character from the set `@ $ ! % * ? &`" — it doesn't say whether a character
   outside letters+digits+that set (e.g., `#`, a space, a Unicode symbol) is simply
   ignored, tolerated as an extra character, or causes outright rejection. This is a
   real ambiguity that isn't captured under OQ-05 (which only covers ASCII vs.
   Unicode for upper/lower/digit, not the special-character set, and not the
   "exclusive set" question at all).

7. **Missing Open Question: validation error precedence when multiple rules are
   violated at once.** The FR never states which error is surfaced when a single
   request violates more than one rule simultaneously (e.g., invalid email format
   AND weak password in the same submission). This matters directly for Phase 3,
   since the domain-test-design rule "never combine two invalid conditions in one
   test case" implicitly assumes a single-fault model that the FR doesn't confirm.

8. **Testability gap not flagged for REQ-15.** REQ-15 ("redirected to Login page")
   is a UI-navigation behavior, but the only interface the FR actually specifies is
   the JSON API (REQ-16/REQ-17), whose success response has no redirect/navigation
   field. Nothing in the artifact currently notes that REQ-15 may not be verifiable
   through API-level test cases alone and may need a separate UI-level test design
   pass.

9. **OQ-04 is narrower than it should be.** It only asks about whitespace-only Full
   Name values; it doesn't ask whether Full Name permits digits, symbols, or is
   effectively unconstrained beyond non-empty. Worth broadening rather than leaving
   as a whitespace-only question.

10. **Minor: no open question about the special-character set's character encoding.**
    OQ-05 asks about ASCII-vs-Unicode for uppercase/lowercase/digit classification
    but doesn't ask the analogous question for the 7 special characters (e.g., could
    a visually similar Unicode punctuation mark be miscounted as one of them). Low
    priority but inconsistent with how OQ-05 treats the other character classes.

## 2026-07-05 — Disposition of Phase 1 self-critique

Reviewed with the user. Items 1, 4, 5, 6, 7, 8, 9 applied to
`output/01_Requirements_Breakdown.md`, plus two additional Open Questions found on
cross-check (email "valid format" precision; empty-string vs. absent-field
equivalence for API testing). Items 2, 3, 10 are **deferred** — not applied yet,
kept here for a later pass (e.g., during Phase 2 when output equivalence classes
and password character-set classes are drawn in detail).

**Correction to item 1:** on re-checking the source text while applying the fix,
item 1's premise was partially wrong. §4 Inputs Summary *does* explicitly mark
Confirm Password as "Required" — so "must be provided/required" is not an unstated
inference, it's a second explicit citation (§4) merged with the §3.1 "must be
present" citation into one REQ-04. Corrected: REQ-04 now cites both §3.1 and §4
directly (no invented fact), and a new ASM-03 was added instead to capture the
genuinely unstated part — that REQ-04's "required" clause may only be verifiable
at the UI/form level, since the API request body has no `confirmPassword` field
to omit for an API-level test.
