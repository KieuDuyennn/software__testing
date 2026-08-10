# Bug Report — HW04

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184
**SUT:** EShop — https://github.com/ttbhanh/eshop-sut
**GitHub Issues page:** **Pending student action** — the local review must not fabricate a public URL.

Only defects revealed by a **failing assertion in an automated run** belong here (§6).
A test that fails because the test is wrong is a fix for `AI_Review_Gap_Analysis.md`,
not a bug — keeping those two apart is most of the credibility of this file.

Each bug must also be filed as a GitHub Issue **with a screenshot attached**, and the
screenshot stored under `reports/github_issues/`.

## Summary

| Severity | Count | Bug IDs |
|---|---|---|
| Blocker | 0 | |
| Critical | 0 | |
| Major | 11 | BUG-FR01-01 through BUG-FR01-11 |
| Minor | 0 | |
| Trivial | 0 | |
| **Total** | **11** | |

## Issue-level bug reports

The lecturer grades the quantity as well as the quality of issue deliverables. Therefore
each independently reproducible failing case below has its own issue ID and screenshot.
The **Root cause** column preserves the engineering relationship between tickets: eleven
issue-level reports map to four shared implementation mechanisms. TC-18, TC-19 and TC-21
remain open questions and are not inflated into confirmed bugs.

| Bug ID | Title / reproducible input | TC | Expected | Actual | Root cause | GitHub Issue | Evidence screenshot |
|---|---|---|---|---|---|---|---|
| BUG-FR01-01 | Requirement-valid `Password123!` is rejected | TC-01a | Register and redirect to Login | Remains on Register with password error | RC-PASSWORD | Pending student filing | `reports/screenshots/BUG-FR01-01-password-valid-rejected.png` |
| BUG-FR01-02 | Minimum valid 8-character password `Pa1!abcd` is rejected | BVA-02 | Accept the documented lower boundary | Password error; no registration | RC-PASSWORD | Pending student filing | `reports/screenshots/BUG-FR01-02-password-minimum-8-rejected.png` |
| BUG-FR01-03 | Valid 9-character password `Pa1!abcde` is rejected | BVA-03 | Accept and create the account | Password error; no registration | RC-PASSWORD | Pending student filing | `reports/screenshots/BUG-FR01-03-password-9-rejected.png` |
| BUG-FR01-04 | Weak whitespace password `Password 123` is accepted | TC-24 | Reject because no documented special character exists | Redirects and creates a usable account | RC-PASSWORD | Pending student filing | `reports/screenshots/BUG-FR01-04-weak-whitespace-password-accepted.png` |
| BUG-FR01-05 | E-mail without `@` is accepted | TC-06 | Reject `userdomain.com` | Redirects to Login | RC-EMAIL-FORMAT | Pending student filing | `reports/screenshots/BUG-FR01-05-email-no-at-accepted.png` |
| BUG-FR01-06 | E-mail without domain is accepted | TC-07 | Reject `user@` | Redirects to Login | RC-EMAIL-FORMAT | Pending student filing | `reports/screenshots/BUG-FR01-06-email-no-domain-accepted.png` |
| BUG-FR01-07 | E-mail without local part is accepted | TC-08 | Reject `@domain.com` | Redirects to Login | RC-EMAIL-FORMAT | Pending student filing | `reports/screenshots/BUG-FR01-07-email-no-local-accepted.png` |
| BUG-FR01-08 | Exact duplicate e-mail registration is accepted | TC-09 | Show uniqueness error and remain on Register | No banner; redirects to Login | RC-EMAIL-UNIQUE | Pending student filing | `reports/screenshots/BUG-FR01-08-duplicate-email-accepted.png` |
| BUG-FR01-09 | API creates account when `name` is omitted | TC-03 | Refuse request; no created `id` | HTTP 200 with numeric `id`; login succeeds | RC-REQUIRED-FIELDS | Pending student filing | `reports/screenshots/BUG-FR01-09-missing-name-created.png` |
| BUG-FR01-10 | API creates account when `email` is omitted | TC-05 | Refuse request; no created `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | Pending student filing | `reports/screenshots/BUG-FR01-10-missing-email-created.png` |
| BUG-FR01-11 | API creates account when `password` is omitted | TC-11 | Refuse request; no created `id` | HTTP 200 with numeric `id` | RC-REQUIRED-FIELDS | Pending student filing | `reports/screenshots/BUG-FR01-11-missing-password-created.png` |

All eleven issue bodies should include the common environment: EShop local deployment,
Chromium/Firefox/WebKit, final run of 2026-08-10, and the matching test detail in
`reports/html/fr01/<browser>/index.html`. The shared analyses below provide full
reproduction steps, assertions, requirement anchors, and implementation mechanism.

## Requirement-clarification issues

These three failed cases should also be filed to maximise useful issue coverage, but they
must be labelled **investigation / requirement clarification**, not confirmed defects.
Their expected result depends on a reasonable interpretation that the current requirement
does not make explicit.

| Issue ID | Title | TC | Observed behaviour | Question to resolve | GitHub Issue | Evidence screenshot |
|---|---|---|---|---|---|---|
| ISSUE-FR01-12 | Whitespace-only full name is accepted | TC-18 | `"   "` registers successfully | Does “name is required” exclude whitespace-only input? | Pending student filing | `reports/screenshots/ISSUE-FR01-12-whitespace-only-name-accepted.png` |
| ISSUE-FR01-13 | E-mail without a top-level domain is accepted | TC-19 | `user@domain` registers successfully | Does “valid format such as user@domain.com” require a TLD? | Pending student filing | `reports/screenshots/ISSUE-FR01-13-email-without-tld-accepted.png` |
| ISSUE-FR01-14 | Case-variant duplicate e-mail is accepted | TC-21 | Upper-case variant registers beside the seeded lower-case address | Must uniqueness be case-insensitive? | Pending student filing | `reports/screenshots/ISSUE-FR01-14-case-variant-duplicate-accepted.png` |

**GitHub delivery target: 14 issues total** = 11 confirmed issue-level bugs + 3
requirement-clarification investigations. Only the first eleven count in the confirmed
defect severity summary.

## Shared root-cause analysis

### RC-PASSWORD — Password validation enforces whitespace and rejects documented special characters

| Field | Value |
|---|---|
| Feature | FR-01 Account registration |
| Severity | Major |
| Browser(s) affected | Chromium, Firefox, WebKit |
| Revealed by | BUG-FR01-01 through BUG-FR01-04 |
| Playwright report | `reports/html/fr01/<browser>/index.html` |
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
| Revealed by | BUG-FR01-05 through BUG-FR01-07 |
| Playwright report | `reports/html/fr01/<browser>/index.html` |
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
| Revealed by | BUG-FR01-08 |
| Playwright report | `reports/html/fr01/<browser>/index.html` |
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
| Revealed by | BUG-FR01-09 through BUG-FR01-11 |
| Playwright report | `reports/html/fr01/<browser>/index.html` |
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
| BUG-FR11-01 | TC-03 | Confirmed defect | Critical | `GET /api/orders/:id` exposes another user's order (HTTP 200). This is an authorization/data-disclosure failure. |
| BUG-FR11-02 | TC-14 | Confirmed defect | Major | Cancel buttons are shown for shipping orders; UI offers an operation that should be unavailable. |
| BUG-FR11-03 | TC-15 | Confirmed defect | Critical | Order-detail route accepts a request without authentication instead of refusing it. |
| BUG-FR11-04 | TC-18 | Confirmed defect | Critical | Non-admin user can list all orders through `/api/admin/orders` (missing role enforcement). |
| BUG-FR11-05 | TC-19 | Confirmed defect | Critical | Non-admin user can change order status through the admin endpoint. |
| BUG-FR11-06 | TC-22 | Confirmed defect | Major | API accepts illegal `canceled → delivered` transition. |
| BUG-FR11-07 | TC-23 | Confirmed defect | Major | UI displays a canceled order as delivered after the illegal transition. |
| BUG-FR11-08 | TC-26 | Confirmed defect | Major | Clicking cancel on a shipping order succeeds; synchronized UI evidence shows `Đã hủy`. |
| BUG-FR11-09 | TC-27 | Confirmed defect | Major | Cancel API accepts a shipping-order cancellation directly, independently of the UI. |
| BUG-FR11-10 | TC-31 | Confirmed defect | Major | Non-numeric `total_amount` renders as `NaN ₫`. |
| BUG-FR11-11 | TC-33 | Confirmed defect | Major | Negative order total is accepted and displayed as a price. |
| BUG-FR11-12 | TC-34 | Confirmed defect | Major | Missing total is silently rendered as `0 ₫`, masking malformed order data. |
| BUG-FR11-13 | TC-35 | Confirmed defect | Major | Checkout accepts a non-numeric client-supplied total and creates the order. |
| BUG-FR11-14 | TC-36 | Confirmed defect | Major | Order-fetch failure is rendered as the empty-history state, misleading the user. |
| BUG-FR11-15 | TC-42 | Confirmed defect | Major | Truthy nested `orders` payload of the wrong type reaches `.map` and breaks the profile page. |
| BUG-FR11-16 | TC-43 | Confirmed defect | Critical | Correctly signed token for a nonexistent user is accepted as a live session (HTTP 200). |

**FR-11 assessment:** 16 failure-level findings, comprising 8 implementation root-cause
clusters. The same underlying cause may therefore appear in multiple issue rows. TC-45
is not included: the final concurrent run returned `200` and `400`, so its single-success
oracle passed. Evidence is in `reports/html/fr11/<browser>/index.html` and the archived
merged runs under `reports/archive/`. Severity is an engineering assessment based on
security exposure, data integrity and user impact; the student may adjust it to match the
course rubric before filing issues.
