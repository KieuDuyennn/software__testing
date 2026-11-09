# HW06 - Local run book

## One-time setup

```powershell
cd HW06
npm install                 # Newman + htmlextra + helpers
npm run sut:install         # EShop backend dependencies
```

## Run the whole suite

```powershell
.\scripts\Invoke-ApiTests.ps1
```

Starts the backend with `LOADTEST=1`, waits for it to answer, runs all four
collections, writes HTML reports to `reports/` and console transcripts to
`evidence/newman-console/`, prints a summary, and stops the backend.

Useful switches:

```powershell
.\scripts\Invoke-ApiTests.ps1 -Api 3            # one API only
.\scripts\Invoke-ApiTests.ps1 -KeepServer       # leave the backend running
```

## Run against an already-running backend

```powershell
npm run sut:start           # terminal 1; sets LOADTEST=1
npm run test:api1           # terminal 2
npm run test:all
```

## Run the CI gate locally

```powershell
npm run sut:start
node scripts/run-suite.js --mode gate --env local     # must be green
node scripts/run-suite.js --mode full --env local     # defects show here
```

## Execution constraints

**1. `LOADTEST=1` is not optional.** The backend rate-limits `/api` to 200
requests per 15 minutes per IP. A full suite exceeds that, and without the flag
the run starts returning HTTP 429 partway through. Every later assertion then
fails for a reason that has nothing to do with the SUT. The collections assert
`code !== 429` globally to identify an invalid rate-limited run. Set the flag
before execution.

**2. Starting the backend wipes the database.** `database.js` drops and
re-seeds every table on startup. That is what makes runs reproducible, but it
also removes manually created data on restart. Seeded
accounts after every restart:

| Account | Email | Password | Role |
|---|---|---|---|
| Admin | `admin@eshop.com` | `Admin123!` | admin |
| User | `test@eshop.com` | `Test1234!` | user |

Seeded data: 3 categories, 5 products (ids 1-5), 4 coupons
(`SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`).

## Exporting the commit log

```powershell
.\scripts\Export-GitLog.ps1            # -> evidence/git-commit-log.txt
```

## Working with the API 1 case specification

API 1's collection is **generated**, not hand-edited. The source of truth is
`scripts/cases/api1_fr01_register.py`, which holds all 121 cases.

```powershell
# Re-render the collection, Excel sheet, JSON export and coverage tally
python scripts/render-cases.py --api 1

# After a full run: rebuild the CI gate from what actually passed
.\scripts\Invoke-ApiTests.ps1 -Api 1
python scripts/render-cases.py --api 1 --refresh-gate
```

Edit cases in the Python module, never in the exported collection JSON.
Re-rendering overwrites the collection.

The renderer fails loudly on a duplicate case ID, and on any case that would
fall outside every folder filter, so a case can never be silently dropped.
