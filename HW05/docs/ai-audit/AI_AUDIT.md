# AI Audit Report

**Assignment:** HW05 - AI-assisted Performance Testing  
**Student ID:** 23127184  
**System under test:** EShop REST backend  
**AI tool:** OpenAI Codex  
**Audit period:** 2026-08-16 to 2026-08-18 (Asia/Saigon)

## 1. Declaration

I used OpenAI Codex as an engineering assistant to review the assignment,
improve reusable Agent Skills, design JMeter scenarios, automate repeatable test
execution, analyse raw JTL data, challenge initial interpretations, and prepare
reviewable documentation. I remained responsible for the final test design,
criteria, interpretation and submission.

The performance measurements in this assignment were not invented by AI. They
were produced by the local EShop backend, Apache JMeter and the Windows resource
monitor on host `KIEUDUYEN`. Raw JTL files, resource samples, screenshots,
JMeter logs and HTML reports are retained in the repository so that every
material claim can be checked independently.

## 2. Prompt and evidence policy

The prompts below document the task instructions used in the working sessions.
Where one activity required several follow-up messages, the instructions are
consolidated into one interaction record so the technical objective, constraints
and expected deliverables remain readable. The Codex conversation history is
the supporting source for the complete message sequence.

AI output is summarized rather than copied as an entire transcript. Each
summary is tied to a file, raw result directory or Git commit. Where AI made an
incorrect or overconfident claim, the correction is recorded explicitly instead
of silently replacing the original interpretation.

## 3. Interaction register

| ID | Date | Purpose | Main verified outcome |
|---:|---|---|---|
| 01 | 2026-08-16 | Requirements and Agent Skill review | Evidence, portability and analysis gaps identified |
| 02 | 2026-08-16 | Agent Skill hardening | Reusable five-skill workflow validated and committed |
| 03 | 2026-08-17 | Environment, baseline and criteria | Real host baseline and pre-registered thresholds recorded |
| 04 | 2026-08-17 | Scenario planning | Measured Load, Stress, Spike and Soak profiles designed |
| 05 | 2026-08-17 | JMX implementation and pilot | Four portable plans generated; partial-journey bug found |
| 06 | 2026-08-17 | Official execution | Four complete genuine result sets retained |
| 07 | 2026-08-17 to 2026-08-18 | Raw analysis and critique | AI misinterpretations corrected from JTL and source code |
| 08 | 2026-08-18 | Continuous testing and reporting | Main report, critique, flow chart and PDFs produced |
| 09 | 2026-08-18 | Submission audit and AI Audit rewrite | Public branch and machine-checkable deliverables verified |

## 4. Detailed interaction log

### Interaction 01 - Review the requirements and existing Agent Skills

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-16 (Asia/Saigon) |
| Objective | Establish a rubric-traceable workflow before changing or running anything |
| Primary inputs | `refs/requirements/ver2.md`, course guidance, `.claude/skills/` |

#### Prompt

> Read the complete HW05 specification and inspect every performance-testing
> Agent Skill, reference, script and asset already present in the repository.
> Map the seven taught performance-testing steps and every rubric requirement to
> concrete artifacts. Identify missing evidence gates, unsafe assumptions,
> portability problems and analysis errors. Do not execute an official test or
> fabricate any screenshot, log, timestamp or measured value. Return a
> prioritized correction list with the files that should change.

#### Condensed AI output and actions

- Mapped environment, criteria, planning, implementation, execution and
  analysis responsibilities across the reusable skills.
- Identified an unsuitable linear Stress shape, machine-specific CSV paths,
  ambiguous Node-process selection and incomplete resource/evidence gates.
- Found that the analyzer could mishandle final partial time buckets and could
  trust Transaction Controller rows too readily.
- Recommended a dedicated HW05 evidence contract to separate genuine execution
  evidence from AI-generated documentation.

#### Human verification and decision

The findings were accepted only where they matched the official brief and the
repository. No official result was claimed at this stage. The review became the
input for Interaction 02.

**Trace:** `.claude/skills/performance-testing/`, commit `e385ad7`.

### Interaction 02 - Harden and validate the reusable Agent Skills

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-16 (Asia/Saigon) |
| Objective | Make the skills safe, reusable and capable of producing auditable HW05 artifacts |
| Primary inputs | Findings from Interaction 01 and the existing skill scripts/assets |

#### Prompt

> Implement the approved corrections in the performance-testing Agent Skills.
> Use a four-stage accumulating Stress profile, a portable runtime `data.dir`,
> live CSV validation, explicit backend-PID monitoring and safe monitor cleanup.
> Correct tail-bucket throughput calculations and make memory warnings cautious
> rather than calling growth a leak. Add an HW05 evidence contract that forbids
> fabricated evidence. Validate all skill files and scripts, perform only a
> technical smoke check where appropriate, and commit the scoped changes with a
> Conventional Commit message and no co-author trailer.

#### Condensed AI output and actions

- Implemented the four-stage Stress design and portable JMeter data path.
- Added CSV preflight checks and mandatory explicit backend PID selection.
- Hardened resource-monitor cleanup and final-bucket duration handling.
- Added cautious memory interpretation and the HW05 evidence contract.
- Validated the five skills and supporting scripts, then created commit
  `e385ad7 feat(hw05): harden performance testing skills`.

#### Human verification and decision

The student reviewed the commit scope and required a normal Conventional Commit
without `Co-authored-by`. Unrelated worktree content was excluded.

**Trace:** `.claude/skills/`, `evidence/git-commit-log.txt`.

### Interaction 03 - Establish the environment, baseline and criteria

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-17 (Asia/Saigon) |
| Objective | Measure the actual local system before selecting load levels |
| Primary inputs | Student ID `23127184`; confirmed unique purchase workflow; local EShop SUT |

#### Prompt

> Begin HW05 for student 23127184 using the confirmed non-duplicated workflow:
> Login -> Search product -> Product detail -> Add to cart -> Checkout. Inventory
> the real host and tool versions, document the co-located load-generator
> limitation, start a fresh backend with `LOADTEST=1`, create deterministic test
> data through the live API, validate every CSV row, and measure a repeatable
> single-user baseline. Propose label-specific p95, error and journey-completion
> criteria before any official run. Clearly separate measured facts from sizing
> assumptions and preserve the commands and evidence paths.

#### Condensed AI output and actions

- Recorded hostname `KIEUDUYEN`, CPU, RAM, Windows, Java, JMeter and Node.js
  versions.
- Started a fresh local backend, created and validated 240 data rows in each CSV
  pool and measured seven single-user samples per endpoint.
- Calculated a 30.4 ms workflow service baseline and documented the co-located
  generator constraint.
- Pre-registered p95 limits of 250 ms for login, 200 ms for reads, 300 ms for
  cart/checkout and 1,000 ms for the complete journey, with error rate below 1%.

#### Human verification and decision

The thresholds were reviewed before the official results were known. The
student confirmed that the selected workflow did not duplicate another group
member's work. Hardware screenshots and same-frame execution evidence remained
mandatory human-attribution items.

**Trace:** `docs/phases/01_environment.md`, `docs/phases/02_criteria.md`,
`evidence/baseline/`, commit `c18293b`.

### Interaction 04 - Plan realistic Load, Stress, Spike and Soak scenarios

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-17 (Asia/Saigon) |
| Objective | Convert the measured baseline into defensible scenario profiles |
| Primary inputs | Baseline, fixed criteria, 240-row CSV pools, 8 GB co-located host |

#### Prompt

> Design Load, Stress, Spike and 10-15 minute Soak scenarios for the confirmed
> five-step workflow. Derive concurrency from the measured service time and a
> disclosed compressed think time instead of choosing round numbers. For each
> scenario, specify VU shape, ramp, stable duration, expected arrival rate,
> question answered, pass/fail criteria and required evidence. Assign three
> different listener types across Load, Stress and Spike. Explain data recycling,
> account-lockout handling, reset requirements and the limitations of running
> JMeter beside the backend. Include a separate human review of what the initial
> AI defaults got wrong and why.

#### Condensed AI output and actions

- Derived Load at 34 VU, Stress stages at 33/66/99/132 VU, Spike at 17 baseline
  plus 168 burst VU, and Soak at 27 VU.
- Used 300-700 ms uniform think time and explicitly described it as a compressed
  arrival-rate model rather than literal browsing behavior.
- Assigned Summary Report, Aggregate Report and error-only View Results Tree to
  the three required scenarios.
- Documented reset, resource, screenshot, raw-log and invalid-run gates.

#### Human verification and decision

The review rejected inherited 50/200/200/40-VU defaults, a linear Stress ramp,
machine-specific paths, weak status-only assertions and process-name-only
monitoring. The reviewed design was accepted for implementation.

**Trace:** `docs/phases/03_plan.md`, `docs/reviews/01_ai_plan_review.md`, commit
`8087833`.

### Interaction 05 - Generate the JMX plans and review a diagnostic pilot

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-17 (Asia/Saigon) |
| Objective | Verify correlation, assertions, data and evidence tooling before official execution |
| Primary inputs | Approved profiles, JMX assets, CSV data and runner scripts |

#### Prompt

> Generate four portable JMeter plans named with student ID 23127184, scenario
> type and date 20260817. Implement JWT extraction, dynamic product correlation,
> data-driven request bodies and content assertions for token, product ID and
> order ID. Validate the XML and CSV references. Then run a short 2-VU/30-second
> diagnostic pilot only, preserving its JTL, HTML report, JMeter log, run record
> and backend resource samples. Analyse the pilot from raw CSV-form JTL, compare
> controller rows with all five endpoint-label counts, document every correction
> and do not present pilot numbers as official results.

#### Condensed AI output and actions

- Generated Load, Stress, Spike and Soak JMX files with portable data paths and
  the approved workflow/assertions.
- Completed a diagnostic pilot with 117 request samples, 0% errors and 17 ms
  request p95.
- Initially observed 23 successful controller rows, then found only 22 journeys
  containing all five endpoint labels because the scheduler ended a tail
  iteration.
- Corrected the analyzer to report endpoint-complete journeys and expose
  tail/ambiguous controller rows.

#### Human verification and decision

The pilot was classified only as implementation validation. The human review
rejected the misleading statement "23/23 transactions passed" and adopted the
conservative 22 complete-journey count for all later analyses.

**Trace:** `test-plans/`, `evidence/pilot-runs/`,
`docs/reviews/02_pilot_review.md`, commit `8087833`.

### Interaction 06 - Execute and preserve the official scenarios

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-17 (Asia/Saigon) |
| Objective | Produce genuine, attributable and reproducible execution evidence |
| Primary inputs | Four reviewed JMX plans and the official execution checklist |

#### Prompt

> Execute the reviewed scenarios in order: Load, reset, Stress, reset, Spike,
> reset, then Soak. Before every run, start a fresh backend with `LOADTEST=1`,
> record its PID, regenerate and validate all 240-row CSV files, verify the API,
> confirm safe free memory and monitor only that backend PID. Preserve the full
> timestamped `result.jtl`, HTML report, `resources.csv`, `jmeter.log` and
> `run.md`. Capture genuine same-frame JMeter and Task Manager screenshots. Stop
> and retain a run as invalid if preflight, monitoring or evidence capture fails.
> Never edit raw results or infer evidence that was not captured.

#### Condensed AI output and actions

- Completed and retained four official result sets for Load, Stress, Spike and
  Soak.
- Preserved 42,810 / 94,104 / 28,325 / 49,727 request samples respectively,
  with 0% request/assertion errors.
- Captured real backend CPU/memory logs, hardware identity and same-frame
  screenshots.
- Committed official plans and evidence in
  `98462cf test(hw05): capture official performance results`.

#### Human verification and decision

Raw evidence was retained unedited. The student remained responsible for the
required Vietnamese narration and YouTube upload; AI did not generate or claim
that evidence.

**Trace:** `results/`, `evidence/screenshots/`, `evidence/reset-records/`, commit
`98462cf`.

### Interaction 07 - Analyse raw JTL data and hunt AI misinterpretations

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-17 to 2026-08-18 (Asia/Saigon) |
| Objective | Recompute ground truth and challenge AI-generated conclusions |
| Primary inputs | Four raw JTL files, four resource logs, fixed criteria and relevant backend code |

#### Prompt

> Analyse every official raw JTL as proper CSV. Separate request samples from
> Transaction Controller rows; calculate count, throughput, mean, p50, p90,
> p95, p99, max, bandwidth, errors, per-label values, 30-second phases and
> endpoint-complete journeys. Identify the Stress knee only if throughput stops
> scaling while latency or errors rise. Compare Spike baseline, burst and
> recovery separately. Treat Soak memory as a trend, not automatic proof of a
> leak. Then review the AI analysis line by line, cite corrected raw values and
> classify each optimization as supported, plausible but unverified, or
> unfounded after checking the source code.

#### Condensed AI output and actions

- Recomputed overall request p95 values of 10/11/19/11 ms for
  Load/Stress/Spike/Soak and 0% errors in every run.
- Corrected controller overcounts: 8,557/18,797/5,622/9,939 controller rows
  versus 8,547/18,775/5,591/9,934 endpoint-complete journeys.
- Found no Stress knee through 132 VU; the highest stable stage reached about
  260.6 request/s at 13 ms p95 with 0% errors.
- Measured Spike burst at 361.6 request/s and 26 ms p95, with recovery to 12 ms
  in the first full recovery bucket.
- Demonstrated a Soak threshold of at least 54.5 request/s at 27 VU with a
  172.0 MB memory ceiling, while rejecting an unsupported leak conclusion.
- Classified cart clearing as supported, email indexing and SQLite WAL as
  plausible but unverified, and a generic connection pool plus a normal B-tree
  index for `LIKE '%keyword%'` as unfounded for this code path.

#### Human verification and decision

The reviewed report uses the conservative endpoint-complete journey count and
does not claim that 132 VU is capacity or that memory growth proves a leak. Every
material correction is linked to raw data or source behavior.

**Trace:** `docs/analysis/`, `docs/reviews/03_ai_analysis_review.md`,
`docs/phases/04_analysis.md`, commit `7327273`.

### Interaction 08 - Propose continuous testing and build the reports

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-18 (Asia/Saigon) |
| Objective | Convert the reviewed evidence into complete submission documents |
| Primary inputs | Reviewed analysis, official rubric, AI Critique requirement and result evidence |

#### Prompt

> Draft the final HW05 report from reviewed evidence only. Include environment,
> fixed criteria, AI-assisted design corrections, scenario results, endurance
> threshold, limitations, AI misinterpretation hunt and optimization judgement.
> Propose a commit-aware continuous-performance pipeline with risky-path
> filtering, a short Load gate, a confirmation run, label-specific p95
> comparison, scheduled Stress/Spike and release-candidate Soak. Discuss cost,
> false positives and false negatives, and include a flow chart. Write a
> 200-300-word AI Critique, update the AI Audit, render the main report and Audit
> as polished PDFs, and visually inspect every page for clipping, blank pages and
> unreadable tables.

#### Condensed AI output and actions

- Produced the main Markdown report, continuous-performance proposal and flow
  chart, plus a 272-word AI Critique.
- Built an eight-page performance report PDF and the then-current three-page AI
  Audit PDF, which Interaction 09 later replaced with the expanded final Audit.
- Detected and fixed a blank trailing Audit page and a clipped Interaction
  heading during visual QA.
- Added a Vietnamese video guide, submission checklist and a fail-closed
  packaging script that refuses to create a final ZIP without a real YouTube
  URL.

#### Human verification and decision

The student must still read the AI Critique in their own voice and record/upload
the genuine narrated video. The packaging guard intentionally leaves
`VIDEO_URL_PENDING` until that evidence exists.

**Trace:** `23127184_HW05_REPORT.md`, `docs/AI_CRITIQUE.md`,
`docs/phases/05_continuous_performance.md`, `output/pdf/`, commits `3770903` and
`b9229a1`.

### Interaction 09 - Audit submission readiness and rewrite this AI Audit

| Field | Record |
|---|---|
| Tool | OpenAI Codex |
| Date | 2026-08-18 (Asia/Saigon) |
| Objective | Make the final audit readable, complete and defensible without altering measured evidence |
| Primary inputs | Official brief, all review files, Git history, final PDFs and public branch |

#### Prompt

> Audit the current HW05 repository against the official submission checklist.
> Verify JMX validity, distinct listeners, 240-row CSV inputs, raw JTL/resource
> counts, HTML report presence, PDF rendering, Git history and public branch
> visibility. Then replace the existing AI Audit completely with a professional
> report. Rewrite the working prompts so they are clear, specific and technically
> correct. Preserve the true chronology, AI mistakes, human corrections,
> artifact paths and commit traceability. Do not fabricate the missing video,
> student narration, issue report or any measured result.

#### Condensed AI output and actions

- Verified all four JMX files as valid XML and confirmed the required distinct
  listeners across Load, Stress and Spike.
- Confirmed three 240-row CSV pools, four raw JTL/HTML/resource result sets and
  recomputed 0% error with p95 values matching the reviewed report.
- Verified public branch `hw5` and synchronized local/remote commit state.
- Replaced the former short-form Audit with this structured interaction log and
  linked every material result to its evidence or commit.

#### Human verification required

Before submission, the student must read this rewritten Audit and confirm that
the prompts preserve the actual intent of the working sessions.
The student must also provide the genuine video URL and remain able to explain
the raw-result corrections during a possible oral defence.

**Trace:** `docs/SUBMISSION_STATUS.md`, `scripts/package-submission.ps1`, public
branch `hw5`.

## 5. Known limitations and student sign-off

- This document consolidates multi-turn working sessions into traceable
  interaction records. The original Codex conversation should also be exported
  or screenshotted if the instructor requires the complete message sequence.
- The Load generator and backend shared one 8 GB laptop, so the demonstrated
  throughput is specific to this test environment and is not production
  capacity.
- The rate limiter was deliberately bypassed with `LOADTEST=1`; the runs measure
  application performance under that disclosed configuration.
- No genuine performance failure occurred, so no GitHub performance issue was
  fabricated.
- AI cannot supply the student's narration or claim that the student personally
  reviewed prose. Those are explicit final human actions.

### Student confirmation before submission

- [ ] I confirm that the prompts preserve the intent of my actual requests.
- [ ] I checked the material values against the raw JTL files and reviewed
  analysis.
- [ ] I reviewed the AI Critique and can explain the corrections in my own
  words.
- [ ] I recorded and uploaded the required unlisted video with my own Vietnamese
  narration.
- [ ] I opened the final ZIP and verified the report, Audit, plans, raw results,
  evidence, Git log and video link.
