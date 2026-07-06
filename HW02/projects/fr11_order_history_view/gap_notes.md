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
