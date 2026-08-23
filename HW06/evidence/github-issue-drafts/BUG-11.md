## Requirement

The JSON API must reject unsupported request media types with a client error, not crash.

## Steps to reproduce

```http
POST /api/register
Content-Type: text/plain
X-Student-Id: 23127184

name=Test&email=a@b.com&password=Password123!
```

## Expected

HTTP 400 or 415 with a structured error.

## Actual

HTTP **500 Internal Server Error**. The route destructures `req.body` when the JSON parser has not populated it.

## Verified evidence

- Newman case: `A1-DP-071`
- Run: `evidence/newman-console/suite_full_20260823-223623.log`
- Report: `HW06/reports/API1_FR01_Register.html`
- Assertion: `expected 500 to be one of [ 400, 415 ]`

Severity: **High**.
