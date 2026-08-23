## Requirement

SEC-01: passwords must not be stored or exposed as plaintext.

## Steps to reproduce

1. Register a new account with `Password123!`.
2. Log in using that account.
3. Inspect the JSON `user` object returned by `POST /api/login` and the profile response.

Every request carries `X-Student-Id: 23127184`.

## Expected

No API response contains a password field or the submitted plaintext. The stored value is a one-way password hash.

## Actual

The login/profile payload contains `password: "Password123!"`, and the stored value equals the submitted plaintext.

## Verified evidence

- Newman cases: `A1-SEC-001`, `A1-SEC-003`, `A1-SEC-004`
- Run: `evidence/newman-console/suite_full_20260823-223623.log`
- Report: `HW06/reports/API1_FR01_Register.html`
- Assertion: `expected 'Password123!' to not deeply equal 'Password123!'`

Severity: **Critical**.
