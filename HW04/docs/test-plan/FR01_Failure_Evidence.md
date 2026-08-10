# FR-01 — final failure evidence (43-case run of 2026-08-10)

> **Authoritative run.** The current reports under `reports/final/html/fr01/` and
> `reports/final/json/fr01-*.json` were generated after the final review changes: TC-01b expects
> the documented `200`, TC-01a uses a specification-valid password, TC-01c preserves
> downstream redirect/persistence coverage, and rejected API responses assert that no
> created-account `id` is returned. A second, data-driven API wave then added 12 rows
> for empty values, malformed e-mails, weak passwords and direct duplicate submission.
> Each engine executed all 43 rows: **17 passed / 26
> failed / 0 skipped**.
>
> An earlier Firefox-only `Browser.removeBrowserContext` teardown error did not reproduce
> in later Firefox runs. The final Firefox report has the same 26 assertion
> failures as Chromium and WebKit and no teardown error. Historical reports are retained
> under `reports/history/archived-runs/`; generated HTML/JSON files were never hand-edited.
>
> The functional run used the SUT's documented `LOADTEST=1` environment switch to bypass
> its global 200-requests/15-minutes limiter. Without that isolation, repeated failed tests
> restart the Playwright worker and re-run setup until unrelated HTTP 429 responses stop the
> feature mid-suite. No source, database, requirement, test input, or expected result was
> changed by this environment switch; rate limiting is outside FR-01's registration rules.

**Purpose.** Raw actual-vs-expected for every red case, with the artefact that proves
each line. This sheet is *input to* `docs/02_Bug_Report.md`, not a bug report: per
CLAUDE.md §4 the verdict on whether a line is a product defect, and the wording of the
bug, belong to the student. This evidence sheet deliberately records no final defect
verdict; confirmed groupings appear only in `docs/02_Bug_Report.md`.

## Run identity

| | |
|---|---|
| Run by | 23127184 — Le Pham Kieu Duyen |
| Spec | `automation/tests/fr01_account_registration/fr01.registration.spec.ts` (43 cases, all rows from `automation/data/fr01_registration.csv`) |
| SUT | EShop — backend `node server.js` :3000 with `LOADTEST=1` to isolate FR-01 from the unrelated global limiter; frontend-web vite :5173 |
| Reports | `reports/final/html/fr01/chromium/index.html` · `.../firefox/index.html` · `.../webkit/index.html` |
| JSON | `reports/final/json/fr01-{chromium,firefox,webkit}.json` (started 12:06:09Z, 14:28:58Z, 14:55:13Z) |
| Artefacts | Embedded in each HTML report; historical unpacked artefacts remain under `reports/history/raw-artifacts/fr01/` and `reports/history/archived-runs/` |

## Result

| Browser | Passed | Failed | Total | Duration |
|---|---|---|---|---|
| chromium | 17 | 26 | 43 | 8.4m |
| firefox | 17 | 26 | 43 | 9.2m |
| webkit | 17 | 26 | 43 | 8.3m |

The **same 26 case IDs** failed on all three engines, with the same assertion messages
and the same received values. No engine-specific behaviour was observed in this feature.

Nothing was changed to reduce the failure count: no assertion softened, no expectation
edited, no data row removed. The expectations are the specification-derived ones
recorded in `TC_Matrix_FR01.md`.

## The 26 red cases

Grouped by mechanism for technical analysis, while `docs/02_Bug_Report.md` and GitHub
retain one issue per independently reproducible failing case for grading traceability.
The **Mechanism** column cites the SUT source line that produces the observed behaviour —
that is an observation from reading the code, not a judgement that it is a defect.

### Second-wave API findings (API-01→API-12)

All twelve rows expected rejection and no created-account `id`. The exact 4xx status is
not documented, so the stronger explicit evidence is that every response returned HTTP
200 with a numeric creation identifier; login also proved persistence wherever the
submitted e-mail/password pair remained usable.

| TC | Input sent directly to `POST /api/register` | Actual on all three browsers | Persistence signal |
|---|---|---|---|
| API-01 | `name: ""` | 200 + numeric `id` | login succeeds |
| API-02 | `email: ""` | 200 + numeric `id` | not login-observable |
| API-03 | `password: ""` | 200 + numeric `id` | not login-observable |
| API-04 | e-mail without `@` | 200 + numeric `id` | login succeeds |
| API-05 | e-mail without domain | 200 + numeric `id` | login succeeds |
| API-06 | e-mail without local part | 200 + numeric `id` | login succeeds |
| API-07 | seven-character password | 200 + numeric `id` | login succeeds |
| API-08 | password without uppercase | 200 + numeric `id` | login succeeds |
| API-09 | password without lowercase | 200 + numeric `id` | login succeeds |
| API-10 | password without digit | 200 + numeric `id` | login succeeds |
| API-11 | password without special character | 200 + numeric `id` | login succeeds |
| API-12 | exact seeded duplicate e-mail | 200 + another numeric `id` | seeded login is deliberately non-discriminating |

### Group A — `POST /api/register` accepts anything and answers 200

Mechanism observed: `backend/server.js:38-47` inserts straight into `users` with no
validation and replies `res.json(...)` (HTTP 200); `backend/database.js:50-61` declares
`email TEXT` with no `UNIQUE` and no `NOT NULL`.

| TC | Input | Expected (spec) | Actual (observed) | Assertion that caught it | Screenshot |
|---|---|---|---|---|---|
| TC-03 | body with **no `name` key** | refusal; no created `id`; no stored account | `200`, numeric `id`, and `POST /api/login` returned OK | status + response-body + persistence assertions | *(API-level case; use the HTML/JSON report entry)* |
| TC-05 | body with **no `email` key** | refusal; no created `id` | `200` with a numeric `id` | status + response-body assertions | *(API-level case; use the HTML/JSON report entry)* |
| TC-11 | body with **no `password` key** | refusal; no created `id` | `200` with a numeric `id` | status + response-body assertions | *(API-level case; use the HTML/JSON report entry)* |

TC-05 and TC-11 carry a `Coverage gap` annotation in the report: the response proves the
server claimed creation by returning an `id`, but `/api/login` cannot look up a record
whose e-mail or password was omitted. Persistence remains unautomated for those two and
is not overstated.

### Group B — e-mail format is never validated, at either tier

Mechanism observed: `frontend-web/src/pages/Register.jsx:46-52` renders the e-mail field
as `type="text"`, so the browser performs no format check either; the backend performs
none.

All four cases behaved identically: **no error banner rendered** (`div.bg-red-100` not
found), the app **navigated to `http://localhost:5173/login`**, and `POST /api/login`
with that address then returned OK — i.e. the account exists.

| TC | E-mail submitted | Expected (spec) | Actual | Screenshot (chromium) |
|---|---|---|---|---|
| TC-06 | `userdomain.com` (no `@`) | banner naming the e-mail field, stay on `/register`, no account | no banner · URL `/login` · account usable | `…--55d40-gative-email-has-no-at-sign-chromium/test-failed-1.png` |
| TC-07 | `user@` (no domain) | as above | as above | `…--3523a-ve-email-has-no-domain-part-chromium/test-failed-1.png` |
| TC-08 | `@domain.com` (no local part) | as above | as above | `…--592b1-ive-email-has-no-local-part-chromium/test-failed-1.png` |
| TC-19 | `user@domain` (no TLD) | as above | as above | `…--c7a71-ail-has-no-top-level-domain-chromium/test-failed-1.png` |

Assertions that caught it: `expect.soft(errorBanner).toBeVisible()` → element not found;
`expect.soft(errorBanner).toHaveText(/email/i)`; `expect.soft(page).toHaveURL(/\/register$/)`
→ received `"http://localhost:5173/login"`; `expect(login.ok()).toBeFalsy()` → received `true`.

### Group C — e-mail uniqueness is not enforced

Mechanism observed: no `UNIQUE` constraint on `users.email`, and no duplicate check in
the register handler.

| TC | Input | Expected (spec) | Actual | Screenshot (chromium) |
|---|---|---|---|---|
| TC-09 | an address already seeded via the API in `beforeAll` | banner naming the e-mail field, stay on `/register` | no banner · URL `/login` — a second account was created for the same address | `…--0f6e2-ready-belongs-to-an-account-chromium/test-failed-1.png` |
| TC-21 | the same seeded address in **UPPER CASE** | as above (OQ-09: case-insensitive uniqueness) | as above | `…--0776a-n-existing-one-only-by-case-chromium/test-failed-1.png` |

The "account must not exist" check is skipped for these two rows by design — the account
exists on purpose — so the observable evidence here is the missing banner and the redirect.

### Group D — full name is not validated

| TC | Input | Expected (spec) | Actual | Screenshot (chromium) |
|---|---|---|---|---|
| TC-18 | name = `"   "` (three spaces) | banner naming the name field, stay on `/register`, no account | no banner · URL `/login` · `POST /api/login` returned OK → account created with a whitespace-only name | `…--d6cb9-ull-name-is-whitespace-only-chromium/test-failed-1.png` |

### Group E — the client-side password rule contradicts the message printed beside it

Mechanism observed: `Register.jsx:15`

```js
const flawedStrongPasswordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*\s)[A-Za-z\d\s]{8,}$/;
```

`(?=.*\s)` **requires a whitespace character**, and the class `[A-Za-z\d\s]` **excludes
every special character**. The message shown on failure (`Register.jsx:18`) and the hint
under the field (`Register.jsx:65`) both state that a special character is required.

| TC | Password submitted | Expected (spec) | Actual | Screenshot (chromium) |
|---|---|---|---|---|
| TC-01a | `Password123!` (valid composition, 12 chars) | account created and redirect `/login` | **rejected** — stayed on `/register` | current HTML report entry `FR01-TC-01a` |
| BVA-02 | `Pa1!abcd` (8 chars, has `!`) | accepted → redirect `/login` | **rejected** — stayed on `http://localhost:5173/register` | `…--f8a63-of-exactly-eight-characters-chromium/test-failed-1.png` |
| BVA-03 | `Pa1!abcde` (9 chars, has `!`) | accepted → redirect `/login` | **rejected** — stayed on `/register` | `…--efa4b--of-exactly-nine-characters-chromium/test-failed-1.png` |
| TC-24 *(diagnostic)* | `Password 123` (space, **no** special char) | rejected, banner naming the password field | **accepted** — URL `/login`, account created and usable | `…--b6784-ce-and-no-special-character-chromium/test-failed-1.png` |

TC-01a is the specification happy path; TC-01c separately proves that redirect and
persistence plumbing work with a password the current build accepts. TC-24, read with
TC-01a and BVA-02/03, isolates the enforced rule: a space is mandatory and `!` is
forbidden — the inverse of what the page tells the user.

## Triage — test-side or app-vs-specification

Two sources decide this, and neither is the AI's opinion. Paths in this subsection are
relative to the separate EShop SUT/HW02 checkouts used during review; they are not claimed
to be bundled inside this HW04 automation repository:

- **`eshop/README.md:30-36`** — the FR-01 functional requirement: three fields required;
  e-mail must be a valid format (`user@domain.com`) **and unique in the system**; password
  ≥ 8 chars with ≥ 1 uppercase, ≥ 1 lowercase, ≥ 1 digit and **1 special character from
  `@ $ ! % * ? &`**; a Confirm Password field; redirect to Login on success.
- **`eshop/api_specification.md:11-21`** — `POST /api/register`, documented success
  response **`200 OK`** with `{"message": "...", "id": n}`. No error response is documented.

Direct reads of `backend/database.sqlite` on 2026-08-10 (manual supporting inspection,
not an automated assertion and not encoded in the JSON reports) were used where the suite
itself recorded a coverage gap. Counts below are mutable observations after six runs that
day (three on the first pass, three on the re-run), not a reproducible database snapshot.

### Resolved test-side finding (not red in the final run)

| TC | Earlier expectation | Final correction |
|---|---|---|
| TC-01b | `201 Created` | `api_specification.md:21` documents **`200 OK`**. The CSV now expects 200; TC-01b passes on all three engines while retaining numeric-`id` and login/persistence checks. |

**Known repeat-run limitation.** TC-06, TC-07, TC-08 and TC-19 intentionally use constant
malformed addresses because their shape is the test input. A later login probe cannot
distinguish a record created by this run from one left by an earlier run. The missing
banner and observed redirect remain per-run evidence; persistence for those constant
addresses is supporting evidence rather than the sole verdict.

### Group 2 — red because the build differs from the specification

The **Anchor** column separates expectations taken from an explicit sentence from
expectations inferred where the specification is silent. The inferred ones are open
questions already recorded in `TC_Matrix_FR01.md`, not settled facts.

| TC | Divergence observed | Anchor |
|---|---|---|
| TC-06, TC-07, TC-08 | e-mail with no `@`, no domain, no local part is accepted and the account is created | **Explicit** — "Email phải có định dạng hợp lệ (`user@domain.com`)" |
| TC-09 | the same address registers twice; the seeded address now appears **2 rows** in `users` | **Explicit** — "và là duy nhất trong hệ thống" |
| BVA-02, BVA-03 | `Pa1!abcd` (8) and `Pa1!abcde` (9) are rejected by the client, although `!` is in the documented special-character set and 8 is the documented minimum | **Explicit** — password rule, set `@ $ ! % * ? &` |
| TC-24 | `Password 123` (no special character) is accepted and the account is created | **Explicit** — a special character is required |
| TC-03 | body without `name` → 200, and the row is written: `name IS NULL` count = **6** | Explicit for "must provide the three fields"; the **status number 400 is inferred** — no error status is documented |
| TC-05 | body without `email` → 200, and the row is written: `email IS NULL` count = **6** | as TC-03. The suite annotated this as unobservable through `/api/login`; the database read supplies the missing observation |
| TC-11 | body without `password` → 200, and the row is written: `password IS NULL` count = **6** | as TC-03 |
| TC-18 | name `"   "` accepted, account created with a whitespace-only name | **Inferred** (OQ-04 / OQ-10) — the spec says the name must be provided, but does not define whitespace as absent |
| TC-19 | `user@domain` (no TLD) accepted | **Inferred** (OQ-11) — the spec gives `user@domain.com` as the shape but states no TLD rule |
| TC-21 | the same address in upper case registers again; `FR01.SEED.…@EXAMPLE.COM` rows exist alongside the lower-case ones | **Inferred** (OQ-09) — "duy nhất" is not qualified as case-insensitive |

No line above says whether a divergence is a defect, and none is worded as a bug. Deciding
that, and deciding whether the three wholly inferred cases (TC-18, TC-19, TC-21) should
stand as written or be re-derived,
is the student's call.

Related and outside these 14: `README.md:35` requires a **Confirm Password** field that the
build does not render. No case asserts on it, so this run neither confirms nor denies it.

## Notes on the artefacts

- **The 15 failed API-only raw page screenshots are blank white images.** Those cases never drive a
  page; the `page` fixture is created but never navigated, so Playwright captured
  `about:blank`. They are not usable evidence — use the JSON/HTML report entry and the
  trace instead. Attaching a blank PNG to a GitHub Issue would misrepresent the run.
- Every UI-case screenshot shows the state **after** the failure, i.e. the `/login`
  page the app navigated to (or `/register` for Group E). The `video.webm` and
  `trace.zip` beside each PNG show the form being filled and submitted, which is the
  fuller reproduction evidence.
- Full directory names are truncated with `…` above; the prefix is
  `reports/history/raw-artifacts/fr01/<browser>/fr01_account_registration-`. The same directory
  exists under `firefox/` and `webkit/` with the matching engine suffix.

## Observed while collecting evidence — outside FR-01's assertions

`frontend-web/src/pages/Login.jsx:24` gives the **login** page the heading `Đăng Ký`
("Register"). It is visible in every Group-B/C/D screenshot, because those cases end up
on `/login`. No FR-01 case asserts on it, so this run neither confirms nor denies it as
a defect — it is recorded here only so it is not mistaken for a rendering artefact of
the screenshots.
