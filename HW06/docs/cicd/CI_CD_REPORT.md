# HW06 - CI/CD Report

Student ID: **23127184**

Pipeline: **GitHub Actions**

Workflow: [`.github/workflows/hw06-api-tests.yml`](../../../.github/workflows/hw06-api-tests.yml)

## 1. Pipeline scope

The final workflow runs all four submitted Postman collections. It does not use
the earlier regression subset as the assignment's all-passing sample.

| API | Test cases | Assertions |
|---|---:|---:|
| API 1, FR-01 Register | 126 | 606 |
| API 2, FR-06 Product detail | 88 | 433 |
| API 3, FR-11 Order history | 94 | 418 |
| API 4, FR-13 Admin orders | 78 | 345 |
| **Total** | **386** | **1,802** |

Any failed assertion makes `scripts/run-suite.js` return exit code 1, so the
GitHub Actions job fails. The workflow no longer suppresses failures from the
full suite.

## 2. Pipeline steps

The workflow runs on pushes to `hw6`, pull requests that touch HW06, and manual
dispatch. It performs these steps:

1. Check out the repository.
2. Install Node.js and the Newman test harness.
3. Install the EShop backend dependencies.
4. Start the backend with `LOADTEST=1` and wait for its health check.
5. Run all four collections with `node scripts/run-suite.js --mode full --env ci`.
6. Write the per-API assertion table to the GitHub job summary.
7. Stop the backend and upload the HTML, JSON, and server log artifacts.

The backend recreates and seeds its SQLite database on startup. Each CI run
therefore begins with the same five products and the same two user accounts.
`LOADTEST=1` prevents the suite from tripping the demo rate limiter. Every
collection still injects and checks `X-Student-Id: 23127184`.

## 3. Required red sample

The red sample runs all 386 cases. A controlled environment switch changes
only the response for `GET /api/products/0` from HTTP 404 to HTTP 400. That
causes one assertion in `A2-DP-009` to fail. No collection, folder, or case is
removed from the run.

| Field | Value |
|---|---|
| Commit | `27b76ae4e34778998164dbda0a1254e388223739` |
| Commit message | `test(hw06): run full suite with one controlled failure` |
| Run | [GitHub Actions run 32700593817](https://github.com/KieuDuyennn/software__testing/actions/runs/32700593817) |
| Job | `All 386 API test cases` |
| Result | **Failure** |
| Assertion result | **1,801 passed, 1 failed, 1,802 total** |
| Only failing case | `A2-DP-009`, product id 0 must return HTTP 404 |
| Screenshot | `evidence/screenshots/github-actions-red-summary.png` |

The GitHub job summary shows zero failed assertions for APIs 1, 3, and 4, and
one failed assertion for API 2.

## 4. Required green sample

The next commit removes the controlled switch from the workflow. It changes no
test case and runs the same 386-case scope.

| Field | Value |
|---|---|
| Commit | `ff360cd3d0aea303ee6d2529c4f00ecfb1e3f37b` |
| Commit message | `test(hw06): restore complete full-suite pass` |
| Run | [GitHub Actions run 32700710575](https://github.com/KieuDuyennn/software__testing/actions/runs/32700710575) |
| Job | `All 386 API test cases` |
| Result | **Success** |
| Assertion result | **1,802 passed, 0 failed, 1,802 total** |
| Screenshot | `evidence/screenshots/github-actions-green-summary.png` |

The green run produced the `newman-all-api-reports` artifact with the HTML and
JSON reports for all four collections.

## 5. Relationship to the bug report

The first execution against the original SUT exposed 16 root-cause bugs and
passed 1,674 of 1,802 assertions. Those original reports, console logs, issue
screenshots, and bug descriptions remain in the repository. The SUT fixes were
then applied and the same test cases were run again to produce the required
all-passing CI sample. The historical failure evidence was not rewritten.

## 6. Commit authorship

Both sample commits list Lê Phạm Kiều Duyên as the only Author and Committer.
Neither commit contains a `Co-authored-by` trailer.
