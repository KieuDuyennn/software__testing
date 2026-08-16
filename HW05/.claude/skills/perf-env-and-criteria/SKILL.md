---
name: perf-env-and-criteria
description: Steps 1, 2 and 4 of performance testing — identify the test environment, determine performance criteria, and configure the environment before any load is applied. Use when starting a performance test on a new target, when asked what hardware/tooling a test ran on, when setting SLO thresholds or pass/fail criteria (p95, error rate, throughput), when a single-user baseline is needed to size thread counts, or when runs are not reproducible because the environment drifts between them. Produces docs/phases/01_environment.md and docs/phases/02_criteria.md.
---

# Environment and Criteria

## Overview

Covers three of the taught steps, which belong together because they answer one
question: *what am I measuring, on what machine, and against what threshold?*

- **Step 1 — Identify test environment.** Hardware, software, network, and which
  testing tools are available.
- **Step 2 — Determine performance criteria.** The metric set and the success
  criteria.
- **Step 4 — Configure test environment.** Arrange the tools and the monitoring
  resources so a run is reproducible.

The output is two documents plus a measured baseline. Nothing here applies load
beyond a handful of single-user requests — that is the point. Thresholds decided
*after* seeing results are not criteria, they are rationalisations, so they get
written down before the first scenario runs.

## Step 1 — Identify the test environment

Run the inventory script; it collects the machine facts and prints a Markdown
table ready to paste into the report:

```powershell
powershell -File <skill-dir>/scripts/inventory-env.ps1
```

It reports hostname, CPU model and core/thread count, physical RAM, OS build,
and the versions of Java, JMeter and Node if present.

Three details matter more than they look:

**Hostname.** Coursework submissions are checked for a hostname consistent with
the student's earlier deployments. Record it verbatim.

**Cores versus threads.** A 4-core / 8-thread laptop running both JMeter and the
target has roughly four real cores to share. This number sets the realistic
ceiling on virtual users far more than RAM does.

**Whether the load generator is co-located.** Over loopback there is no network
latency and no bandwidth limit, so response times look better than production
ever will, while CPU contention makes high thread counts look worse. Both
distortions must be stated in the report — they are the main threat to the
validity of every number that follows.

Also record what the target *is*: language/runtime, web framework, database
engine, and whether the runtime is single-threaded. A single-threaded event loop
(Node.js) means one CPU-bound request blocks every other request, which changes
how a saturation curve should be read.

## Step 2 — Determine performance criteria

Report the ten metrics taught in the course — see the `performance-testing`
skill for the full table. Add percentiles for response time: an average hides
the tail, and the tail is what a user notices.

Set thresholds from one of three sources, in descending order of preference:

1. **A stated requirement.** "Response under 4 s with 1000 concurrent users" —
   use it as given.
2. **The measured baseline times a degradation factor.** If a single user sees
   50 ms, allowing 10× under load (p95 < 500 ms) is a defensible starting point.
   State the factor and why.
3. **A common default**, when nothing else exists: p95 < 500 ms, error rate
   < 1%. Say plainly that it is a default, not a derived figure.

Write criteria per endpoint group, not one number for the whole system. An
endpoint returning a 1 MB catalogue and an endpoint returning a token cannot
share a latency budget without making one of them meaningless.

### Measure the single-user baseline

Every thread count in the plan should trace back to a measurement. Run:

```bash
node <skill-dir>/scripts/baseline.js --spec baseline-spec.json --requests 7
```

The spec file lists the workflow's requests in order; the script reports average,
min, median and max latency plus response size per endpoint, from a single user
with no concurrency. It can capture a value from one response (a token, an id)
and substitute it into later requests, so a journey whose later steps need
authentication is still measurable step by step. The header comment in
`baseline.js` documents the spec format.

Two things fall out of the baseline:

**Capacity estimate.** For a single-threaded server, the ceiling for one
endpoint is roughly `1 / service_time`. A 45 ms endpoint cannot exceed ~22
requests/second no matter how many threads are thrown at it. Knowing this before
the run tells you whether a scenario will saturate the target or merely tickle
it.

**Thread count via Little's Law.** Concurrency `N = throughput × (service_time +
think_time)`. To drive 20 iterations/second through a workflow costing 25 ms of
server time with 2 s of think time: `N = 20 × 2.025 ≈ 40` virtual users. Working
backwards from a target rate produces defensible thread counts; picking 50
because it is a round number does not.

Record the response *size* too. A large payload moves the bottleneck from
database I/O to serialisation and bandwidth, which changes which optimisation
would help — and which optimisation suggestions to reject later.

## Step 4 — Configure the test environment

Bring the environment to a known state and prove it is reachable before
designing anything:

1. **Start the target** and confirm it answers a trivial request.
2. **Seed deterministic data.** Runs are comparable only if the data is
   identical. Note the seeded volume (row counts) in the environment document —
   it is an input to the results, and volume testing varies it deliberately.
3. **Look for defences that will answer instead of the application.** Rate
   limiters, circuit breakers, WAFs, account lockouts and connection caps all
   turn a load test into a test of the defence. Grep the target for
   `rate`, `limit`, `throttle`, `429` before designing anything, and check
   whether a documented bypass exists for measurement.

   This is not a rare edge case. The EShop SUT caps `/api` at 200 requests per
   15 minutes per IP — a single 50-thread run exhausts that in seconds — and
   exposes `LOADTEST=1` to disable it while measuring. Discovered during a run,
   it looks like an inexplicable 85% error rate on a plan that worked minutes
   before. Discovered here, it is one line in the environment document.

   Whichever way it is configured, record the setting. "Rate limiting disabled
   via LOADTEST=1" is part of what makes the numbers reproducible, and leaving
   it out makes the run impossible to repeat honestly.

4. **Verify the monitoring resource.** Confirm the process-level CPU and memory
   sampler works *before* a run, not during one. On Windows, `Get-Process` on
   the target's PID; on Linux/macOS, `htop`/`top`. The run scripts in
   `perf-implement-and-run` automate the sampling, but the tool has to exist.
5. **Establish the reset procedure.** Write down exactly how to return to the
   starting state between runs, and what forces a reset. Common triggers:
   - the target rebuilds its schema on restart, so restarting requires reseeding;
   - a lockout, rate limit or circuit breaker latched during a previous run;
   - accumulated writes from a previous transactional run changed the data volume;
   - in-memory state in the target that only a restart clears.

A reset procedure that lives only in someone's head is the most common reason
two runs of "the same" test disagree.

## Output

Write `docs/phases/01_environment.md`:

```markdown
# Test environment
## Hardware and OS          <- inventory table, hostname stated
## System under test        <- runtime, framework, database, single-threaded?
## Tooling                  <- tool + version for each
## Topology                 <- co-located or separate, network path
## Seeded data              <- what was seeded, how much, with which command
## Single-user baseline     <- per-endpoint avg/min/max latency and response size
## Capacity estimate        <- 1/service_time per endpoint, stated as an estimate
## Reset procedure          <- exact steps, and what triggers a reset
## Validity threats         <- co-location, shared CPU, loopback network
```

Write `docs/phases/02_criteria.md`:

```markdown
# Performance criteria
## Metric set               <- the ten metrics, plus percentiles
## Thresholds               <- per endpoint group, with the source of each number
## Rationale                <- requirement / baseline×factor / stated default
## Out of scope             <- what these criteria deliberately do not cover
```

Both documents are inputs to `perf-plan-and-design`. Hand over once the baseline
table has real measured numbers in it — a plan built on estimated service times
inherits the estimate's error into every thread count.
