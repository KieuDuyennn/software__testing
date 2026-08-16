---
name: perf-plan-and-design
description: Step 3 of performance testing — plan and design the scenarios before any script is written. Use when deciding which user journey to load-test, how many virtual users to run, what ramp-up and think-time to use, how to shape a load/stress/spike/endurance/volume profile, or how to design CSV test data so runs stay realistic and repeatable. Also use when thread counts were picked arbitrarily and need justification, or when test accounts interfere with each other between runs. Consumes docs/phases/01_environment.md and 02_criteria.md, produces docs/phases/03_plan.md plus the CSV data design.
---

# Plan and Design

## Overview

Step 3 of the taught method: identify key scenarios considering **user
variability**, **test data** and **plan performance**; simulate a variety of use
cases; and outline what metrics will be gathered.

This phase produces no executable artefact. That is deliberate — the cost of
changing a load profile in a document is a sentence, and in a `.jmx` file with
three variants it is an afternoon.

Read `docs/phases/01_environment.md` first. The baseline table there is the
input to every number chosen here; designing without it means inventing service
times.

## Identify the key scenarios

A scenario is a user journey plus a load shape. Pick journeys that carry real
risk, not the ones easiest to script:

- **What the business would miss.** The path that produces revenue or blocks
  every other action when it breaks.
- **What the architecture makes fragile.** Endpoints that return unbounded
  payloads, write to a single-writer database, hold locks, or grow memory
  without releasing it.
- **What the coursework or requirement asks for.** When the brief names endpoint
  groups (read-heavy, auth-heavy, transactional), map each group to concrete
  endpoints and show the mapping in a table.

For an end-to-end journey, state explicitly which step covers which group, so
coverage is verifiable rather than asserted:

| Step | Endpoint | Group covered |
|---|---|---|
| 1 | `POST /api/login` | auth-heavy |
| 2 | `GET /api/products?search=` | read-heavy |
| 3 | `GET /api/products/:id` | read-heavy |
| 4 | `POST /api/cart` | transactional |
| 5 | `POST /api/checkout` | transactional |

One journey exercised under three different load shapes covers the groups three
times over. Separate journeys per group give cleaner per-endpoint numbers but
lose the interaction effects — a journey holds a session open and carries state
between steps, and that is where correlation bugs and session leaks appear.
Choose consciously and record the reason.

## User variability

Virtual users that behave identically produce a lockstep artefact, not a load
test. Three knobs, all of which belong in the plan:

**Think time.** Real users pause between actions. Without think time each thread
becomes a tight loop and the run measures how fast the client can spam, not how
the system serves people. Use a randomised range (uniform or Gaussian) rather
than a constant, so requests do not arrive in synchronised waves.

Think time also determines what a thread count *means*: `N` users at 5 s think
time generate a fraction of the demand of `N` users at 0.5 s. When a plan
compresses think time to reach a target rate with fewer threads — a legitimate
technique when the load generator is the constraint — say so and state the real
think time it stands in for.

**Data variation.** Every thread hitting the same product ID measures the
database's cache, not the query. Vary inputs through CSV so the working set is
realistic.

**Arrival shape.** Ramp-up spreads thread starts over time. Starting 200 threads
simultaneously measures the thread scheduler; a ramp measures the system. The
exception is the spike scenario, where the abrupt arrival *is* the thing under
test.

## Test data design

Data defects surface as fake performance defects, so design the data as
carefully as the profile.

**One file per concern.** Credentials, catalogue identifiers and order payloads
change for different reasons and get regenerated at different times. Splitting
them keeps a change to one from silently invalidating another. When a brief
requires a separate file per endpoint group, this happens naturally.

**Partition accounts by outcome.** If the same account is used for both
successful and failing logins, a lockout or rate limit triggered by the failure
path makes the success path fail too — and the run reports an error rate that
belongs to the test data, not to the system. Reserve disjoint account pools for
success cases and failure cases, and note the partition in the plan.

**Size the pool against the thread count.** Fewer rows than threads means
threads share rows; whether that is acceptable depends on whether the endpoint
keeps per-user state. State the intended recycling behaviour explicitly.

**Regenerate from the live system.** Identifiers hardcoded from an earlier
session break the moment the database is reseeded. Generate data files from the
running target so they cannot drift out of step with it.

**Expected outcome as a column.** Carrying the expected status code per row lets
one assertion serve rows that should succeed and rows that should fail, instead
of splitting the scenario in two.

## Load profiles

Load, stress and spike differ only in the shape of concurrency over time, which
is why a single workflow script can serve all three. Read
`references/load-profiles.md` for the shapes, the arithmetic that turns a
baseline into a thread count, and how to choose the hold duration.

The short version: derive the target rate from the capacity estimate, then apply
Little's Law — `N = target_rate × (service_time + think_time)` — rather than
choosing a round number of threads and discovering afterwards what load it
produced.

## Outline the metrics to gather

Name, per scenario, which of the ten metrics will be collected and how. The
point is to notice missing instrumentation now: CPU and memory utilisation come
from a resource monitor sampling the target process, not from the load tool, and
if nobody arranges that sampler before the run the numbers are simply gone.

Also assign the report view per scenario. When a brief requires distinct listener
types across scenarios, decide the mapping here and justify it by what each view
is good for — a results tree is for reading individual failures, an aggregate
report for percentile comparison across labels, a summary report for a compact
per-label overview.

## Output

Write `docs/phases/03_plan.md`:

```markdown
# Test plan and design
## Scenarios                <- table: scenario, type, journey, why it matters
## Endpoint group coverage  <- step -> endpoint -> group mapping
## User variability         <- think time range and its justification, arrival shape
## Test data design         <- one row per CSV: purpose, columns, size, how generated,
                               partitioning rules, recycling behaviour
## Load profiles            <- per scenario: threads, ramp-up, hold, derivation from baseline
## Metrics gathered         <- per scenario: which metrics, from which source
## Report views             <- per scenario: which listener/view and why
## Assumptions and risks    <- what could make these numbers wrong
```

Every load figure in this document should be traceable to a measured value in
`01_environment.md` or to a stated requirement in `02_criteria.md`. If a number
cannot be traced, it is a guess — mark it as one so the analysis phase treats it
with the right suspicion.

Hand over to `perf-implement-and-run` once the profiles and the data design are
settled.
