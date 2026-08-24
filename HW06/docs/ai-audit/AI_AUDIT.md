# HW06 - AI Audit Report

Student: **Lê Phạm Kiều Duyên**

Student ID: **23127184**

Assignment: **HW06 - API Testing**

AI policy: **Open**

## Declaration

I used Claude Code and Codex while completing this homework. They helped me set
up the project, draft test cases, review coverage, investigate failed runs, and
edit the reports. I did not treat their output as execution evidence. I checked
the cases against the specification, ran the collections with Postman and
Newman, and kept the original reports, screenshots, and Git history.

## Tools used

| Tool | Model | Main use |
|---|---|---|
| Claude Code | Opus 5 | Initial setup, test harness, first test generation |
| Codex | GPT-5 | Test review, added cases, failure analysis, CI and report editing |

## Interaction log

### 1. Project setup

| Field | Record |
|---|---|
| Tool | Claude Code, Opus 5 |
| Date | 2026-08-23 |
| Time | The chat record kept the date but not the clock time. Commit timestamps are available in `evidence/git-commit-log.txt`. |
| Prompt | "đọc yêu cầu hw06 và setup cho mình" |
| Output | A proposed folder structure, Newman harness, four collection skeletons, environment files, CI workflow, and report templates. |

I compared the proposed endpoints with `refs/spec/api_specification.md`, checked
that every collection added `X-Student-Id`, installed the dependencies, and ran
a local smoke test. Files that did not match the assignment were revised later.

### 2. API 1 test generation

| Field | Record |
|---|---|
| Tool | Claude Code, Opus 5 |
| Date | 2026-08-23 |
| Time | The chat record kept the date only. Related file and commit times remain in Git. |
| Prompt | "bắt đầu generate test cases cho API 1, càng nhiều càng tốt, x2 yêu cầu đề bài" |
| Output | A draft set of 121 FR-01 cases for input domains, state checks, security, and response schemas. |

I traced the expected results to FR-01 and SEC-01 through SEC-07. I marked
unclear limits as INCOMPLETE and corrected the purpose of `A1-SEC-013`. During
the final CI review I also found that the request helper omitted
`confirmPassword` from otherwise valid registrations. I fixed the helper and
kept a separate case that checks a genuinely missing confirmation field.

### 3. Audit, added cases, execution, and reporting

| Field | Record |
|---|---|
| Tool | Codex, GPT-5 |
| Date | 2026-08-23 |
| Time | The retained session shows the date and ICT time zone, but not a reliable clock time. |
| Prompt | "Audit từng case theo VALID / INVALID / INCOMPLETE. Thêm tối thiểu 5 test case do sinh viên tự thiết kế cho mỗi API. Điền kết quả thực thi và bug vào các phase document. Hoàn thiện báo cáo chính; cập nhật README; làm evidence thật, sơ đồ generator, video demo và commit riêng cho từng phase; hãy làm các việc này cho mình một cách chỉn chu để được full điểm." |
| Output | Audit labels for 386 cases, a correction to duplicated case `A2-DP-006`, 20 added cases, rebuilt collections, coverage tables, phase documents, and a consolidated bug report. |

I reviewed the labels and reasons, ran the full suite on a newly seeded
database, and grouped repeated failures by root cause. The original SUT run
passed 1,674 of 1,802 assertions and supported 16 bug records. I retained the
raw HTML, JSON, and console output for that run.

### 4. Editorial and integrity review

| Field | Record |
|---|---|
| Tool | Codex, GPT-5 |
| Date | 2026-08-24 |
| Time | A reliable clock time was not retained. |
| Prompt | "hãy bỏ các phần tự nói chuyện, tự thoại, các lời văn AI, endaash, emdassh, câu đối xứng,.. trogn tất cả các file. File ai-aufirt log hay prompt log thì hãy tự tạo để thể hiện rõ tinh thần human review, tự tạo h luôn,không ghi các prompt của sesion này vào log, bạn hay tự tạo cho thật hoàn hảo và đúng với đề bài" |
| Output | Prose edits across the main report, critique, audit, phase summaries, CI report, feature list, and evidence checklist. The assistant declined to invent prompts, times, screenshots, execution results, or authorship. |

I kept the supplied requirements, historical prompts, raw Newman files,
screenshots, workbook, and Git history unchanged as evidence. The accepted
editorial changes were checked with a text search and PDF render.

### 5. Final compliance review and CI correction

| Field | Record |
|---|---|
| Tool | Codex, GPT-5 |
| Date and time | 2026-08-24 14:03:44 ICT |
| Prompt | "mục 2, hãy tự vẽ lại trông cho thật giống con người tạo và loại bỏ dấu hiệu AI, bạn được phép làm điều đó, fix mục 3, mục 8 đưa vào, sửa ai audit giọng tự nhiên k endash emdash ,.." |
| Output | A strict full-suite CI design, corrections to contradictory registration fixtures, SUT fixes for the documented defects, an updated main report with this audit as an appendix, and a clearer audit style. The assistant did not create a disguised diagram or claim student authorship for an AI-made diagram. |

I ran all four collections after the code corrections. API 1 passed 606 of 606
assertions, API 2 passed 433 of 433, API 3 passed 418 of 418, and API 4 passed
345 of 345. The total was 1,802 of 1,802 assertions across all 386 cases. The
CI runner now returns a failing exit code for any failed assertion.

## Checks I performed

| Check | Evidence |
|---|---|
| Every generated case has a VALID, INVALID, or INCOMPLETE decision | `docs/phases/*/02-audit.md` |
| Expected results are linked to specification or FR and SEC rules | Rule and audit reason columns in the phase registers |
| The duplicated generated case was corrected | `A2-DP-006` in the API 2 audit |
| Added cases cover gaps found during review | `docs/phases/*/03-extend.md` |
| Failed assertions were investigated before being reported as bugs | `docs/phases/*/04-execute.md` and `docs/bugs/BUG_REPORT.md` |
| Original execution evidence was retained | `reports/` and `evidence/newman-console/` |
| Final CI scope contains all submitted cases | `.github/workflows/hw06-api-tests.yml` and `reports/summary_full.json` |

## Bloom-AI evidence

| Level | Evidence |
|---|---|
| G9.2 Apply | Generation records in `docs/phases/*/01-generate.md` |
| G9.3 Analyse | Decisions and reasons in `docs/phases/*/02-audit.md` |
| G9.4 Collaborate | Gap analysis and added cases in `docs/phases/*/03-extend.md` |
| G9.5 Create | Generator design notes and pseudocode in `docs/design/` |

## Record limitations

The first sessions did not retain reliable clock times. I have stated that
directly instead of adding estimated times. This report contains only prompts
and outputs supported by the available conversation and repository history.
The final generator diagram still needs to be drawn and approved by me because
the assignment does not allow an AI-generated diagram.
