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

## 2026-07-05 — Phase 2 self-critique

Re-reading `output/02_Equivalence_Partitioning.md` against the EP heuristics before
approval. Findings only — nothing fixed yet.

1. **Wrong partitioning guideline for password length (EC-18).** REQ-07 ("minimum 8
   characters") is a RANGE / NUMBER-OF-VALUES condition — guideline (a)/(b) — but I
   modeled it as a single "must-be-X"-style invalid class ("< 8 chars"). Guideline
   (a) would frame it as one valid class (len ≥ 8) and an invalid class bounded on
   the low side, which also makes the lower boundary explicit for Phase 4. As
   written, EC-18's class is open-ended downward and blurs into the empty class.

2. **Overlapping partitions — EC-16 ⊆ EC-18 (contradicts my own self-check).** An
   empty password (EC-16, length 0) is also a member of "fewer than 8 characters"
   (EC-18). The two partitions overlap, so a length-0 value is classifiable into two
   classes at once — exactly the "overlapping partitions" mistake the heuristics warn
   against. EC-18 should be bounded as `1 ≤ len ≤ 7` to be disjoint from the empty
   class. My §5 self-check line "No overlapping partitions … at exactly 8" was
   therefore overstated/wrong — it only checked the upper edge of the valid range,
   not the empty-vs-short overlap at the low end.

3. **Inconsistent empty-vs-absent handling across fields.** Full Name, Email, and
   Password each split "empty string" from "absent field" into two classes
   (EC-02/03, EC-06/07, EC-16/17), all flagged as possibly collapsing per OQ-12. But
   Confirm Password (EC-26) merges "absent / empty" into a single class. The same
   OQ-12 ambiguity is treated two different ways within one artifact — either all
   four fields should split-pending-OQ-12 or all should merge, consistently.

4. **Output side conflates "missing field" with "present-but-empty."** EC-29 is
   labeled "Missing required field," yet I route present-but-empty-string inputs
   (EC-02, EC-06, EC-16) into it. An empty-string value is not literally a *missing*
   field; if the system distinguishes them (the input-side OQ-12 question), there may
   be a distinct "empty/blank field" rejection output class separate from EC-29. The
   OQ-12 ambiguity is captured on the input side but not mirrored on the output side.

5. **EC-27 still merges two distinct output facts.** Success bundles the exact
   message string and the numeric `id` into one class. This is the Phase-1-deferred
   item 2, and I flagged it, but strictly it remains a merged output class — "`id` is
   present and numeric" is a separable output assertion that currently has no class of
   its own and could go untested in Phase 3.

6. **Possibly missed output class: malformed / non-JSON request.** There is no class
   for a structurally invalid request (invalid JSON, wrong content-type, non-object
   body). It may be out of FR scope, but it isn't even noted as a deliberate
   exclusion — worth a one-line decision rather than silent omission.

7. **EC-25 (password mismatch) may hide sub-classes under guideline (e).** If the
   implementation trims or normalizes before comparing Password to Confirm Password,
   "wholly different" vs "differs only by trailing whitespace" vs "differs only by
   case" would not be handled identically. Currently a single invalid class with no
   flag; guideline (e) suggests at least noting the possible split (and it has no
   backing implementation to confirm uniform handling).

8. **EC-12 may be a second VALID class collapsed into "Ambiguous," not just an
   ambiguous invalid.** Subdomain/plus-addressing emails, if accepted, would be a
   distinct valid-format partition of Email (valid emails are not necessarily handled
   uniformly — guideline (e)), not merely an unresolved accept/reject. Framing it only
   as "Ambiguous → EC-27 or EC-30" understates that the *valid* side of Email may
   itself need more than the single EC-05 class.

9. **Minor / cosmetic.** Ambiguous-output ordering is written inconsistently
   ("EC-30 or EC-27" for EC-11 vs "EC-27 or EC-30" for EC-12); harmless but
   inconsistent. Also, the backward-trace table calls success coverage "Partial"
   while §5 self-check does not carry that caveat forward — the two summaries are
   slightly out of step.

## 2026-07-05 — Disposition of Phase 2 self-critique

Reviewed with the user. **Applied** to `output/02_Equivalence_Partitioning.md`:
- Item 1 — EC-18 (password length) reclassified under **guideline (a) RANGE**
  (measurable length), explicitly not (b) number-of-values; valid class kept
  open-ended above (`len ≥ 8`, no invented max — OQ-03).
- Item 2 — EC-18 rebounded to `1 ≤ len ≤ 7` so it no longer overlaps EC-16 (empty,
  `len = 0`); §5 self-check corrected to state the prior "no overlapping partitions"
  tick was wrong (only checked the upper edge) and what was fixed.
- Item 3 — Confirm Password split into EC-26 (empty) and new **EC-34** (absent),
  consistent with the other three fields, both flagged with OQ-12. EC-34 appended
  after the output block with an explicit numbering note to avoid renumbering.
- Item 4 — output EC-29 relabeled "Missing **or** empty required field" with an
  explicit note that absent-vs-empty are merged on purpose pending OQ-12/OQ-02
  (identical expected results today); EC-34 added to its trace.
- Item 6 — malformed / non-JSON request added as a **deliberate exclusion** note in
  §2 plus new **OQ-13**, rather than inventing an unspecified response class.

**Deferred** (logged here, not applied — reasons below):
- Item 5 — split EC-27 success into separate message-string and numeric-`id` output
  classes. *Reason:* this is the same split already deferred from Phase 1 (gap_notes
  item 2); keeping the deferral consistent. It is now honestly recorded as "Partial"
  in both the §3 backward-trace and the §5 self-check, so it is visible rather than
  hidden. Revisit alongside Phase 1 item 2.
- Item 7 — split EC-25 (password mismatch) into guideline-(e) sub-classes
  (wholly-different vs whitespace-only vs case-only difference). *Reason:* the split
  hinges on whether the implementation trims/normalizes before comparing, and there
  is **no backend in the repo** to confirm non-uniform handling; splitting now would
  invent structure. Better resolved when an implementation or an answer to the
  trimming question (relates to OQ-10) is available.
- Item 8 — treat EC-12 (subdomain/plus-addressing email) as a possible second
  *valid* Email class rather than only "Ambiguous." *Reason:* depends on OQ-11
  (what counts as valid email format); until that resolves, its valid-vs-invalid
  status is genuinely unknown, so promoting it to a valid class now would pre-judge
  the open question. Re-evaluate when OQ-11 is answered.
- Item 9 — cosmetic ambiguous-output ordering inconsistency ("EC-30 or EC-27" vs
  "EC-27 or EC-30"). *Reason:* purely presentational, no effect on classes or
  traceability; not worth a revision cycle now. (The §3-vs-§5 "Partial" mismatch part
  of item 9 *was* fixed as part of item 5's honest recording.)
