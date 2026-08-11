# Bug Report — HW04

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**GitHub Issues page:** https://github.com/KieuDuyennn/software__testing/issues —
FR-01 issue-level evidence is published as
[#39](https://github.com/KieuDuyennn/software__testing/issues/39) through
[#64](https://github.com/KieuDuyennn/software__testing/issues/64).

Only defects revealed by a **failing assertion in an automated run** belong here (§6).
A test that fails because the test is wrong is a fix for `AI_Review_Gap_Analysis.md`,
not a bug — keeping those two apart is most of the credibility of this file.

Each finding is filed as a GitHub Issue. The 26 public issue-page screenshots are stored
under `reports/evidence/github-issues/fr01/`; the matching Playwright failure screenshots live under
`reports/evidence/failure-screenshots/fr01/`. All 26 failure images are also attached directly to their matching
GitHub issues.

## Summary

| Severity | Count | Bug IDs |
|---|---|---|
| Blocker | 0 | |
| Critical | 0 | |
| Major | 23 | BUG-FR01-01→11 and BUG-FR01-15→26 |
| Minor | 0 | |
| Trivial | 0 | |
| **Total confirmed FR-01 defects** | **23** | |

## Issue-level bug reports

The lecturer grades the quantity as well as the quality of issue deliverables. Therefore
each independently reproducible failing case below has its own issue ID and screenshot.
The **Root cause** column preserves the engineering relationship between tickets: twenty-three
issue-level reports map to five shared implementation mechanisms. TC-18, TC-19 and TC-21
remain open questions and are not inflated into confirmed bugs.

| Bug ID | Title / reproducible input | TC | Expected | Actual | Root cause | GitHub Issue | Evidence screenshot |
|---|---|---|---|---|---|---|---|
| BUG-FR01-01 | Requirement-valid `Password123!` is rejected | TC-01a | Register and redirect to Login | Remains on Register with password error | RC-PASSWORD | [#39](https://github.com/KieuDuyennn/software__testing/issues/39) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-01-password-valid-rejected.png` |
| BUG-FR01-02 | Minimum valid 8-character password `Pa1!abcd` is rejected | BVA-02 | Accept the documented lower boundary | Password error; no registration | RC-PASSWORD | [#40](https://github.com/KieuDuyennn/software__testing/issues/40) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-02-password-minimum-8-rejected.png` |
| BUG-FR01-03 | Valid 9-character password `Pa1!abcde` is rejected | BVA-03 | Accept and create the account | Password error; no registration | RC-PASSWORD | [#41](https://github.com/KieuDuyennn/software__testing/issues/41) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-03-password-9-rejected.png` |
| BUG-FR01-04 | Weak whitespace password `Password 123` is accepted | TC-24 | Reject because no documented special character exists | Redirects and creates a usable account | RC-PASSWORD | [#42](https://github.com/KieuDuyennn/software__testing/issues/42) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-04-weak-whitespace-password-accepted.png` |
| BUG-FR01-05 | E-mail without `@` is accepted | TC-06 | Reject `userdomain.com` | Redirects to Login | RC-EMAIL-FORMAT | [#43](https://github.com/KieuDuyennn/software__testing/issues/43) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-05-email-no-at-accepted.png` |
| BUG-FR01-06 | E-mail without domain is accepted | TC-07 | Reject `user@` | Redirects to Login | RC-EMAIL-FORMAT | [#44](https://github.com/KieuDuyennn/software__testing/issues/44) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-06-email-no-domain-accepted.png` |
| BUG-FR01-07 | E-mail without local part is accepted | TC-08 | Reject `@domain.com` | Redirects to Login | RC-EMAIL-FORMAT | [#45](https://github.com/KieuDuyennn/software__testing/issues/45) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-07-email-no-local-accepted.png` |
| BUG-FR01-08 | Exact duplicate e-mail registration is accepted | TC-09 | Show uniqueness error and remain on Register | No banner; redirects to Login | RC-EMAIL-UNIQUE | [#46](https://github.com/KieuDuyennn/software__testing/issues/46) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-08-duplicate-email-accepted.png` |
| BUG-FR01-09 | API creates account when `name` is omitted | TC-03 | Refuse request; no created `id` | HTTP 200 with numeric `id`; login succeeds | RC-REQUIRED-FIELDS | [#47](https://github.com/KieuDuyennn/software__testing/issues/47) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-09-missing-name-created.png` |
| BUG-FR01-10 | API creates account when `email` is omitted | TC-05 | Refuse request; no created `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | [#48](https://github.com/KieuDuyennn/software__testing/issues/48) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-10-missing-email-created.png` |
| BUG-FR01-11 | API creates account when `password` is omitted | TC-11 | Refuse request; no created `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | [#49](https://github.com/KieuDuyennn/software__testing/issues/49) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-11-missing-password-created.png` |
| BUG-FR01-15 | API accepts empty name | API-01 | Refuse request; no `id` | HTTP 200, numeric `id`, usable account | RC-REQUIRED-FIELDS | [#53](https://github.com/KieuDuyennn/software__testing/issues/53) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-15-api-empty-name-accepted.png` |
| BUG-FR01-16 | API accepts empty e-mail | API-02 | Refuse request; no `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | [#54](https://github.com/KieuDuyennn/software__testing/issues/54) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-16-api-empty-email-accepted.png` |
| BUG-FR01-17 | API accepts empty password | API-03 | Refuse request; no `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | [#55](https://github.com/KieuDuyennn/software__testing/issues/55) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-17-api-empty-password-accepted.png` |
| BUG-FR01-18 | API accepts e-mail without `@` | API-04 | Refuse malformed e-mail | HTTP 200, numeric `id`, usable account | RC-EMAIL-FORMAT | [#56](https://github.com/KieuDuyennn/software__testing/issues/56) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-18-api-email-no-at-accepted.png` |
| BUG-FR01-19 | API accepts e-mail without domain | API-05 | Refuse malformed e-mail | HTTP 200, numeric `id`, usable account | RC-EMAIL-FORMAT | [#57](https://github.com/KieuDuyennn/software__testing/issues/57) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-19-api-email-no-domain-accepted.png` |
| BUG-FR01-20 | API accepts e-mail without local part | API-06 | Refuse malformed e-mail | HTTP 200, numeric `id`, usable account | RC-EMAIL-FORMAT | [#58](https://github.com/KieuDuyennn/software__testing/issues/58) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-20-api-email-no-local-accepted.png` |
| BUG-FR01-21 | API accepts seven-character password | API-07 | Refuse password below minimum | HTTP 200, numeric `id`, usable account | RC-PASSWORD-API | [#59](https://github.com/KieuDuyennn/software__testing/issues/59) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-21-api-seven-char-password-accepted.png` |
| BUG-FR01-22 | API accepts password without uppercase | API-08 | Refuse weak password | HTTP 200, numeric `id`, usable account | RC-PASSWORD-API | [#60](https://github.com/KieuDuyennn/software__testing/issues/60) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-22-api-password-no-uppercase-accepted.png` |
| BUG-FR01-23 | API accepts password without lowercase | API-09 | Refuse weak password | HTTP 200, numeric `id`, usable account | RC-PASSWORD-API | [#61](https://github.com/KieuDuyennn/software__testing/issues/61) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-23-api-password-no-lowercase-accepted.png` |
| BUG-FR01-24 | API accepts password without digit | API-10 | Refuse weak password | HTTP 200, numeric `id`, usable account | RC-PASSWORD-API | [#62](https://github.com/KieuDuyennn/software__testing/issues/62) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-24-api-password-no-digit-accepted.png` |
| BUG-FR01-25 | API accepts password without special character | API-11 | Refuse weak password | HTTP 200, numeric `id`, usable account | RC-PASSWORD-API | [#63](https://github.com/KieuDuyennn/software__testing/issues/63) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-25-api-password-no-special-accepted.png` |
| BUG-FR01-26 | API accepts exact duplicate e-mail | API-12 | Refuse duplicate; no new `id` | HTTP 200 with another numeric `id` | RC-EMAIL-UNIQUE | [#64](https://github.com/KieuDuyennn/software__testing/issues/64) | `reports/evidence/failure-screenshots/fr01/BUG-FR01-26-api-duplicate-email-accepted.png` |

All twenty-three confirmed issue bodies include the common environment: EShop local deployment,
Chromium/Firefox/WebKit, final run of 2026-08-10, and the matching test detail in
`reports/final/html/fr01/<browser>/index.html`. The shared analyses below provide full
reproduction steps, assertions, requirement anchors, and implementation mechanism.

## Requirement-clarification issues

These three failed cases should also be filed to maximise useful issue coverage, but they
must be labelled **investigation / requirement clarification**, not confirmed defects.
Their expected result depends on a reasonable interpretation that the current requirement
does not make explicit.

| Issue ID | Title | TC | Observed behaviour | Question to resolve | GitHub Issue | Evidence screenshot |
|---|---|---|---|---|---|---|
| ISSUE-FR01-12 | Whitespace-only full name is accepted | TC-18 | `"   "` registers successfully | Does “name is required” exclude whitespace-only input? | [#50](https://github.com/KieuDuyennn/software__testing/issues/50) | `reports/evidence/failure-screenshots/fr01/ISSUE-FR01-12-whitespace-only-name-accepted.png` |
| ISSUE-FR01-13 | E-mail without a top-level domain is accepted | TC-19 | `user@domain` registers successfully | Does “valid format such as user@domain.com” require a TLD? | [#51](https://github.com/KieuDuyennn/software__testing/issues/51) | `reports/evidence/failure-screenshots/fr01/ISSUE-FR01-13-email-without-tld-accepted.png` |
| ISSUE-FR01-14 | Case-variant duplicate e-mail is accepted | TC-21 | Upper-case variant registers beside the seeded lower-case address | Must uniqueness be case-insensitive? | [#52](https://github.com/KieuDuyennn/software__testing/issues/52) | `reports/evidence/failure-screenshots/fr01/ISSUE-FR01-14-case-variant-duplicate-accepted.png` |

**GitHub delivery: 26 issues total** = 23 confirmed issue-level bugs + 3
requirement-clarification investigations. Only the 23 bug-labelled issues count in the confirmed
defect severity summary.

## Shared root-cause analysis

### RC-PASSWORD — Password validation enforces whitespace and rejects documented special characters

| Field | Value |
|---|---|
| Feature | FR-01 Account registration |
| Severity | Major |
| Browser(s) affected | Chromium, Firefox, WebKit |
| Revealed by | BUG-FR01-01 through BUG-FR01-04 |
| Playwright report | `reports/final/html/fr01/<browser>/index.html` |
| Issue-level evidence | See the four distinct screenshots in the table above |

**Steps to reproduce**

1. Open `/register`.
2. Enter a valid name and unique valid e-mail.
3. Submit `Password123!` (or boundary value `Pa1!abcd`).
4. Repeat with `Password 123`, which has whitespace but no documented special character.

`Password123!` is accepted; `Password 123` is rejected. The rule requires at least one
uppercase, lowercase, digit, and one character from `@ $ ! % * ? &`.

Passwords containing `!` are rejected, while `Password 123` is accepted and creates a
usable account. The client regex requires `\s` and excludes special characters.

**Assertion that caught it**

```ts
await expect(page).toHaveURL(/\/login$/); // TC-01a/BVA-02/BVA-03 stays on /register
expect(login.ok()).toBeFalsy();            // TC-24 returns true
```

The functional requirement and the page's own hint both require a documented special
character. TC-01c separately proves the downstream redirect/persistence path works when
the current implementation's gate accepts the password.

---

### RC-EMAIL-FORMAT — Registration accepts structurally invalid e-mail addresses

| Field | Value |
|---|---|
| Feature | FR-01 Account registration |
| Severity | Major |
| Browser(s) affected | Chromium, Firefox, WebKit |
| Revealed by | BUG-FR01-05→07 and BUG-FR01-18→20 |
| Playwright report | `reports/final/html/fr01/<browser>/index.html` |
| Issue-level evidence | See the three distinct screenshots in the table above |

**Steps to reproduce**

1. Open `/register` and provide a valid name.
2. Use `userdomain.com`, `user@`, or `@domain.com` as the e-mail.
3. Use the diagnostic gate-passing password and submit.

**Expected**

Registration remains on `/register`, explains the e-mail error, and creates no account.

**Actual**

No error banner appears; the app redirects to `/login`, and the submitted address is
usable through the login API. `Register.jsx` renders the e-mail input as `type="text"`
and neither tier performs format validation.

**Assertion that caught it**

```ts
await expect.soft(registerPage.errorBanner).toBeVisible();
await expect.soft(page).toHaveURL(/\/register$/);
expect(login.ok()).toBeFalsy();
```

**Why this is a product defect and not a test defect**

The requirement explicitly defines a valid shape such as `user@domain.com`; all three
inputs omit a mandatory structural component.

---

### RC-EMAIL-UNIQUE — Duplicate e-mail registration is not rejected

| Field | Value |
|---|---|
| Feature | FR-01 Account registration |
| Severity | Major |
| Browser(s) affected | Chromium, Firefox, WebKit |
| Revealed by | BUG-FR01-08 and BUG-FR01-26 |
| Playwright report | `reports/final/html/fr01/<browser>/index.html` |
| Issue-level evidence | See the BUG-FR01-08 screenshot in the table above |

**Steps to reproduce**

1. Register or seed an account with a fresh address.
2. Submit the registration form again with exactly the same address.

**Expected**

Registration is refused, an e-mail uniqueness error is shown, and the page stays on
`/register`.

**Actual**

No banner appears and the app redirects to `/login`, so the automated UI evidence proves
the duplicate submission was accepted. A separate manual database inspection found two
rows for the seeded address; this row-count observation is supporting evidence rather than
an assertion in TC-09. The schema has no `UNIQUE` constraint and the handler has no
duplicate check.

**Assertion that caught it**

```ts
await expect.soft(registerPage.errorBanner).toBeVisible();
await expect.soft(page).toHaveURL(/\/register$/);
```

**Why this is a product defect and not a test defect**

The FR-01 requirement explicitly states that the e-mail must be unique in the system.
TC-21's case-insensitive variant remains an open question and is not needed for this bug.

---

### RC-REQUIRED-FIELDS — Registration API creates accounts with missing required fields

| Field | Value |
|---|---|
| Feature | FR-01 Account registration |
| Severity | Major |
| Browser(s) affected | API result reproduced during all three browser-project runs |
| Revealed by | BUG-FR01-09→11 and BUG-FR01-15→17 |
| Playwright report | `reports/final/html/fr01/<browser>/index.html` |
| Issue-level evidence | See the three distinct HTML-report screenshots in the table above; raw API pages are `about:blank` |

**Steps to reproduce**

1. POST `/api/register` while omitting `name`, `email`, or `password`.
2. Inspect the response status and JSON body.
3. For omitted `name`, try logging in with the submitted e-mail and password.

**Expected**

The request is refused and the response does not contain a created-account identifier.
No account is persisted.

**Actual**

The endpoint returns HTTP 200 and a numeric `id` for all three omissions. The omitted-name
account is also usable through `/api/login`. Persistence cannot be looked up automatically
for omitted e-mail/password, so that limitation remains explicitly annotated.

**Assertion that caught it**

```ts
expect.soft(response.status()).toBe(400);
expect.soft(rejectedBody.id).toBeUndefined();
expect(login.ok()).toBeFalsy(); // applicable when name alone was omitted
```

**Why this is a product defect and not a test defect**

FR-01 defines name, e-mail, and password as required. The exact rejection status is not
documented, but returning a creation identifier for a request missing a required field
contradicts the functional rule regardless of which 4xx code is chosen.

---

### RC-PASSWORD-API — Register API performs no password validation

Direct `POST /api/register` requests with a seven-character password or with one
documented composition category missing all return HTTP 200, a numeric account `id`,
and usable credentials. BUG-FR01-21→25 isolate minimum length, uppercase, lowercase,
digit, and special-character enforcement at the server layer. The exact rejection status
is not documented, but returning a creation identifier and persisting each weak-password
account directly contradicts FR-01.

---

The three open-question failures TC-18, TC-19 and TC-21 are intentionally not counted as
confirmed defects here; their requirement anchors are inferred and require student triage.
The missing Confirm Password field is documented as an unautomatable requirement gap,
not as a failure revealed by this run.

## FR-11 Order history — failure-level bug assessment

Final execution (2026-08-10) ran 46 data-driven cases on Chromium, Firefox and WebKit.
Each row below is one failing test assertion, as requested; identical root causes are
kept as separate bugs so every reproducible failure has a traceable finding.

| Bug ID | TC | Verdict | Severity | Finding |
|---|---|---|---|---|
| BUG-FR11-01 | TC-03 | Confirmed defect | Critical | [Issue #18](https://github.com/KieuDuyennn/software__testing/issues/18) — `GET /api/orders/:id` exposes another user's order (HTTP 200). |
| BUG-FR11-02 | TC-14 | Confirmed defect | Major | [Issue #19](https://github.com/KieuDuyennn/software__testing/issues/19) — cancel buttons are shown for shipping orders. |
| BUG-FR11-03 | TC-15 | Confirmed defect | Critical | [Issue #20](https://github.com/KieuDuyennn/software__testing/issues/20) — order-detail route accepts an unauthenticated request. |
| BUG-FR11-04 | TC-18 | Confirmed defect | Critical | [Issue #21](https://github.com/KieuDuyennn/software__testing/issues/21) — non-admin user can list all orders. |
| BUG-FR11-05 | TC-19 | Confirmed defect | Critical | [Issue #22](https://github.com/KieuDuyennn/software__testing/issues/22) — non-admin user can change order status. |
| BUG-FR11-06 | TC-22 | Confirmed defect | Major | [Issue #23](https://github.com/KieuDuyennn/software__testing/issues/23) — API accepts illegal `canceled → delivered` transition. |
| BUG-FR11-07 | TC-23 | Confirmed defect | Major | [Issue #24](https://github.com/KieuDuyennn/software__testing/issues/24) — UI displays a canceled order as delivered. |
| BUG-FR11-08 | TC-26 | Confirmed defect | Major | [Issue #25](https://github.com/KieuDuyennn/software__testing/issues/25) — cancel on a shipping order succeeds. |
| BUG-FR11-09 | TC-27 | Confirmed defect | Major | [Issue #26](https://github.com/KieuDuyennn/software__testing/issues/26) — cancel API accepts a shipping-order cancellation. |
| BUG-FR11-10 | TC-31 | Confirmed defect | Major | [Issue #27](https://github.com/KieuDuyennn/software__testing/issues/27) — non-numeric `total_amount` renders as `NaN ₫`. |
| BUG-FR11-11 | TC-33 | Confirmed defect | Major | [Issue #28](https://github.com/KieuDuyennn/software__testing/issues/28) — negative order total is accepted and displayed. |
| BUG-FR11-12 | TC-34 | Confirmed defect | Major | [Issue #29](https://github.com/KieuDuyennn/software__testing/issues/29) — missing total is silently rendered as `0 ₫`. |
| BUG-FR11-13 | TC-35 | Confirmed defect | Major | [Issue #30](https://github.com/KieuDuyennn/software__testing/issues/30) — checkout accepts a non-numeric total. |
| BUG-FR11-14 | TC-36 | Confirmed defect | Major | [Issue #31](https://github.com/KieuDuyennn/software__testing/issues/31) — fetch failure is shown as empty history. |
| BUG-FR11-15 | TC-42 | Confirmed defect | Major | [Issue #32](https://github.com/KieuDuyennn/software__testing/issues/32) — malformed nested `orders` payload breaks the profile page. |
| BUG-FR11-16 | TC-43 | Confirmed defect | Critical | [Issue #33](https://github.com/KieuDuyennn/software__testing/issues/33) — signed token for a nonexistent user is accepted. |

**FR-11 assessment:** 16 failure-level findings, comprising 8 implementation root-cause
clusters. The same underlying cause may therefore appear in multiple issue rows. TC-45
is not included: the final concurrent run returned `200` and `400`, so its single-success
oracle passed. Evidence is in `reports/final/html/fr11/<browser>/index.html` and the archived
merged runs under `reports/history/archived-runs/`. Severity is an engineering assessment
based on security exposure, data integrity and user impact and was reviewed before the
issues were filed.

Evidence screenshots for BUG-FR11-01 through BUG-FR11-16 are stored under
`reports/evidence/failure-screenshots/fr11/BUG-FR11-*.png` and linked from GitHub Issues #18–#33.
Screenshots of the filed issue pages themselves are stored under
`reports/evidence/github-issues/fr11/`; filenames map Issue #18–#33 in order to
BUG-FR11-01–BUG-FR11-16 (for example,
`issue-18-BUG-FR11-01.png` and `issue-33-BUG-FR11-16.png`).

## FR-13 Dashboard — root-cause bug assessment

The 50-case Chromium run produced 29 passes and 21 failed assertions. Firefox and
WebKit reproduced the same six root-cause mechanisms across the `tc`, `bva`, and `api`
report groups. These are filed and preserved as follows:

| Bug ID | Severity | Finding | GitHub Issue | Issue-page screenshot |
|---|---|---|---|---|
| BUG-FR13-01 | Major | Delivered revenue is multiplied by two. | [#15](https://github.com/KieuDuyennn/software__testing/issues/15) | `reports/evidence/github-issues/fr13/issue-15-BUG-FR13-01.png` |
| BUG-FR13-02 | Major | `canceled → delivered` is accepted and mutates the order. | [#38](https://github.com/KieuDuyennn/software__testing/issues/38) | `reports/evidence/github-issues/fr13/issue-38-BUG-FR13-02.png` |
| BUG-FR13-03 | Critical | Checkout trusts malformed client `total_amount` values. | [#34](https://github.com/KieuDuyennn/software__testing/issues/34) | `reports/evidence/github-issues/fr13/issue-34-BUG-FR13-03.png` |
| BUG-FR13-04 | Critical | Admin endpoints authenticate tokens without enforcing the admin role. | [#14](https://github.com/KieuDuyennn/software__testing/issues/14) | `reports/evidence/github-issues/fr13/issue-14-BUG-FR13-04.png` |
| BUG-FR13-05 | Critical | A signed admin token for a nonexistent user reads global orders. | [#36](https://github.com/KieuDuyennn/software__testing/issues/36) | `reports/evidence/github-issues/fr13/issue-36-BUG-FR13-05.png` |
| BUG-FR13-06 | Critical | A normal user can promote their own profile to `admin`. | [#37](https://github.com/KieuDuyennn/software__testing/issues/37) | `reports/evidence/github-issues/fr13/issue-37-BUG-FR13-06.png` |

Execution evidence remains in `reports/final/json/fr13-chromium.json` and the Firefox/
WebKit `tc`, `bva`, and `api` reports. The issue-page screenshots document filing status;
they do not replace the generated execution evidence.
