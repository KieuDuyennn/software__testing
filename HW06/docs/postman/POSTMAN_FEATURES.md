# HW06 - Postman Features Used

Section 6 of the brief: *"Exercise as many Postman features as you reasonably
can … List the Postman features you used in your report."*

The **Used** status requires working configuration and matching evidence.

| # | Feature | Status | Where it is used / evidence |
|---|---|---|---|
| 1 | **Workspace** | ✅ Used | Signed-in workspace with all four collections in `evidence/postman-cloud/workspace.png` |
| 2 | **Collections** | ✅ Used | Four generated and executed collections in `collections/`, one per API |
| 3 | **Folders** | ✅ Used | Coverage folders execute in the full and gate runs |
| 4 | **Environments** | ✅ Used | Local and CI environments were used in Newman; the mock environment is configured |
| 5 | **Environment variables** | ✅ Used | `base_url`, `student_id`, credentials, and captured run-time values |
| 6 | **Globals** | ✅ Configured | `config/hw06.postman_globals.json` |
| 7 | **Secret variable type** | ✅ Configured | Password and token variables use the `secret` type |
| 8 | **Pre-request scripts** | ✅ Used | Collection scripts inject and log `X-Student-Id`; request scripts build fixtures |
| 9 | **Test scripts** | ✅ Used | Full run: 1,802 assertions; gate run: 1,262 assertions |
| 10 | **`pm.response.to.have.jsonSchema`** | ✅ Used | Schema assertions execute in all four collections |
| 11 | **Dynamic variables** | ✅ Used | `{{$guid}}` creates unique test email addresses |
| 12 | **`pm.sendRequest`** | ✅ Used | Pre-request scripts create required fixtures |
| 13 | **Chained requests / token capture** | ✅ Used | Login captures JWT values for later requests |
| 14 | **Collection Runner** | ☐ | Run each collection in the Runner; screenshot the result |
| 15 | **Data-driven runs (CSV)** | ◐ Fixtures ready | CSVs in `data/`; build a `05 - Data-driven` folder that reads `pm.iterationData`, then `npm run ddt:api1` |
| 16 | **Newman CLI** | ✅ Working | `npm run test:api1..4`, `scripts/run-suite.js` |
| 17 | **newman-reporter-htmlextra** | ✅ Working | HTML reports in `reports/` |
| 18 | **`--folder` selective runs** | ✅ Working | The CI green gate, driven by `config/ci-suite.json` |
| 19 | **CI integration** | ✅ Working | `.github/workflows/hw06-api-tests.yml` |
| 20 | **Monitor** | ☐ | Cloud only; schedule a monitor on one collection and screenshot a run |
| 21 | **Mock server** | ◐ Running | Public API2 mock and authentic call log in `evidence/postman-cloud/mock-server.png`; successful example response pending |
| 22 | **Collection documentation** | ◐ | Each collection and folder carries a description; export the docs view when finished |
| 23 | **Collection variables** | ☐ | Optional; current values are stored in the environment |
| 24 | **Postman console** | ✅ Used | Real localhost HTTP 200 run and `[HW06] X-Student-Id=23127184` in `evidence/screenshots/postman-console-x-student-id.png` |

Legend: ✅ done · ◐ partially done · ☐ not yet

---

## Remaining cloud evidence

1. Sign in to Postman and create the workspace `HW06 - API Testing - 23127184`.
2. Import all four collections from `collections/` and the three environments
   from `config/`.
3. Run each collection in the **Collection Runner**; screenshot the summary.
4. Open **View → Show Postman Console**, run one collection, and screenshot the
   `[HW06] X-Student-Id=…` lines. *This is the anti-AI-cheat evidence required
   by Section 11. Do not skip it.*
5. Create a **monitor** on one collection (a daily schedule is enough) and let
   one run complete; screenshot it.
6. Create a **mock server** from one collection, copy its URL into
   `config/eshop-mock.postman_environment.json`, and run one request against it
   to show the spec-conformant response.
7. Save every screenshot to `evidence/postman-cloud/`.

> The mock server is worth a paragraph in the main report: it returns what the
> **specification** says, while the real SUT returns something else. Running the
> same schema-validation folder against both makes the contract mismatch
> (BUG-04's string-typed `price`) visible in the response comparison.

## Mock server value note

The completed mock comparison belongs in this table:

| Request | Mock response | Real SUT response | Verdict |
|---|---|---|---|
| `GET /api/products/2` | `"price": 28000000` (number, per spec) | `"price": "28000000"` (string) | Contract mismatch → BUG-04 |
