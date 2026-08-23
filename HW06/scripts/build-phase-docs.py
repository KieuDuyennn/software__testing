#!/usr/bin/env python3
"""Generate the per-API phase document skeletons under docs/phases/.

The brief (Section 6) defines a four-step pipeline per API - generate, audit,
extend, execute - and Section 12 asks for one commit per step. This script lays
down one document per step per API, pre-filled with that API's endpoint, its
requirement ids and the coverage dimensions that must be evidenced.

Safe to re-run: existing files are never overwritten.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PHASES = ROOT / "docs" / "phases"

APIS = [
    {
        "slug": "api1-fr01-register",
        "n": 1,
        "title": "API 1 - FR-01 Account Registration",
        "pool": "A",
        "fr": "FR-01",
        "endpoint": "POST /api/register",
        "collection": "API1_FR01_Register",
        "params": "`name` (string), `email` (string), `password` (string)",
        "spec": (
            "Request `{name, email, password}` -> `200 "
            '{"message": "User registered successfully", "id": <int>}`.'
        ),
        "rules": [
            "FR-01: email must be well formed (`user@domain.com`) and unique.",
            "FR-01: password >= 8 chars with an uppercase, a lowercase, a digit "
            "and a special character from `@ $ ! % * ? &`.",
            "FR-01: a confirm-password field must be present and must match.",
            "SEC-01: passwords must not be stored in plaintext.",
            "SEC-05: queries must be parameterised.",
            "SEC-06: the client must not be able to set `role`.",
        ],
        "states": "new -> registered -> authenticated (login succeeds with the new credentials)",
    },
    {
        "slug": "api2-fr06-product-detail",
        "n": 2,
        "title": "API 2 - FR-06 Product Detail",
        "pool": "A",
        "fr": "FR-06",
        "endpoint": "GET /api/products/:id",
        "collection": "API2_FR06_ProductDetail",
        "params": "`id` (path parameter, integer)",
        "spec": "Request `GET /api/products/:id` -> the product record.",
        "rules": [
            "FR-06: the detail view shows image, name, price, description and category, "
            "so all of those fields must be present and correctly typed.",
            "REST contract: an unknown id is `404`, not `200` with an empty body.",
            "SEC-05: the `:id` path parameter must be parameterised, not concatenated.",
        ],
        "states": "product present -> deleted -> absent",
    },
    {
        "slug": "api3-fr11-order-history",
        "n": 3,
        "title": "API 3 - FR-11 Order History (user)",
        "pool": "B",
        "fr": "FR-11 (with FR-10)",
        "endpoint": "GET /api/orders/my-orders  (+ GET /api/orders/:id)",
        "collection": "API3_FR11_OrderHistory",
        "params": "`Authorization: Bearer <token>` header; `id` (path parameter) on the detail route",
        "spec": (
            "`GET /api/orders/my-orders` -> the caller's orders, each with order id, "
            "date, total and current status."
        ),
        "rules": [
            "FR-11: a user may see only their own orders.",
            "FR-10: status is one of `pending`, `confirmed`, `shipping`, "
            "`delivered`, `canceled`; cancellation is allowed only from "
            "`pending` or `confirmed`.",
            "SEC-02: security-relevant APIs require a valid JWT.",
        ],
        "states": (
            "pending -> confirmed -> shipping -> delivered, plus "
            "pending|confirmed -> canceled, observed through order history"
        ),
    },
    {
        "slug": "api4-fr13-admin-orders",
        "n": 4,
        "title": "API 4 - FR-13 Admin Dashboard",
        "pool": "C",
        "fr": "FR-13 (with FR-12)",
        "endpoint": "GET /api/admin/orders",
        "collection": "API4_FR13_AdminOrders",
        "params": "`Authorization: Bearer <admin token>` header",
        "spec": (
            "`GET /api/admin/orders` -> every order joined with the ordering "
            "user's name. The dashboard derives total revenue and total order "
            "count from this payload."
        ),
        "rules": [
            "FR-13: total revenue sums `total_amount` over orders with "
            "`status = 'delivered'` only.",
            "FR-13: the dashboard also reports the total order count.",
            "FR-12 / SEC-03: admin APIs must verify `role = 'admin'` in the "
            "token, not merely that a token exists.",
        ],
        "states": "the aggregate is a projection of the FR-10 state machine",
    },
]

GENERATE = """# {title} - Phase 1: Generate with AI

> Pipeline step 1 of 4. Commit this file on its own (`docs(hw06): generate test
> cases for API {n}`) before starting the audit phase.

| Field | Value |
|---|---|
| Pool | {pool} |
| Requirement | {fr} |
| Endpoint under test | `{endpoint}` |
| Postman collection | `collections/{collection}.postman_collection.json` |
| Parameters | {params} |
| Target | >= 35 test cases |

## Contract under test

{spec}

Rules the test cases must hold the implementation to:

{rules}

Expected state transitions: {states}

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
"""

AUDIT = """# {title} - Phase 2: Audit (human review)

> Pipeline step 2 of 4. Every AI-generated case gets a VALID / INVALID /
> INCOMPLETE label with reasoning, and the invalid or incomplete ones get
> corrected. You are responsible for the final test cases.

| Field | Value |
|---|---|
| Endpoint | `{endpoint}` |
| Requirement | {fr} |
| Cases reviewed | |
| VALID | |
| INVALID | |
| INCOMPLETE | |

## Labelling rules used

- **VALID** - the case is correct as written: right precondition, right input,
  right expected result per the specification, and it is actually executable.
- **INVALID** - the expected result contradicts the spec, the case is not
  executable, or it duplicates another case.
- **INCOMPLETE** - the idea is right but something is missing: no precondition,
  a vague oracle ("should work"), no cleanup, or an assertion too weak to catch
  the defect it targets.

A trap worth watching for: a case that asserts the SUT's *current* behaviour
rather than the *specified* behaviour passes but proves nothing. Label those
INVALID - they hide defects.

## Audit table

| TC ID | Dimension | Label | Reasoning | Correction applied |
|---|---|---|---|---|
| | | | | |

## Corrections made

Describe the substantive rewrites, not the typos.

## Patterns in what the AI got wrong

Feed this into `docs/AI_CRITIQUE.md`.
"""

EXTEND = """# {title} - Phase 3: Extend

> Pipeline step 3 of 4. At least five test cases of your own that the AI missed,
> weighted towards security and state transitions, each with an explanation of
> *why* the AI missed it.

| Field | Value |
|---|---|
| Endpoint | `{endpoint}` |
| Requirement | {fr} |
| Cases added | (>= 5) |

## Added test cases

### EXT-01 |

- **Dimension:** security / state transition / domain / schema
- **Requirement or SEC id:**
- **Precondition:**
- **Steps:**
- **Expected result:**
- **Actual result:**
- **Why the AI missed it:** prompt quality / model limitation / a property of
  the API that is not visible in the specification (be specific - "the spec
  documents the happy path only, so nothing in the text hints that the detail
  route has no auth middleware" is a real reason; "the AI was lazy" is not)

### EXT-02 |

### EXT-03 |

### EXT-04 |

### EXT-05 |

## Why these gaps existed

Group the five reasons into causes. The three that usually appear:

1. **The spec does not describe it.** The AI reads `api_specification.md`; a
   missing auth middleware or a wrong comparison operator is invisible there.
   Only the requirement document, or the implementation, exposes it.
2. **The prompt framed the endpoint in isolation.** Cross-resource attacks
   (IDOR, privilege escalation, ownership) need a second actor, which a
   single-endpoint prompt never introduces.
3. **The AI asserts observed behaviour.** Asked what a response looks like, it
   describes what the SUT returns - which cannot, by construction, find a bug.
"""

EXECUTE = """# {title} - Phase 4: Execute

> Pipeline step 4 of 4. Run the cases with Newman, capture the report, and
> triage every failure into either a defect or a test-case correction.

| Field | Value |
|---|---|
| Endpoint | `{endpoint}` |
| Collection | `collections/{collection}.postman_collection.json` |
| Environment | `config/eshop-local.postman_environment.json` |
| Data file | `data/{data}` |
| HTML report | `reports/{collection}.html` |
| Console transcript | `evidence/newman-console/` |

## How to run

```powershell
# The whole suite, with the backend started and stopped for you:
.\\scripts\\Invoke-ApiTests.ps1 -Api {n}

# Or, with the backend already running (LOADTEST=1):
npm run test:api{n}
```

The backend must be started with `LOADTEST=1`. Without it the 200-request /
15-minute rate limiter returns HTTP 429 partway through the run and every later
assertion fails for the wrong reason. The global test script asserts this
explicitly so a rate-limited run is never mistaken for a defect.

Starting the backend drops and re-seeds `database.sqlite`, so each run begins
from identical state.

## Run record

| Run | Date/time | Requests | Assertions | Passed | Failed | Report |
|---|---|---:|---:|---:|---:|---|
| | | | | | | |

## Failure triage

Every failed assertion is either a defect in the SUT or a defect in the test
case. Decide which, one row per failure.

| # | Failing assertion | Expected | Actual | Verdict | Bug ID |
|---|---|---|---|---|---|
| | | | | | defect -> `docs/bugs/BUG_REPORT.md` |

## Evidence captured

- [ ] Newman HTML report in `reports/`
- [ ] Console transcript showing the `X-Student-Id` line (Section 11 evidence)
- [ ] Screenshot of the Postman console with the pre-request log
- [ ] Hostname in the Newman output matches the deployment (`localhost` is accepted)
"""

TEMPLATES = {
    "01-generate.md": GENERATE,
    "02-audit.md": AUDIT,
    "03-extend.md": EXTEND,
    "04-execute.md": EXECUTE,
}

DATA_FILES = {
    1: "api1_fr01_register.csv",
    2: "api2_fr06_product_detail.csv",
    3: "api3_fr11_order_history.csv",
    4: "api4_fr13_admin_orders.csv",
}


def main():
    written, skipped = 0, 0
    for api in APIS:
        folder = PHASES / api["slug"]
        folder.mkdir(parents=True, exist_ok=True)
        ctx = dict(api)
        ctx["rules"] = "\n".join("- " + r for r in api["rules"])
        ctx["data"] = DATA_FILES[api["n"]]
        for filename, template in TEMPLATES.items():
            path = folder / filename
            if path.exists():
                skipped += 1
                continue
            path.write_text(template.format(**ctx), encoding="utf-8")
            written += 1
    print("phase docs: {0} written, {1} left untouched".format(written, skipped))


if __name__ == "__main__":
    main()
