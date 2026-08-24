# HW06 Authentic Evidence Index

Student ID: **23127184**  
Captured: **2026-08-23**

Completed items below come from real signed-in GitHub/Postman sessions or are
clearly labelled renderings of verbatim fields retained in raw Newman JSON.
No placeholder or simulated application UI is included.

## Completed evidence

| Evidence | File | Verification visible in image |
|---|---|---|
| GitHub Actions green run | `screenshots/github-actions-green-summary.png` | Repository, branch `hw6`, commit `66c151a`, Success status, green regression/full jobs |
| GitHub Actions red run | `screenshots/github-actions-red-summary.png` | Repository, branch `hw6`, commit `3c34519`, Failure status, red regression job |
| GitHub Issue #7 | `screenshots/github-issue-7-malformed-email-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A1-DP-019`: request, `X-Student-Id: 23127184`, expected 4xx, actual 200 and failed assertion. Fixed in commit `73ce207`; the case passes in the current reports |
| GitHub Issue #14 | `screenshots/github-issue-14-admin-role-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A4-SEC-001`: request, student header, expected 401-403, actual 200 and failed assertion. Fixed in commit `73ce207` |
| GitHub Issue #38 | `screenshots/github-issue-38-terminal-transition-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A4-ST-016`: request, student header, expected 4xx, actual 200 and failed assertion. Fixed in commit `73ce207` |
| GitHub Issue #66 | `screenshots/github-issue-66-plaintext-password.png` | Signed-in account, issue title/number, reproduction steps and `X-Student-Id: 23127184` |
| GitHub Issue #67 | `screenshots/github-issue-67-confirm-password.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #68 | `screenshots/github-issue-68-text-plain-http500.png` | Signed-in account, issue title/number, request and student header |
| GitHub Issue #69 | `screenshots/github-issue-69-html-stack-trace.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #70 | `screenshots/github-issue-70-product-write-auth.png` | Signed-in account, issue title/number and student header |
| Postman Cloud workspace | `postman-cloud/workspace.png` | Signed-in workspace and all four imported HW06 collections |
| Postman environment | `postman-cloud/environment.png` | Imported `EShop - Local (23127184)` environment |
| Real Postman Console run | `screenshots/postman-console-x-student-id.png` | Postman Desktop, localhost URL, HTTP 200 and `[HW06] X-Student-Id=23127184` |
| Postman Mock Server | `postman-cloud/mock-server.png` | Public API2 mock is Running and records `GET /api/products/2`; the request currently has no example response |
| Collection Runner | `postman-cloud/runner.png` | Authentic API2 local run: 433 tests, 390 passed, 43 failed and 0 errors |
| Postman Monitor | `postman-cloud/monitor.png` | Completed cloud run at 13:44 on 2026-08-24; failure explicitly demonstrates that a cloud monitor cannot reach localhost |
| Data-driven Newman run | `newman-console/suite_ddt_20260824-145525.log` | Four CSV-fed collections, 27 iterations, 128 assertions, 0 failed; each line shows `[HW06] X-Student-Id=23127184` and the iteration's `tc_id` |

> **Two SUT states.** Every screenshot and log that shows a failing assertion
> was captured against the SUT **as delivered**, before commit `73ce207` fixed
> the 16 defects. The HTML/JSON reports in `reports/` are the **post-fix**
> regression run, where all 386 cases pass. Neither set was edited to agree
> with the other; they document two different points in time. The pre-fix
> transcripts are `newman-console/suite_full_20260823-223623.log` and
> `newman-console/suite_full_20260824-002523.log` (1,674/1,802 assertions).

Cloud URLs:

- Green CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32650162410>
- Red CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32649883960>
- Issues with attached evidence: [#7](https://github.com/KieuDuyennn/software__testing/issues/7),
  [#14](https://github.com/KieuDuyennn/software__testing/issues/14),
  [#38](https://github.com/KieuDuyennn/software__testing/issues/38), and
  [#66](https://github.com/KieuDuyennn/software__testing/issues/66) through
  [#70](https://github.com/KieuDuyennn/software__testing/issues/70)

## Still requires the student/device

- A successful Mock Server example response (the server and authentic call log
  exist, but the current call correctly reports that no example is attached).
- Failure screenshots attached to the corresponding GitHub Issues, if the
  marking rubric requires attachments rather than issue-page screenshots.
- Student authorship review of the editable generator diagram. The optional
  narrated demo video is still absent. The dated group uniqueness confirmation is recorded in `README.md` and
  the main report. The Mermaid source and PNG export exist at
  `docs/design/diagram/`.

Postman Desktop 12.24.6 and Desktop Agent 0.4.90 were installed on 2026-08-23.
The localhost SUT request was executed in Postman Desktop and captured without
fabrication. The Desktop lightweight client requires account sign-in before it
will enable collection import and Runner.
