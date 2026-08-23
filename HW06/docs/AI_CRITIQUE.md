# HW06 - AI Critique

**Word count: 249**

## Final critique

Human review found several weaknesses in the generated cases. `A2-DP-006`
requested product 5, which duplicated `A2-DP-005`, although its title described
a boundary case. I marked it INVALID and replaced it with a percent-encoded ID
case. `A1-SEC-013` also had an incorrect explanation. Its title blamed a role
value supplied by the client. A separate case showed that the server ignored
that value. The actual defect was missing role authorization on the admin
route. I changed its audit status to INCOMPLETE and corrected the traceability.

The first generated set relied heavily on single-response checks. For example,
it expected an error when cancelling a shipping order but did not read the
order again. `A3-HR-001` added that post-condition check and showed that the
order changed from `shipping` to `canceled`. `A4-HR-004` added a similar state
check after a non-admin transition attempt.

Three conditions contributed to these misses. Some requirements do not define
strong boundary behavior, so several drafts could assert only that the server
must avoid a 5xx response. Endpoint-focused generation missed invariants that
span multiple routes. Clear titles also made duplicate or incorrectly
attributed cases appear credible before inspection.

Execution exposed symptoms, but it did not validate the explanation attached
to each test. I therefore treated every generated case as a draft. Acceptance
required a rule reference, deterministic setup, executable oracle, and review
of the resulting state. Failed assertions were grouped by root cause before
being reported as bugs. This process produced fewer unsupported conclusions
and stronger evidence for the defects that remained.
