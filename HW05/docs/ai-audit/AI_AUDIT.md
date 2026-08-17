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


## Interaction 05 — Plan and design

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date and time | 2026-08-17, Phase 2 session (Asia/Saigon) |
| Prompt context | Continue the confirmed HW05 workflow toward a 100/100-quality submission. |
| Output | Applied Little's Law to the measured 30.4 ms workflow and a disclosed 2.5 s compressed think time. Replaced inherited defaults with Load 34 VU, four-stage Stress to 132 VU, Spike 168 burst VU plus a 17 VU baseline, and Soak 27 VU; documented data recycling, metrics, listeners, reset/evidence gates and a human critique of the AI plan. |
| Human review required | Confirm the calculations and do not execute official runs until free RAM and same-frame video evidence are ready. |

## Interaction 06 — Plan generation and pilot review

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date and time | 2026-08-17, implementation/pilot session (Asia/Saigon) |
| Prompt context | Implement and verify the approved HW05 performance plan without fabricating official evidence. |
| Output | Generated the four official JMX plans dated 20260817 and corrected stale sizing comments. Reset/reseeded the backend, ran a 2 VU/30 s diagnostic pilot with JTL, HTML and resource sampling, then recomputed the raw JTL. Human review found that 23 successful controller rows represented only 22 endpoint-complete journeys because the scheduler stopped an iteration at the tail. The analyzer and skill documentation were corrected to require all five journey labels and expose tail/ambiguous rows. |
| Human review required | Treat the pilot only as implementation validation; record free RAM and same-frame video before official runs. |

## Interaction 07 — Uniqueness confirmation and official-run gate

| Field | Value |
|---|---|
| Tool | OpenAI Codex |
| Date and time | 2026-08-17, pre-execution review (Asia/Saigon) |
| Prompt | `mình xác nhận k trùng` |
| Output | Recorded the student's confirmation that Login → Search → Detail → Cart → Checkout is not duplicated. Rechecked the host and found only 0.36 GB free RAM, so official execution was withheld. Added a scenario-by-scenario checklist for reset, same-frame recording, genuine artifacts, invalid-run handling, analysis and submission gates. |
| Human review required | Close unnecessary applications, verify at least 2 GB free RAM, capture the hardware screenshot and start screen recording before authorising the first official Load run. |
