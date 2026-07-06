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

## 2026-07-06 — Phase 2 self-critique (per user checklist)

Re-reading `output/02_Equivalence_Partitioning.md` before approval. Findings
only — nothing fixed yet. Each finding tagged `[P2-Gxx]` with evidence and
an honest severity call (real gap vs. nitpick). No backend source code
exists anywhere in this repository (checked via grep across the repo and
`repomix-output.xml`, which only contains this same coursework project's own
files) — any risk theory cited below is a plausible implementation-pattern
argument, not something verified against actual code, exactly the same
epistemic footing as OQ-05's canceled-order risk flag in the artifact itself.

### Specific check — EC-20 vs. EC-21 field-scope asymmetry

**Answer: yes, this is a real, unrationalized inconsistency. EC-20 should be
split.**

- **[P2-G01] real gap, high severity.** EC-20 ("Dashboard's displayed state
  when zero orders exist at all... covers whatever fields the dashboard
  shows in this case — revenue and/or count") bundles two independently
  verifiable behaviors — the revenue field's zero-display and the order
  count field's zero-display — into one output class. EC-21, covering the
  sibling empty-state precondition (EC-10), does NOT do this: it is scoped
  to revenue only. This is an inconsistent atomicity decision, for four
  reasons:
  1. **REQ-04 (revenue) and REQ-07 (order count) are already separate,
     independently-stated atomic requirements** in the APPROVED Phase 1
     artifact — the exact same kind of "independently stated, so
     independently testable" reasoning that justified keeping access
     control's 3 denial conditions unmerged (§2.1's own rationale: "the FR
     never claims the 3 denial paths produce identical output... collapsing
     them here would hide that question rather than test it"). The same
     logic applies to revenue vs. count: nothing in the FR claims they are
     displayed/computed identically, so they shouldn't be silently bundled
     either.
  2. **EC-20's own REQ/OQ Ref cell cites both REQ-04 and REQ-07 together** —
     the only output-class row in the entire artifact that spans two
     different *display fields*. Contrast EC-21's REQ/OQ Ref, which cites
     REQ-04 + REQ-05 — both about the *same* field (revenue). This is
     internal evidence the row is doing double duty.
  3. **A concrete, plausible risk theory supports the split**: `SUM()` over
     an empty group commonly returns `NULL` in SQL, while `COUNT()` over the
     same empty group correctly returns `0` — a well-known class of bug
     that would make the zero-orders revenue display wrong (null/error)
     while the count display stays correct, or vice versa. This is at least
     as strong a risk signal as OQ-05's canceled-order flag, which was
     sufficient by itself to split EC-06 from EC-07 under guideline (e). No
     backend source exists here to confirm/refute it (see note above), so
     the same conservative posture (split rather than merge) should apply.
  4. **Unlike the EC-19/EC-10 asymmetry** (a count-under-EC-10 companion
     class arguably could be missing too), that gap **is** explicitly
     disclosed and deferred via the artifact's own new OQ-14. EC-20's
     bundling carries no equivalent disclosure — it is presented as a
     settled modeling choice ("OQ-03 asks about the dashboard holistically
     without distinguishing fields") but that rationale conflates "the FR's
     wording doesn't distinguish fields" with "the two fields are one
     behavior," when Phase 1 already established they are two separate
     requirements.
  5. Self-Check bullet 6 states EC-09/EC-10 "each" have "its own output
     twin (EC-20, EC-21)," which reads as claiming clean symmetry — it
     never surfaces that one twin (EC-20) is field-combined while the other
     (EC-21) is field-scoped. Not a false statement, but an incomplete one
     that hid the asymmetry from view.

  Not fixing now, per instruction — but if directed, the fix would split
  EC-20 into a revenue-scoped twin and a count-scoped twin (mirroring
  EC-21's shape), renumbering EC-21 onward.

### General checks

1. **Any other output class silently combining 2+ independently-verifiable
   behaviors?** No other instance found. EC-11..EC-17 are each single,
   field/condition-scoped behaviors. EC-18 and EC-19 each carry multiple
   *open questions* about one single output value (format, precision,
   trustworthiness) — that is not the same defect as combining two
   different *displayed fields*, so they PASS. EC-20 (P2-G01 above) is the
   only real instance.
2. **Does EC-19 still correctly avoid guessing OQ-02's scope?** PASS. EC-19's
   own row states "scope of which orders are counted unresolved — OQ-02"
   directly, and its "Traces From: EC-08" reference is consistent with
   EC-08's own explicit "subset undetermined" caveat (§2.3) — nothing in
   EC-19's wording implies a specific scope (e.g. it never says "count of
   all orders" or "count of delivered orders").
3. **Any input/output class missing a counterpart beyond §4's disclosure?**
   One candidate was checked: a count-specific output companion to EC-21
   (i.e., "order count display under the EC-10 precondition"). This is
   *not* a hidden gap — it is exactly what new OQ-14 already anticipates
   and defers pending OQ-02's resolution. No other missing counterpart was
   found beyond the EC-20 issue already covered under P2-G01.
4. **Terminology/ID consistency.**
   - EC IDs are sequential EC-01..EC-21 with no gaps — PASS.
   - **[P2-G02] nitpick.** Input tables (§2.1–2.4) label their citation
     column "REQ Ref", but several of those rows already cite Open
     Questions too (EC-06 cites OQ-05; EC-08 cites OQ-02; EC-09 cites OQ-03;
     EC-10 cites OQ-04) — the same mixed REQ+OQ content that Output tables
     (§3.1–3.5) correctly label "REQ/OQ Ref". The §2 header should match
     §3's for consistency; this is cosmetic, not a substantive defect.

## Suggested Verdict (Phase 2)

**INCOMPLETE.** One real, non-trivial gap: EC-20 bundles two independently
testable display behaviors (revenue, order count) into a single output
class, inconsistent with how this same artifact split access control and
revenue-membership classes elsewhere, and inconsistent with Phase 1's own
REQ-04/REQ-07 separation — a plausible SUM-vs-COUNT-on-empty-set fault
theory means a bug could pass undetected in one field while a test against
the combined class reports "some assertion failed" without isolating which
(P2-G01). One low-severity nitpick: a column-header labeling inconsistency
between §2 and §3 (P2-G02). Everything else checked (guideline application,
OQ-02 scope neutrality, backward traceability, ID formatting) held up.
Final verdict is yours to decide.
