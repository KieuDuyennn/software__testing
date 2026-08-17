# Human review of the AI analysis

## Review method

The files in `docs/analysis/` are retained as the attributed AI/tool-generated
analysis. This review checks their claims against the raw CSV-form JTL logs,
using request/controller separation, nearest-rank percentiles, 30-second buckets
and all five required journey-label counts.

## Misinterpretations found and corrected

| AI/tool claim or risk | Correct value from raw JTL | Why the original reading is incomplete |
|---|---|---|
| A single 300 ms p95 verdict represents every SLO | Load/Stress/Spike/Soak overall p95 values are 10/11/19/11 ms, but the actual limits are login 250 ms, reads 200 ms, writes 300 ms and E2E 1,000 ms | The analyzer accepts one convenience threshold; human review must apply the pre-registered per-label budgets. |
| Successful controller rows equal successful purchases | Controller rows were 8,557/18,797/5,622/9,939, while endpoint-complete lower bounds were 8,547/18,775/5,591/9,934 | JMeter emitted controllers for scheduler-stopped partial tails. Counting them all overstates passed end-to-end transactions. |
| The highest Stress level is the capacity | At 132 VU, stable throughput was about 260.6 req/s, p95 13 ms and errors 0% | Throughput still scaled from the 99-VU level (~196.1 req/s); no knee or threshold violation was observed. Capacity is above the tested range, not exactly 132 VU. |
| Overall Spike p95 proves recovery | Overall p95 was 19 ms; phase values were baseline 11 ms, burst 26 ms and first recovery bucket 12 ms | Mixing phases can hide a burst or delayed recovery. Recovery must be compared bucket-to-bucket against baseline. |
| Soak end memory >10% proves a leak | Working set was 52.8 MB start, 172.0 MB peak and 89.6 MB end, with a mid-run fall from ~170 MB to ~68 MB | The drop is consistent with garbage collection. The remaining +36.8 MB is a suspected accumulation signal, not proof of an unbounded leak. |

## Recommendation judgement

AI-style generic advice was checked against the source. Clearing `userCarts`
after checkout is supported because the array is appended to but never cleared.
Indexes on `users.email` and SQLite WAL are feasible mechanisms but unverified by
these low-latency results. A generic connection pool is hallucinated for the
current single shared `sqlite3.Database` handle. A normal B-tree index cannot
solve `LIKE '%keyword%'` because the leading wildcard prevents a prefix lookup.

## Review conclusion

The computed tables are reproducible, but their automatic verdict is only a
starting point. Scenario phase, label-specific criteria, controller semantics,
source-code mechanism and host limitations must be reviewed before making a
capacity, leak or optimization claim.
