# Gap Notes — fr06_product_detail_view

## 2026-07-06 — Phase 1 self-critique (per user checklist)

Re-reading `output/01_Requirements_Breakdown.md` against
`input/Functional_Requirement.md`, not re-asserting the artifact's own
Section 7 Self-Check. Findings only — nothing fixed yet. Each finding
tagged `[P1-Gxx]` with evidence and an honest severity call.

### 1. REQ-15 classification — is "Functional Requirement" the right bucket?

- **[P1-G01] real gap.** REQ-15's statement — "For the primary/valid-case
  scenario, the product id path parameter MUST refer to an existing
  product" — is not a behavior the mobile app performs or enforces. It
  originates from §4's "Inputs Summary (**for test design**)" table, i.e.
  it describes a constraint on which *test data* to select to exercise the
  valid-id path, not a MUST-behavior like REQ-05–REQ-14 (e.g. "the screen
  MUST display X," "quantity MUST accept only positive integers" — things
  the running app actually does or is required to do). Grouping REQ-15
  under AREA-05 "Test Setup Data" is correct and consistent with its real
  nature, but labeling it "Functional Requirement" in the same
  Classification column as REQ-05–REQ-14 is internally inconsistent: a
  reader scanning the Classification column alone cannot distinguish "the
  system must behave this way" from "testers must pick this kind of
  input." Evidence: REQ-15 row vs. §4 Inputs Summary table heading ("for
  test design") vs. REQ-05–REQ-14 rows (genuine system-behavior MUSTs).
  Severity: real gap, not a nitpick — the classification scheme is meant
  to let Phase 2/3 trust the column at a glance, and this row breaks that.
  Not fixed here per instruction; candidate fix directions (not applied):
  either introduce a distinct classification value (e.g. "Test Data
  Constraint") or move REQ-15's content into a note under AREA-05 instead
  of the REQ-xx/Classification table.

### 2. Any hands-on/device observation anywhere in the artifact?

- **[P1-G02] real gap, most significant finding of this pass.** End-to-end
  re-read of `01_Requirements_Breakdown.md` confirms: **no**, there is no
  observation anywhere in the artifact that came from actually running the
  Expo app on a device/emulator. Every behavioral claim traces to exactly
  one of two sources: (a) direct quotes/citations of the spec text (§1–§5,
  §7), or (b) REQ-16–REQ-22, all explicitly tagged `source: code, not
  spec`, and all of them — including CF-01 and CF-02, the two candidate
  findings — are derived purely from reading `frontend-mobile/App.js` as
  pasted into this session (`repomix-output.md`), not from launching the
  app. I am stating this plainly rather than rounding it up: reading
  source code and running the app are different evidence sources, and
  this artifact currently rests entirely on the former for every §8-derived
  claim. This matters most for CF-01 (category never rendered) and CF-02
  (invalid quantity silently coerced) — exactly the two places a live
  device check could confirm, contradict, or complicate the code-reading
  conclusion (e.g. if the running app is built from a newer/different
  `App.js` than the pasted snapshot, a caching layer masks the behavior,
  or iOS/Android render the same code differently). Side factual note,
  not part of the gap itself: an earlier version of the input file (read
  earlier in this session, before the user replaced it with the current
  8-section version) contained a "Section 0 — VERIFY FIRST" checklist
  instructing exactly this kind of hands-on check; the current
  authoritative 8-section input file no longer contains that section. That
  removal doesn't manufacture the gap, but it does mean nothing in the
  *current* input explicitly re-requests a device check either — so this
  gap won't self-resolve on the next read of the input as it stands.
  Evidence: full-text re-read of `01_Requirements_Breakdown.md` — every
  REQ-16–REQ-22 row and both CF rows cite `§8.x` (i.e. code), never a
  device observation; no other section of the artifact introduces one.
  Severity: real gap, high — it doesn't make REQ-16–REQ-22 or CF-01/CF-02
  wrong, but it means their evidentiary basis is one source, not two, and
  the artifact doesn't flag this limitation as prominently as it flags
  "not spec."

### 3. Does any REQ/OQ/CF wording drift toward treating the code as more authoritative/settled than it should be?

- **[P1-G03] real gap, moderate.** The CF-01 and CF-02 table rows in
  Section 4 state the code side as flat, unqualified fact within the cell
  itself — e.g. CF-01: "category is **never rendered** anywhere on the
  mobile detail screen"; CF-02: "invalid input ... **is never rejected** —
  it is silently coerced to quantity = 1." Neither cell restates, in the
  cell text itself, that this is a static-code-reading conclusion, not a
  confirmed running-app behavior. The mitigating factor is real but
  partial: Section 4's own header ("Candidate Findings — Spec vs. Observed
  Code (**Unconfirmed**, Not Adjudicated Here)") and its intro paragraph do
  carry the caveat at the section level, and REQ-16/REQ-17 (which the CF
  rows reference) are individually tagged `source: code, not spec`. So the
  caveat exists, but only by cross-reference — a reader who reads the CF
  table in isolation, without also holding the section header and REQ-16/
  REQ-17's own phrasing in mind, could come away treating "category is
  never rendered" as a settled fact rather than "per the pasted source
  snapshot, unconfirmed on-device" (this is the same underlying limitation
  as P1-G02, showing up as a wording-precision issue here). Evidence: CF
  table row text in Section 4 vs. Section 4's own header/intro.
- **[P1-G04] nitpick, for contrast.** By comparison, the Section 3 TD table
  (TD-01, TD-03, TD-04, TD-05) is consistently *more* hedged than the CF
  table or CF-referencing OQ rows — e.g. TD-05: "Code suggests yes; **not
  yet confirmed by running the app**," TD-01: "still needs **hands-on
  confirmation** on both iOS and Android." This is good practice, but its
  absence from the CF table (P1-G03) means the artifact is internally
  inconsistent in how firmly it states code-derived claims: cautious in
  Section 3, flatter in Section 4 for the two most consequential findings.
  Not itself a factual error, just a consistency issue worth naming since
  it compounds P1-G03.
- **OQ table check (no new gap found here):** OQ-02 and OQ-04, which both
  reference §8 code facts, explicitly hedge correctly — OQ-02: "this is a
  candidate finding (CF-02), not **a confirmed answer** to 'how it *should*
  be rejected'"; OQ-04: "that describes only the mobile client's reaction
  ... so the underlying question **is still open**." These are not
  drifting toward treating code as settled. OQ-05's phrasing ("REQ-18/§8.3
  **shows this question is moot** for the mobile Add-to-Cart action
  specifically") is a closer call — it states a firm conclusion ("moot")
  rather than "conditionally moot per this static snapshot" — but this
  phrasing is inherited near-verbatim from the input's own §8.3 text ("The
  'guest cart allowed?' open question **is moot** for this specific action
  on mobile"), so it is not overreach introduced by the artifact beyond
  what the input itself already asserts. Flagged here for completeness,
  not logged as a separate `[P1-Gxx]`, since the artifact did not amplify
  the input's own certainty.

## 2026-07-06 — Fix pass (P1-G01, P1-G03, P1-G04)

P1-G01 fixed: REQ-15 reclassified to a new "Test Data Constraint" value,
with a preamble note in Section 2 explaining the scheme. P1-G03/P1-G04
fixed via wording only (CF-01/CF-02 now say "source: static code read;
not yet confirmed by running the app," matching the TD table's hedge
style) — no device data was invented. P1-G02 (no hands-on device
observation exists) remains open by the user's explicit instruction;
device verification is deferred to before Phase 5 is reached (note: this
skill's workflow has only 4 phases, so in practice this means before the
artifact is treated as fully confirmed / before any later phase leans on
CF-01 or CF-02 being settled).

## Summary

Four items logged: `[P1-G01]` real gap (REQ-15 classification
inconsistency), `[P1-G02]` real gap, high severity (no hands-on/device
observation anywhere in the artifact — every §8 claim is code-reading
only), `[P1-G03]` real gap, moderate (CF table states code-side facts
without an inline unconfirmed-on-device qualifier, relying on
cross-reference), `[P1-G04]` nitpick (TD table hedges more consistently
than the CF table, worth aligning). No edits made to
`01_Requirements_Breakdown.md` in this pass — awaiting the user's decision
on which to fix.
