## Single-user baseline

Base URL `http://localhost:3000` · 7 measured requests per endpoint, one warm-up discarded, no concurrency.

| Endpoint | Method | Status | avg ms | min | median | max | Response size | Est. ceiling |
|---|---|---|---|---|---|---|---|---|
| 01 login | POST | 200 | 7.3 | 4.0 | 7.5 | 10.4 | 0.4 KB | ~137 req/s |
| 02 search products | GET | 200 | 4.7 | 2.8 | 3.8 | 8.0 | 0.2 KB | ~214 req/s |
| 03 product detail | GET | 200 | 4.4 | 2.3 | 4.5 | 6.2 | 0.2 KB | ~230 req/s |
| 04 add to cart | POST | 200 | 3.8 | 3.4 | 3.5 | 4.7 | 0.0 KB | ~266 req/s |
| 05 checkout | POST | 200 | 10.3 | 9.0 | 10.5 | 11.9 | 0.0 KB | ~97 req/s |

Full workflow costs **30.4 ms** of server time per iteration (~32.9 iterations/s upper bound if run back to back).

Little's Law for sizing: `N = target_rate × (service_time + think_time)`.
