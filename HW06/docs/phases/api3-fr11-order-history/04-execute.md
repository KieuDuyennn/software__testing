# API 3 - FR-11 Order History (user) - Phase 4: Execute

> Pipeline step 4 of 4. Run the cases with Newman, capture the report, and
> triage every failure into either a defect or a test-case correction.

| Field | Value |
|---|---|
| Endpoint | `GET /api/orders/my-orders  (+ GET /api/orders/:id)` |
| Collection | `collections/API3_FR11_OrderHistory.postman_collection.json` |
| Environment | `config/eshop-local.postman_environment.json` |
| Data file | `data/api3_fr11_order_history.csv` |
| HTML report | `reports/API3_FR11_OrderHistory.html` |
| Console transcript | `evidence/newman-console/` |

## How to run

```powershell
# The whole suite, with the backend started and stopped for you:
.\scripts\Invoke-ApiTests.ps1 -Api 3

# Or, with the backend already running (LOADTEST=1):
npm run test:api3
```

The backend must be started with `LOADTEST=1`. Without it the 200-request /
15-minute rate limiter returns HTTP 429 partway through the run and every later
assertion fails for the wrong reason. The global test script asserts this
explicitly so a rate-limited run is never mistaken for a defect.

Starting the backend drops and re-seeds `database.sqlite`, so each run begins
from identical state.

## Run record

| Run | Date/time | Requests | Assertions | Passed | Failed | Report |
|---|---|---:|---:|---:|---:|---|
| | | | | | | |

## Failure triage

Every failed assertion is either a defect in the SUT or a defect in the test
case. Decide which, one row per failure.

| # | Failing assertion | Expected | Actual | Verdict | Bug ID |
|---|---|---|---|---|---|
| | | | | | defect -> `docs/bugs/BUG_REPORT.md` |

## Evidence captured

- [ ] Newman HTML report in `reports/`
- [ ] Console transcript showing the `X-Student-Id` line (Section 11 evidence)
- [ ] Screenshot of the Postman console with the pre-request log
- [ ] Hostname in the Newman output matches the deployment (`localhost` is accepted)
