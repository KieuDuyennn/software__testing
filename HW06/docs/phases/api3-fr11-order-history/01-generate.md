# API 3 - FR-11 Order History (user) - Phase 1: Generate with AI

> Pipeline step 1 of 4. Commit this file on its own (`docs(hw06): generate test
> cases for API 3`) before starting the audit phase.

| Field | Value |
|---|---|
| Pool | B |
| Requirement | FR-11 (with FR-10) |
| Endpoint under test | `GET /api/orders/my-orders  (+ GET /api/orders/:id)` |
| Postman collection | `collections/API3_FR11_OrderHistory.postman_collection.json` |
| Parameters | `Authorization: Bearer <token>` header; `id` (path parameter) on the detail route |
| Target | >= 35 test cases |

## Contract under test

`GET /api/orders/my-orders` -> the caller's orders, each with order id, date, total and current status.

Rules the test cases must hold the implementation to:

- FR-11: a user may see only their own orders.
- FR-10: status is one of `pending`, `confirmed`, `shipping`, `delivered`, `canceled`; cancellation is allowed only from `pending` or `confirmed`.
- SEC-02: security-relevant APIs require a valid JWT.

Expected state transitions: pending -> confirmed -> shipping -> delivered, plus pending|confirmed -> canceled, observed through order history

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
