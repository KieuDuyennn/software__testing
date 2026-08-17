# Performance analysis and retest decision

## Evidence and method

All figures below were recomputed from the unedited `result.jtl` files. Request
rows are the five HTTP labels; `E2E purchase journey` controller rows are kept
separate to avoid double counting. Percentiles use the nearest-rank method.
Throughput uses the observed first-to-last sample interval. A complete purchase
is counted conservatively as the minimum count across all five required labels,
so scheduler-stopped tail iterations are not reported as successful journeys.

| Scenario | Official result directory |
|---|---|
| Load | `results/23127184_Load_20260817_20260817-222415/` |
| Stress | `results/23127184_Stress_20260817_20260817-223704/` |
| Spike | `results/23127184_Spike_20260817_20260817-224818/` |
| Soak | `results/23127184_Soak_20260817_20260817-225434/` |

The generated per-scenario calculations are preserved unchanged in
`docs/analysis/`. The interpretation in this document is the reviewed layer.

## Measured results

| Metric | Load | Stress | Spike | Soak |
|---|---:|---:|---:|---:|
| Request samples | 42,810 | 94,104 | 28,325 | 49,727 |
| Complete journeys | 8,547 | 18,775 | 5,591 | 9,934 |
| Requests/s | 64.16 | 157.00 | 105.26 | 52.17 |
| Complete journeys/s | 12.83 | 31.39 | 20.91 | 10.44 |
| Mean response/load time | 4.0 ms | 4.3 ms | 6.3 ms | 4.2 ms |
| Average latency/wait time | 4.02 ms | 4.30 ms | 6.27 ms | 4.17 ms |
| Average connect time | 0.20 ms | 0.17 ms | 0.20 ms | 0.19 ms |
| Request p95 / p99 / max | 10 / 20 / 52 ms | 11 / 19 / 74 ms | 19 / 37 / 111 ms | 11 / 16 / 40 ms |
| E2E p95 / max | 34 / 77 ms | 36 / 88 ms | 64 / 192 ms | 31 / 73 ms |
| Error rate | 0.00% | 0.00% | 0.00% | 0.00% |
| Conservative passed / failed | 8,547 / 0 | 18,775 / 0 | 5,591 / 0 | 9,934 / 0 |
| Tail/ambiguous controller rows | 10 | 22 | 31 | 5 |
| Bandwidth | 27.4 KB/s | 67.2 KB/s | 45.1 KB/s | 22.3 KB/s |
| Backend CPU mean / peak | 2.2 / 4.4% | 4.4 / 8.2% | 2.9 / 11.1% | 2.0 / 3.7% |
| Backend memory start / peak / end | 52.2 / 172.2 / 73.7 MB | 52.8 / 172.8 / 122.2 MB | 53.7 / 178.4 / 64.3 MB | 52.8 / 172.0 / 89.6 MB |

`Latency` and `Connect` are read directly from the JTL columns. On this local
HTTP target, latency is almost equal to elapsed time and connection setup is
negligible. The small values must not be generalized to WAN/TLS deployment.

## Verdict against pre-registered criteria

All endpoint-specific limits passed. Worst observed p95 values were login 25 ms
during Spike (limit 250 ms), search/detail 16/15 ms (limit 200 ms), cart 8 ms
and checkout 24 ms (limit 300 ms). Worst E2E p95 was 64 ms during Spike (limit
1,000 ms). Every request and every endpoint-complete journey passed assertions.

| Scenario criterion | Reviewed result | Verdict |
|---|---|---|
| Load sustains planned rate | 12.83 journey/s including ramp, 97.5% of the planned 13.16 journey/s; stable request buckets were about 67.3 req/s | PASS |
| Stress identifies first failing stage/knee | 33, 66, 99 and 132 VU remained healthy; no threshold violation or knee appeared within the tested range | INCONCLUSIVE CAPACITY, run valid |
| Spike returns within 20% of baseline p95 in 120 s | Request p95 changed from 11 ms baseline to 26 ms burst and 12 ms in the first recovery bucket (+9.1% vs baseline) | PASS |
| Soak holds 10-15 minutes | 27 VU held for 900 s after ramp; stable buckets were 52.8-54.5 req/s with 0% error | PASS |

Stress does not justify saying that 132 VU is the system capacity. Throughput
rose from about 65.9 to 130.7, 196.1 and 260.6 req/s across the four stable
levels while p95 stayed 10-13 ms. The defensible statement is that the measured
knee is **above 132 VU under this co-located, five-product configuration**.

## Spike recovery

The burst reached 185 active VU. Thirty-second buckets rose from 34.1 req/s at
p95 11 ms to 361.6 req/s at p95 26 ms. Immediately after the 168 burst threads
finished, the next full bucket returned to 33.8 req/s and p95 12 ms with no
errors. Recovery therefore completed within 30 seconds, well inside the
120-second criterion.

## Endurance threshold and memory interpretation

The empirically demonstrated endurance threshold is **at least 54.5 request/s
(about 10.9 complete journeys/s) at 27 VU for a 15-minute stable hold**, with
p95 no higher than 12 ms in any full 30-second stable bucket and 0% errors. The
observed backend working-set ceiling was 172.0 MB.

Soak memory started at 52.8 MB, peaked at 172.0 MB and ended at 89.6 MB. The
resource trace includes a drop from roughly 170 MB to roughly 68 MB near minute
five, followed by a slow rise to about 90 MB. That garbage-collection pattern
contradicts a simple monotonic-leak claim. End memory is nevertheless 69.7%
above start, so the correct classification is **suspected accumulation requiring
a longer recovery/soak retest**, not a proven leak. One known mechanism is the
in-memory `userCarts` object: checkout creates an order but never clears a
user's cart, and recycled accounts append items throughout the run.

## Bottleneck analysis

No application bottleneck was reached. Even at the 185-VU Spike, backend CPU
peaked at 11.1% of total machine capacity, errors remained zero and p95 stayed
below 30 ms. SQLite write serialization did not dominate at the tested database
size. The limiting concern is measurement validity on an 8 GB co-located host:
JMeter, the IDE and the SUT share CPU and memory, and system free RAM fell close
to 1 GB during runs. A higher-load breaking-point claim needs a clean host or a
separate load generator.

## Optimization review

| Proposal | Classification | Evidence-based reasoning |
|---|---|---|
| Clear a user's in-memory cart after successful checkout | Supported | `POST /api/cart` appends to `userCarts[userId]`; checkout inserts an order but never deletes/empties that array. This matches the endurance accumulation risk and the expected business workflow. |
| Add an index on `users.email` | Plausible but unverified | Login queries `WHERE email = ?` and the schema has no index/UNIQUE constraint, so an index can help at production user volume. With only 242 users, login p95 was at most 25 ms and no bottleneck was measured. |
| Enable SQLite WAL | Plausible but unverified | Concurrent checkout writes could benefit from improved read/write concurrency, but current write p95 was at most 24 ms and no lock/error appeared. Verify with a larger write-heavy retest. |
| Add a generic connection pool | Unfounded for this implementation | The Node `sqlite3` module already exposes one shared `Database` handle. A network database connection-pool recommendation does not apply as stated. |
| Add a normal B-tree index for `name LIKE '%keyword%'` | Unfounded for this query shape | The leading wildcard prevents a conventional prefix index from servicing the search. Use FTS/prefix-search redesign only after a volume test shows scans dominate. |

## Retest decision

`evidence/retest/23127184_Stress_20260817RETEST.jmx` changes one factor only:
the Stress ceiling increases from 132 to 198 VU while the four-stage spacing,
duration, workflow, data and assertions remain fixed. It is ready but must not
run until the host again has at least 2 GB free RAM. If the co-located generator
becomes the constraint, the correct next experiment is a separate load-generator
host rather than increasing local threads indefinitely.

## Limitations

- JMeter and Node ran on the same four-core/eight-thread, 8 GB laptop.
- `LOADTEST=1` bypassed the rate limiter, so results describe application
  capacity, not abuse-control capacity.
- The catalogue contained only five products and is highly cache-friendly.
- Think time was compressed to 300-700 ms per step to fit the local generator.
- Account/CSV recycling makes cart accumulation part of this particular model.
- No WAN, TLS proxy, browser rendering, production database volume or multi-host
  contention was measured.
