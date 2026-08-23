## Requirement

SEC-05/general information disclosure: malformed input must not return an HTML stack trace.

## Steps to reproduce

Send malformed JSON such as `{"name":"Broken",` to `POST /api/register` with `Content-Type: application/json` and `X-Student-Id: 23127184`.

## Expected

HTTP 400 with a structured JSON error and no stack details.

## Actual

HTTP 400 with `Content-Type: text/html; charset=utf-8`; the body contains a `<pre>` stack-trace block with server internals.

## Verified evidence

- Newman case: `A1-SCH-012`
- Run: `evidence/newman-console/suite_full_20260823-223623.log`
- Report: `HW06/reports/API1_FR01_Register.html`
- Assertions: response must not include `text/html` or `<pre>`.

Severity: **Medium**.
