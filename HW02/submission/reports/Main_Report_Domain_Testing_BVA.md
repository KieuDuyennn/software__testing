# HW02 Main Report: Domain Testing and Boundary Value Analysis on EShop

- **Student ID:** 23127184
- **Course:** CS423/CSC13003, Software Testing (FIT@HCMUS)
- **SUT:** EShop (https://github.com/ttbhanh/eshop-sut)
- **Submission repository:** https://github.com/KieuDuyennn/KTPM_23127184/tree/main/HW02
- **Date:** 2026-07-07

> **How this report was made.** This report pulls together the four per-feature
> test-design workspaces that I built, reviewed, and approved one phase at a time.
> The full step-by-step work for each feature lives in
> `../projects/<feature>/output/`. This document explains the process, walks through
> how I applied each technique, and links to the detailed artifacts. Every AI
> interaction that produced or changed an artifact is recorded word for word in the
> AI Audit Report (`AI_Audit_Report.md` and `prompt_logs.md`). I put this report
> together with Claude Code, and that step is logged in the audit trail too.

---

## 1. What I tested and how (overview)

I picked four features, one from each of the four pools, and ran each of them through
the same testing workflow. FR-06 is listed under Pool A in the spec catalog, but here
it is tested through the Expo mobile app, so it serves as this submission's Pool D
(Mobile App) feature:

| Feature | Pool | Folder |
|---|---|---|
| FR-01 Account registration | A | `../projects/fr01_account_registration/` |
| FR-06 Product detail view (Mobile) | D | `../projects/fr06_product_detail_view/` |
| FR-11 Order history view (user) | B | `../projects/fr11_order_history_view/` |
| FR-13 Dashboard | C | `../projects/fr13_dashboard/` |

For each feature I applied two techniques from class: **Domain Testing** (Section 3)
and **Boundary Value Analysis** (Section 4). Section 5 reports where the AI came up
short. Section 6 points to the bug report. The full counts (designed, executed,
passed, failed, bugs) are in the top-level [`../README.md`](../README.md) test
summary; they are not repeated here.

---

## 2. How I applied the techniques

### 2.1 The four-phase workflow (Agent Skill: `domain-testing-bva`)

I did not just ask the AI to "generate test cases." I walked it through the technique
one step at a time, using a reusable Agent Skill I built
(`../skills/domain-testing-bva/SKILL.md`). Every feature went through the same four
phases:

| Phase | What happens | Output file |
|---|---|---|
| 1. Requirement analysis | Break the feature down into small, single-idea requirements (REQ-xx). Mark each as a real rule, an observation, or an assumption. If the spec does not say something, write it down as an Open Question instead of guessing. | `01_Requirements_Breakdown.md` |
| 2. Equivalence partitioning | Group inputs and outputs into valid and invalid classes (EC-xx), and trace each class back to a requirement and forward to a test. | `02_Equivalence_Partitioning.md` |
| 3. Domain test design | Bundle as many valid classes as possible into a few "combined valid" tests. Give each invalid class its own "isolated invalid" test, and never put two invalid conditions in one test. | `03_Domain_Test_Cases.md` |
| 4. Boundary value analysis | For each field with an ordered range, state the precision and step first, then test just below, at, and just above each bound. If a bound is open-ended, say so instead of inventing a limit. | `04_Boundary_Value_Test_Cases.md` |

The rules I made the AI follow (enforced by the skill and by `../skills/CLAUDE.md`):

- **Never invent a rule.** Anything the spec does not state becomes an Open Question
  (OQ-xx), not a quiet assumption.
- **Keep a full trail:** feature to REQ-xx to EC-xx to TC-xx or BVA-xx.
- **One phase at a time.** After each phase the AI stops. I review it, ask for a
  self-critique, decide which findings are real, direct the fixes, and only then
  approve. The workflow state is tracked by a script, never edited by hand.
- **Self-critique before I approve.** For each phase I ran a checklist review, saved
  the findings to a dated section of `gap_notes.md`, and then marked each finding as
  Applied, Deferred, or Rejected.
- **One git commit per phase per feature** (see `../git_commit_log.txt`).

### 2.2 How I reviewed the AI

No phase was approved automatically. Each artifact carries a verdict I stated myself
at approval time, and that verdict is in the audit log. Most phases needed at least
one round of self-critique and targeted fixes before I approved them. The
`gap_notes.md` file in each feature folder keeps the full "finding to decision" trail.

---

## 3. Domain Testing report

This section explains how I applied domain testing to each feature. The full tables
are in each feature's `03_Domain_Test_Cases.md`.

### 3.1 FR-01, Account Registration (Pool A)

| Metric | Value |
|---|---|
| Atomic requirements | 18 (REQ-01 to REQ-18) |
| Equivalence classes | 34 (inputs and outputs) |
| Domain test cases | 24 |

Steps I followed:

1. I split the registration form into fields (full name, email, password, confirm
   password) and split the password rule into five separate requirements, one per
   condition (length, lowercase, uppercase, digit, special character).
2. I turned each field into valid and invalid classes. For example, email became
   "valid format," "no @," "no domain," "no local part," and "empty."
3. I bundled all the valid classes into a small number of "combined valid" tests,
   and gave each invalid class its own "isolated invalid" test so a failure points to
   one cause.
4. I caught a spec inconsistency early: the UI asks for a confirm-password field, but
   the API body does not include one. I recorded this as OQ-01 and split the main
   valid test into a UI version (TC-01a) and an API version (TC-01b).
5. During review I found that pinning the confirm-password value to a constant would
   sneak a second fault into the password tests, so I redefined that test-data rule so
   each password test isolates exactly one fault.

Artifacts: [`../projects/fr01_account_registration/output/`](../projects/fr01_account_registration/output/)

### 3.2 FR-06, Product Detail View (Pool D)

| Metric | Value |
|---|---|
| Atomic requirements | 22 |
| Equivalence classes | 43 |
| Domain test cases | 13 |

Steps I followed:

1. This is mostly a read-and-display screen, so I partitioned each display field
   (image, name, price, description, category) and the quantity input into classes.
2. I built product fixtures for the normal case and for the edge cases (empty image,
   empty name, empty or null price, empty description, dangling category), because one
   product record can only hold one value per field at a time.
3. Valid classes went into a few combined tests; each empty or null field and each bad
   quantity value got its own isolated test.
4. For quantity I kept two competing predictions side by side (reject the bad value,
   or silently default it to 1) instead of guessing which one the code does, and told
   the tester to record what actually happens.
5. Since the spec never says whether viewing a product needs a login, I did not assume
   it. I recorded it as an Open Question and noted that every test assumes no login
   only to stay runnable.

Artifacts: [`../projects/fr06_product_detail_view/output/`](../projects/fr06_product_detail_view/output/)

### 3.3 FR-11, Order History View, user (Pool B)

| Metric | Value |
|---|---|
| Atomic requirements | 22 |
| Equivalence classes | 21 (8 input, 13 output) |
| Domain test cases | 8 |

Steps I followed:

1. This is a read plus authorization feature, so I did not partition it by input
   field. Instead I partitioned by authorization state (valid token on your own
   resource, valid token on someone else's resource, no token, bad token), by
   order-id ownership (your own order, another user's existing order, an id that does
   not exist), and by output (the five status values plus an out-of-set catch-all,
   and an empty-state class).
2. I kept the three order-id ownership classes separate on purpose, because the spec
   does not say whether "another user's order" and "nonexistent order" behave the same.
3. During review I noticed the ownership rule was named in the traceability but never
   actually tested. I extended TC-01 with an order that belongs to a different account
   and a "must not appear" check. Without that, a serious data-leak bug (returning
   every user's orders) would have slipped through.

Artifacts: [`../projects/fr11_order_history_view/output/`](../projects/fr11_order_history_view/output/)

### 3.4 FR-13, Dashboard (Pool C)

| Metric | Value |
|---|---|
| Atomic requirements | 17 |
| Equivalence classes | 22 |
| Domain test cases | 8 |

Steps I followed:

1. I broke the dashboard into two parts: admin access control (only an admin should
   see it) and revenue aggregation (only delivered orders count toward revenue).
2. I wrote tests for each access-control condition (valid admin token, no token, bad
   token, valid non-admin token) and for the revenue math (delivered orders counted,
   other statuses excluded).
3. I gave the empty-state situations their own tests (no orders at all, and orders
   that exist but none delivered), with separate checks for the revenue value and the
   order count.
4. A phase-1 citation error and a non-atomic access-control requirement were caught by
   self-critique and fixed before I approved (commits `ee9cce0`, `4f45529`).

Artifacts: [`../projects/fr13_dashboard/output/`](../projects/fr13_dashboard/output/)

---

## 4. Boundary Value Analysis report

For each feature I looked for fields with an ordered numeric range and tested right at
their edges. The full tables are in each feature's `04_Boundary_Value_Test_Cases.md`.

### 4.1 FR-01, password length and name length

BVA test cases: **7**.

- Password length has a stated minimum of 8. I stated the step (whole numbers, step of
  1) first, then tested the 7 versus 8 edge.
- I also tested the 0 versus 1 edge, which is the boundary between "missing field" and
  "weak password" outputs. This one is easy to miss because it sits between two
  classes rather than on the quoted rule.
- Full name has no stated minimum, so I derived an implicit minimum of one character,
  labeled it clearly as my inference, and tested around it.

### 4.2 FR-06, quantity and price

BVA test cases: **4** (BVA-01 restates TC-04 on purpose, so there are 16 distinct runs
in total, as stated in the artifact).

- Quantity has a stated minimum of 1, so I tested 0, 1, and 2 (just below, at, and just
  above), with the step declared up front.
- Price has no stated minimum. At first the AI dropped price from BVA. During review I
  reversed that to stay consistent with my own FR-13 work, derived an implicit floor of
  0 (clearly marked as an inference, not a spec quote), and added a test for price
  equal to -1. I raised a new Open Question about whether a negative price is even a
  reachable state.

### 4.3 FR-11, order id

BVA test cases: **3**.

- Order id is the only ordered field here, so I tested ids -1, 0, and 1. The spec does
  not say whether ids are 0-indexed or 1-indexed, so I kept both readings open as
  Open Questions instead of picking one.
- Status, authorization state, and empty-state are not ordered ranges, so I left them
  out of BVA on purpose and said why.

### 4.4 FR-13, revenue aggregation

BVA test cases: **6**.

- The revenue total sums the `total_amount` of delivered orders. I derived an implicit
  floor of 0 for a single order's amount and tested around it (negative, zero, and
  small positive amounts, including small decimals to check rounding).

---

## 5. AI gap analysis (what the AI missed, and why)

This is task 3 from the assignment. Everything below was **missing from the AI's first
draft** and would have shipped if I had approved the raw output. The full details are
in each feature's `gap_notes.md` (finding plus decision) and in the audit log's
verdict and reasoning columns.

### 5.1 Test-design and technique gaps

| # | Feature / phase | What the AI missed on the first draft | Why it happened (my read) |
|---|---|---|---|
| 1 | FR-01, phase 2 | A real technique error: it modeled password length as a "must equal X" class instead of a range, so the "empty" class overlapped the "too short" class, and its own self-check still ticked "no overlapping partitions." | It reused the common "exact length" template and then wrote the self-check as boilerplate instead of checking it against its own table. A self-graded checklist is not proof. |
| 2 | FR-01, phase 3 | A single-fault violation: pinning the confirm-password value to a constant made six password tests secretly carry a second fault (a mismatch). | It reasoned row by row and never re-checked the shared data rule against each row's "one fault only" claim. |
| 3 | FR-01, phase 4 | It missed the 0 versus 1 edge between "missing field" and "weak password," and only tested the 8-character edge. | It anchored on the number the spec quoted (8) and did not look for edges that sit between two classes. |
| 4 | FR-11, phase 3 | It named the ownership rule in the traceability but never actually tested it, so a data-leak bug that returns every user's orders would have passed. | It treated "mentioned in the trace" as "covered." A missing negative test is invisible unless you ask "what bug would slip through here?" |
| 5 | FR-06, phase 3 | It stated as fact that the feature needs no login, when the spec is simply silent on it. That unmarked assumption sat under all 13 tests. | It filled the gap with the most likely reading instead of raising a question. Models tend to flatten "the spec says nothing" into "the spec says no." |
| 6 | FR-06, phase 4 | It dropped price from BVA as "no stated threshold," which contradicts my own FR-13 work on a similar money field. | It worked one feature at a time and did not check its own earlier decision for consistency. |
| 7 | FR-13, phase 1 | A citation error (it quoted the wrong spec section) plus access-control conditions bundled into one non-atomic requirement. | Long-context quoting drifted, and it merged related conditions for a tidier sentence. |
| 8 | Cross-cutting | The self-check sections repeatedly over-claimed, for example "every N/A has a stated reason" when six cells were blank. | The self-check is written by the same process it is checking, so it shares the same blind spots. Only an outside review catches this. |

**What I take from this:** every phase needed the self-critique, decide, fix loop.
None of the four features' first drafts were good enough to approve as-is; every first
review in the audit log is marked INCOMPLETE, none VALID.

### 5.2 Bugs the AI did or did not predict

The bug determinations themselves are mine and live in
[`Bug_Report.md`](Bug_Report.md) (nine confirmed bugs, BUG-01 to BUG-09). Here I only
map those confirmed bugs back to the design phase to show which ones the AI's tests
were aimed at and which one it would have missed on its own.

- **The AI's tests were pointed at most of the bugs.** The designs included tests that
  directly targeted the areas where BUG-01, BUG-02, BUG-05, BUG-06, BUG-08, and BUG-09
  later turned up. For FR-06 the AI even flagged the quantity-validation and category
  concerns itself as "candidate findings" (CF-01, CF-02) before any test ran, which
  lines up with BUG-06.
- **The AI would have missed BUG-07 on its own.** BUG-07 is the order-history data leak
  (any user can read another user's order). The AI's first draft named the ownership
  rule but never wrote a test that reads someone else's order. I added that negative
  test during review (see gap #4 above). This is the clearest case where raw AI output
  would have let a serious bug through, because the AI mistook "requirement mentioned"
  for "requirement tested."
- **Some findings surfaced through follow-up probing, not the first design.** The price
  type inconsistency behind BUG-04 came out while exploring how the price field behaved
  across product ids, not from a test the AI designed up front.

The reasons track the gaps in Section 5.1: the AI is strong at covering the paths it
can see stated in the spec, but weak at the tests that only matter when you ask what a
malicious or unusual caller could do, and at staying consistent with its own earlier
decisions.

---

## 6. Bug reporting

The test execution results and all bug reports are kept separately, in
[`Bug_Report.md`](Bug_Report.md), which I wrote entirely myself per the course
integrity policy, and on the group's GitHub Issues page with screenshots. That report
covers ten candidate observations that resolve to nine confirmed bugs (BUG-01 merges
two of them). The raw Actual-versus-Expected output that the bug report draws on is in
[`test_execution_log.md`](test_execution_log.md) and the raw transcripts next to it.

---

## 7. Test summary and appendices

- **Test summary (features, designed, executed, passed, failed, bugs):**
  [`../README.md`](../README.md)
- **AI Audit Report:** [`AI_Audit_Report.md`](AI_Audit_Report.md), full log table in
  [`prompt_logs.md`](prompt_logs.md)
- **AI Critique:** [`AI_Critique.md`](AI_Critique.md)
- **Git commit log:** [`../git_commit_log.txt`](../git_commit_log.txt)
- **Agent Skills:** [`../skills/`](../skills/), which holds `domain-testing-bva` (the
  four-phase test-design workflow) and `ai-audit-log` (automatic audit-trail
  recording). Demo video: [demo video link to be added before submission]
