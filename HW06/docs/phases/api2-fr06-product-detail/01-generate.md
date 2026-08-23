# API 2 - FR-06 Product Detail - Phase 1: Generate with AI

> Pipeline step 1 of 4.

| Field | Value |
|---|---|
| Pool | A |
| Requirement | FR-06 |
| Endpoint under test | `GET /api/products/:id` |
| Postman collection | `collections/API2_FR06_ProductDetail.postman_collection.json` |
| Case specification | `scripts/cases/api2_fr06_product_detail.py` |
| Coverage tally | `reports/coverage_api2-fr06-product-detail.md` |
| Parameters | `id` (path parameter, integer) |
| Target set by the brief | >= 35 test cases |
| **Generated** | **83 test cases (2.4x the minimum)** |

## 1. Contract under test

```http
GET /api/products/:id
200 OK -> { id, name, price, description, imageUrl, category_id }
```

| Source | Rule |
|---|---|
| FR-06 | The detail view shows image, name, price, description and category - so all five must be present and correctly typed |
| FR-06 | The quantity input takes positive integers, which means `price` has to be arithmetic-safe on the client |
| REST contract | A resource that does not exist is `404`, not `200` with an empty body |
| SEC-05 | The `:id` path parameter must be parameterised, not concatenated |
| SEC-04 | Stored product names must come back as data, never as markup |
| FR-12 / SEC-03 | `POST` / `PUT` / `DELETE /api/products` share this route's path and must require a valid token **and** `role='admin'` |
| SEC-02 | **Not applicable** to the read - product browsing is public by design (documented by `A2-SEC-010`) |

## 2. How the AI was driven, step by step

Same five-stage procedure as API 1, with one deliberate change of emphasis
carried over from what API 1's run taught: **the request envelope and the HTTP
method are part of the input domain**, not just the documented parameters. On
API 1 that decision is what found the HTTP 500 (BUG-11).

### Step 1 - Establish the contract

The AI restated the endpoint and enumerated the constraining rules (section 1).
The restatement raised the question that shaped the whole collection: FR-06
requires the price to be *displayed and multiplied by a quantity*, so its JSON
**type** - not merely its presence - is a requirement.

### Step 2 - Domain partitions

One parameter, so the partitioning went deep rather than wide: **35 cases** on
`:id` and the HTTP method. Existence classes, numeric boundaries, wrong-type
classes, formatting edges and routing edges.

### Step 3 - State transitions

**10 cases** on the product existence lifecycle. Every fixture creates its own
throwaway product; the five seeded products are never modified or deleted, so a
case that deletes cannot disturb a case that runs later.

### Step 4 - Security

**16 cases**. SEC-05 injection through the path parameter (5 payloads plus an
integrity check), SEC-04 stored XSS, SEC-01 disclosure, and the FR-12 / SEC-03
access control on the mutating siblings of this route.

### Step 5 - Schema validation

**22 cases** - the largest schema folder in the assignment, because this is
where the endpoint is weakest. The instruction given to the AI was explicit:
*repeat the strict schema and the price-type assertion across **every** seeded
product id, not one representative*, because type drift can be data-dependent.

## 3. Domain partition table

| Class | Representatives | Expected | Cases |
|---|---|---|---|
| Valid, every seeded id | 1, 2, 3, 4, 5 | 200 with that product | DP-001..005 |
| Boundary of the seeded range | 5, 6 | 200 / 404 | DP-006, DP-007 |
| Non-existent | 999999 | 404 | DP-008 |
| Zero and negative | 0, -1, -0 | 404 / 400 | DP-009..011 |
| Integer overflow | 2^31, 22 digits | 404, no 5xx | DP-012, DP-013 |
| Wrong type | `abc`, `1.5`, `1e0`, `0x1`, `+1`, `null`, `undefined`, `true`, `NaN`, `Infinity`, `1abc`, `abc1` | 400 | DP-014..025 |
| Formatting edges | `01`, ` 1`, `%20`, 300 digits | no 5xx | DP-026..029 |
| Routing edges | extra segment, trailing slash | 404 / list route | DP-030, DP-031 |
| HTTP method | POST, PATCH, HEAD | 404/405, 200 | DP-032..034 |
| Idempotence | repeated read | identical payload | DP-035 |

## 4. Generated test cases

| Dimension | Cases |
|---|---:|
| Domain partitions | 35 |
| State transitions | 10 |
| Security | 16 |
| Schema validation | 22 |
| **Total** | **83** |

### First execution

| Metric | Value |
|---|---:|
| Cases executed | 83 |
| Assertions | 403 |
| Assertions passed | 362 |
| Cases fully passing | 51 |
| **Cases with >= 1 failing assertion** | **32** |
| Client-level request errors | 0 |

Zero client-level errors, so every case is executable as written. Failure
clusters:

| Cluster | Cases | Apparent cause |
|---|---:|---|
| Any unresolvable id returns `200 {}` | 20 | non-existent, zero, negative, and all twelve wrong-type ids |
| `price` typed as a string on even ids | 4 | SCH-002, SCH-004, SCH-007, SCH-009 |
| Product write routes have no auth at all | 5 | SEC-011..015 |
| Deleted product still returns `200 {}` | 1 | ST-004 |
| Detail disagrees with the list | 1 | ST-006 |
| Created product also affected by the type bug | 1 | ST-010 |

### The strongest evidence this collection produced

`A2-SCH-007` does not just assert the type - it demonstrates the consequence:

```
adding 1 must not concatenate: expected '280000001' to deeply equal 28000001
```

Adding 1 to product 2's price yields the string `"280000001"`. Any client that
computes a line total gets a nonsense number.

`A2-SCH-021` **passed**, and that is the diagnostically useful part: the list
route `GET /api/products` types every price correctly. The corruption exists
only on the detail route, which `A2-ST-006` confirms by diffing the two views
of the same product. That narrows the defect from "prices are broken" to "the
detail handler coerces the type", which is a far more actionable report.

### What passed, and why it matters

- **All five SEC-05 injection cases passed**, and `A2-SEC-006` confirms the
  catalogue survives them. Parameterised queries hold here.
- **`A2-DP-034` (HEAD) and `A2-DP-031` (trailing slash)** behave correctly.
- **`A2-ST-008`** shows product detail survives its category being deleted.

## 5. Notes for the audit phase

1. **`A2-DP-026`, `A2-DP-027`, `A2-DP-028`, `A2-DP-029`, `A2-DP-031` carry
   specification gaps** and assert only `no 5xx` or a routing observation.
   That is a weak oracle - decide whether FR-06 justifies tightening them.
2. **20 domain cases share one root cause.** They are twenty *symptoms* of a
   single missing guard in the detail handler. Group them before filing.
3. **`A2-SEC-011`..`015` arguably belong to FR-15, not FR-06.** They are
   included because FR-12 names these routes explicitly and they share the
   path. Confirm that scoping decision rather than leaving it implicit.
4. **`A2-DP-006` duplicates `A2-DP-005`** (both request id 5). It is kept as a
   distinct boundary case, but a reviewer could reasonably label it INVALID as
   a duplicate.
