# HW06 - AI Critique

**Word count: 258**

The AI produced broad coverage quickly, but its first output still contained
plausible-looking weaknesses that required human review. The clearest error was
`A2-DP-006`: it duplicated `A2-DP-005` by requesting product 5 again and called
the duplicate a boundary case. I labelled the generated version INVALID and
replaced it with a percent-encoded-id case. `A1-SEC-013` was more subtle. The
test failed, but its title blamed client-supplied role injection. Another case
proved that the role field was ignored; the actual cause was missing role
authorization on the admin route. I therefore labelled it INCOMPLETE and
corrected its traceability and title. The AI also favored single-request
oracles. It checked that canceling a shipping order should return an error, but
did not verify the post-state. My student-designed `A3-HR-001` performed an
independent history read and proved that the order really changed from
`shipping` to `canceled`. Similarly, `A4-HR-004` checks both rejection and
atomicity after a non-admin transition attempt.

These misses came from three limitations: specification gaps encouraged weak
“no 5xx” oracles; endpoint-by-endpoint prompting hid cross-route invariants;
and fluent case titles made duplicated or incorrectly attributed tests appear
credible. Execution alone was not enough either—a red assertion can identify a
real symptom while explaining the wrong cause. The principle I learned is to
treat AI output as a review queue, not as evidence. Every case needs an
independent trace to an FR/SEC rule, a deterministic precondition, and an oracle
that does not copy observed behavior. Failures must then be clustered by root
cause and strengthened with post-condition or cross-route checks before they
become bug reports.
