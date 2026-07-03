# Boundary Value Analysis Heuristics

Reference for Phase 4 (Boundary Value Analysis). Load only when executing this phase.

## Standard Boundary Technique

For every equivalence class from Phase 2 that is bounded by a numeric or length
limit (`min..max`), generate up to six boundary test cases:

| Boundary | Description |
|---|---|
| min - 1 | Just below the lower bound (invalid) |
| min | Lower bound itself (valid) |
| min + 1 | Just above the lower bound (valid) |
| max - 1 | Just below the upper bound (valid) |
| max | Upper bound itself (valid) |
| max + 1 | Just above the upper bound (invalid) |

If a bound is open-ended (e.g. "quantity must be at least 1, no stated maximum"),
only generate boundaries for the side that has a stated limit — do not invent an
upper bound. Note the absence of the other bound as an Open Question if it seems
like a plausible gap in the requirement (e.g. no max cart quantity could be an
oversight), but don't fabricate a test case for it.

## Boundaries for Common Special Domains

- **Date ranges**: treat the calendar day as the unit. Boundaries are
  `startDate - 1 day`, `startDate`, `startDate + 1 day`, `endDate - 1 day`,
  `endDate`, `endDate + 1 day`. Watch for stated inclusive/exclusive range wording
  in the FR (e.g. "up to and including" vs "before").
- **File sizes**: boundaries are in the unit the FR specifies (bytes/KB/MB) — don't
  silently convert units. `maxSize - 1`, `maxSize`, `maxSize + 1`.
- **Pagination / page counts**: boundaries are page 0 or 1 (whichever the FR defines
  as the first page) and the last valid page number, plus one page past the last
  valid page and (if 1-indexed) page 0 as an invalid/edge case.
- **Rate-limit-like counters** (e.g. "max 5 login attempts"): boundaries are
  `limit - 1` (still allowed), `limit` (last allowed attempt), `limit + 1` (should be
  blocked).

## Business-Rule Cutoffs ("Just Inside" vs "Just Outside")

For thresholds that trigger a business rule rather than a simple accept/reject
(e.g. "orders over $100 get free shipping"), generate boundary cases on both sides
of the cutoff to confirm which side gets the rule applied:

- Just below the cutoff (rule does NOT apply)
- Exactly at the cutoff (confirm whether the FR says "over" [exclusive] or "at
  least"/"or more" [inclusive] — this determines whether the rule applies here)
- Just above the cutoff (rule DOES apply)

If the FR's wording is ambiguous about inclusive/exclusive (e.g. "over $100" is
usually exclusive, but confirm rather than assume for ambiguous phrasing), flag it
as an Open Question instead of guessing which side the boundary value falls on.

## Boundaries on Enumerated / Discrete Values

For an ordered enum (e.g. star rating 1–5, priority Low/Medium/High treated as
ordered), boundaries are the first and last valid members plus the values
immediately outside the valid set (if the underlying type allows out-of-set values,
e.g. rating 0 or 6 for a 1–5 star scale). For unordered enums (e.g. category ∈
{Electronics, Books, Clothing}), boundary analysis does not apply — equivalence
partitioning from Phase 2 already provides full coverage; do not force boundary
cases onto unordered sets.
