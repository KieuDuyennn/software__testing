# AI Audit Report

## Declaration

I use AI tools for the following tasks: reviewing the HW05 requirements,
designing and validating reusable performance-testing skills, preparing the test
environment, generating deterministic test data, measuring the baseline, and
drafting reviewable Markdown artifacts. All execution evidence and measured
values are produced by the real local SUT and tools and are subject to human
review.

## Interaction 01 — Skill review

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-16 (Asia/Saigon) |
| Prompt | `đọc yêu cầu HW05 và xem skills mình xây đã chuẩn chưa để bắt đầu làm các bước tiếp theo` |
| Output | Reviewed the official requirements, course slide, five skills, scripts and JMeter assets; identified Stress-shape, portability, analyzer, PID-selection and evidence-coverage gaps. |
| Human review | Accepted the valid findings and requested fixes before execution. |

## Interaction 02 — Skill hardening

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-16 (Asia/Saigon) |
| Prompt | `oce sửa để 10/10` |
| Output | Implemented a four-stage Stress staircase, portable `data.dir`, CSV preflight validation, explicit backend PID selection, safer resource-job cleanup, corrected JTL tail-bucket logic, cautious memory interpretation and an HW05 evidence contract. All five skills passed validation and a JMeter smoke test. |
| Human review | The student requested a conventional Git commit without co-author attribution. |

## Interaction 03 — Skill commit

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-16 (Asia/Saigon) |
| Prompt | `commit cho mình theo conventional, k có co author` |
| Output | Created commit `e385ad7 feat(hw05): harden performance testing skills`; verified no `Co-authored-by` trailer and excluded unrelated untracked files. |
| Human review | Commit scope and message were accepted. |

## Interaction 04 — Begin HW05 execution

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date and time | 2026-08-17, Phase 1 session (Asia/Saigon) |
| Prompts | `mssv cuar mình là 23127184, hãy làm thật chuẩn cho mình để được 100/100 nha` and `mình xác nhận k trùng` |
| Output | Confirmed Student ID `23127184` and the unique Login → Search → Detail → Cart → Checkout workflow. Inventoried real hardware/tools, started EShop with `LOADTEST=1`, recorded backend PID 16028, seeded and validated 240 API-created test accounts/CSV rows, measured seven single-user samples per endpoint, verified resource monitoring, and created Phase 1 environment/criteria artifacts. |
| Human review required | Verify all thresholds, capture dxdiag/Task Manager screenshots, and retain only genuine run/video evidence. |

## Audit limitation

This Markdown log records the prompts and material outputs/actions. Export or
screenshot the original Codex conversation too if the instructor requires every
assistant message verbatim rather than an attributable audit summary.

