# Performance criteria

## Basis

The SUT has no stated production SLO. Criteria are therefore fixed before load
execution from the measured single-user baseline in `01_environment.md`, using
conservative degradation allowances and explicit functional assertions. They
must not be relaxed after viewing results merely to turn a failure into a pass.

## Metric set

| Metric | Source | Use |
|---|---|---|
| CPU utilisation | `resources.csv` | Diagnose saturation; total-machine convention |
| Memory utilisation | `resources.csv` | Start/peak/end and accumulation trend |
| Response time | JTL `elapsed` | Mean and p50/p90/p95/p99/max per label |
| Average load time | JMeter report | Mean sampler completion time |
| Throughput | JTL transaction rows | Completed journeys per second |
| Average latency/wait time | JTL `Latency` | Time to first response byte |
| Bandwidth | JTL bytes over measured window | KB/s transferred |
| Requests per second | JTL request rows | HTTP requests per second |
| Error rate | JTL `success` plus assertions | Failed requests / all requests |
| Transactions passed/failed | Transaction Controller rows | E2E journey success/failure |

## Pass/fail thresholds

| Scope | p95 response time | Error criterion | Functional assertion |
|---|---:|---:|---|
| Auth-heavy: login | ≤ 250 ms | < 1.00% | HTTP 200 and token present |
| Read-heavy: search/detail | ≤ 200 ms per label | < 1.00% | Search returns JSON; detail contains `id` |
| Transactional: cart/checkout | ≤ 300 ms per label | < 1.00% | Cart HTTP 200; checkout contains `orderId` |
| Complete E2E journey | ≤ 1,000 ms | ≥ 99.00% transactions passed | All five steps pass |

The latency budgets are deliberately well above the baseline maxima (10.4 ms
auth, 8.0 ms read, 11.9 ms transactional), leaving roughly 20–25× degradation
headroom while remaining stricter than the generic 500 ms per-endpoint default.

## Scenario-specific success criteria

### Load

- Sustain the planned offered rate for the full hold period.
- Achieve at least 90% of the planned transaction rate.
- Meet all p95, error-rate and transaction-pass thresholds.
- Show no monotonic memory growth remaining after the recovery observation.

### Stress

- Record the first staircase stage that violates any p95/error threshold.
- Identify the knee where throughput stops increasing materially while p95
  continues to rise; do not equate the highest submitted thread count with
  capacity.
- Distinguish application saturation from load-generator saturation using both
  Node and JMeter resource evidence.

### Spike

- During the spike, report threshold violations rather than hiding them in an
  overall average.
- Within the 120-second recovery window, transaction p95 must return to within
  20% of the pre-spike baseline phase and error rate must return below 1%.

### Endurance / soak

- Hold the selected sustainable load for 10–15 minutes.
- Meet the Load latency/error criteria throughout the stable window.
- Report the maximum stable RPS and memory ceiling as measured numbers.
- Treat end memory more than 10% above the start after recovery as suspected
  accumulation requiring a longer retest, not automatic proof of a leak.

## Resource interpretation criteria

CPU and memory are diagnostic inputs, not standalone pass/fail percentages. A
single Node.js event-loop thread can saturate one logical processor while the
total-machine CPU figure remains near 12.5%; therefore an arbitrary “CPU < 80%”
criterion would miss the actual bottleneck. Capacity claims require the
throughput/p95 curve plus process resource evidence.

## Out of scope

- Internet/WAN latency, TLS termination and production proxies.
- Multi-host or distributed load generation.
- Production-sized product catalogues and volume testing.
- Security capacity of the rate limiter; it is disabled for application
  measurement and must be tested separately if required.
- Mobile and browser-rendering performance.

