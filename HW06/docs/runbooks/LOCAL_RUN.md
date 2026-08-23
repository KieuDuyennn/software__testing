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
npm run sut:start           # terminal 1 - LOADTEST=1 is set for you
npm run test:api1           # terminal 2
npm run test:all
```

## Run the CI gate locally

```powershell
npm run sut:start
node scripts/run-suite.js --mode gate --env local     # must be green
node scripts/run-suite.js --mode full --env local     # defects show here
```

## Two things that will bite you

**1. `LOADTEST=1` is not optional.** The backend rate-limits `/api` to 200
requests per 15 minutes per IP. A full suite exceeds that, and without the flag
the run starts returning HTTP 429 partway through — every later assertion then
fails for a reason that has nothing to do with the SUT. The collections assert
`code !== 429` globally so this is caught rather than misread, but the fix is
to set the flag.

**2. Starting the backend wipes the database.** `database.js` drops and
re-seeds every table on startup. That is what makes runs reproducible, but it
also means any data you created by hand is gone the moment you restart. Seeded
accounts after every restart:

| Account | Email | Password | Role |
|---|---|---|---|
| Admin | `admin@eshop.com` | `Admin123!` | admin |
| User | `test@eshop.com` | `Test1234!` | user |

Seeded data: 3 categories, 5 products (ids 1-5), 4 coupons
(`SAVE10`, `BIGBUY`, `VIP100`, `EXPIRED`).

## Rebuilding the collection skeletons

```powershell
python scripts/build-collections.py    # OVERWRITES collections/
```

Only useful before you start editing in Postman. Once you have imported the
collections and added cases there, the exported JSON is the source of truth —
re-running the builder would discard your work.

## Exporting the commit log

```powershell
.\scripts\Export-GitLog.ps1            # -> evidence/git-commit-log.txt
```
