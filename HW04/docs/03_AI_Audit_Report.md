# AI Audit Report — HW04 (Mandatory Appendix, §9)

**Student:** Lê Phạm Kiều Duyên · **Student ID:** 23127184
**Assignment:** HW04-AI — Automation Testing

## Declaration

> I use AI tools to interpret the HW04 requirements, scaffold the
> Playwright/TypeScript project, generate initial automation artifacts, create reusable
> Agent Skills, and revise those outputs under human review. I remain responsible for
> the final configuration, skills and test suite.

## Tools declared (§8)

| Tool | Version / model | Used for |
|---|---|---|
| Claude Code | Claude Opus 5 (attribution in HW04 commit trailers) | Initial setup, automation scaffolds, documentation and first versions of both Agent Skills |
| OpenAI Codex | Model/version not exposed in the recorded session | FR-01 requirement/data-driven review, live SUT execution, evidence reconciliation and reader testing |
| Playwright | `@playwright/test ^1.50.0` | Browser automation, discovery and HTML/JSON reports; an execution tool, not an AI model |

## Curated interaction log

Rows 1–7 are normalised summaries of mixed Vietnamese/English interactions because the
original verbatim transcripts are not available in the repository. They are labelled as
summaries rather than reconstructed quotations. Row 8 was recorded during the active
session and preserves the student's prompt verbatim.

| # | Date & time (UTC+7) | Tool | Prompt summary | AI output | Human review outcome |
|---|---|---|---|---|---|
| 1 | 2026-08-06 23:14:51–23:14:53 | Claude Code — Claude Opus 5 | Scaffold HW04 with Playwright, TypeScript, safe environment config, three browsers and attributable reports. | Created base configuration and project rules in seven focused commits. | The student checked the structure against the brief. Runtime URLs remained provisional and were later rejected after SUT verification. |
| 2 | 2026-08-06 23:14:53–23:14:59 | Claude Code — Claude Opus 5 | Add utilities, fixtures, page objects, data-driven specs, runner, matrices and an AI-correction log. | Created the initial automation architecture and per-feature artifacts. | The student distinguished architecture from execution evidence: files and a `--list` dry run were not reported as successful E2E runs. Source/DOM review later led to targeted corrections, not wholesale regeneration. |
| 3 | 2026-08-06 23:15:00–23:15:01 | Claude Code — Claude Opus 5 | Create reusable Playwright and audit-log skills with human approval gates. | Added two Agent Skills and their README. | Accepted only as version 1; usefulness was evaluated against the real FR-01 setup before revision. |
| 4 | 2026-08-09 18:19:03–18:19:22 | Claude Code | Verify setup against the real SUT and correct proven configuration errors. | Separated customer UI `:5173`, admin UI `:5174` and API `:3000`; corrected Playwright navigation URL. | The student caught a high-impact setup error: generated browser config targeted the API. The correction was grounded in SUT config/runtime and documented beside the setting. |
| 5 | 2026-08-09 18:35:33–18:36:15 | Claude Code | Revise the Playwright skill using concrete FR-01 setup failures. | Added environment proof, source inspection, selector probes, case reclassification, diagnostic cases, staged approvals and pitfalls. | The student rejected generic/wrongly ordered guidance. Selector checks now precede data generation; source/DOM override stale assumptions; every major stage stops for approval. |
| 6 | 2026-08-09 18:36:02 | Claude Code | Harden the audit skill against invented timestamps and altered multilingual prompts. | Added observed-time, no-backfill and original-language rules. | The student required accurate timestamps and preservation of the prompt's original language. |
| 7 | 2026-08-10 | OpenAI Codex | Review whether FR-01 matched the requirement and was genuinely data-driven; run the SUT, extend server-layer coverage, and publish issue evidence. | Audited traceability, expanded the CSV from 31 to 43 cases with 12 API validation rows, and ran Chromium, Firefox and WebKit. | The student authorised live SUT execution and GitHub issue creation. All engines produced 17 passed / 26 failed / 0 skipped; 23 confirmed findings and 3 requirement questions were filed as issues #39–#64 without weakening assertions. |
| 8 | 2026-08-11 00:28:34 | OpenAI Codex | “quy định 4 ngày git đã được bỏ, fix các phần còn lại cho mình. video demo mình sẽ up link sau” | Re-audited the submission against the revised rule, completed the mandatory critique and report fields, updated paths and checklists, exported the actual Git log, and generated the required PDFs. | The student explicitly supplied the changed Git rule and retained responsibility for uploading the two YouTube links. No video evidence or URL was invented. |
## Human review evidence — HW04 setup

The setup review checked the AI output against the brief, SUT configuration and
observable runtime structure; it was not a formatting pass.

| Checkpoint | AI baseline | Human finding and decision | Evidence |
|---|---|---|---|
| Secrets and artifacts | Generated environment and report structure. | Kept `.env`/auth state out of Git, retained only a credential-free template, and did not treat placeholder report folders as results. | `c8111c7`, `0b92d33`, `7986880`–`80ab93b` |
| Navigation URL | Default `baseURL` was `http://localhost:3000`. | Rejected after checking the SUT: `:3000` is API, customer UI is `:5173`, admin UI is `:5174`. Updated config and rationale. | `ea52e13`; reviewed 2026-08-09 diff in `.env.example` and `playwright.config.ts` |
| Brief conformance | Three projects and HTML/JSON reporters existed. | Verified external data, three assertion helpers, 3 × 3 runner and student identity in report metadata/title/test annotations. | `d01b283`, `ea52e13`, `e26c32a`–`f06b8a5` |
| Evidence integrity | Chromium `--list` JSON/HTML existed. | Classified it only as discovery/scaffold evidence; inferred no pass/fail or nine-run completion. | `9262daf`, `0102467` |
| Correction scope | Initial page objects/matrices existed. | Applied focused corrections after source/DOM inspection and preserved the diff for review. | Current `RegisterPage.ts` and `TC_Matrix_FR01/11/13.md` diffs |

## Human review evidence — Agent Skills

The committed initial skills provide a visible baseline. The student exercised the
workflow, identified concrete weaknesses and refined it from observed failure modes.

| Review area | Initial limitation | Human-directed refinement | Significance |
|---|---|---|---|
| Environment | Workflow assumed the SUT was ready. | Added Step 0 for processes, dependencies, engines and actual ports. | Prevents config failures being misread as test failures. |
| Grounding | Skill read FR/design documents only. | Required implementing source and treated running SUT as fact. | Exposed stale “no UI” assumptions and validation contradictions. |
| Selectors | “Verify selectors” came after data creation. | Moved it earlier; required count probes, rejected alternatives and absence checks. | Makes selection repeatable and avoids cases for nonexistent fields. |
| Approval | Only the final pre-run gate was prominent. | Required stops after behaviours, cases, locators, data and spec. | Preserves human decisions throughout, not one final rubber stamp. |
| Audit | Missing-history handling was underspecified. | Added observed timestamps, no backfill and original-language prompts. | Prevents the audit itself from overstating evidence. |

## Git traceability and limitations

- Setup baseline: `c8111c7` through `005ef91`.
- Automation baseline/review surfaces: `e26c32a` through `7e4cf80`.
- Skill baseline: `a11d1c0`, `71c8a2a`, `25cfd6c`.
- Dry-run evidence only: `9262daf`, `0102467`.
- Human corrections dated 2026-08-09 were preserved in focused commits and remain
  visible in the repository history.
- All nine feature/browser combinations have attributable report evidence under
  `reports/final/`. FR-13 Firefox and WebKit are preserved as three case-group reports
  (`tc`, `bva`, `api`) per browser rather than falsely merged by hand.
