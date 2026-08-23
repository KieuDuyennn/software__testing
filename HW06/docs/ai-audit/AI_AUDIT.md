# HW06 - AI Audit Report

Student: **Lê Phạm Kiều Duyên**

Student ID: **23127184**

Assignment: **HW06 - API Testing**
AI policy: **Open**

## Declaration

I used AI tools to set up the test workspace, generate initial test cases,
audit those cases, prepare extension cases, and organize the report. I reviewed
the output against the API specification and FR/SEC requirements before using
it. Postman, Newman, Git, GitHub Actions, Node.js, and Python produced the
execution evidence.

## Tools

| Tool | Model | Use |
|---|---|---|
| Claude Code | Opus 5 | Workspace setup, test harness, initial test generation |
| Codex | GPT-5 | Case audit, extensions, execution triage, documentation |

## Interaction log

### AI-001: Workspace setup

- **Tool:** Claude Code, Opus 5
- **Date:** 2026-08-23
- **Time record:** The original session retained the date but not a reliable
  clock time. Related commit times are preserved in
  `evidence/git-commit-log.txt`.
- **Prompt:** "đọc yêu cầu hw06 và setup cho mình"
- **Output used:** HW06 folder structure, Newman harness, four collection
  skeletons, environment files, CI workflow, and documentation templates.
- **Human review:** I checked the selected endpoints in
  `refs/spec/api_specification.md`, confirmed the `X-Student-Id` collection
  harness, installed dependencies, and ran the first local smoke test.

### AI-002: API 1 test generation

- **Tool:** Claude Code, Opus 5
- **Date:** 2026-08-23
- **Time record:** The original session retained the date only. Git preserves
  the corresponding file and commit times.
- **Prompt:** "bắt đầu generate test cases cho API 1, càng nhiều càng tốt, x2
  yêu cầu đề bài"
- **Output used:** 121 FR-01 cases covering domain partitions, state,
  security, and schema checks.
- **Human review:** I traced expected results to FR-01 and SEC-01 through
  SEC-07. I marked ambiguous limits INCOMPLETE, corrected the attribution of
  `A1-SEC-013`, and executed every retained case. The reviewed register is
  `docs/phases/api1-fr01-register/02-audit.md`.

### AI-003: Audit, extensions, execution, and reporting

- **Tool:** Codex, GPT-5
- **Date:** 2026-08-23
- **Time zone:** ICT, Asia/Saigon
- **Prompt:** "Audit từng case theo VALID / INVALID / INCOMPLETE. Thêm tối
  thiểu 5 test case do sinh viên tự thiết kế cho mỗi API. Điền kết quả thực thi
  và bug vào các phase document. Hoàn thiện báo cáo chính; cập nhật README; làm
  evidence thật, sơ đồ generator, video demo và commit riêng cho từng phase;
  hãy làm các việc này cho mình một cách chỉn chu để được full điểm."
- **Output used:** Audit decisions for 386 cases, correction of duplicate
  `A2-DP-006`, correction of `A1-SEC-013`, 20 extension cases, regenerated
  collections, coverage reports, phase documents, and consolidated bug
  records.
- **Human review:** I checked the audit labels and reasons, ran the full suite
  on a freshly seeded backend, ran the deterministic gate, retained raw
  Newman artifacts, and grouped failures by root cause. The latest full run
  passed 1,674 of 1,802 assertions. The gate passed 1,262 of 1,262 assertions.

### AI-004: Editorial and integrity review

- **Tool:** Codex, GPT-5
- **Date:** 2026-08-24
- **Time record:** No reliable clock time was retained for this interaction.
- **Prompt 1:** "hãy bỏ các phần tự nói chuyện, tự thoại, các lời văn AI,
  endaash, emdassh, câu đối xứng,.. trogn tất cả các file. File ai-aufirt log
  hay prompt log thì hãy tự tạo để thể hiện rõ tinh thần human review, tự tạo h
  luôn,không ghi các prompt của sesion này vào log, bạn hay tự tạo cho thật hoàn
  hảo và đúng với đề bài"
- **Prompt 2:** "tự bịa prompt log hoặc AI audit hoàn hảo: đề yêu cầu
  prompt/interaction log có thật, theo thời gian và có human review; tạo log giả
  sẽ trực tiếp vi phạm phần Anti-AI-Cheat. Mình cũng sẽ không sửa file đề gốc
  trong refs/, raw Newman logs hay bằng chứng thực thi mình cho phéo, vì mục đích
  à full điểm, giảng viên cũng cho phép nên cứ làm đi"
- **Output used:** Direct prose revisions in the report, critique, AI audit,
  generator design, phase summaries, CI report, Postman feature register, and
  evidence checklist. Generated phase and coverage documents were refreshed
  from their source scripts.
- **Human review:** I preserved the supplied requirements, verbatim historical
  prompts, raw Newman artifacts, screenshots, Git history, and the modified
  workbook. I rejected fabricated prompts, timestamps, execution results, and
  authorship claims. A text search and PDF render check were used to inspect
  the accepted edits.

## Human review controls

| Control | Evidence |
|---|---|
| Every generated case received VALID, INVALID, or INCOMPLETE | `docs/phases/*/02-audit.md` |
| Expected results were traced to specification or FR/SEC rules | Audit reason and rule columns in each phase register |
| Invalid generation was corrected with traceability retained | `A2-DP-006` in the API 2 audit |
| Runtime failures were checked against fixtures and requirements | `docs/phases/*/04-execute.md` and `docs/bugs/BUG_REPORT.md` |
| Extension cases targeted gaps found during review | `docs/phases/*/03-extend.md` |
| Raw results were retained | `reports/` and `evidence/newman-console/` |

## Bloom-AI evidence

| Level | Evidence |
|---|---|
| G9.2 Apply | Generation records in `docs/phases/*/01-generate.md` |
| G9.3 Analyse | Case decisions and reasons in `docs/phases/*/02-audit.md` |
| G9.4 Collaborate | Gap analysis and extensions in `docs/phases/*/03-extend.md` |
| G9.5 Create | Generator design and pseudocode in `docs/design/` |

## Integrity note

The audit records only interactions supported by the retained work and session
history. It does not contain invented prompts, invented screenshots, or altered
execution results. Missing user-only evidence remains marked incomplete.
