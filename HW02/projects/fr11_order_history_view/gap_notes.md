# Gap Notes — fr11_order_history_view

## 2026-07-06 — Phase 1 self-critique (per user checklist)

Re-reading `output/01_Requirements_Breakdown.md` against
`input/Functional_Requirement.md` before approval. Findings only — nothing
fixed yet.

### 1. Coverage — §3, §4, §5 sentence-by-sentence

**§3.1** (2 sentences)
- PASS — "A user MUST be able to view only their own orders." → REQ-05.
- PASS — "A user MUST NOT be able to view another user's orders." → REQ-06.

**§3.2** (intro + 4 fields)
- PASS — Order ID → REQ-08; Order date → REQ-09; Total amount → REQ-10;
  Current status → REQ-11.

**§3.3** (3 sentences)
- PASS — Vietnamese translation → REQ-12.
- PASS — Color distinction → REQ-13.
- PASS — Five status values → REQ-14; "(from the FR-10 state machine)" clause
  → REQ-19 (Observation).

**§4 Inputs Summary** (3 table rows)
- Row "Authenticated user (JWT token) | token | Required; identifies whose
  orders are returned":
  - "Required" — loosely backed by REQ-01, but REQ-01's Source Reference cites
    only §2, not this §4 row.
  - **GAP** — the clause "identifies whose orders are returned" has no REQ
    citing it. REQ-05 covers the ownership *outcome* ("view only their own
    orders") but its Source Reference cites only §3.1. The specific idea in
    §4 — that the token is *how* whose-orders-to-return gets determined — is
    never explicitly traced to any REQ.
- Row "Order id ... | integer | Must belong to the requesting user":
  - PASS for the constraint → REQ-07.
  - **GAP (minor)** — the "integer" type descriptor itself is not captured in
    any REQ or Observation. Nothing currently records that Order id is
    integer-typed, which Phase 2/4 will need for domain/BVA design (e.g.
    non-numeric id, negative id, id `0`).
- Row "Order status ... | enum | One of: ...":
  - PASS → REQ-14. (See Item 6 — this row's own "Inputs Summary" label
    conflicts with status actually being an output.)

**§5 Expected Outputs** (4 bullets)
- PASS — bullet 1 (own orders list w/ 4 fields, VN + color) → REQ-08..REQ-13.
- PASS — bullet 2 (another user's order id denied) → REQ-07.
- PASS — bullet 3 (no/invalid token rejected) → REQ-15.
- PASS — bullet 4 (empty state) → REQ-16.

**Verdict: GAP** — 1 clause in §4 row 1 uncited; 1 minor type descriptor in §4
row 2 uncited. All sentences in §3 and §5 are fully covered.

### 2. Open Questions

- Input §7 has exactly 8 bullets; breakdown maps OQ-01..OQ-08 to them 1:1 in
  the same order. **PASS** — no §7 bullet is missing from the breakdown.
- Hidden-assumption scan across REQ-01..REQ-19: none assign a color, an HTTP
  status code, or a sort order. REQ-13 requires color distinction without
  naming a color (left to OQ-05); REQ-07/REQ-15 require denial/rejection
  without naming a status code (left to OQ-06/OQ-07); no REQ states a sort
  order. **PASS** — no REQ found that smuggles in an unstated concrete value.
- **GAP** — the input file's header/overview block (lines 1-5: "Pool B —
  Shopping Cart and Checkout (per HW02 group assignment)" and "Source of
  truth: ... README.md, Section 5, FR-11") is not decomposed into any REQ,
  Observation, or OQ at all — it was skipped entirely in Phase 1. "Pool B —
  Shopping Cart and Checkout" is a non-obvious pool assignment for a
  read-only order-history-viewing feature, and nothing in the artifact flags
  this for a cross-check against README §5's actual FR-11 framing.

### 3. Atomicity

- **GAP** — REQ-01 folds two independently-testable assertions ("list
  endpoint requires auth" AND "detail endpoint requires auth") into one REQ.
  A bug that adds auth middleware to one route but not the other would not be
  distinguishable at the requirement level.
- **GAP** — REQ-15 folds two failure conditions ("no token" and "invalid
  token") **and** both endpoints into a single REQ ("If no token or an
  invalid token is provided to either endpoint, the request MUST be
  rejected"). This is inconsistent with OQ-07, which already suspects "no
  token" and "invalid token" may produce *different* response shapes — if
  they can differ, they arguably should not share one REQ.
- **GAP** — REQ-07 folds a precondition ("order id MUST belong to the
  requesting user") and its consequence ("if it belongs to a different user,
  MUST be denied / not returned") into a single REQ. This repo's own prior
  Phase 1 artifact (`projects/fr01_account_registration/output/01_Requirements_Breakdown.md`,
  REQ-13 vs. REQ-14) split an analogous precondition/consequence pair into
  two separate REQs — REQ-07 is inconsistent with that established pattern.
- **GAP (minor)** — REQ-18 (Observation) bundles the seed-account credentials
  with the admin-password source-inconsistency note in one row. Not a
  correctness risk since it's an Observation, not an FR, but still two
  distinct facts in one row.
- PASS — REQ-08..REQ-11 (one field each), REQ-12/REQ-13 (Vietnamese kept
  separate from color, matching the checklist's own example), and REQ-14
  (single enumeration fact) are each atomic.

### 4. Classification

- PASS — admin password mismatch (README `Admin123!` vs. setup_guide.md
  `admin123`) is classified Observation → REQ-18. Not asserted as FR.
- PASS — the client-supplied `total_amount` / FR-08 recompute contradiction
  is captured only as an Open Question → OQ-02, never asserted as FR. REQ-10
  only requires *displaying* the field; it does not assert the value's
  trustworthiness or how it's computed.
- **GAP** — same finding as Item 2's last bullet: the "Pool B —
  Shopping Cart and Checkout" vs. "README.md, Section 5, FR-11" framing is
  never classified as an Observation or raised as an OQ; it is simply absent
  from the artifact.

### 5. Scope (FR-08 / FR-10 / FR-02 leakage)

- PASS — FR-02 (authentication mechanics) is confined to the Global
  Precondition (§0), not restated as a REQ; REQ-01/REQ-15 only assert that
  FR-11's own endpoints require/reject on the token, not how FR-02 issues or
  validates it.
- PASS — FR-10 (state-machine origin of the 5 statuses) is confined to
  REQ-19, explicitly classified Observation and explicitly noted as "an
  external requirement not included in this FR-11 input file."
- PASS — FR-08 (recompute-total-amount rule) is confined to OQ-02, never
  asserted as fact in any REQ.
- **No leakage found** for this item.

### 6. Status recorded as displayed OUTPUT, not user input?

- **GAP** — §4's table is titled "Inputs Summary" and lists "Order status
  (value being displayed) | enum | ..." as a row, even though status is not
  actually submittable by the client to either GET endpoint — it is a
  stored/output value. REQ-14's Source Reference cites "§4 Inputs Summary —
  Order status enum" without flagging this label conflict. Functionally,
  REQ-11/REQ-12/REQ-13/REQ-14 are grouped under AREA-04 "Displayed Fields" /
  AREA-05 "Status Presentation" (an output-oriented framing), so the
  *classification* is effectively correct in practice — but the artifact
  never explicitly states "status is a display-only output for these two
  endpoints, not a user-supplied input." This risks Phase 2 mistakenly
  deriving input-side invalid equivalence classes for status (e.g., "invalid
  status value submitted") that don't apply to read-only GET endpoints with
  no status parameter.

## Summary

8 findings total: 2 coverage gaps (Item 1), 1 header/metadata gap (raised
under both Item 2 and Item 4 — same underlying issue), 4 atomicity gaps
(3 substantive: REQ-01, REQ-07, REQ-15; 1 minor: REQ-18), and 1
output-vs-input labeling gap (Item 6, re: REQ-14). Item 5 (scope leakage) had
no findings — fully PASS. Nothing in `01_Requirements_Breakdown.md` has been
changed as a result of this review.

## 2026-07-06 — Disposition of Phase 1 self-critique

Reviewed with the user. Per user decision:

**APPLIED:**
- Atomicity finding on old REQ-01 (auth requirement combining both endpoints)
  — split into new REQ-01 (`GET /api/orders/my-orders`) and REQ-02
  (`GET /api/orders/:id`), each requiring auth independently. All downstream
  REQ IDs renumbered.
- Atomicity finding on old REQ-15 (no-token/invalid-token combined) — split
  into new REQ-16 (no token) and REQ-17 (invalid token). OQ-07 left
  unresolved as-is (still an open question on whether the response *shape*
  differs), only its REQ cross-reference was updated.
- Status output-vs-input labeling gap (Item 6) — new REQ-15 (the five-value
  status enum REQ) now carries an explicit note: "status is a displayed
  output value for these two GET endpoints, not a user-submitted input
  parameter."
- Pool B / README §5 categorization gap (Items 2 and 4) — added as a new
  Observation, REQ-22 under a new AREA-09 (Documentation Metadata), noting
  the mismatch has no test-design impact and is flagged for TA
  clarification.

**DEFERRED (style/low-impact):**
- REQ-07's (now REQ-08) precondition+consequence bundling — left as one REQ;
  order-id ownership precondition and its denial consequence are two sides
  of the same rule and splitting them was judged lower-value than the other
  atomicity fixes.
- §4's "integer" type descriptor for Order id — not promoted to its own
  REQ/Observation; will be captured directly as part of the input's type
  definition when Order id's domain is defined in Phase 2.
- §4 row 1's uncited "identifies whose orders are returned" clause — left
  without a dedicated citation; considered adequately implied by REQ-06
  (own-orders-only) and not worth a separate REQ.
- REQ-18's (now REQ-20) bundling of seed-account credentials with the
  admin-password inconsistency note — left as one Observation row; low
  impact since it's not classified as an FR.

No other sections of `01_Requirements_Breakdown.md` were touched.

## 2026-07-06 — Phase 2 self-critique (per user checklist)

Re-reading `output/02_Equivalence_Partitioning.md` against the task instructions
and `01_Requirements_Breakdown.md` before approval. Findings only — nothing
fixed yet.

### 1. Partitioned by field (FR-01 style) anywhere instead of by
   authorization/ownership/status/empty-state?

- PASS for the four requested groups — EC-01..EC-04 (Authorization), EC-05..EC-07
  (order-id ownership), EC-09..EC-14 (status), EC-15 (empty-state) are all
  partitioned by authorization/ownership/status/empty-state, not by "field" the
  way FR-01 partitioned by Full Name/Email/Password/Confirm Password. Order date
  (REQ-10) and Total amount (REQ-11) were explicitly left unpartitioned (see the
  "Scope note" at the top of the artifact) rather than given FR-01-style field
  sub-classes.
- **GAP** — **EC-08** ("Order id supplied in a non-integer / malformed format")
  is a self-initiated addition, not one of the 3 order-id classes the task
  specified. Structurally it is exactly the FR-01 pattern applied to a path
  parameter instead of a form field: a guideline-(d) "must-be-X" format
  validation (X = valid integer), the same shape as FR-01's email-format
  sub-classes. Even though Order id is a path parameter rather than a form
  field, and even though its purpose (closing the Phase 1 `gap_notes.md`
  integer-type deferral) is legitimate, this arguably reintroduces the exact
  "partition by field/format" pattern the task said not to replicate — it was
  added on my own initiative, not requested.

### 2. All 4 authorization classes present as discrete classes, not ranges?

- PASS — EC-01 (valid token + own resource, both endpoints), EC-02 (valid token +
  another user's resource, detail endpoint only), EC-03 (no token), EC-04
  (invalid/malformed token) are four separate rows in §1.1, each described in
  purely discrete/enumerated terms (no "≥", "≤", "range," or ordering language
  anywhere in their descriptions). The §1.1 preamble explicitly states "no
  boundary-value reasoning applies to them."

### 3. Are the 3 order-id classes (own / other's-existing / non-existent) kept
   separate, not merged into 2?

- PASS — EC-05 (owned by requester), EC-06 (owned by another user, existing),
  EC-07 (does not exist at all) are three separate rows in §1.2. EC-06's Flag
  cell states "Kept distinct from EC-07 per task instruction — see OQ-12";
  EC-07's Flag cell states "Kept distinct from EC-06 per task instruction, not
  merged." The §3 Backward-Trace table also keeps their corresponding outputs
  separate (EC-17 for EC-06, EC-18 for EC-07), noting only that "EC-17/EC-18 not
  yet confirmed distinguishable — OQ-12" as an open question, not a merge.

### 4. All 5 status ECs exist, each tagged OUTPUT, no invented Vietnamese text
   or color value?

- PASS — EC-09 (`pending`), EC-10 (`confirmed`), EC-11 (`shipping`), EC-12
  (`delivered`), EC-13 (`canceled`) are five separate rows in §2.1, each tagged
  via the "Outcome Type" column as "Valid (output)" and via the section heading
  "Status-Mapping Output Classes." No Vietnamese string or color value is stated
  in any of the five rows — each Flag cell instead cites "VN label — OQ-08;
  color — OQ-05," leaving both unresolved as instructed.
- Note (not a gap): a sixth class, EC-14, was added for values outside the
  5-value set (guideline (c)'s mandatory invalid catch-all) — not explicitly
  requested, but required by the reference heuristic for a "set of discrete
  values" partition; noted for visibility, not as a violation.

### 5. Is empty-state its own EC, not folded into "no orders = invalid input"?

- PASS — EC-15 sits in its own subsection (§2.2 "Empty-State Output Class"),
  tagged "Valid (output)" in the Outcome Type column, entirely separate from the
  INPUT authorization/ownership classes (EC-01..EC-08). It is not framed as an
  invalid input condition anywhere; its Traces Back To cell explicitly
  distinguishes it from a request-input EC: "EC-01 (valid auth) plus an external
  data precondition ... which is test-data setup, not a request-input EC."

### 6. Any EC assigning boundary/range treatment to something outside the
   order-id integer domain (smuggled-in BVA for status/auth)?

- PASS — no EC outside §1.2 uses ordering/boundary language. EC-01..EC-04
  (authorization) and EC-09..EC-21 (status/empty-state/outcome) are all
  described in purely discrete/categorical terms. Within §1.2, EC-08 (format
  validity) uses example values (`"abc"`, `"1.5"`, empty path segment) to
  illustrate non-integer input, but these are format-violation examples, not
  ordered boundary values (no `0`, negative value, or magnitude is used as a
  class boundary) — the §1.2 preamble explicitly excludes "magnitude, sign, and
  boundary values such as `0` or a negative id" from this phase. See Item 1,
  however, for the separate finding that EC-08 itself may not have belonged in
  this phase at all.

### 7. Every EC traces to a REQ-xx from Phase 1 — list any that doesn't.

- **GAP** — four classes do not trace to any Phase 1 REQ:
  - **EC-07** ("order id does not exist at all") — Source REQ cell reads "Not
    stated by any REQ — raised only as OQ-12 in Phase 1."
  - **EC-08** (malformed order-id format) — Source REQ cell cites the raw input
    FR's §4 table directly ("§4 Inputs Summary of the input FR states the Order
    id type is 'integer'"), not a Phase 1 REQ-xx.
  - **EC-18** (Not Found output) — Source REQ cell reads "Not stated by any REQ
    (OQ-12 gap)."
  - **EC-21** (malformed-id-format output) — Source REQ cell reads "Not stated
    by any REQ (new OQ-13)."
  This was already self-disclosed in the artifact's own Self-Check line 1
  ("...or explicitly states 'no REQ — OQ-xx gap' when none exists (EC-07, EC-08,
  EC-18, EC-21)"), so it is not a hidden gap — but per a strict reading of
  "every EC traces to a REQ-xx," these four do not, and are listed here as
  requested.

### 8. Empty/null decision made explicitly for every applicable class, not
   skipped?

- PASS (with a documented exception below) — EC-01 through EC-13, EC-15, and
  EC-16 each carry a substantive Empty/Null Decision with a stated reason (e.g.
  EC-03: "This class IS the mandatory empty/null case for the token input — the
  header value is empty/absent"; EC-08: "This IS the empty/null case for the
  order-id format dimension if the path segment is empty..."; EC-15: "This IS
  the mandatory empty/null case for the returned orders collection itself...").
- **GAP** — six classes carry a bare **"N/A"** with no stated reasoning:
  **EC-14**, **EC-17**, **EC-18**, **EC-19**, **EC-20**, **EC-21** (the status
  catch-all row in §2.1, and five of the six rows in §2.3's Request-Outcome
  table). This contradicts the artifact's own Self-Check claim (bullet 5):
  "'N/A' used consistently for empty/null decisions where the condition doesn't
  apply, with a reason stated each time" — for these six rows, no reason is
  actually stated, just the bare marker.

## Summary (Phase 2 self-critique)

8 checks run: 5 clean PASS (items 2, 3, 4, 5, 6), 3 GAPs (item 1: EC-08 may
reintroduce FR-01-style field/format partitioning beyond the requested 3
order-id classes; item 7: EC-07/EC-08/EC-18/EC-21 don't trace to any Phase 1
REQ — already self-disclosed in-artifact but listed here per the explicit
request; item 8: EC-14/EC-17/EC-18/EC-19/EC-20/EC-21 have bare "N/A" empty/null
cells with no stated reason, contradicting the artifact's own Self-Check
claim). No edits made to `02_Equivalence_Partitioning.md`.

## 2026-07-06 — Disposition of Phase 2 self-critique

Reviewed with the user. Of the 3 findings, only Item 8 was applied.

**APPLIED:**
- Item 8 (bare "N/A" empty/null cells) — added a short stated reason to each of
  EC-14, EC-17, EC-18, EC-19, EC-20, EC-21 in `02_Equivalence_Partitioning.md`
  §2.1/§2.3 (e.g. EC-14: "this is an anomaly/defect class, not a normal
  response; no empty/null dimension applies"; EC-17/18: "a denial/not-found
  response has no field-level empty/null dimension to decide"; EC-19/20: "an
  unauthorized rejection has no field-level empty/null dimension to decide";
  EC-21: "a malformed-id error response has no field-level empty/null
  dimension to decide"). Self-Check bullet 5 updated to note the correction.

**REJECTED (reviewed and kept as-is):**
- Item 1 (EC-08 field/format partitioning concern) — rejected. EC-08 fills a
  gap Phase 1 explicitly deferred to this phase (the `01_Requirements_Breakdown.md`
  gap_notes disposition: "order-id type will be captured in Phase 2 domain
  definition"), not a regression back to FR-01's per-field partitioning
  pattern. EC-08 and its missing-REQ-trace note are unchanged.
- Item 7 (EC-07/EC-08/EC-18/EC-21 missing REQ traces) — rejected. These are
  already transparently self-disclosed in the artifact's own Self-Check
  (bullet 1: "...or explicitly states 'no REQ — OQ-xx gap' when none exists"),
  not hidden assumptions, so no change was made.

No other sections of `02_Equivalence_Partitioning.md` were touched.
