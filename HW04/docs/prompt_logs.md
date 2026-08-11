# AI interaction log — HW04

Appendix to `docs/03_AI_Audit_Report.md`.

| # | Date & time (UTC+7)           | Tool                         | Prompt summary                                                                    | AI output (factual summary)                                                               | Human review outcome          | Evidence                         |
| - | ----------------------------- | ---------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- | ----------------------------- | -------------------------------- |
| 1 | 2026-08-06 23:14:51–23:14:53 | Claude Code — Claude Opus 5 | Read the brief and scaffold Playwright + TypeScript for FR-01, FR-11 and FR-13.   | Created the initial project structure, environment template and Playwright configuration. | Historical baseline retained. | Initial project commits          |
| 2 | 2026-08-06 23:14:53–23:14:59 | Claude Code — Claude Opus 5 | Add utilities, fixtures, page objects, external data, matrices and audit logging. | Created the initial automation architecture and feature artifacts.                        | Historical baseline retained. | Initial automation commits       |
| 3 | 2026-08-06 23:15:00–23:15:01 | Claude Code — Claude Opus 5 | Create reusable Playwright and audit-log skills with human approval gates.        | Added the initial Agent Skills and README.                                                | Historical baseline retained. | Skill commits                    |
| 4 | 2026-08-09 18:19:03–18:19:22 | Claude Code                  | Verify setup against the real SUT and correct proven configuration errors.        | Separated customer UI`:5173`, admin UI `:5174` and API `:3000`.                     | Historical baseline retained. | Environment/configuration review |
| 5 | 2026-08-09 18:35:33–18:36:15 | Claude Code                  | Revise the Playwright skill using concrete setup failures.                        | Added source inspection, selector probes, case classification and staged approvals.       | Historical baseline retained. | Skill review                     |
| 6 | 2026-08-09 18:36:02           | Claude Code                  | Harden the audit skill against invented timestamps and altered prompts.           | Added observed-time and original-language rules.                                          | Historical baseline retained. | Audit-skill review               |
| 7 | 2026-08-11 00:28:34          | OpenAI Codex                 | `quy định 4 ngày git đã được bỏ, fix các phần còn lại cho mình. video demo mình sẽ up link sau` | Completed the reports, removed the obsolete Git threshold, exported and visually checked the mandatory PDFs, and committed the result. | Accepted; video URL intentionally left pending. | Commit `b33a5f1` and `output/pdf/` |
| 8 | 2026-08-11 00:39:08          | OpenAI Codex                 | `điểm tự đánh giá hãy đánh giá full cho mình` | Updated every self-assessment criterion to full marks and fixed the intended ZIP grade at 100. | Accepted as the student's requested self-assessment; video evidence remains pending. | Current README change |
| 9 | 2026-08-11 10:02:48          | Claude Code                  | `https://youtu.be/krqH7ua7CNA đây là link video demo nè, hãy fill vào cho tôi` | Added the supplied YouTube demo URL to the README, Task 2 and Agent Skill demo registers, main report, and regenerated 7-page PDF; marked the mandatory video checklist items complete and visually verified all three PDF hyperlinks. | Pending student review. | `README.md`, `docs/demo_links.md`, `docs/01_Main_Report.md`, `output/pdf/01_Main_Report.pdf` |

## Late-captured submission-QA interactions

The following prompts are preserved verbatim from the active conversation. Their exact
occurrence times were not logged at the moment of interaction, so they are not assigned
invented timestamps. They were consolidated at the observed log time
`2026-08-11 10:54:06 UTC+7`; this limitation is explicit in the AI Audit Report.

### 10 — occurrence time not retained

```text
cách quay video demo ?
```

- Tool: OpenAI Codex
- Output: proposed a timed Task 2/Agent Skill recording structure.
- Verdict: `REVISED` by the following request for a full narration script.

### 11 — occurrence time not retained

```text
tạo script day đủ để mình nói luôn
```

- Tool: OpenAI Codex
- Output: produced a complete Vietnamese narration and on-screen action script.
- Verdict: `ACCEPTED` provisionally; the student recorded and uploaded a follow-up video.

### 12 — occurrence time not retained

```text
mình mới tạo demo nên tọa 1 vài file rác và có một vài chỗ thay đổi gay bug, hãy check lại và xóa
```

- Tool: OpenAI Codex
- Output: removed temporary render files, reconciled the supplied video link and reviewed the Main Report PDF.
- Verdict: `REVISED`; the later audit found that the video content and exported PDF still required correction.

### 13 — occurrence time not retained

```text
hãy rà soát lại toàn bộ HW4 xem có đáp uwnsgd dủ tiêu chauanr nộp bài chưa, hãy chấm điểm bài cảu mình
```

- Tool: OpenAI Codex
- Output: audited local/remote Git state, all three feature reports, PDFs, issues, skills and the 10:06 unlisted video; assessed 85/100 and identified blocking evidence gaps.
- Verdict: `ACCEPTED`; the student immediately requested remediation.

### 14 — observed 2026-08-11 10:54:06 UTC+7

```text
fix cho mình để 100/100
```

- Tool: OpenAI Codex
- Output: added the eighth meaningful `.spec.ts` commit, corrected submission links and documentation, regenerated evidence documents, and prepared the final submission audit. The non-fabricatable replacement video remains the student's responsibility.
- Verdict: `PENDING` until student review and replacement-video upload.
