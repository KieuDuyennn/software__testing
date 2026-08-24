# HW06 - Evidence completion status

Student ID: **23127184**

Only authentic captures and URLs qualify as evidence. Generated interface
images and invented links are excluded.

## Completed evidence

| Evidence | Location | Verification |
|---|---|---|
| Postman Console | `evidence/screenshots/postman-console-x-student-id.png` | Localhost request, HTTP 200, and `X-Student-Id=23127184` are visible |
| Postman workspace | `evidence/postman-cloud/workspace.png` | Four imported collections are visible |
| Postman environment | `evidence/postman-cloud/environment.png` | `EShop - Local (23127184)` is visible |
| Postman mock call log | `evidence/postman-cloud/mock-server.png` | Public API2 mock and authentic request log are visible; a successful example response is still pending |
| GitHub Issues | `evidence/screenshots/` | Signed-in issue pages #66 through #70 |
| GitHub Actions red run | `evidence/screenshots/github-actions-red-summary.png` | Run 32649883960 |
| GitHub Actions green run | `evidence/screenshots/github-actions-green-summary.png` | Run 32650090578 |
| Generator diagram draft | `docs/design/diagram/` | Mermaid source, SVG, and PNG with student ID |
| Collection Runner | `evidence/postman-cloud/runner.png` | API2 local run completed: 433 assertions, 390 passed, 43 failed, 0 errors |
| Monitor | `evidence/postman-cloud/monitor.png` | Authentic cloud run completed; Unhealthy because Postman Cloud cannot reach localhost |

The mock comparison uses product 2. The contract response should contain a
numeric `price`; the real SUT returns a string, as recorded in BUG-04.

## Remaining evidence

| Evidence | Required result | Target |
|---|---|---|
| Demo video (optional) | Narrated end-to-end generation, review, execution, and `X-Student-Id` proof | Real unlisted YouTube URL in README and main report |

The generator diagram is an editable draft. Before submission, the student
must review its labels and be able to explain its design decisions in the demo.

## Issue attachment check

Issue-page screenshots exist for #66 through #70. If the rubric requires an
image attachment inside each GitHub Issue, attach the matching Newman or
Postman failure image. A generic image cannot support unrelated defects.

## Final packaging checks

- Confirm the group uniqueness statement and date.
- Keep the self-assessed score supported by the completed artifacts.
- Add a real video URL only if submitting the optional demonstration.
- Name the ZIP with the final three-digit self-assessed score.
