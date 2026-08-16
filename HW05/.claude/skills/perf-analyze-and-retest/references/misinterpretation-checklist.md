# Misinterpretation checklist

Recurring ways a performance result gets read wrong, each with the check that
settles it from the raw `.jtl`. Use it to review someone else's analysis — and to
review your own before publishing.

The entries are ordered roughly by how often they appear.

## Contents

- [1. The average quoted as if it were typical](#1-the-average-quoted-as-if-it-were-typical)
- [2. Transaction rows counted with request rows](#2-transaction-rows-counted-with-request-rows)
- [3. The .jtl split on commas](#3-the-jtl-split-on-commas)
- [4. Zero errors read as "everything worked"](#4-zero-errors-read-as-everything-worked)
- [5. Throughput computed over the wrong window](#5-throughput-computed-over-the-wrong-window)
- [6. elapsed, Latency and Connect confused](#6-elapsed-latency-and-connect-confused)
- [7. A mixed-label percentile attributed to one endpoint](#7-a-mixed-label-percentile-attributed-to-one-endpoint)
- [8. A defence mechanism read as system overload](#8-a-defence-mechanism-read-as-system-overload)
- [9. Client saturation attributed to the server](#9-client-saturation-attributed-to-the-server)
- [10. Capacity extrapolated linearly](#10-capacity-extrapolated-linearly)
- [11. Memory growth called a leak too early](#11-memory-growth-called-a-leak-too-early)
- [12. Runs compared across different conditions](#12-runs-compared-across-different-conditions)
- [13. Generic optimisations applied without checking the mechanism](#13-generic-optimisations-applied-without-checking-the-mechanism)

---

## 1. The average quoted as if it were typical

**Claim:** "Average response time is 45 ms, so performance is good."

**Check:** compare mean against p95 and p99 in the per-label table. A mean far
below p95 means a long tail that most users in the tail actually felt.

**Correct statement:** report mean *and* percentiles, and judge against the
criterion, which is normally expressed as a percentile. A run whose mean is 45 ms
and whose p99 is 2 400 ms is not a run that went well.

## 2. Transaction rows counted with request rows

**Claim:** a sample count or throughput figure noticeably higher than the number
of requests actually issued.

**Check:** transaction-controller rows carry a `responseMessage` of
`"Number of samples in transaction : N, number of failing samples : M"`. Count
rows with and without that marker separately.

**Correct statement:** requests/second and transactions/second are two different
metrics — both are on the required metric list — and a transaction row is an
aggregate of its children. Adding them counts the same work twice.

## 3. The .jtl split on commas

**Claim:** "every transaction failed" on a run whose individual requests all
succeeded.

**Check:** the transaction message above contains a comma inside quotes. Naive
splitting shifts `success` out of its column, and the value read is empty rather
than `true`.

**Correct statement:** parse with a real CSV reader. This is the single most
common way a healthy run is reported as a total failure.

## 4. Zero errors read as "everything worked"

**Claim:** "0% error rate, the system handled the load."

**Check:** read what the assertions actually assert. A status-code-only assertion
passes on `200 {}` — an endpoint answering with an empty body for a missing
record is recorded as a success. Look at response `bytes` per label: a detail
endpoint returning near-zero bytes is answering with nothing.

**Correct statement:** error rate is only as strong as the assertions behind it.
Say which assertions were in force.

## 5. Throughput computed over the wrong window

**Claim:** a throughput figure that does not match the tool's own summary.

**Check:** throughput is samples divided by the elapsed window. Including ramp-up
and the tail after the last thread stops depresses it; measuring only the busiest
minute inflates it.

**Correct statement:** state the window. For a steady-state figure, use the hold
period and exclude ramp-up explicitly rather than silently.

**The same error inside a timeline.** A run almost never ends on a bucket
boundary, so the final bucket covers fewer seconds than the others. Divide its
samples by the nominal bucket width and the table shows a throughput cliff that
nothing caused — and a stress run is exactly where someone will read that cliff
as the system giving out. `analyze-jtl.py` divides the last bucket by the span it
actually covers and marks the row with `*`; if you are reading a timeline from
another tool, check how it handles the tail before believing the last row.

## 6. elapsed, Latency and Connect confused

**Claim:** "server processing time is 300 ms."

**Check:** in a `.jtl`, `elapsed` is the full round trip including receiving the
whole response body; `Latency` is time to the first byte; `Connect` is connection
setup. For a large payload, `elapsed` minus `Latency` is transfer time, not
server work.

**Correct statement:** name the field. A 660 KB response with `elapsed` 45 ms and
`Latency` 12 ms spent most of its time transferring, so the fix is pagination,
not query tuning.

## 7. A mixed-label percentile attributed to one endpoint

**Claim:** "p95 is 800 ms, the search endpoint is slow."

**Check:** the overall p95 mixes every label. In an end-to-end journey the
expensive step dominates the tail while cheap steps pull the median down.

**Correct statement:** quote the per-label p95. Overall percentiles describe the
journey, not any single endpoint.

## 8. A defence mechanism read as system overload

**Claim:** "the server collapsed under load — 85% errors."

**Check:** group failures by response code. `429` is a rate limiter, `403` with a
lockout message is an authentication protection, `503` from a proxy is a circuit
breaker. None of them mean the application ran out of capacity — the application
may not have been reached at all.

**Correct statement:** name the mechanism and whether it was active. A run
against a limiter measures the limiter. Either disable it for measurement and say
so, or report it as a deliberate test of the limiter.

## 9. Client saturation attributed to the server

**Claim:** "throughput plateaued at 300 req/s, that is the server's limit."

**Check:** target CPU from `resources.csv` during the plateau. If the target is
idle while throughput is flat, the constraint is upstream — the load generator,
its heap, or its thread scheduler.

**Correct statement:** with a co-located generator, report the plateau as a lower
bound on the target's capacity, not as its capacity.

## 10. Capacity extrapolated linearly

**Claim:** "50 users gave 20 req/s, so 500 users will give 200 req/s."

**Check:** the timeline table. Throughput per user falls as concurrency rises;
past the knee, added users add only queueing.

**Correct statement:** capacity comes from the measured knee, not from
multiplying a single point. Extrapolation beyond the measured range is a
hypothesis for the next run.

## 11. Memory growth called a leak too early

**Claim:** "memory rose 40 MB during the run, there is a leak."

**Check:** did it come back down after load stopped? Managed runtimes grow the
heap under load and collect later. A leak is growth that survives the load
ending, and it shows up as a *monotonic* trend across a longer run.

**Correct statement:** compare start, peak and end, over a duration long enough
for at least one collection cycle. If the mechanism is known — an in-memory
collection that is appended to and never cleared — say so and point at the code.

## 12. Runs compared across different conditions

**Claim:** "the fix improved p95 by 30%."

**Check:** were the runs equivalent? Same seeded data volume, same reset applied,
same background load, same duration, same thread count, same limiter setting.

**Correct statement:** a comparison is only valid across runs that differ in one
variable. Note what was held constant; if the database grew between runs, the
volume changed too and the comparison is confounded.

## 13. Generic optimisations applied without checking the mechanism

**Claim:** "add an index on the searched column."

**Check:** read the actual query. A B-tree index cannot serve
`LIKE '%keyword%'` — the leading wildcard makes it unusable and the engine scans
regardless. Correct general advice, wrong for this query.

**Correct statement:** tie each recommendation to the observed bottleneck and to
the code path it would change. Classify as supported by the data, plausible but
unverified, or unfounded — and for the middle category, name the measurement that
would decide it.

Recommendations worth checking against the code rather than dismissing:
connection pooling where connections are per-request, write-ahead logging where a
single writer serialises commits, pagination where an endpoint returns unbounded
results, caching where identical reads dominate the profile.
