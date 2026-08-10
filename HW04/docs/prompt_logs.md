# AI interaction log — HW04

Appendix to `docs/03_AI_Audit_Report.md`.

| # | Date & time (UTC+7) | Tool | Prompt summary | AI output (factual summary) | Human review outcome | Evidence |
|---|---|---|---|---|---|---|
| 1 | 2026-08-06 23:14:51–23:14:53 | Claude Code — Claude Opus 5 | Read the brief and scaffold Playwright + TypeScript for FR-01, FR-11 and FR-13. | Created the initial project structure, environment template and Playwright configuration. | Historical baseline retained. | Initial project commits |
| 2 | 2026-08-06 23:14:53–23:14:59 | Claude Code — Claude Opus 5 | Add utilities, fixtures, page objects, external data, matrices and audit logging. | Created the initial automation architecture and feature artifacts. | Historical baseline retained. | Initial automation commits |
| 3 | 2026-08-06 23:15:00–23:15:01 | Claude Code — Claude Opus 5 | Create reusable Playwright and audit-log skills with human approval gates. | Added the initial Agent Skills and README. | Historical baseline retained. | Skill commits |
| 4 | 2026-08-09 18:19:03–18:19:22 | Claude Code | Verify setup against the real SUT and correct proven configuration errors. | Separated customer UI `:5173`, admin UI `:5174` and API `:3000`. | Historical baseline retained. | Environment/configuration review |
| 5 | 2026-08-09 18:35:33–18:36:15 | Claude Code | Revise the Playwright skill using concrete setup failures. | Added source inspection, selector probes, case classification and staged approvals. | Historical baseline retained. | Skill review |
| 6 | 2026-08-09 18:36:02 | Claude Code | Harden the audit skill against invented timestamps and altered prompts. | Added observed-time and original-language rules. | Historical baseline retained. | Audit-skill review |

Prompt entries from the current FR13 session were removed at the student's request.
