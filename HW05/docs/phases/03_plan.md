# Test plan and design

## Inputs and sizing model

| Input | Measured/planned value |
|---|---:|
| Baseline workflow service time | 30.4 ms = 0.0304 s |
| Heuristic workflow capacity | 32.9 iterations/s |
| Timer per sampler | Uniform 300–700 ms; mean 500 ms |
| Timers per workflow | 5 |
| Mean compressed think time | 2.5 s/workflow |
| Mean iteration residence time | 2.5304 s |

Thread counts use Little's Law:

```text
N = target iterations/s × (0.0304 s service + 2.5 s think time)
```

The 300–700 ms timer is intentionally compressed. A shopper would commonly
pause 2–5 seconds per action, but reproducing the same request rate with that
think time would require several hundred additional threads on the same 8 GB
laptop. The test therefore models the intended arrival rate, not literal human
reading time, and records this as a validity limitation.

## Scenarios

All scenarios execute the same stateful E2E purchase journey. Only the arrival
shape changes, allowing results to be compared without changing endpoint mix.

| Scenario | Question | Why it matters |
|---|---|---|
| Load | Can EShop sustain an anticipated peak near 40% of estimated capacity? | Validates normal peak latency, errors and stability |
| Stress | At which staircase stage does throughput stop scaling or an SLO fail? | Locates the measured knee/breaking point |
| Spike | Can EShop absorb a near-instant burst above 200% capacity and recover? | Exposes queueing and post-spike degradation |
| Soak | Can EShop sustain a moderate rate for 15 minutes without accumulation? | Determines a hardware-specific endurance threshold |

## Endpoint group coverage

| Step | Request | Group | Correlation/assertion |
|---:|---|---|---|
| 1 | `POST /api/login` | Auth-heavy | Extract `$.token`; require HTTP 200 and token content |
| 2 | `GET /api/products?search=${keyword}` | Read-heavy | URL-encoded CSV keyword; require HTTP 200 |
| 3 | `GET /api/products/${product_id}` | Read-heavy | Live CSV product ID; require body containing `id` |
| 4 | `POST /api/cart` | Transactional | Bearer token; require HTTP 200 |
| 5 | `POST /api/checkout` | Transactional | Bearer token; require returned `orderId` |

The student confirmed on 2026-08-17 that this workflow is not duplicated by
another group member.

## User variability

- Apply a Uniform Random Timer of 300–700 ms before each sampler to avoid
  synchronised lockstep traffic.
- Cycle through 240 unique successful-login accounts.
- Cycle through keywords and IDs derived from all five live seeded products.
- Cycle through 240 distinct shipping addresses and matching order totals.
- Ramp Load/Soak at approximately one thread every two seconds.
- Use accumulating thread groups for Stress and a one-second burst ramp for Spike.

No failing credential is mixed into the E2E pool. Negative-login/lockout testing
must use a separate account and a separate diagnostic run; otherwise a lockout
would contaminate every downstream transactional sample.

## Test data design

| CSV | Columns | Rows | Generation and validity | Recycling |
|---|---|---:|---|---|
| `credentials.csv` | `email,password` | 240 | Registered through live `/api/register`; first/last login verified | Shared cursor; wraps after 240 iterations |
| `search_keywords.csv` | `keyword,product_id,product_price` | 240 | Derived from live `/api/products` response | Shared cursor; wraps after 240 iterations |
| `order_payloads.csv` | `total_amount,shipping_address` | 240 | Total matches cycled live product; unique address per row | Shared cursor; wraps after 240 iterations |

Recycling is intentional because a 10–15 minute test executes more journeys than
the data pool. The consequence is also explicit: accounts and their in-memory
carts are reused after wraparound. Because checkout does not clear the cart in
the current SUT, the backend must be restarted and reseeded between scenarios.

## Load profiles

### Derived values

| Level | Target iter/s | Formula | Rounded VU |
|---|---:|---|---:|
| 20% capacity | 6.58 | `6.58 × 2.5304` | 17 |
| 32.5% capacity | 10.69 | `10.69 × 2.5304` | 27 |
| 40% capacity | 13.16 | `13.16 × 2.5304` | 34 |
| 79% capacity | 26.08 | `26.08 × 2.5304` | 66 |
| 119% capacity | 39.12 | `39.12 × 2.5304` | 99 |
| 159% capacity | 52.16 | `52.16 × 2.5304` | 132 |
| 200% capacity | 65.80 | `65.80 × 2.5304` | 167 → 168 |

### Executable profiles

| Scenario | Threads | Ramp/shape | Total duration | Stable observation | Rationale |
|---|---:|---|---:|---:|---|
| Load | 34 | Linear ramp 68 s | 668 s | 600 s | 40% estimated capacity; one thread/2 s |
| Stress | 132 | Four +33 VU stages, 150 s apart, 30 s ramp/stage | 600 s | 120 s stable between stages | Stages reach ~40%, 79%, 119%, 159% capacity |
| Spike | 17 baseline + 168 burst | Baseline 90 s; burst ramps in 1 s and holds 60 s | 270 s | 120 s recovery | Combined peak ~220% capacity |
| Soak | 27 | Linear ramp 54 s | 954 s | 900 s | 32.5% capacity for the required 15-minute hold |

Durations include ramp time because the standard JMeter Thread Group scheduler
interprets `duration` as total group lifetime.

## Metrics gathered

Every scenario records all ten taught metrics. JTL request rows provide response
time, average load time, latency, bandwidth, RPS and error rate. Transaction
Controller rows separately provide throughput and transaction pass/fail. The
resource sampler records backend PID CPU/memory every two seconds. Analysis also
reports p50/p90/p95/p99/max per label and a 30-second timeline.

## Report views

| Scenario | Listener/view | Reason |
|---|---|---|
| Load | Summary Report | Compact steady-state per-label health |
| Stress | Aggregate Report | Percentile comparison across labels/stages |
| Spike | View Results Tree, errors only | Inspect individual burst failures without retaining every response in GUI memory |
| Soak | Summary Report | Compact long-run status; raw evidence remains JTL + HTML |

All official execution uses non-GUI mode. Listener type remains embedded in each
plan for the required distinct report views; the raw JTL and HTML dashboard are
the authoritative retained evidence.

## Reset and evidence gates

Before each official run:

1. Apply the reset procedure in `01_environment.md`.
2. Confirm at least 2 GB free RAM and record the reading.
3. Validate all CSV files and API reachability.
4. Pass the new backend PID explicitly to the runner.
5. Start screen recording with JMeter and Task Manager in the same frame.
6. Preserve the JMX, JTL, HTML report, resources CSV, JMeter log and run record.

## Assumptions and risks

- The 32.9 iter/s value is a single-user sizing estimate; only Stress can locate
  the real knee.
- Co-location can make JMeter the bottleneck before the backend.
- Only five products create a cache-friendly read working set.
- Recycled accounts make in-memory cart growth part of the observed SUT behaviour.
- SQLite write serialisation may dominate checkout under Stress.
- Free RAM was only 0.6 GB during inventory; running in that state is prohibited.
- Rate limiting is bypassed, so the result does not describe defence capacity.

