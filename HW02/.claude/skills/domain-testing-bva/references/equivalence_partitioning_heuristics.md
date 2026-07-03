# Equivalence Partitioning Heuristics

Reference for Phase 2 (Equivalence Partitioning). Load only when executing this phase.

## Splitting a Single Input Field

For every atomic requirement, identify each input field it constrains, then derive
partitions so that every possible value of the field falls into exactly one partition.

- **Numeric ranges** — if a field must be `min..max`, the classes are:
  - Valid: `min..max`
  - Invalid: `< min` (below range)
  - Invalid: `> max` (above range)
  - If the field has a data type constraint (e.g. integer only), add an invalid class
    for non-numeric / wrong-type input.

- **String length** — if a field must be `minLen..maxLen` characters:
  - Valid: length within `minLen..maxLen`
  - Invalid: length `< minLen`
  - Invalid: length `> maxLen`
  - Invalid: empty string (unless empty is explicitly a valid case — don't assume)

- **Enums / fixed value sets** — e.g. status ∈ {Pending, Shipped, Delivered}:
  - Valid: one class per accepted member, OR one class for "any accepted member" if
    the requirement treats them identically. Only split members into separate classes
    if the requirement says they're handled differently.
  - Invalid: any value outside the set (one class), plus case-sensitivity variants
    only if the requirement specifies case sensitivity.

- **Optional vs mandatory fields**:
  - Mandatory field: "empty/absent" is an **invalid** class.
  - Optional field: "empty/absent" is a **valid** class (the default-handling
    behavior), and you still need valid/invalid classes for when a value IS supplied.
  - Common mistake: treating an optional field's absence as untested, or as invalid
    when the requirement says it's optional.

- **Format constraints** (email, phone, date, etc.):
  - Valid: conforms to the stated format.
  - Invalid: violates the format (malformed structure — e.g. missing "@", wrong
    number of digits). Only enumerate format-violation sub-classes the requirement
    actually implies; don't invent format rules not stated (e.g. don't assume RFC 5322
    email validation unless the FR specifies it).

## Combining Partitions Across Multiple Inputs

When a feature has multiple input fields, avoid combinatorial explosion:

- **Single-fault assumption** (default, use unless the FR implies interacting
  validations): test one invalid class at a time, with all other fields holding a
  valid value. This is what Phase 3 (Domain Test Design) will build test cases from.
- **Multi-fault / combination testing**: only required when the FR explicitly
  describes interaction rules between fields (e.g. "field B is required only if field
  A = X"). In that case, note the dependency explicitly in the equivalence class
  description so Phase 3 can construct a combined test case.
- Do not enumerate the full Cartesian product of all classes across all fields —
  that is Domain Testing's job to minimize, not this phase's job to expand.

## Common Mistakes to Avoid

- **Overlapping partitions**: a value must not be classifiable into two partitions
  at once (e.g. defining `<=100` as valid and `>=100` as invalid — 100 is ambiguous).
  Always make the boundary explicit and exclusive.
- **Missing the invalid partition for optional fields**: optional does not mean
  "no invalid classes" — a supplied-but-malformed value is still invalid.
  Only the "absent" state is valid-by-default.
- **Forgetting the empty/null partition**: for every field, explicitly decide
  whether empty/null is valid or invalid, and state it — don't leave it implicit.
- **Splitting an enum into per-member classes when the requirement treats them
  uniformly** — this inflates the equivalence class count without adding coverage
  value; only split when behavior actually differs per member.
