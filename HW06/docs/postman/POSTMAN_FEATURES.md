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
| 15 | **Data-driven runs (CSV)** | ✅ Used | Four dedicated collections replay one request per CSV row via `pm.iterationData`; `npm run ddt:all` executed 27 iterations and 128 assertions, all passing (`reports/*_ddt.html`, `evidence/newman-console/suite_ddt_20260824-145525.log`) |
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

---

## Data-driven execution (feature 15) in detail

The suite is data-driven at two different levels, and the brief's wording
("the Collection Runner with a data file") asks for the second one.

**1. Generation time.** Every one of the 386 cases is a record in
`scripts/cases/apiN_*.py`, not hand-written request JSON. `render-cases.py`
turns those records into the collection, the Excel sheet and the JSON export in
one pass, so a correction made during the audit cannot leave the three
artefacts disagreeing.

**2. Execution time.** `scripts/build-ddt.py` renders four extra collections,
each containing exactly **one** request whose inputs, target and expected
status all come from `pm.iterationData`:

| Collection | Request | Data file | Rows | What the row varies |
|---|---|---|---:|---|
| `API1_FR01_Register_ddt` | `POST /api/register` | `data/api1_fr01_register.csv` | 10 | name, email, password partitions |
| `API2_FR06_ProductDetail_ddt` | `GET /api/products/{{ddt_product_id}}` | `data/api2_fr06_product_detail.csv` | 8 | the `:id` partition, incl. a SEC-05 payload |
| `API3_FR11_OrderHistory_ddt` | `GET /api/orders/{{ddt_target}}` | `data/api3_fr11_order_history.csv` | 5 | actor token and target (own history vs. another user's order) |
| `API4_FR13_AdminOrders_ddt` | `GET /api/admin/orders` | `data/api4_fr13_admin_orders.csv` | 4 | the SEC-03 role matrix |

```powershell
npm run ddt:rebuild     # regenerate the four collections from data/
npm run ddt:all         # run all four through Newman with their CSVs
```

Result of the recorded run (2026-08-24): **27 iterations, 27 requests,
128 assertions, 0 failed.** Reports in `reports/*_ddt.html`, console transcript
in `evidence/newman-console/suite_ddt_20260824-145525.log`.

Three design notes worth defending orally:

- **Separate collections, not a fifth folder.** The 386-case totals quoted in
  `README.md`, the main report and `reports/` are documented evidence. Adding
  iteration-driven requests to those collections would silently change every
  assertion total the report cites, so the data-driven runs live beside the
  baseline instead of inside it.
- **The anonymous rows send no `Authorization` header at all.** The header is
  attached by the pre-request script only when the row names a token. Sending
  an empty `Bearer ` would still produce a 401 and the case would pass while
  proving the wrong thing.
- **Fixed emails in the CSV are made unique at run time.** FR-01 requires a
  unique email, so a second run of a fixed address would collide. The
  pre-request script inserts the harness's `uniq` value into the local part and
  leaves malformed addresses malformed, which keeps the file readable and the
  run repeatable.
