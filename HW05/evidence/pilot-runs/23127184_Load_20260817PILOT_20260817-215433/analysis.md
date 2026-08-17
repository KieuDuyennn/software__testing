# Analysis — `result.jtl`

## Overall (request samples)

- Samples: **117** over 28.9 s
- Requests/second: **4.05**
- Error rate: **0.00%** (0 failed)
- Response time: mean **6.0 ms**, p50 4, p90 14, **p95 17**, p99 24, max 74
- Bandwidth: **1.7 KB/s**

Percentiles use the nearest-rank method; JMeter's dashboard interpolates, so small differences are expected and not an error.

## Transactions passed/failed

- Controller rows: **23**, reported passed **23**, failed **0**
- Required-label counts: `01 login`=24, `02 search products`=24, `03 product detail`=24, `04 add to cart`=23, `05 checkout`=22
- Endpoint-complete journey lower bound: **22**; conservative passed **22**, failed **0**, tail/ambiguous **1**
- Complete journeys/second: **0.80**
> The scheduler ended with a partial iteration. JMeter emitted a successful controller row even though not every required label completed; the raw controller pass rate is therefore not used.
- Controller time: mean **30.1 ms**, p95 **45 ms**, max 102

Controller rows are counted separately from request samples: adding them would count the same work twice.

## Per request label

| Label | n | Err % | mean | p50 | p90 | p95 | p99 | max | req/s | KB/s |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 01 login | 24 | 0.00 | 9.0 | 5 | 14 | 15 | 74 | 74 | 0.87 | 0.6 |
| 02 search products | 24 | 0.00 | 2.9 | 2 | 5 | 5 | 10 | 10 | 0.87 | 0.4 |
| 03 product detail | 24 | 0.00 | 2.7 | 2 | 4 | 5 | 5 | 5 | 0.88 | 0.4 |
| 04 add to cart | 23 | 0.00 | 3.6 | 3 | 6 | 6 | 11 | 11 | 0.84 | 0.2 |
| 05 checkout | 22 | 0.00 | 12.1 | 9 | 19 | 19 | 24 | 24 | 0.89 | 0.3 |

## Timeline (10s buckets)

Where throughput stops rising while response time climbs is the knee — the capacity limit. It usually appears well before errors do.

| t (s) | Peak VU | req/s | mean ms | p95 ms | Err % |
|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 3.9 | 6.5 | 15 | 0.00 |
| 10 | 2 | 4.0 | 5.2 | 16 | 0.00 |
| 20* | 2 | 4.3 | 6.3 | 19 | 0.00 |

`*` = partial bucket: req/s uses only the observed seconds. Tails shorter than one second are reported as `n/a` because their rate is unstable.

## Target resource usage

- CPU utilisation: peak **0.4%**, mean 0.1% (percentage of total machine capacity, not of one core)
- Memory: start **52.6 MB** → end **53.4 MB**, peak **53.4 MB**
- Net change: **+0.8 MB** over 36 s

## Verdict against criteria

| Criterion | Threshold | Measured | Result |
|---|---:|---:|---|
| p95 response time | 1000 ms | 17 ms | **PASS** |
| Error rate | 1.00% | 0.00% | **PASS** |

