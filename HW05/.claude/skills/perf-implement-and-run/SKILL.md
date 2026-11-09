---
name: perf-implement-and-run
description: Steps 5 and 6 of performance testing — implement the test design as JMeter test plans and execute them with evidence capture. Use when generating or editing .jmx files, running a load/stress/spike/soak scenario, capturing .jtl results and HTML dashboards, sampling CPU and memory of the target during a run, or when a run produced surprising errors (429, 403, empty bodies) that need diagnosing before the numbers can be trusted. Generates {StudentId}_{Scenario}_{yyyyMMdd}.jmx from a shared workflow template and writes each run into its own timestamped results folder.
---

# Implement and Run

## Overview

Steps 5 and 6 of the taught method: turn the design into an executable plan, then
execute and monitor it. They sit together because a plan that has never run is
not yet evidence, and a run whose plan cannot be regenerated is not yet
repeatable.

Inputs: `docs/phases/03_plan.md` for the profiles, `docs/phases/01_environment.md`
for the reset procedure. Outputs: `.jmx` files in `test-plans/` and one folder
per run under `results/`.

## Step 5 — Implement the test design

Generate plans rather than hand-editing XML:

```powershell
powershell -File <skill-dir>/scripts/new-plan.ps1 -Scenario Load   -StudentId 23127184
powershell -File <skill-dir>/scripts/new-plan.ps1 -Scenario Stress -StudentId 23127184
powershell -File <skill-dir>/scripts/new-plan.ps1 -Scenario Spike  -StudentId 23127184
powershell -File <skill-dir>/scripts/new-plan.ps1 -Scenario Soak   -StudentId 23127184
```

Before generation, create `credentials.csv`, `search_keywords.csv`, and
`order_payloads.csv` from the live seeded target. The generator calls
`scripts/validate-test-data.ps1` and refuses missing columns, empty rows, or
duplicate credentials. Pass `-DataDir` when the project uses another directory.
Keep that generation-time path relative to the project root; use the runner's
`-DataDir` argument for an absolute runtime override.

Each plan is `assets/plan-skeleton.jmx` (test-plan settings, HTTP defaults,
headers, CSV data sets) wrapped around `assets/workflow-fragment.xml` (the user
journey), with the thread-group shape and listener chosen per scenario.
Load, stress and spike differ only in the concurrency curve, so keeping one
workflow definition means a fix to an assertion lands in every plan at once.

Stress uses four accumulating thread groups to form a staircase; each stage is
held before the next increment, making the first threshold violation traceable.
CSV paths remain portable through the JMeter property `data.dir`: the plan keeps
a relative default and a run may override it with `-Jdata.dir=PATH`.

Override any profile value when the target differs:
`-Threads`, `-RampSeconds`, `-DurationSeconds`, `-TargetHost`, `-Port`, `-DataDir`.

Adapting the workflow to a different API means editing `workflow-fragment.xml`:
the samplers, their bodies, the token extractor and the assertions. Read
`references/jmx-authoring.md` before doing so — JMeter's XML has several traps
that produce a file which loads but silently does the wrong thing.

### What the generated plan already handles

- **Token correlation.** The login sampler extracts `$.token` into `authToken`;
  later samplers send it as a bearer header. The extractor has a default value of
  `TOKEN_NOT_FOUND`, so a broken login shows up as an authorisation failure with
  an obvious marker rather than as a blank variable.
- **Content assertions, not just status codes.** An endpoint answering `200` with
  an empty body is a success to any listener. The product-detail sampler asserts
  the body actually contains an `"id"`, and checkout asserts an `orderId` came
  back.
- **A transaction controller** around the journey, so transactions passed/failed
  is measurable — one of the ten required metrics — alongside per-request numbers.
- **Shared CSV pools** at test-plan level, so 200 threads read 200 different rows
  instead of 200 copies of row one.

## Step 6 — Run the tests

```powershell
powershell -File <skill-dir>/scripts/run-scenario.ps1 `
  -Plan test-plans/23127184_Load_20260815.jmx `
  -DataDir data -TargetProcessId <backend-pid>
```

The script runs JMeter non-GUI, starts the resource sampler against the target
process for the duration, and collects everything into
`results/<PlanName>_<timestamp>/`:

| File | What it is |
|---|---|
| `result.jtl` | raw samples — the evidence, never edited |
| `report/` | JMeter HTML dashboard |
| `resources.csv` | target CPU and memory sampled through the run |
| `jmeter.log` | tool log; where a failed run explains itself |
| `run.md` | plan, timestamps, host, memory before/after |

Non-GUI mode is not a convenience. The GUI competes with the test for CPU on the
same machine, so a GUI run measures a slower system than a headless one.

### Before every run

1. Apply the reset procedure from `01_environment.md`. Skipping it is the usual
   reason two runs of the same plan disagree.
2. Confirm the target is up and answering.
3. Pass the backend PID explicitly when more than one process shares its name.
   The runner refuses to guess because monitoring a frontend/helper process
   would invalidate the resource evidence.
4. Confirm nothing else heavy is running — a browser or an indexer competing for
   the same four cores will show up as latency the report cannot explain.

### Read the console while it runs

The summariser line updates every 30 seconds. Two things are worth catching
early, because both waste the whole run:

- **Error rate climbing immediately.** Usually a broken plan, not a slow system.
  Stop and diagnose rather than collecting fifteen minutes of garbage.
- **Throughput far below the target rate** with the target's CPU idle. The load
  generator is the constraint, not the system under test.

## Diagnosing surprising errors

A run that fails is only useful once the cause is known. The failures worth
recognising on sight:

**429 Too Many Requests.** The target has a rate limiter, and the test is
measuring the limiter rather than the system. Real example from the EShop SUT: a
cap of 200 requests per 15 minutes per IP across the whole `/api` surface, which
a single 50-thread run exhausts within seconds. It exposes a bypass —
`LOADTEST=1` in the environment — precisely so performance runs can measure the
application instead. Check for a limiter *before* the first run; the symptom
otherwise appears as a mysterious 85% error rate on a plan that worked minutes
earlier.

**403 with a lockout message.** An authentication protection latched during a
previous run and has not expired. Reset it, and prefer test data that keeps
failing-login accounts disjoint from succeeding ones.

**200 with an empty body.** Not an error to the tool, and invisible unless a
content assertion catches it. If error rate is suspiciously perfect, check what
the assertions actually assert.

**Errors that begin only after several minutes.** Resource exhaustion rather than
overload — connections, file handles, or memory. Read `resources.csv` alongside
the error timestamps.

## Output

Runs are self-describing, so the phase produces no separate document. Note in
`docs/phases/03_plan.md` which run folder corresponds to which scenario, and
hand over to `perf-analyze-and-retest`.

Keep every run folder, including the failed ones. A run that hit a rate limiter
is evidence about the system, and deleting it loses the finding.
