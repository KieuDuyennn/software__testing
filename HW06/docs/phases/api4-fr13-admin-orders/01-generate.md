# API 4 - FR-13 Admin Dashboard - Phase 1: Generate with AI

> Pipeline step 1 of 4.

| Field | Value |
|---|---|
| Pool | C |
| Requirement | FR-13, with FR-12 |
| Endpoint under test | `GET /api/admin/orders` |
| Postman collection | `collections/API4_FR13_AdminOrders.postman_collection.json` |
| Case specification | `scripts/cases/api4_fr13_admin_orders.py` |
| Coverage tally | `reports/coverage_api4-fr13-admin-orders.md` |
| Target set by the brief | >= 35 test cases |
| **Generated** | **73 test cases (2.1x the minimum)** |

## 1. Contract under test

The dashboard has **no endpoint of its own**. FR-13 requires two figures:

- total revenue = the sum of `total_amount` over orders with `status='delivered'`, and
- the total order count.

Both are computed from `GET /api/admin/orders`, so that endpoint is the API
under test. Establishing this was the first generation step, and it is what
turns FR-13 from a UI requirement into a testable API contract.

| Source | Rule |
|---|---|
| FR-13 | Revenue counts `delivered` orders **only** |
| FR-13 | The order count covers all orders, whatever their status |
| FR-12 / SEC-03 | Admin APIs must verify `role='admin'` in the token, not merely that a token exists |
| FR-10 | The aggregate is a projection of the order state machine |
| SEC-01 | The payload must not disclose credential material |
| SEC-05 | Ids and status values must be parameterised |

## 2. How the AI was driven, step by step

### Step 1 - Establish the contract

Produced the mapping above. The consequence for test design: **the revenue
figure is a state-machine assertion, not an arithmetic one.** Checking it means
driving orders into each status and observing whether the aggregate moves.

### Step 2 - Domain partitions

**18 cases**, mostly on the authorisation header: genuine admin, absent, empty,
malformed, wrong signature, wrong scheme, no scheme, and a valid non-admin
token. Then content partitions (other users' orders visible, the joined
`user_name`, an order whose user was deleted), query-string tampering, ordering
stability and the HTTP methods the route does not accept.

### Step 3 - State transitions

**22 cases**. Four cases prove an order in `pending`, `confirmed`, `shipping` or
`canceled` is *excluded* from revenue while still counted in the order total;
one proves a `delivered` order *is* counted; and `A4-ST-006` snapshots revenue
before and after a delivery and asserts the difference is **exactly** the
order's total. Then ten illegal admin transitions, a positive control, an
unknown status value, a missing status field, a non-existent order, and an
end-to-end aggregate consistency check.

### Step 4 - Security

**18 cases**. SEC-03 is exercised with three different kinds of token - a
genuine non-admin token, a wholly forged one, and a real token whose `role`
claim was edited but whose signature was left intact.

The instruction that produced the best case: *escalation cases must request a
**legal** state transition*, so that a refusal can only mean authorisation was
checked. That is what makes `A4-SEC-017` conclusive.

### Step 5 - Schema validation

**15 cases**: the joined admin order schema, the closed status enum,
`user_name` typing including the null case, `created_at` parseability, and the
arithmetic safety the revenue sum depends on.

## 3. Generated test cases

| Dimension | Cases |
|---|---:|
| Domain partitions | 18 |
| State transitions | 22 |
| Security | 18 |
| Schema validation | 15 |
| **Total** | **73** |

### First execution

| Metric | Value |
|---|---:|
| Cases executed | 73 |
| Assertions | 323 |
| Assertions passed | 313 |
| Cases fully passing | 64 |
| **Cases with >= 1 failing assertion** | **9** |
| Client-level request errors | 0 |

| Case | Defect |
|---|---|
| DP-008, SEC-001, SEC-002 | a valid non-admin token reads the entire admin order list |
| SEC-005 | a non-admin performs a legal status transition |
| SEC-006 | a non-admin lists every account |
| SEC-007 | a non-admin deletes another user's account |
| SEC-017 | **a customer marks their own order delivered** |
| ST-016 | `canceled -> delivered` is accepted |
| SCH-010 | the forbidden-response body is the order list, not an error |

### The strongest evidence this collection produced

`A4-SEC-017` is the case worth putting in the report. It builds an order in
`shipping`, has the **order's own owner** call the admin status route with their
ordinary token to mark it `delivered`, then reads the dashboard payload back:

```
a customer must not be able to mark their own order delivered:
expected 'delivered' to equal 'shipping'
```

It succeeded. The missing role check is an information-disclosure
problem - it lets any customer **inflate the company's reported revenue** by
delivering their own orders. That converts an abstract SEC-03 violation into a
concrete business impact, which is what a bug report needs.

`A4-SCH-010` is the quiet one: asked for the shape of a 403 body, the endpoint
returned `200` with an array of 91 orders. The assertion failure literally
reads `expected [ ...(91) ] to have property 'error'`.

### What passed, and why it matters

- **Nine of the ten illegal transitions are correctly refused.** The admin
  status handler does implement FR-10 - it just has one wrong branch
  (`canceled -> delivered`). Reporting it as "the state machine is not
  implemented" would be inaccurate.
- **`A4-ST-006` passed**: delivering a 400,000 order raises revenue by exactly
  400,000. The revenue *arithmetic* is correct; only its authorisation is not.
- **`A4-SCH-003` passed**: `total_amount` is a number here, so the revenue sum
  does not concatenate. The type bug is confined to the product detail route.
- All SEC-05 injection cases passed.

## 4. Notes for the audit phase

1. **DP-008, SEC-001 and SEC-002 are the same defect** tested three ways. File
   once; keep the others as regression coverage.
2. **SEC-006 and SEC-007 target `/api/admin/users`, which is FR-19, not
   FR-13.** They are included because FR-12 covers the whole `/api/admin/*`
   surface. The audit groups this finding under one root cause.
3. **`A4-DP-012` (deleted user) carries a specification gap** - the spec does
   not say how orphaned orders should appear. It asserts only presence.
4. **`A4-SEC-017` overlaps SEC-005** in root cause but not in impact. Keep both:
   one shows the control is missing, the other shows what it costs.
