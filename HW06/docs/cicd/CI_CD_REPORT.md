# HW06 - CI/CD Report

Student ID: **23127184** · Pipeline: **GitHub Actions** · Runner: `ubuntu-latest`
Workflow file: [`.github/workflows/hw06-api-tests.yml`](../../../.github/workflows/hw06-api-tests.yml)

---

## 1. Why the pipeline has two jobs

The EShop SUT ships with genuine defects, and the test suite is written against
the **specification**, not against the SUT's current behaviour. A suite written
that way is red by design — which is correct testing, but useless as a build
gate, because a permanently red pipeline tells you nothing when something new
breaks.

So the workflow splits in two:

| Job | Scope | Fails the build? | Purpose |
|---|---|---|---|
| `regression-gate` | Only the folders listed in `HW06/config/ci-suite.json` | **Yes** | The expectations the SUT currently meets. This is the regression baseline: if it goes red, something that used to work has broken. |
| `full-suite` | Every folder in all four collections | No | Runs the complete suite and uploads the reports. Its failures are the SUT's defects, tracked in `docs/bugs/BUG_REPORT.md`. |

`config/ci-suite.json` is the single place that defines the gate. When new test
cases are added, re-run the suite locally, then update that file so the gate
still means "everything that passes today".

## 2. Pipeline configuration

Triggers: pushes to any branch touching `HW06/**`, pull requests, and manual
`workflow_dispatch`.

Each job runs the same six steps:

1. `actions/checkout@v4`
2. `actions/setup-node@v4` with Node 20
3. Install the test harness — `npm ci || npm install` in `HW06/`
4. Install the SUT — `npm --prefix eshop/backend install`
5. **Start the backend** with `LOADTEST=1`, then poll
   `http://127.0.0.1:3000/api/products` until it answers (40 attempts, 0.5 s
   apart) before any test runs
6. Run `node scripts/run-suite.js --mode {gate|full} --env ci`, stop the
   backend, and upload the HTML reports as an artifact (`if: always()`)

Two configuration details that matter:

- **`LOADTEST=1` is mandatory.** The backend applies a 200-request /
  15-minute-per-IP rate limiter to the whole `/api` surface. A full run makes
  more requests than that, so without the flag the run starts returning HTTP
  429 partway through and every later assertion fails for a reason that has
  nothing to do with the SUT. The collections assert `code !== 429` globally so
  a rate-limited run can never be mistaken for a defect.
- **The backend re-seeds itself on start.** `database.js` drops and recreates
  every table, so each CI run begins from byte-identical state and results are
  comparable across runs.

The `X-Student-Id: 23127184` header is injected by the collection-level
pre-request script, so it is present on every request in CI exactly as it is
locally.

## 3. Required run 1 — all test cases passing

| Field | Value |
|---|---|
| Commit SHA | |
| Commit message | |
| Workflow run URL | |
| Job | `regression-gate` |
| Result | |
| Assertions passed | |
| Screenshot | `evidence/screenshots/` |

**Screenshot must show:** the green check on the run, the job name, and the
Newman summary with 0 failed assertions.

## 4. Required run 2 — one test case failing

| Field | Value |
|---|---|
| Commit SHA | |
| Commit message | |
| Workflow run URL | |
| Job | `regression-gate` |
| Result | |
| Failing test case | |
| Screenshot | `evidence/screenshots/` |

**How to produce this run honestly.** Do not fabricate a failure by breaking an
assertion at random. Move one *defect-revealing* case into the gate — for
example add `"03 - Security (SEC-01..SEC-07)"` to `API4_FR13_AdminOrders` in
`config/ci-suite.json`, which pulls in the SEC-03 case that the SUT genuinely
fails. Commit that one-line change. The same pipeline then goes red on a real
defect, which is a far better demonstration than a sabotaged assertion, and the
failing run doubles as evidence for BUG-06.

**Screenshot must show:** the red X on the run, and the Newman failure detail
naming the failing test case.

## 5. Artifacts produced by the pipeline

| Artifact | Contents |
|---|---|
| `newman-gate-reports` | `reports/*_gate.html`, `reports/summary_gate.json`, `sut.log` |
| `newman-full-reports` | every `reports/*.html` and `*.json`, `sut.log` |

## 6. What the pipeline does not cover

State honestly, so the report does not overclaim:

- [ ] Postman **monitors** run against the Postman cloud, not this pipeline —
      note whether one was configured and link it.
- [ ] The **mock server** is used for contract work, not in the gate.
- [ ] The SUT runs on the CI runner itself (`127.0.0.1`), not on a deployed
      environment.
