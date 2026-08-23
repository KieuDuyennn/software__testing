## Requirement

FR-01 requires password confirmation and rejects registration when the values do not match.

## Steps to reproduce

Send `POST /api/register` with a valid password and either an absent, mismatching, or numeric `confirmPassword` value. Every request carries `X-Student-Id: 23127184`.

## Expected

HTTP 4xx and no account creation.

## Actual

HTTP 200 and the account is created. The backend ignores `confirmPassword` completely.

## Verified evidence

- Newman cases: `A1-DP-066`, `A1-DP-067`, student-designed `A1-HR-005`
- Run: `evidence/newman-console/suite_full_20260823-223623.log`
- Report: `HW06/reports/API1_FR01_Register.html`
- Assertion: `status code: expected 200 to be within 400..499`

Severity: **Medium**.
