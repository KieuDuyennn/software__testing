# Gap Notes — fr13_dashboard

## 2026-07-06 — Phase 1 self-critique (per user checklist)

Re-reading `output/01_Requirements_Breakdown.md` against
`input/Functional_Requirement.md` before approval. Findings only — nothing
fixed yet. Each finding tagged `[P1-Gxx]` with evidence and an honest
severity call (real gap vs. nitpick).

### 1. Atomicity — any REQ merging two independently-testable rules?

On the two examples the user specifically flagged:
- **PASS** — delivered-inclusion (REQ-05) and other-status-exclusion (REQ-06)
  are already split into two separate REQs, not merged.
- **PASS** — valid-JWT-required (REQ-08) and role-must-be-admin (REQ-09) are
  already split into two separate REQs, not merged.

But two *other* atomicity issues exist that weren't named in the prompt's
examples:

- **[P1-G01] real gap** — REQ-08 and REQ-09 each state "the dashboard **and**
  its underlying admin APIs" as a single combined access surface (inherited
  verbatim from §3.3's own phrasing). This conflates two potentially distinct
  surfaces — a frontend dashboard route vs. the `/api/admin/*` endpoints —
  into one MUST statement. If the two surfaces enforce access differently
  (e.g. the API correctly returns 401/403 but a client-side-only dashboard
  route doesn't re-check role, or vice versa), neither REQ-08 nor REQ-09 can
  attribute the failure to a single surface. Evidence: REQ-08, REQ-09
  statements in `01_Requirements_Breakdown.md`.
- **[P1-G02] real gap** — REQ-08 ("valid JWT required") does not split "no
  token" vs. "invalid/malformed token" into separate atomic sub-conditions.
  This project's own FR-11 precedent split exactly this distinction into
  REQ-16/REQ-17 for the same reason (a bug affecting only one condition
  should stay distinguishable at the requirement level). Evidence: REQ-08
  statement; contrast with `fr11_order_history_view/output/01_Requirements_Breakdown.md`
  REQ-16/REQ-17.

### 2. Any REQ inferred beyond the spec? Quote check per REQ

Quotes verified as direct/accurate for: REQ-01, REQ-03, REQ-04, REQ-05,
REQ-06, REQ-07, REQ-09, REQ-10, REQ-11, REQ-12, REQ-13. Two issues found:

- **[P1-G03] real gap** — REQ-08's Source Reference cites "§3.3 ...
  (JWT-presence clause, per FR-12)", but the literal §3.3 bullet 1 text is
  "The dashboard and its underlying admin APIs MUST be accessible only to
  accounts with `role = 'admin'`" — that sentence is about the **role**
  requirement, not JWT presence/validity. The parenthetical "(JWT-presence
  clause, per FR-12)" is my own inferential label, not a quote of FR-13 text.
  The actual direct textual support for "a valid JWT is required" is §5:
  "No token / invalid token: access denied." — which was never cited. This
  contradicts the artifact's own Self-Check claim that "each REQ row cites
  the exact section/quote" (Self-Check item 1). Evidence: REQ-08 Source
  Reference cell vs. §3.3/§5 text in `input/Functional_Requirement.md`.
- **[P1-G04] nitpick** — REQ-14's statement adds an interpretive clause
  ("meaning the value summed into revenue (REQ-05) may rest on a
  client-controlled number rather than a backend-verified one") beyond a
  literal restatement of the §7 bullet. This is a reasonable analytical
  bridge, not an invented business rule or threshold, so severity is low —
  but it is inference layered on the quote, not the quote itself. Evidence:
  REQ-14 vs. §7 "total_amount trustworthiness" bullet.
- **[P1-G05] nitpick** — REQ-02 bundles three distinct facts (endpoint path,
  request body shape, the 5-value status enum) into one row. Lower severity
  since REQ-02 is tagged Observation, not a testable FR-13 business rule.
  Evidence: REQ-02 vs. §2.

### 3. Is the exclusion rule its own REQ, or only implied inside inclusion?

**PASS** — REQ-06 ("Orders whose status is pending/confirmed/shipping/
canceled MUST NOT contribute to total revenue") is a fully separate row from
REQ-05 (inclusion), not folded into it or left implicit. This matches the
user's original special instruction 1.

### 4. Does access control cover admin / valid-but-non-admin / no-or-invalid-token? Any REQ treating "valid token" as sufficient?

**PASS (mostly)** — REQ-09 explicitly states a valid JWT alone is NOT
sufficient (role must be admin), so no REQ treats "valid token" as
sufficient on its own. All three cases are represented: admin (implicit
success precondition satisfying both REQ-08+REQ-09), valid-but-non-admin
(REQ-09), no-or-invalid-token (REQ-08). However, per **P1-G02** above, the
"no-or-invalid-token" case is handled as one merged condition rather than
two atomic ones, so the *coverage* is present but not fully atomic.

### 5. Open Questions vs. checklist — what's missing?

- **[P1-G06] real gap** — No Open Question asks whether "no token" and
  "invalid/malformed token" produce the **same or different** denied-access
  response (status code/body). Current OQ-08 only contrasts "no/invalid
  token" (as one bucket) against "valid token + role=user" (401 vs 403); it
  never asks whether "no token" and "invalid token" differ *from each
  other*. This is a direct consequence of P1-G02 — fr11 had an equivalent
  question (OQ-07) that this artifact lacks. Evidence: OQ-08 wording in
  `01_Requirements_Breakdown.md`.
- **[P1-G07] nitpick (partially covered by OQ-01)** — No Open Question asks
  whether the dashboard's own access enforcement (if a separate frontend
  route/guard exists) can be verified independently of the underlying
  `/api/admin/orders` API's access check, given REQ-08/REQ-09 bundle
  "dashboard" and "admin APIs" together (P1-G01). OQ-01 already flags that no
  dedicated dashboard endpoint is confirmed, which partially covers this, but
  does not explicitly raise the dashboard-vs-API enforcement-parity question.
  Evidence: REQ-08/09 wording + OQ-01.

### 6. FR/Observation/Assumption labeling — password mismatch and total_amount contradiction correctly labeled?

**PASS** — REQ-13 (admin password mismatch) and REQ-14 (client-supplied
`total_amount` vs. README FR-08 backend-recompute contradiction) are both
labeled **Observation**, matching the user's explicit instruction 4. No
other REQ appears mislabeled: REQ-01/02/03 (API contract facts) and
REQ-10/11/12 (test setup data) are Observations; REQ-04 through REQ-09 (the
actual MUST-statements from §3.1/3.2/3.3) are Functional Requirements.
Assumptions section states "None identified," and no REQ actually asserts an
unstated business rule as fact — though see P1-G03, which is a citation
defect (wrong/inferred source reference) rather than a mislabeling of the
REQ's own FR/Observation/Assumption tag.

### 7. Does any REQ silently assume "total order count" includes all statuses?

**PASS** — REQ-07 explicitly states "Scope by status is not stated in the FR
— not assumed here; see OQ-02," and OQ-02 correctly leaves the scope
unresolved rather than guessing. No REQ or OQ silently assumes all-statuses
or delivered-only scope.

## Suggested Verdict

**INCOMPLETE.** Two explicitly-flagged merge risks (delivered-inclusion vs.
exclusion; valid-JWT vs. role=admin) were correctly avoided, and item 3/4/6/7
checks pass cleanly. But four real gaps remain: REQ-08/REQ-09 conflate the
dashboard and admin-API access surfaces (P1-G01); REQ-08 conflates "no
token" and "invalid token" into one atomic unit, inconsistent with this
project's own FR-11 precedent (P1-G02); REQ-08's Source Reference cites an
inferred annotation rather than the actual supporting quote, which is in §5,
not §3.3 (P1-G03) — this directly contradicts the artifact's Self-Check
claim of exact quoting; and the resulting Open Questions are missing a
no-token-vs-invalid-token response-parity question (P1-G06). P1-G04, P1-G05,
and P1-G07 are lower-severity nitpicks. Final verdict is yours to decide.
