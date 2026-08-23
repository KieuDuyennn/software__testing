# API 1 - FR-01 Account Registration - Phase 1: Generate with AI

> Pipeline step 1 of 4. Commit this file on its own (`docs(hw06): generate test
> cases for API 1`) before starting the audit phase.

| Field | Value |
|---|---|
| Pool | A |
| Requirement | FR-01 |
| Endpoint under test | `POST /api/register` |
| Postman collection | `collections/API1_FR01_Register.postman_collection.json` |
| Parameters | `name` (string), `email` (string), `password` (string) |
| Target | >= 35 test cases |

## Contract under test

Request `{name, email, password}` -> `200 {"message": "User registered successfully", "id": <int>}`.

Rules the test cases must hold the implementation to:

- FR-01: email must be well formed (`user@domain.com`) and unique.
- FR-01: password >= 8 chars with an uppercase, a lowercase, a digit and a special character from `@ $ ! % * ? &`.
- FR-01: a confirm-password field must be present and must match.
- SEC-01: passwords must not be stored in plaintext.
- SEC-05: queries must be parameterised.
- SEC-06: the client must not be able to set `role`.

Expected state transitions: new -> registered -> authenticated (login succeeds with the new credentials)

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
