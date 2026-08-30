# Per-dimension coverage checklist

Run this against a finished API before declaring the pipeline complete for it.
Target: >= 35 cases per API.

## Domain partitions

For **every** parameter, not just the interesting ones:

- [ ] One valid representative per valid class
- [ ] One case per invalid class
- [ ] Boundaries: min, min−1, min+1, max, max−1, max+1
- [ ] Empty string, whitespace-only, missing key entirely, explicit `null`
- [ ] Wrong JSON type (number where a string is specified, and the reverse)
- [ ] Very long input (1 000+ characters)
- [ ] Unicode and Vietnamese diacritics
- [ ] Leading/trailing whitespace
- [ ] For numbers: zero, negative, non-integer, scientific notation, overflow
- [ ] For ids in a path: non-existent, zero, negative, non-numeric

## State transitions

- [ ] Every state in the machine is reached by at least one case
- [ ] Every **legal** transition is exercised and accepted
- [ ] Every **illegal** transition is exercised and rejected - this is where the
      defects live
- [ ] Terminal states reject every further transition
- [ ] Each case documents how it reaches its starting state
- [ ] The state is verified by reading it back, not by trusting the response

## Security

- [ ] SEC-01..SEC-07 each either covered or explicitly marked not-applicable
      with a reason
- [ ] At least two actors set up (see `sec-rules.md`)
- [ ] Anonymous access attempted on every protected route
- [ ] Cross-user access attempted on every owned resource
- [ ] Non-admin token attempted on every admin route
- [ ] Injection attempted in every string parameter and path segment
- [ ] Privileged fields (`role`, `id`, `user_id`) injected into every write body

## Schema validation

- [ ] One case per documented status code
- [ ] `additionalProperties: false` - catches fields the spec never promised
- [ ] Every field's JSON **type** asserted, not just its presence
- [ ] Enum fields constrained to their legal values
- [ ] Schema assertions repeated across **every** id partition, not one id
- [ ] Error responses have an asserted shape too, not just a status code

## Case-quality gate

Every case, regardless of dimension:

- [ ] Names the FR or SEC id it enforces
- [ ] Expectation derived from the spec, never from the SUT's response
- [ ] Runs independently of the other cases and of run order
- [ ] Cleans up, or uses unique data (`{{$guid}}`) so re-runs stay valid
- [ ] Its assertion message says what broke, not just "failed"
