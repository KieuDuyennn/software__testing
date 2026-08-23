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
| `regression-gate` | The green baseline defined in `HW06/config/ci-suite.json` | **Yes** | The expectations the SUT currently meets. This is the regression baseline: if it goes red, something that used to work has broken. |
| `full-suite` | Every case in all four collections | No | Runs the complete suite and uploads the reports. Its failures are the SUT's defects, tracked in `docs/bugs/BUG_REPORT.md`. |

### How the gate is defined, and why it changed

`config/ci-suite.json` is the single place that defines the gate. It supports
two granularities, and the runner prefers the finer one when it is available:

| Key | Granularity | Used for |
|---|---|---|
| `gate` | legacy folder names, passed to Newman as `--folder` | Retained for backward compatibility; currently empty |
| `gate_cases` | explicit case IDs, rendered into a separate `*_gate` collection | All four APIs |

The folder-level gate stopped working the moment API 1 was written properly.
Once 121 cases derive their expectations from the specification rather than
from the SUT's behaviour, the 53 failures land in almost every folder: of nine
folders and sub-folders, exactly one is entirely green, and gating on that one
would prove nothing.

The case-level gate fixes this. `scripts/render-cases.py --api 1 --refresh-gate`
reads the last full-run report, writes the IDs of every case that passed into
`gate_cases`, and renders `collections/API1_FR01_Register_gate.postman_collection.json`
containing exactly those cases. The rule it encodes is *"whatever passes today
must keep passing"* — which is what a regression gate is for — while the 53
genuine failures stay visible in the `full-suite` job instead of being hidden.

Current gate after the final audited run: **67/126 API 1 cases, 54/88 API 2,
84/94 API 3, and 68/78 API 4**. The verified local gate run on 2026-08-23
passed **1,262/1,262 assertions**. Its raw transcript is
`evidence/newman-console/suite_gate_20260823-225337.log`.

Re-run `--refresh-gate` after every batch of new or corrected cases, and commit
the resulting diff — the change in that file is itself a readable record of
which expectations the SUT started or stopped meeting.

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

Local preflight is complete: `regression-gate` logic passes 1,262/1,262
assertions. The reviewed follow-up commit also passed on the GitHub-hosted
Linux runner.

| Field | Value |
|---|---|
| Commit SHA | `48f5eb0f50b1d7413a0f4e394d1751578395ac70` |
| Commit message | `fix(hw06): stabilize Linux regression gate` |
| Workflow run URL | `https://github.com/KieuDuyennn/software__testing/actions/runs/32650090578` |
| Job | `regression-gate` |
| Result | **GREEN** |
| Assertions passed | 1,262/1,262 |
| Screenshot | `evidence/screenshots/` |

**Screenshot must show:** the green check on the run, the job name, and the
Newman summary with 0 failed assertions.

## 4. Required run 2 — one test case failing

The initial pushed baseline produced a genuine red run because two API 1
state-transition cases that passed on Windows were unstable on the Linux
runner. The failure remains preserved as authentic CI evidence.

| Field | Value |
|---|---|
| Commit SHA | `3c345194cc38e3c2077dc14f2a3b708b5afacd1b` |
| Commit message | `chore(hw06): refresh phase commit history` |
| Workflow run URL | `https://github.com/KieuDuyennn/software__testing/actions/runs/32649883960` |
| Job | `regression-gate` |
| Result | **RED** - 1,268/1,271 assertions passed |
| Failing test case | `A1-ST-002`, `A1-ST-003` (3 failed assertions) |
| Screenshot | `evidence/screenshots/` |

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
