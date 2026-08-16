---
name: perf-analyze-and-retest
description: Step 7 of performance testing — analyse raw .jtl results and decide what to retest. Use when reading JMeter results, computing p95/p99/throughput/error rate from a .jtl, finding the knee or breaking point in a stress run, judging whether a run met its SLO, determining an endurance threshold or memory ceiling, or checking someone else's (including an AI's) performance analysis against the raw data. Also use when a proposed optimisation needs judging as feasible or unfounded. Produces docs/phases/04_analysis.md.
---

# Analyze and Retest

## Overview

Step 7 of the taught method: analyse the findings, fine-tune, and run again with
the same or different parameters. It is the step where a pile of samples becomes
a claim about the system — and the step where most wrong claims are made.

The discipline is simple to state: **every number in the analysis comes from the
raw `.jtl`, and the method used to compute it is named.** A figure that cannot be
recomputed cannot be defended, and an analysis that disagrees with a dashboard
has no way to settle the argument otherwise.

## Compute the ground truth first

Before forming any opinion:

```bash
python <skill-dir>/scripts/analyze-jtl.py results/<run>/result.jtl --bucket 30 \
    --p95 500 --error-rate 1.0 --out docs/phases/04_analysis.md
```

It reports, from the raw samples: overall throughput, error rate, mean and
p50/p90/p95/p99/max, bandwidth, a per-label breakdown, failures by response code,
a bucketed timeline, target CPU and memory from `resources.csv`, and a
pass/fail verdict against the thresholds given.

It also handles two things that quietly corrupt hand-rolled analyses: it parses
the `.jtl` as real CSV (quoted fields contain commas), and it separates
transaction-controller rows from request samples instead of counting the same
work twice.

## Read the results

**Start with the verdict, not the average.** Whether the run met its criteria is
the question the phase exists to answer. The average response time answers
almost nothing on its own — it is the percentiles that describe what users
experienced, and a healthy mean routinely hides a p99 an order of magnitude
worse.

**Find the knee in the timeline.** Throughput that stops rising while response
time climbs marks the capacity limit. That point is the answer to "how many users
can this handle", and it is usually well before the point where errors appear —
which is why a run with a 0% error rate can still have failed.

**Attribute the bottleneck before proposing a fix.** The per-label table plus the
resource samples usually name it:

| Pattern | Likely cause |
|---|---|
| One label's latency grows, others flat | That endpoint's own work — query, payload size, serialisation |
| All labels grow together, target CPU saturated | The target is CPU-bound; a single-threaded runtime blocks everything |
| All labels grow, target CPU *idle* | Not the target: the load generator, the network, or a queue in front |
| Latency grows only for writes | Write serialisation, locking, or fsync per commit |
| Errors appear only after minutes | Resource exhaustion, not overload |

**Read memory as a trend, not a level.** Compare the first, peak, recovery and
last resource samples. Growth that remains after load stops is a suspicion to
retest, not proof by itself; a peak that falls back is consistent with caching
or garbage collection doing its job.

## Check the analysis against the raw data

When an analysis comes from somewhere else — a teammate, a dashboard, an AI —
verify each claim rather than accepting or rejecting it wholesale. Quote the
correct value from the `.jtl` and name where the reasoning went wrong.

`references/misinterpretation-checklist.md` catalogues the recurring errors: the
average quoted as if typical, transaction rows double-counted, throughput
computed over the wrong window, a 429 from a rate limiter read as server
overload, `elapsed` confused with `Latency`, a mixed-label p95 attributed to one
endpoint, capacity extrapolated linearly from a single load point. Each entry
says how to check it from the raw samples.

That checklist is also the fastest route to reviewing your *own* analysis before
publishing it.

## Judge proposed optimisations

A recommendation is only worth acting on if the measurement supports it and the
mechanism is real. Classify each one:

- **Supported** — the data shows the bottleneck it addresses, and the mechanism
  applies to this code. Say what improvement to expect and how it would be
  verified.
- **Plausible but unverified** — the mechanism is real but the data does not show
  this bottleneck dominating. Name the measurement that would settle it.
- **Unfounded** — the mechanism does not apply here. Say why.

The third category is common and worth checking carefully, because generic advice
sounds authoritative. A worked example: adding a B-tree index on a column
searched with `LIKE '%keyword%'` cannot help, because a leading wildcard makes
the index unusable and the engine still scans the table. The advice is standard,
correct in general, and wrong for this query — which is exactly why it needs to
be checked against the actual query rather than the general principle.

Recommendations that *are* worth checking against the code: connection pooling
when connections are created per request, WAL mode when a SQLite writer
serialises commits, pagination when an endpoint returns an unbounded result set,
caching when identical reads dominate.

## Retest

Retesting is part of the step, not an optional extra. Change **one** thing and
run again, or the comparison means nothing:

- Same parameters, to check the result is stable rather than a one-off.
- Different load level, to locate the knee more precisely.
- Same load with a fix applied, to measure the fix.
- Longer duration, when the question is about trend rather than level.

Apply the reset procedure between runs and record both runs. A before/after pair
is far more persuasive than a single measurement plus an assertion.

## Output

Write `docs/phases/04_analysis.md` — the generated report is the starting point;
add the interpretation the numbers cannot supply themselves:

```markdown
# Analysis
## Measured results          <- generated tables, unedited
## Verdict against criteria  <- pass/fail per threshold, per scenario
## Bottleneck analysis       <- what limits throughput, with the evidence
## Endurance threshold       <- max sustained rate, memory ceiling, with numbers
## Review of prior analysis  <- claims checked, corrected values cited
## Optimisations             <- supported / plausible / unfounded, with reasoning
## Retest plan               <- what to change, what it would prove
```

State the limits of the measurement honestly: co-located load generator, thread
count capped by client capacity, a rate limiter disabled for measurement. Those
caveats are what make the numbers usable by someone else.
