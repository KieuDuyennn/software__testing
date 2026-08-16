---
name: performance-testing
description: Entry point for performance testing an HTTP/REST backend with JMeter — load, stress, spike, endurance, volume, or scalability runs. Use this whenever the user wants to measure throughput, response time, p95/p99 latency, error rate, or resource usage under load; find a breaking point or endurance threshold; build or run a .jmx test plan; analyse .jtl results; check performance against an SLO; or package attributable performance-test evidence for coursework. Also use it when the user names a scenario type ("spike test the login endpoint", "how many users can this handle", "is the API fast enough") even if they never say the words "performance testing". Routes to the four phase skills and keeps the artifact contract between them.
---

# Performance Testing

## Overview

Performance testing is non-functional testing: the goal is not to find functional
bugs but to eliminate bottlenecks, and to report on three properties — **speed**
(does it respond quickly), **scalability** (what user load can it carry), and
**stability** (does it stay healthy as load varies).

This skill set follows the seven-step method taught in CSC13003 *Performance
Testing* (slides 26–30). Each step maps to a phase skill, so any report produced
here can be traced back to the taught process rather than to an ad-hoc routine:

| # | Taught step | Phase skill |
|---|---|---|
| 1 | Identify test environment | `perf-env-and-criteria` |
| 2 | Determine performance criteria | `perf-env-and-criteria` |
| 3 | Plan and design | `perf-plan-and-design` |
| 4 | Configure test environment | `perf-env-and-criteria` |
| 5 | Implement test design | `perf-implement-and-run` |
| 6 | Run tests | `perf-implement-and-run` |
| 7 | Analyze and retest | `perf-analyze-and-retest` |

Steps 1, 2 and 4 sit in one skill because they answer one question — *what am I
measuring, on what machine, against what threshold* — and splitting them makes
you walk the same ground twice. Steps 5 and 6 sit together because a test plan
that has never been executed is not yet evidence.

## When to use which phase

Work the phases in order on a fresh target. Jump straight to a later phase only
when its inputs already exist on disk:

- No numbers yet, no idea what the machine can do → start at `perf-env-and-criteria`.
- Environment known and thresholds agreed, no scenarios designed → `perf-plan-and-design`.
- Plan exists, need `.jmx` files and runs → `perf-implement-and-run`.
- `.jtl` files exist and need reading → `perf-analyze-and-retest`.

Read the phase skill before doing its work. Each one carries the detail this
file deliberately leaves out.

## Artifact contract

Phases talk to each other through files, not through conversation memory. That
matters because a run may happen hours after the plan was written, in a fresh
session, and because the grader/reader needs to follow the same trail. Default
layout, relative to the project root:

```
docs/phases/01_environment.md    <- step 1 + 4: hardware, tools, monitoring, baseline
docs/phases/02_criteria.md       <- step 2: metric set + pass/fail thresholds
docs/phases/03_plan.md           <- step 3: scenarios, load profiles, test data design
data/*.csv                       <- step 3: parameterisation data
test-plans/*.jmx                 <- step 5: one file per scenario
results/<scenario>_<timestamp>/  <- step 6: result.jtl, report/, resources.csv
docs/phases/04_analysis.md       <- step 7: measured values vs criteria, verdict
evidence/                        <- screenshots, hardware report, monitor captures
```

If the project already uses different folder names, follow the project's names
and say so in `01_environment.md`. The contract is about *what exists*, not
about spelling.

## The metric set

Report these ten metrics — the set taught in the course (slides 9–10). Naming
them consistently is what lets two runs be compared at all:

| Metric | Meaning |
|---|---|
| CPU utilization | percentage of CPU capacity used |
| Memory utilization | primary memory used by the system under test |
| Response time | time between sending a request and receiving the response |
| Average load time | average time to complete the loading process |
| Throughput | transactions handled per second |
| Average latency / wait time | time a request spends queued before processing |
| Bandwidth | volume of data transferred per second |
| Requests per second | requests handled per second |
| Error rate | percentage of requests that returned an error |
| Transactions passed/failed | percentage of passed/failed transactions |

Percentiles (p50/p90/p95/p99) are how response time gets reported in practice —
an average hides the tail, and the tail is what users feel. Report the average
*and* the percentiles, never the average alone.

## The scenario types

Six types are taught; pick by the question being asked, not by habit:

| Type | Question it answers |
|---|---|
| **Load** | Does it hold up under the *anticipated* user load? |
| **Stress** | Where is the breaking point under extreme load? |
| **Spike** | How does it react to a *sudden* large jump in load? |
| **Endurance** (soak) | Does it survive the expected load over a *long* period? |
| **Volume** | How does it behave as the *database* grows? |
| **Scalability** | How far can it scale up as load increases — capacity planning? |

Load, stress and spike differ only in the shape of the load curve over time, so
one workflow script can serve all three; that is why `perf-implement-and-run`
generates them from a single template. Endurance differs in duration, volume
differs in seeded data size, scalability differs in what you vary between runs.

## Ground rules

**Measure before you guess.** Every thread count, ramp-up and think-time in the
plan should trace back to a measured single-user baseline, not to a round number
that looked plausible. `perf-env-and-criteria` produces that baseline first for
exactly this reason.

**The load generator is part of the system.** When JMeter and the target share
one machine — normal for coursework — the client competes with the server for
CPU. Past a certain thread count you stop measuring the server and start
measuring JMeter. Find that ceiling, state it, and stay under it.

**A 200 is not a success.** Endpoints that return `200` with an empty or error
body will read as healthy in every listener. Assertions on response *content*,
not just status code, are what keep an error rate honest.

**Raw results are the evidence.** Keep `.jtl` files intact. Summaries are
derived; when an analysis and a summary disagree, the `.jtl` wins.

## Coursework evidence gate

When the task is HW05 or has comparable attribution requirements, read
`references/hw05-evidence-contract.md` before the first run. Preserve AI output
verbatim before reviewing it, require real screenshots/video/hardware evidence,
and never create or infer evidence that was not captured during execution.
