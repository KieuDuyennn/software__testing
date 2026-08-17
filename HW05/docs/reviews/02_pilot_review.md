# Pilot execution review

## Purpose and scope

This was a diagnostic run, not the official Load result. It used 2 VU, a
2-second ramp and 30-second scheduler duration to verify XML loading, CSV
variables, token correlation, content assertions, HTML generation and backend
resource sampling before committing the full plans.

| Item | Value |
|---|---|
| Plan | `evidence/pilot/23127184_Load_20260817PILOT.jmx` |
| Run | `evidence/pilot-runs/23127184_Load_20260817PILOT_20260817-215433/` |
| Backend PID | `22512` |
| Rate limiter | Disabled with `LOADTEST=1` |
| Raw request samples | 117 |
| Request error rate | 0.00% |
| Overall request p95 | 17 ms |
| Complete journey lower bound | 22 |
| Backend memory | 52.6 → 53.4 MB; +0.8 MB |

## What passed

- JMeter loaded the generated XML and all three CSV pools.
- Login token extraction authenticated cart and checkout requests.
- Product and checkout content assertions produced no failures.
- Raw JTL, HTML report, JMeter log, run record and resources CSV were produced.
- The resource sampler monitored the explicitly selected backend PID.

## Misinterpretation found during human review

JMeter emitted 23 successful Transaction Controller rows, but request-label
counts were 24 login, 24 search, 24 detail, 23 cart and 22 checkout. At least one
controller row therefore represented a scheduler-ended partial journey rather
than a complete five-step purchase.

Reporting “23/23 transactions passed” would be wrong even though the JMeter row
itself says success. The analyzer was corrected to accept every required
`--journey-label`, report the minimum endpoint-complete lower bound, and separate
tail/ambiguous controller rows. The corrected pilot result is:

- endpoint-complete journeys: 22;
- conservative passed: 22;
- failed: 0;
- tail/ambiguous: 1.

This correction must be used for all official run analyses. The pilot also shows
why raw JTL review is necessary even when both the summary and controller rows
report 0% errors.

## Decision

The workflow implementation is technically ready for official execution. The
official runs remain blocked until the student closes unnecessary applications,
records at least 2 GB free RAM, and starts same-frame JMeter/Task Manager video
capture. Pilot numbers must not be presented as Load/Stress/Spike evidence.

