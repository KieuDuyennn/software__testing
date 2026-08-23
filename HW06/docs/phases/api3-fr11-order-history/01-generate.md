# API 3 - FR-11 Order History - Phase 1: Generate with AI

> Pipeline step 1 of 4.

| Field | Value |
|---|---|
| Pool | B |
| Requirement | FR-11, with FR-10 |
| Endpoints under test | `GET /api/orders/my-orders`, `GET /api/orders/:id`, `PUT /api/orders/:id/cancel` |
| Postman collection | `collections/API3_FR11_OrderHistory.postman_collection.json` |
| Case specification | `scripts/cases/api3_fr11_order_history.py` |
| Coverage tally | `reports/coverage_api3-fr11-order-history.md` |
| Target set by the brief | >= 35 test cases |
| **Generated** | **89 test cases (2.5x the minimum)** |

## 1. Contract under test

| Source | Rule |
|---|---|
| FR-11 | *"Nguoi dung chi xem duoc don hang cua chinh minh"* - a user may see only their own orders |
| FR-11 | The history displays order id, order date, total and current status |
| FR-10 | `pending -> confirmed -> shipping -> delivered`, and `pending\|confirmed -> canceled` |
| FR-10 | Cancellation is permitted **only** from `pending` or `confirmed` |
| SEC-02 | These routes require a valid JWT |
| SEC-03 | Admin order routes require `role='admin'` |
| SEC-05 | The order id must be parameterised |

## 2. How the AI was driven, step by step

### Step 1 - Establish the contract

The restatement produced the scoping decision that defines this collection:
FR-11's single sentence about ownership makes the *detail* route
(`GET /api/orders/:id`) and the *cancel* route part of FR-11's surface, not just
the history list. All three are therefore in scope.

### Step 2 - Domain partitions

**30 cases**. Because the primary input is a bearer token, the partitioning is
mostly on *authentication states*: absent, empty, malformed, wrong scheme, no
scheme, wrong signature, lowercase keyword, and a token whose account has since
been deleted. Then content partitions (zero / one / many orders), query-string
tampering, HTTP methods, and id partitions on the detail and cancel routes.

### Step 3 - State transitions

**24 cases** - the largest state folder in the assignment, and the point of
choosing this API. The AI was instructed to build the full state x event matrix
and generate a case for **every cell**, legal and illegal alike, because the
illegal ones are where defects hide.

### Step 4 - Security

**20 cases** across two users plus an admin. The instruction that mattered:
*IDOR and ownership are undetectable with a single actor* - so every ownership
case builds a victim and an attacker in its fixture.

### Step 5 - Schema validation

**15 cases**: the order schema, the closed FR-10 status enum, `created_at`
parseability, `total_amount` arithmetic safety, and the four fields FR-11
requires the history to display.

## 3. State machine and the cases covering it

```
   pending ------> confirmed ------> shipping ------> delivered
      |                |                                  (terminal)
      +----> canceled <+                canceled is terminal
```

| Cases | Coverage |
|---|---|
| ST-001..005 | each state reached and observed in history |
| ST-006, ST-007 | legal cancellation from `pending` and `confirmed` |
| ST-008..010 | **illegal** cancellation from `shipping`, `delivered`, `canceled` |
| ST-011 | cancellation is visible in history afterwards |
| ST-012..021 | ten **illegal** admin transitions, one per cell |
| ST-022 | status value outside the closed set |
| ST-023 | order data preserved across the full lifecycle |
| ST-024 | cancelling another user's order |

## 4. Generated test cases

| Dimension | Cases |
|---|---:|
| Domain partitions | 30 |
| State transitions | 24 |
| Security | 20 |
| Schema validation | 15 |
| **Total** | **89** |

### First execution

| Metric | Value |
|---|---:|
| Cases executed | 89 |
| Assertions | 393 |
| Assertions passed | 383 |
| Cases fully passing | 80 |
| **Cases with >= 1 failing assertion** | **9** |
| Client-level request errors | 0 |

Only nine failures - far fewer than API 1 or 2 - so the first thing done was to
check the cases were not passing **vacuously**. Three pieces of evidence say
they were not:

1. `A3-ST-002`..`005` assert that the fixture order *is present in history*
   with a specific status. A fixture that failed to drive the order would fail
   that first assertion. They pass, so the multi-step chain
   (register -> login -> checkout -> admin login -> status transitions) works.
2. `A3-DP-011` and `A3-DP-012` assert exact history lengths of 1 and 3.
3. `A3-SEC-004`'s failure message quotes a real order payload
   (`{"id":38,"user_id":177,...}`), which only exists if the fixtures ran.

The nine failures:

| Case | Defect |
|---|---|
| DP-009 | a token whose account was deleted still authenticates |
| ST-008 | an order in `shipping` can be cancelled - FR-10 forbids it |
| ST-020 | `canceled -> delivered` is accepted |
| SEC-001 | anonymous read of any order returns 200 |
| SEC-002 | cross-user read returns 200 |
| SEC-003 | ids are enumerable from 1 anonymously |
| SEC-004 | a customer's shipping address is disclosed to an anonymous caller |
| SEC-008 | an ordinary user reaches `GET /api/admin/orders` |
| SEC-009 | an ordinary user performs a **legal** status transition |

### A correction made during generation

`A3-SEC-009` was written first with an **illegal** transition
(`pending -> delivered`). It failed with `400` - but a 400 there is ambiguous:
it could mean "refused because you are not an admin" *or* "refused because the
transition is illegal". The case could not distinguish the two, so it could not
prove the role claim was ever checked.

It was rewritten to request a **legal** transition (`pending -> confirmed`), so
that only authorisation can refuse it. It now returns `200`, which proves the
role claim is never inspected. `A4-SEC-005` applies the same reasoning.

This is worth carrying into the AI critique: the first version of the case
looked correct, ran, and produced a red result for the wrong reason.

### What passed, and why it matters

- **ST-017 (`shipping -> canceled` via the admin route) passed** while
  **ST-008 (cancel from `shipping` via the user route) failed.** The two routes
  disagree about the same rule: the admin status endpoint enforces FR-10's
  cancellation rule and the user cancel endpoint does not. That is a much
  sharper finding than "cancellation is broken".
- Nine of the ten illegal admin transitions are correctly refused; only
  `canceled -> delivered` slips through.
- `A3-SEC-005` passed: `my-orders` itself is correctly scoped. The ownership
  defect is confined to the detail route.

## 5. Notes for the audit phase

1. **`A3-DP-008` (lowercase `bearer`) and `A3-DP-013` (ordering) carry
   specification gaps** and assert weakly. Tighten or accept explicitly.
2. **SEC-001, SEC-002, SEC-003 and SEC-004 are one defect** - the missing
   middleware on `GET /api/orders/:id` - seen from four angles. File once.
3. **SEC-008 belongs to API 4's requirement (FR-13/FR-12), not FR-11.** It is
   here because FR-11's scoping rule motivated it. Decide where it is reported
   so it is not double-counted.
4. **ST-008 and ST-020 are separate defects** in separate handlers, even though
   both are FR-10 violations. Do not merge them.
