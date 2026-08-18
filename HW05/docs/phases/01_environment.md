# Test environment

## Identification and workflow scope

| Item | Value |
|---|---|
| Student ID | `23127184` |
| System under test | EShop REST backend |
| Base URL | `http://localhost:3000` |
| Selected workflow | Login → product search → product detail → add to cart → checkout |
| Endpoint groups | Auth-heavy → read-heavy → transactional |
| Group uniqueness | Confirmed by the student on 2026-08-17 |
| Measurement mode | Backend started with `LOADTEST=1` |

## Hardware and OS

| Item | Value |
|---|---|
| Hostname | `KIEUDUYEN` |
| CPU | Intel(R) Core(TM) i7-10510U CPU @ 1.80 GHz |
| Cores / logical processors | 4 / 8 |
| Physical RAM | 7.8 GB |
| Free RAM at inventory capture | 0.6 GB |
| OS | Microsoft Windows 11 Home Single Language 10.0.26200 |
| Hardware evidence | `evidence/hardware/inventory.md`, `evidence/hardware/dxdiag.txt` |

The low free-memory reading is a pre-run warning. Official Load/Stress/Spike/Soak
runs must not start until unnecessary applications are closed and a fresh free
memory reading is recorded in the run evidence.

## System under test

| Component | Detail |
|---|---|
| Runtime | Node.js 24.4.1, single JavaScript event loop with asynchronous I/O |
| Web framework | Express 5.2.1 |
| Database | SQLite via `sqlite3` 6.0.1 |
| Backend process | `node server.js`; PID `16028` for this baseline session |
| Rate limiter | 200 requests per 15 minutes per IP; bypassed with `LOADTEST=1` |
| Account lockout | Stored in `users.login_attempts` / `locked_until` |
| In-memory state | Shopping carts live in backend process memory |

Starting `server.js` loads `database.js`, which drops and recreates the schema,
seeds 2 base users and 5 products, clears orders and clears in-memory carts. This
behaviour is part of the reset procedure, not an incidental implementation detail.

## Tooling

| Tool | Version / purpose |
|---|---|
| Java | 21.0.12 |
| Apache JMeter | 5.6.3; load generation and raw JTL/HTML reports |
| Node.js | 24.4.1; SUT and baseline/data scripts |
| PowerShell resource sampler | Backend process CPU and memory every 2 seconds |
| Windows Task Manager | Same-frame visual evidence during official runs |
| dxdiag | Hardware evidence |

## Topology

JMeter, Node.js, SQLite and the resource monitor run on the same Windows laptop.
Requests use loopback (`localhost`), so the measurements omit real network
latency but include CPU and memory contention between the load generator and SUT.

## Seeded data

The backend was started from a clean seed: 2 users, 5 products, 3 categories,
4 coupons and 0 orders. Then:

```powershell
node scripts/prepare-performance-data.js --count 240 --out data
powershell -File .claude/skills/perf-implement-and-run/scripts/validate-test-data.ps1 `
  -DataDir data -ExpectedMaxThreads 240
```

The script registered users through the live API and verified the first and last
account by login. Final pre-baseline pools:

| File | Rows | Purpose |
|---|---:|---|
| `data/credentials.csv` | 240 | Unique successful-login accounts |
| `data/search_keywords.csv` | 240 | Live product keyword, ID and price |
| `data/order_payloads.csv` | 240 | Order totals and distinct addresses |

After the baseline, the database contained 242 users, 5 products, 8 orders and
0 locked users. Reset before the first load run so those eight baseline orders
do not change the starting volume.

## Single-user baseline

Command:

```powershell
node .claude/skills/perf-env-and-criteria/scripts/baseline.js `
  --spec config/baseline-spec.json --base http://localhost:3000 `
  --requests 7 --out evidence/baseline/single-user-baseline.md
```

Seven measured requests per endpoint were executed sequentially after one
discarded warm-up request.

| Endpoint | Group | Status | Avg ms | Min | Median | Max | Size | Heuristic ceiling |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| Login | Auth-heavy | 200 | 7.3 | 4.0 | 7.5 | 10.4 | 0.4 KB | ~137 req/s |
| Search products | Read-heavy | 200 | 4.7 | 2.8 | 3.8 | 8.0 | 0.2 KB | ~214 req/s |
| Product detail | Read-heavy | 200 | 4.4 | 2.3 | 4.5 | 6.2 | 0.2 KB | ~230 req/s |
| Add to cart | Transactional | 200 | 3.8 | 3.4 | 3.5 | 4.7 | <0.1 KB | ~266 req/s |
| Checkout | Transactional | 200 | 10.3 | 9.0 | 10.5 | 11.9 | <0.1 KB | ~97 req/s |

The full workflow averaged **30.4 ms** of request time, giving a heuristic
back-to-back ceiling of **32.9 iterations/s**. This is a sizing estimate, not a
capacity claim: asynchronous I/O, SQLite worker behaviour, queueing and the
co-located generator can move the measured knee.

## Monitoring verification

`monitor-resources.ps1` sampled PID 16028 successfully for six seconds. Three
idle samples reported 55.6 MB working set, 62 MB private memory and 0% CPU on the
tool's total-machine 0–100% convention. Evidence:
`evidence/baseline/monitor-smoke.csv`.

## Reset procedure

Apply this procedure before every official scenario and retest:

1. Stop the current backend process and record its PID/end time.
2. Start `node server.js` with environment variable `LOADTEST=1`. Startup resets
   SQLite to 2 users, 5 products and 0 orders, and clears in-memory carts.
3. Wait for both `Database initialized and seeded` and `Server is running` in
   the backend log.
4. Run `node scripts/prepare-performance-data.js --count 240 --out data`.
5. Run `validate-test-data.ps1 -DataDir data -ExpectedMaxThreads 240`.
6. Verify `/api/products` returns HTTP 200, user count is 242, product count is
   5, order count is 0 and no user is locked.
7. Record the new backend PID and pass it explicitly to `run-scenario.ps1`.

Reset is mandatory after any transactional run, any negative-login test, or any
restart. The current EShop implementation increments failed-login attempts by 2,
so the lockout behaviour must not be assumed to match a three-failure policy.

## Validity threats

- The generator and SUT compete for the same 4 cores / 8 logical processors.
- Loopback removes real network latency and bandwidth constraints.
- Only seven samples per endpoint were used for baseline sizing; this is not a
  statistically stable percentile study.
- The baseline inventory captured only 0.6 GB free RAM; official runs therefore
  used a cleaner machine state documented in the execution evidence.
- SQLite and in-memory carts make results specific to this seeded volume and
  process lifetime.
- The rate limiter is deliberately bypassed, so results measure application
  capacity rather than the production defence.

## Attribution evidence

- Hardware identity and same-frame JMeter/Task Manager captures are retained in
  `evidence/screenshots/`.
- The Vietnamese-narrated demo is a separate student-authored artifact and is
  not generated by AI.
