# API 4 - FR-13 Admin Dashboard - Phase 1: Generate with AI

> Pipeline step 1 of 4. Commit this file on its own (`docs(hw06): generate test
> cases for API 4`) before starting the audit phase.

| Field | Value |
|---|---|
| Pool | C |
| Requirement | FR-13 (with FR-12) |
| Endpoint under test | `GET /api/admin/orders` |
| Postman collection | `collections/API4_FR13_AdminOrders.postman_collection.json` |
| Parameters | `Authorization: Bearer <admin token>` header |
| Target | >= 35 test cases |

## Contract under test

`GET /api/admin/orders` -> every order joined with the ordering user's name. The dashboard derives total revenue and total order count from this payload.

Rules the test cases must hold the implementation to:

- FR-13: total revenue sums `total_amount` over orders with `status = 'delivered'` only.
- FR-13: the dashboard also reports the total order count.
- FR-12 / SEC-03: admin APIs must verify `role = 'admin'` in the token, not merely that a token exists.

Expected state transitions: the aggregate is a projection of the FR-10 state machine

## How the AI was driven, step by step

The brief forbids a single generic prompt. Record each step separately - the
prompt, what came back, and what you did with it. Every prompt and output here
must also appear in `docs/ai-audit/AI_AUDIT.md`.

### Step 1 - Establish the contract

*Goal:* make the AI restate the endpoint's contract from the spec before it
writes any case, so later output can be checked against its own reading.

- **Tool / model:**
- **Timestamp:**
- **Prompt:**
- **Output (summary + link to the full text in the audit log):**
- **My reaction:**

### Step 2 - Domain partitions per parameter

*Goal:* an equivalence-class and boundary table for every parameter, before any
test case is written.

- **Tool / model:**
- **Timestamp:**
- **Prompt:**
- **Output:**
- **My reaction:**

### Step 3 - State transitions

*Goal:* enumerate the reachable states and the legal / illegal transitions,
then a case per transition, including the invalid ones.

- **Tool / model:**
- **Timestamp:**
- **Prompt:**
- **Output:**
- **My reaction:**

### Step 4 - Security (SEC-01..SEC-07)

*Goal:* a case per applicable SEC id. Ask the AI to state which SEC ids do
*not* apply to this endpoint and why - the gaps are as informative as the hits.

- **Tool / model:**
- **Timestamp:**
- **Prompt:**
- **Output:**
- **My reaction:**

### Step 5 - Schema validation

*Goal:* the exact response schema per status code, then assertions that the
response shape matches the spec - no missing fields, no extra fields, correct
JSON types.

- **Tool / model:**
- **Timestamp:**
- **Prompt:**
- **Output:**
- **My reaction:**

## Generated test cases

Full table in `testcases/` (Excel). Summary of what step 1-5 produced:

| Dimension | Cases generated |
|---|---:|
| Domain partitions | |
| State transitions | |
| Security (SEC-01..07) | |
| Schema validation | |
| **Total** | |

## Notes for the audit phase

Anything that looked wrong on first read - record it here now, resolve it in
phase 2.
