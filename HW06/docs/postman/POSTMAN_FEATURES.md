# HW06 - Postman Features Used

Section 6 of the brief: *"Exercise as many Postman features as you reasonably
can … List the Postman features you used in your report."*

Mark each row **Used** only once it is genuinely in place, and point at the
evidence. A feature listed without evidence is worse than a feature left out.

| # | Feature | Status | Where it is used / evidence |
|---|---|---|---|
| 1 | **Workspace** | ✅ Used | Signed-in workspace with all four collections in `evidence/postman-cloud/workspace.png` |
| 2 | **Collections** | ✅ Scaffolded | Four collections in `collections/`, one per API, each foldered by coverage dimension |
| 3 | **Folders** | ✅ Scaffolded | `00 - Setup`, `01 - Domain partitions`, `02 - State transitions`, `03 - Security`, `04 - Schema validation` |
| 4 | **Environments** | ✅ Scaffolded | `config/eshop-local`, `eshop-ci`, `eshop-mock` |
| 5 | **Environment variables** | ✅ Scaffolded | `base_url`, `student_id`, credentials, and run-time captures (`user_token`, `own_order_id`, `victim_order_id`) |
| 6 | **Globals** | ✅ Scaffolded | `config/hw06.postman_globals.json` |
| 7 | **Secret variable type** | ✅ Scaffolded | Passwords and tokens are typed `secret` in the environments |
| 8 | **Pre-request scripts** | ✅ Scaffolded | Collection level: injects `X-Student-Id` and logs it. Request level: builds fixtures via `pm.sendRequest` |
| 9 | **Test scripts** | ✅ Scaffolded | Collection-level global assertions + per-request assertions |
| 10 | **`pm.response.to.have.jsonSchema`** | ✅ Scaffolded | Schema-validation folder in each collection |
| 11 | **Dynamic variables** | ✅ Scaffolded | `{{$guid}}` for unique emails so re-runs stay independent |
| 12 | **`pm.sendRequest`** | ✅ Scaffolded | Fixture setup inside pre-request scripts (API1 ST-001, API2 ST-001, API3 victim account) |
| 13 | **Chained requests / token capture** | ✅ Scaffolded | Login writes the JWT to an environment variable consumed by later requests |
| 14 | **Collection Runner** | ☐ | Run each collection in the Runner; screenshot the result |
| 15 | **Data-driven runs (CSV)** | ◐ Fixtures ready | CSVs in `data/`; build a `05 - Data-driven` folder that reads `pm.iterationData`, then `npm run ddt:api1` |
| 16 | **Newman CLI** | ✅ Working | `npm run test:api1..4`, `scripts/run-suite.js` |
| 17 | **newman-reporter-htmlextra** | ✅ Working | HTML reports in `reports/` |
| 18 | **`--folder` selective runs** | ✅ Working | The CI green gate, driven by `config/ci-suite.json` |
| 19 | **CI integration** | ✅ Working | `.github/workflows/hw06-api-tests.yml` |
| 20 | **Monitor** | ☐ | Cloud only — schedule a monitor on one collection, screenshot a run |
| 21 | **Mock server** | ◐ Running | Public API2 mock and authentic call log in `evidence/postman-cloud/mock-server.png`; successful example response pending |
| 22 | **Collection documentation** | ◐ | Each collection and folder carries a description; export the docs view when finished |
| 23 | **Collection variables** | ☐ | Optional — currently everything lives in the environment |
| 24 | **Postman console** | ✅ Used | Real localhost HTTP 200 run and `[HW06] X-Student-Id=23127184` in `evidence/screenshots/postman-console-x-student-id.png` |

Legend: ✅ done · ◐ partially done · ☐ not yet

---

## Cloud checklist (only you can do these)

1. Sign in to Postman and create the workspace `HW06 - API Testing - 23127184`.
2. Import all four collections from `collections/` and the three environments
   from `config/`.
3. Run each collection in the **Collection Runner**; screenshot the summary.
4. Open **View → Show Postman Console**, run one collection, and screenshot the
   `[HW06] X-Student-Id=…` lines. *This is the anti-AI-cheat evidence required
   by Section 11 — do not skip it.*
5. Create a **monitor** on one collection (a daily schedule is enough) and let
   one run complete; screenshot it.
6. Create a **mock server** from one collection, copy its URL into
   `config/eshop-mock.postman_environment.json`, and run one request against it
   to show the spec-conformant response.
7. Save every screenshot to `evidence/postman-cloud/`.

> The mock server is worth a paragraph in the main report: it returns what the
> **specification** says, while the real SUT returns something else. Running the
> same schema-validation folder against both makes the contract mismatch
> (BUG-04's string-typed `price`) visible as a diff rather than an opinion.

## Mock server value note

If you get the mock working, record the comparison here:

| Request | Mock response | Real SUT response | Verdict |
|---|---|---|---|
| `GET /api/products/2` | `"price": 28000000` (number, per spec) | `"price": "28000000"` (string) | Contract mismatch → BUG-04 |
