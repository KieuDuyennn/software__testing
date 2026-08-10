# FR-13 failure evidence

Execution date: 2026-08-10 (UTC+7). The complete Chromium run contains 50 cases:
29 passed, 21 failed, 0 skipped. The SUT was started with its documented
`LOADTEST=1` harness flag so the 200-request global limiter did not turn functional
assertions into 429 failures.

Evidence bundle: [Chromium HTML report](../../reports/final/html/fr13/chromium/index.html) and
[Chromium JSON report](../../reports/final/json/fr13-chromium.json).

The 21 red assertions represent six implementation mechanisms:

| Root cause | Failing cases | Expected | Observed |
|---|---|---|---|
| Delivered revenue is multiplied by two | TC-02, BVA-03/05/01/04/06, TC-13b, TC-21 | Sum each delivered `total_amount` once | KPI doubles the seeded delta; e.g. BVA-03 shows `+2` for an order worth `1` |
| Invalid `canceled → delivered` transition | TC-13 | Refuse the transition | API returns HTTP 200 and updates the order |
| Checkout trusts client totals and accepts malformed types | TC-11, API-14–17 | Recompute/validate and create no invalid order | HTTP 200; each malformed payload creates an order |
| Admin endpoints authenticate but do not authorise role | TC-04b, API-03/04/06/09 | Non-admin token is refused | UI/API exposes or mutates admin data with HTTP 200 |
| JWT subject is not resolved against an existing user | API-10 | Nonexistent subject is refused | Signed token with admin claim reads the order feed with HTTP 200 |
| Self-profile update permits role escalation | TC-19 | User cannot grant `admin` to self | HTTP 200 and the role changes |

The ten new cases were also executed in short, clean batches on Firefox and WebKit.
Each engine produced the same 4-pass/6-fail verdict for the new wave; the interrupted
long Firefox attempt containing one `ECONNREFUSED` is excluded from product findings.

Full browser coverage was then completed with three non-overlapping batches per engine
(27 TC + 6 BVA + 17 API = 50 cases). Firefox: 30 passed / 20 failed. WebKit: 30
passed / 20 failed. All six batch reports had zero skipped cases.
