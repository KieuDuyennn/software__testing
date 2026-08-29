# HW06 Authentic Evidence Index

Student ID: **23127184**  
Captured: **2026-08-23 to 2026-08-29**

Completed items below come from real signed-in GitHub/Postman sessions or are
clearly labelled renderings of verbatim fields retained in raw Newman JSON.
No placeholder or simulated application UI is included.

## Completed evidence

| Evidence | File | Verification visible in image |
|---|---|---|
| GitHub Actions green run | `screenshots/github-actions-green-summary.png` | Repository, branch `hw6`, commit `ff360cd`, run #15, Success, job `All 386 API test cases`, and the summary table reading 1,802 passed / 0 failed |
| GitHub Actions red run | `screenshots/github-actions-red-summary.png` | Repository, branch `hw6`, commit `27b76ae`, run #14, Failure, job `All 386 API test cases` |
| GitHub Actions red run, assertion table | `screenshots/github-actions-red-one-case.png` | The same run's job summary: `API2_FR06_ProductDetail` 432 passed / **1 failed** / 433, APIs 1, 3 and 4 at 0 failed, total 1,801 / 1 / 1,802 |
| GitHub Issue #7 | `screenshots/github-issue-7-malformed-email-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A1-DP-019`: request, `X-Student-Id: 23127184`, expected 4xx, actual 200 and failed assertion. Fixed in commit `73ce207`; the case passes in the current reports |
| GitHub Issue #14 | `screenshots/github-issue-14-admin-role-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A4-SEC-001`: request, student header, expected 401-403, actual 200 and failed assertion. Fixed in commit `73ce207` |
| GitHub Issue #38 | `screenshots/github-issue-38-terminal-transition-newman.png` | **Pre-fix SUT.** Raw Newman fields for `A4-ST-016`: request, student header, expected 4xx, actual 200 and failed assertion. Fixed in commit `73ce207` |
| GitHub Issue #66 | `screenshots/github-issue-66-plaintext-password.png` | Signed-in account, issue title/number, reproduction steps and `X-Student-Id: 23127184` |
| GitHub Issue #67 | `screenshots/github-issue-67-confirm-password.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #68 | `screenshots/github-issue-68-text-plain-http500.png` | Signed-in account, issue title/number, request and student header |
| GitHub Issue #69 | `screenshots/github-issue-69-html-stack-trace.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #70 | `screenshots/github-issue-70-product-write-auth.png` | Signed-in account, issue title/number and student header |
| GitHub Issue #26 | `screenshots/github-issue-26-cancel-shipping-order-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A3-ST-008`: the fixture chain, `PUT /api/orders/19/cancel`, `X-Student-Id: 23127184`, actual HTTP 200 and the failed assertion |
| GitHub Issue #33 | `screenshots/github-issue-33-deleted-account-token-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A3-DP-009`: the fixture chain including the account deletion, `GET /api/orders/my-orders`, actual HTTP 200 and the failed assertion |
| GitHub Issue #47 | `screenshots/github-issue-47-name-omitted-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-002` (name omitted): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #48 | `screenshots/github-issue-48-email-omitted-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-015` (email omitted): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #49 | `screenshots/github-issue-49-password-omitted-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-039` (password omitted): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #50 | `screenshots/github-issue-50-whitespace-name-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-005` (whitespace-only name): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #51 | `screenshots/github-issue-51-email-no-tld-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-022` (email without a TLD): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #52 | `screenshots/github-issue-52-email-case-uniqueness-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-034` (case-insensitive uniqueness): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #53 | `screenshots/github-issue-53-empty-name-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-004` (empty name): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #54 | `screenshots/github-issue-54-empty-email-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-017` (empty email): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #55 | `screenshots/github-issue-55-empty-password-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-041` (empty password): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #59 | `screenshots/github-issue-59-password-7-chars-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-042` (7-character password): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #60 | `screenshots/github-issue-60-password-no-uppercase-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-045` (password without uppercase): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #61 | `screenshots/github-issue-61-password-no-lowercase-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-046` (password without lowercase): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #62 | `screenshots/github-issue-62-password-no-digit-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-047` (password without a digit): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #63 | `screenshots/github-issue-63-password-no-special-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-048` (password without a special character): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| GitHub Issue #64 | `screenshots/github-issue-64-duplicate-email-newman.png` | **Pre-fix SUT.** Verbatim console fields for `A1-DP-033` (exact duplicate email): request, `X-Student-Id: 23127184`, expected 4xx, actual HTTP 200 and the failed assertion. Rendered by `scripts/build-issue-evidence.py` from the retained transcript |
| Postman Cloud workspace | `postman-cloud/workspace.png` | Signed-in workspace and all four imported HW06 collections |
| Postman environment | `postman-cloud/environment.png` | Imported `EShop - Local (23127184)` environment |
| Real Postman Console run | `screenshots/postman-console-x-student-id.png` | Postman Desktop, localhost URL, HTTP 200 and `[HW06] X-Student-Id=23127184` |
| Postman Mock Server | `postman-cloud/mock-server.png` | Public API2 mock is Running and records `GET /api/products/2`; the request currently has no example response |
| Collection Runner | `postman-cloud/runner.png` | Authentic API2 local run: 433 tests, 390 passed, 43 failed and 0 errors |
| Postman Monitor | `postman-cloud/monitor.png` | Completed cloud run at 13:44 on 2026-08-24; failure explicitly demonstrates that a cloud monitor cannot reach localhost |
| Data-driven Newman run | `newman-console/suite_ddt_20260824-154226.log` | Four CSV-fed collections, 27 iterations, 128 assertions, 0 failed; each line shows `[HW06] X-Student-Id=23127184` and the iteration's `tc_id` |

> **Two SUT states.** Every screenshot and log that shows a failing assertion
> was captured against the SUT **as delivered**, before commit `73ce207` fixed
> the 16 defects. The HTML/JSON reports in `reports/` are the **post-fix**
> regression run, where all 386 cases pass. Neither set was edited to agree
> with the other; they document two different points in time. The pre-fix
> transcripts are `newman-console/suite_full_20260823-223623.log` and
> `newman-console/suite_full_20260824-002523.log` (1,674/1,802 assertions).

Cloud URLs:

- Green CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32700710575>
  (commit `ff360cd`, Success, 1,802/1,802 assertions)
- Red CI: <https://github.com/KieuDuyennn/software__testing/actions/runs/32700593817>
  (commit `27b76ae`, Failure, 1,801/1,802 assertions, only `A2-DP-009` failing)
- Issues carrying evidence: #7, #8, #9, #13, #14, #26, #33, #38, #47-#55,
  #59-#64 and #66-#70, at
  <https://github.com/KieuDuyennn/software__testing/issues>

## Still requires the student/device

- A successful Mock Server example response (the server and authentic call log
  exist, but the current call correctly reports that no example is attached).
- Student authorship review of the editable generator diagram. The optional
  narrated demo video is still absent. The dated group uniqueness confirmation is recorded in `README.md` and
  the main report. The Mermaid source and PNG export exist at
  `docs/design/diagram/`.

Postman Desktop 12.24.6 and Desktop Agent 0.4.90 were installed on 2026-08-23.
The localhost SUT request was executed in Postman Desktop and captured without
fabrication. The Desktop lightweight client requires account sign-in before it
will enable collection import and Runner.
