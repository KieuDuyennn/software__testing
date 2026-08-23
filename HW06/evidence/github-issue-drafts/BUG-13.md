## Requirement

SEC-03 / FR-12: mutating product APIs require a valid admin token.

## Steps to reproduce

Call each route with no token and with a genuine ordinary-user token:

- `POST /api/products`
- `PUT /api/products/:id`
- `DELETE /api/products/:id`

Every request carries `X-Student-Id: 23127184`.

## Expected

No token: 401. Non-admin token: 403. No catalogue mutation.

## Actual

All three routes return HTTP 200 and perform the requested mutation. Neither authentication nor role authorization is enforced.

## Verified evidence

- Newman cases: `A2-SEC-011` through `A2-SEC-015`
- Run: `evidence/newman-console/suite_full_20260823-223623.log`
- Report: `HW06/reports/API2_FR06_ProductDetail.html`
- Assertion: `status code: expected 200 to be within 401..403`

Severity: **Critical**.
