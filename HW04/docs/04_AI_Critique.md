# AI Critique — HW04 (Mandatory, §10)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184

**Word count:** 263 words (essay body)

The AI accelerated the initial Playwright structure, but several confident outputs were
wrong or incomplete. Its first configuration pointed `baseURL` to port 3000, which is the
EShop API rather than the customer web application. It also generated `getByLabel`
locators without checking whether the visible labels were programmatically associated
with their inputs, and guessed button text that did not exist. More seriously, in FR-11
it derived some expected values from the current implementation instead of the
requirement. This produced contradictory cancellation oracles: one row expected a
shipping order to expose a cancel action while other rows correctly required shipping
cancellation to be refused. A defensive optional-field guard then allowed one control
case to skip its data-integrity assertion entirely.

These failures occurred because the first generation pass treated documentation and
common UI conventions as sufficient evidence. Cases were considered independently, so
the model did not compare expectations across the whole dataset. Runtime probing helped
verify selectors, but it became dangerous when observed product behaviour was reused as
the oracle. The AI also preferred fail-soft code that avoided exceptions, even when a
missing field should have failed fast as invalid test data.

I learned that effective AI collaboration requires separate evidence gates. Requirements
define expected behaviour; source and DOM inspection verify how to reach it; execution
reveals whether the product conforms. These sources must not be substituted for one
another. I now require selector-count probes, cross-row consistency checks, fail-fast
data validation, and a human review stop before execution. A red assertion is preserved
until it is classified, rather than weakened to make the suite appear successful.
