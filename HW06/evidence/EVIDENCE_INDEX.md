# HW06 Authentic Evidence Index

Student ID: **23127184**  
Captured: **2026-08-23**

Only screenshots taken from the real signed-in GitHub and Postman sessions are
listed as complete. No placeholder or generated UI image is included.

## Completed evidence

| Evidence | File | Verification visible in image |
|---|---|---|
| GitHub Actions green run | `screenshots/github-actions-green-summary.png` | Repository, branch `hw6`, commit `66c151a`, Success status, green regression/full jobs |
| GitHub Actions red run | `screenshots/github-actions-red-summary.png` | Repository, branch `hw6`, commit `3c34519`, Failure status, red regression job |
| GitHub Issue #66 | `screenshots/github-issue-66-plaintext-password.png` | Signed-in account, issue title/number, reproduction steps and `X-Student-Id: 23127184` |
| GitHub Issue #67 | `screenshots/github-issue-67-confirm-password.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #68 | `screenshots/github-issue-68-text-plain-http500.png` | Signed-in account, issue title/number, request and student header |
| GitHub Issue #69 | `screenshots/github-issue-69-html-stack-trace.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #70 | `screenshots/github-issue-70-product-write-auth.png` | Signed-in account, issue title/number and student header |
| Postman Cloud workspace | `postman-cloud/workspace.png` | Signed-in workspace and all four imported HW06 collections |
| Postman environment | `postman-cloud/environment.png` | Imported `EShop - Local (23127184)` environment |
| Real Postman Console run | `screenshots/postman-console-x-student-id.png` | Postman Desktop, localhost URL, HTTP 200 and `[HW06] X-Student-Id=23127184` |
| Postman Mock Server | `postman-cloud/mock-server.png` | Public API2 mock is Running and records `GET /api/products/2`; the request currently has no example response |

Cloud URLs:

- Green CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32650162410>
- Red CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32649883960>
- Issues: <https://github.com/KieuDuyennn/software__testing/issues/66> through
  <https://github.com/KieuDuyennn/software__testing/issues/70>

## Still requires the student/device

- Collection Runner and Monitor results.
- A successful Mock Server example response (the server and authentic call log
  exist, but the current call correctly reports that no example is attached).
- Failure screenshots attached to the corresponding GitHub Issues, if the
  marking rubric requires attachments rather than issue-page screenshots.
- Student authorship review of the editable generator diagram and narrated demo
  video. The dated group uniqueness confirmation is recorded in `README.md` and
  the main report. The Mermaid source and PNG export exist at
  `docs/design/diagram/`.

Postman Desktop 12.24.6 and Desktop Agent 0.4.90 were installed on 2026-08-23.
The localhost SUT request was executed in Postman Desktop and captured without
fabrication. The Desktop lightweight client requires account sign-in before it
will enable collection import and Runner.
