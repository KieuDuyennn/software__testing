# Load profiles

Shapes, arithmetic and duration choices for the six taught scenario types.

## Contents

- [From baseline to thread count](#from-baseline-to-thread-count)
- [Load](#load)
- [Stress](#stress)
- [Spike](#spike)
- [Endurance / soak](#endurance--soak)
- [Volume](#volume)
- [Scalability](#scalability)
- [When the load generator is the bottleneck](#when-the-load-generator-is-the-bottleneck)

## From baseline to thread count

Three numbers come out of the baseline measurement:

- `service_time` — server time for one iteration of the journey, the sum of the
  per-step averages.
- `capacity ≈ 1 / service_time` — the upper bound on iterations per second for a
  single-threaded target running this journey alone.
- `payload` — bytes per iteration, which decides whether bandwidth or the client
  becomes the limit before the server does.

Then size threads by the rate you want, not the other way round:

```
N = target_rate × (service_time + think_time)
```

Worked example. A journey costs 70 ms of server time, so capacity is about 14
iterations/s. To run a load test at 40% of capacity — about 5.7 iterations/s —
with 2 s of think time:

```
N = 5.7 × (0.07 + 2) ≈ 12 virtual users
```

Twelve threads sounds small next to the round numbers people usually pick, and
that is exactly the value of doing the arithmetic: 50 threads at the same think
time would demand 24 iterations/s against a ceiling of 14, which is not a load
test at all — it is a stress test that will be reported as a failed load test.

Choose the utilisation target by intent:

| Intent | Target utilisation |
|---|---|
| Load — anticipated production peak | 30–60% of capacity |
| Stress — find the breaking point | step past 100% |
| Spike — survive a transient | 200–400% of capacity, briefly |
| Endurance — sustainable over hours | 30–50% of capacity |

## Load

**Question:** does the system hold up under anticipated load?

```
threads   ┌──────────────── hold ────────────────┐
          │                                      │
      ────┘                                      └────
          ramp-up                               ramp-down
```

- Threads: from Little's Law at 30–60% of capacity.
- Ramp-up: long enough that threads do not all start together — a common rule is
  one thread every 1–2 seconds.
- Hold: long enough for the system to reach steady state and for percentiles to
  stabilise. Ten minutes is a reasonable floor; under two minutes the numbers are
  dominated by warm-up.

Expect: p95 within threshold, error rate near zero, flat memory. A load test that
fails is a finding; a load test tuned until it passes is decoration.

## Stress

**Question:** where does it break?

```
threads          ┌───┐
             ┌───┘   │
         ┌───┘       │
     ┌───┘           │
 ────┘               └────
   step 1..n        stop
```

Step the load up in stages and hold each stage long enough to read a stable
number — two minutes per step is usually enough. The generator implements this
with accumulating thread groups: each stage adds users and stays active until
the common end time. Stepping matters more than the peak: a single jump to a
huge thread count tells you it broke, while a staircase tells you *where* it
broke and what the curve looked like on the way.

Watch for the knee: the point where throughput stops rising while response time
starts climbing. Past the knee, added threads only add queueing. That knee is the
answer to "how many users can this handle", and it is usually well below the
point where errors start.

Record the first stage that violates a threshold, not just the stage that
produced errors — degradation precedes failure.

## Spike

**Question:** how does it react to a sudden jump, and does it recover?

```
threads       ┌────┐
              │    │
 ─────────────┘    └─────────────
   baseline   spike    recovery
```

Three phases, and the third is the one people forget. The interesting questions
are whether errors appear during the spike, and whether response times return to
baseline afterwards or stay elevated — the second is what distinguishes a system
that absorbed the spike from one that is still digesting it.

- Baseline: a modest steady load, held long enough to establish a reference.
- Spike: a near-instant ramp to several times capacity, held 30–60 s.
- Recovery: back to baseline, held at least as long as the spike.

Deliberately no ramp on the way up. Everywhere else a ramp avoids measuring the
scheduler; here the abrupt arrival is the experiment.

## Endurance / soak

**Question:** does it survive the expected load over a long period?

Same shape as load, but held far longer and read for *trends* rather than
levels. Coursework-scale soaks run 10–15 minutes; production soaks run hours.

What matters is the slope, not the average:

- Memory that climbs monotonically and never returns to its floor is a leak —
  compare the resource sampler's first and last readings, not just the peak.
- Response times that drift upward while throughput stays flat point at
  accumulating state: growing tables, unbounded caches, connection exhaustion.
- Error rate that appears only after minutes indicates resource exhaustion rather
  than overload.

Report the endurance threshold as concrete numbers: maximum sustained rate held
without threshold violation, and the memory ceiling reached.

## Volume

**Question:** how does behaviour change as the database grows?

Hold the load profile constant and vary the *seeded data size* between runs —
for example 200, 2 000, 20 000 rows. Any endpoint that returns unbounded results
or scans without an index degrades roughly linearly with row count, and that
shows up here and nowhere else.

Volume testing needs a reseed between runs, so the reset procedure from
`perf-env-and-criteria` has to be reliable before starting.

## Scalability

**Question:** how far can it scale, and what should be added?

Run the same scenario at increasing load levels (or increasing resources) and
plot throughput against offered load. Three shapes are worth naming:

- **Linear then flat** — a hard resource limit, usually CPU or a single writer.
- **Linear then declining** — contention: added concurrency actively costs
  throughput, typical of lock or context-switch pressure.
- **Sub-linear from the start** — a serialised section in the path; the fraction
  that is serial caps the achievable speed-up no matter what is added.

## When the load generator is the bottleneck

Co-located client and server share CPU, so past some thread count the numbers
describe JMeter rather than the target. Signs to watch:

- The load tool's own process saturates a core, or its heap approaches its limit.
- Reported latency rises while the target's CPU utilisation *falls* — the client
  cannot issue requests fast enough to keep the server busy.
- Throughput plateaus at a suspiciously round number and stops responding to
  added threads.

Mitigations, cheapest first: raise the tool's heap; use non-GUI mode; disable
per-sample listeners and keep only the `.jtl` writer; reduce response-body
processing; then finally cap the thread count and state the cap as a limitation
of the measurement rather than a property of the system.
