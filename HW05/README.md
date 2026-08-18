# HW05 - AI-assisted Performance Testing

Student ID: **23127184**  
SUT: **EShop REST backend**  
Workflow: **Login → Search → Product detail → Add to cart → Checkout**  
Uniqueness: confirmed by the student on 2026-08-17.  
Public repository: <https://github.com/KieuDuyennn/software__testing/tree/hw5/HW05>

## Test summary

| Scenario | Profile | Requests/s | Request p95 | Error rate | Complete journeys | Verdict |
|---|---|---:|---:|---:|---:|---|
| Load | 34 VU, 68 s ramp, 600 s stable | 64.16 overall | 10 ms | 0.00% | 8,547 | PASS |
| Stress | 33 → 66 → 99 → 132 VU | 260.6 at highest stable stage | 13 ms at highest stage | 0.00% | 18,775 | Valid; knee above tested range |
| Spike | 17 baseline + 168 burst | 361.6 burst | 26 ms burst | 0.00% | 5,591 | PASS; recovery ≤30 s |
| Soak | 27 VU, 900 s stable | 52.8-54.5 stable | ≤12 ms per full bucket | 0.00% | 9,934 | PASS |

Endpoint groups covered:

- Auth-heavy: `POST /api/login` with token extraction.
- Read-heavy: product search and product detail.
- Transactional: add to cart and checkout/order creation.

The demonstrated endurance threshold is at least **54.5 request/s (about 10.9
complete journeys/s) at 27 VU for 15 minutes**, with 0% errors and a measured
backend working-set ceiling of **172.0 MB**. No performance failure was observed.
One code-supported accumulation risk was found: successful checkout does not
clear the in-memory cart. This is documented as a risk, not falsely reported as
a proven leak or GitHub performance issue.

Observed bug/performance-issue count: **0**. Code-supported risks requiring a
longer confirmation test: **1** (cart state retained after checkout).

Demo video (unlisted, at least six minutes): **VIDEO_URL_PENDING**
Agent Skill demo: **VIDEO_URL_PENDING** (the same video may cover both requirements).

## Deliverables

- Main phase documents: `docs/phases/`
- Human reviews: `docs/reviews/`
- Official JMeter plans: `test-plans/`
- Data-driven CSV inputs: `data/`
- Raw JTL, HTML dashboards and resource logs: `results/`
- Hardware, reset and screenshot evidence: `evidence/`
- Reusable Agent Skills: `.claude/skills/`
- One-command Agent Skill demonstration: `demo.ps1`
- AI audit: `docs/ai-audit/AI_AUDIT.md`
- AI critique: `docs/AI_CRITIQUE.md`

## Self-assessment

| No. | Criterion | Maximum | Self-assessed |
|---:|---|---:|---:|
| 1 | Task 1 - Load testing | 20 | 20 |
| 2 | Task 1 - Stress testing | 20 | 20 |
| 3 | Task 1 - Spike testing | 20 | 20 |
| 4 | Task 2 - AI analysis and misinterpretation hunt | 10 | 10 |
| 5 | Task 3 - Continuous Performance Testing proposal | 10 | 10 |
| 6 | Agent Skills | 10 | 10 |
| | Listed rubric subtotal | 90 | 90 |

The listed rubric rows total 90 points although the published total row says
100. The submission filename therefore uses the listed-row subtotal `090`.
