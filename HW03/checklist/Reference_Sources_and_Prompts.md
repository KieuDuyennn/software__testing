# Reference Sources & AI Prompts — Shared GUI Checklist

> Group deliverable — supports **Task 1, Part A**. Documents the sources the checklist is grounded in and the full prompt chain used to generate and refine it (required by §6 and §15 of the assignment).
> Companion files: `Shared_GUI_Checklist.md` (the checklist itself) · `../AI_Audit_Report.md` (§10 mandatory appendix).
> Checklist version covered: **v1.7 — 53 items** (2026-07-26). Superseded the earlier v1.2/66-item
> pass covered by this file up to Prompt 4 below — v1.3–v1.7 (Prompts 5–10) reduced and corrected
> the set via the live-EMS survey and the screenshot-verification pass; full detail for those steps
> is in `../AI_Audit_Report.md` Interactions 5–10 and is only summarised here to avoid duplicating
> pages of verbatim log across two files.

## 1. Reference Sources

Every source below is cited by at least one checklist item. Sources that grounded no item have been removed — see §4 Human Review Notes for what was removed and why.

| # | Source                                                                 | Type                | Sections / criteria actually used                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Citation                                                                                               |
| - | ---------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1 | Nielsen, J. —*10 Usability Heuristics for User Interface Design*    | Heuristic framework | All ten: H1 Visibility of system status · H2 Match between system and real world · H3 User control and freedom · H4 Consistency and standards · H5 Error prevention · H6 Recognition rather than recall · H7 Flexibility and efficiency of use · H8 Aesthetic and minimalist design · H9 Help users recognize/diagnose/recover from errors · H10 Help and documentation                                                                                                                                                                                                                                                                                                                                                                                                                          | Nielsen Norman Group, 1994 (rev. 2024) — https://www.nngroup.com/articles/ten-usability-heuristics/   |
| 2 | Norman, D. A. —*The Design of Everyday Things* (Revised & Expanded) | Book                | All six principles: P1 Visibility · P2 Feedback · P3 Constraints · P4 Mapping · P5 Consistency · P6 Signifiers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Basic Books, 2013                                                                                      |
| 3 | Shneiderman, B. et al. —*Eight Golden Rules of Interface Design*    | Heuristic framework | All eight: R1 Strive for consistency · R2 Enable shortcuts for frequent users · R3 Offer informative feedback · R4 Design dialogs to yield closure · R5 Offer simple error handling · R6 Permit easy reversal of actions · R7 Support internal locus of control · R8 Reduce short-term memory load                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | *Designing the User Interface*, 6th ed., Pearson, 2016                                               |
| 4 | **Course slides — `S13_GUI Testing & Usability Testing.pdf`** | Course material     | p.6 GUI elements to test (buttons, checkboxes, radio buttons, dropdown menus, text fields, error messages) · p.7 visual consistency, text overflow, distorted graphics · p.8 accessibility features · p.11–14 Common GUI bugs (data validation · incorrect field default · mishandling of server process failures · mandatory fields not mandatory · field order · currency of data on screens · window modality · focus on objects needing it · state of controls aligns with state of data) · p.16 Checklist testing categories (GUI standards, colour scheme, typography, layout and alignment, labels, error messages) · p.17–18 Navigation testing (main menu,**breadcrumb**, links and buttons, form navigation and focus order) · p.26 Localization and Internationalization | Local file:`HW03/refs/S13_GUI Testing & Usability Testing.pdf`                                       |
| 5 | **W3C — Web Content Accessibility Guidelines (WCAG) 2.1**       | Standard            | SC 1.1.1 Non-text Content · SC 1.4.3 Contrast (Minimum) · SC 2.2.2 Pause, Stop, Hide · SC 2.4.7 Focus Visible · SC 4.1.3 Status Messages                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | W3C Recommendation, 5 June 2018 — https://www.w3.org/TR/WCAG21/                                       |
| 6 | Assignment specification                                               | Assignment spec     | §4 SUT (EMS feature pools A–D; IA-01…IA-04 definitions — used as the conformance map in the checklist) · §5 suggested screens · §6 Task 1 Part A requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Local file:`HW03/requirments/2026.HW03.GUI Usability EMS_En.md` (+ `_Vi.md`)                       |
| 7 | Real EMS interface captures — 14 screenshots, plus the live-EMS survey (14 pages) | Product evidence    | Grounded the EMS-specific items and, from v1.3 onward, superseded six items the survey had gotten wrong (see `AI_Audit_Report.md` Interaction 10 for the four factual errors this caught) | Local folder: `HW03/screenshots/` · `HW03/checklist/EMS_Live_Survey_2026-07-26.md` — **on disk, not yet committed to git (see §5)** |

### Sources considered but not used

| Source                                                                                    | Why it is not in the table above                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ISTQB Foundation Level Syllabus                                                           | Listed in §17 of the assignment as general course reading, but it contains no GUI-checklist or per-widget material, and**no checklist item cites it**. Listing an uncited source would misrepresent the grounding. It is expected to be relevant later for defect-severity terminology in the Task 1B bug reports, not for Task 1A. |
| `HW03/refs/EN.UsabilityTesting.pdf`, `HW03/refs/GUI-VulqUpdated.UsabilityTesting.pdf` | Cover usability-testing method (test plan format, task selection, Likert/semantic-differential questionnaires, performance vs preference data, severity × probability analysis). These ground**Task 2**, not the Task 1A checklist, and are cited in the Task 2 report instead.                                                     |
| `HW03/refs/Testing GUI Applications.pdf`                                                | The file could not be opened during the v1.2 audit (`PdfReadError: EOF marker not found` — the PDF appears truncated). Nothing was cited from it because nothing could be read from it. Re-download and re-check before submission.                                                                                                     |

## 2. Source-to-Item Traceability

> Tables 2a and 2b below are **machine-regenerated** from `Shared_GUI_Checklist.md`'s own
> *Reference Source* column, using `.claude/skills/gui-checklist-design/scripts/check_checklist.py
> --emit-traceability` — the same command re-derives them from any future version, so drift like
> the v1.2→v1.7 staleness this file previously had cannot happen silently again. Regenerated
> 2026-07-30 against v1.7 (53 items); script exit 0, IDs unique and contiguous, all 10+6+8
> framework citations present, evidence resolves against `screenshots/`.

### 2a. By framework

| Source | Items citing it |
| --- | --- |
| Nielsen H1 | IA01-06, IA01-07, IA01-11, IA02-14, IA03-01, IA03-03, IA03-05, IA04-04, IA04-05, IA04-07, IA04-10, IA04-13 |
| Nielsen H2 | IA04-01 |
| Nielsen H3 | IA03-04, IA03-10, IA03-13 |
| Nielsen H4 | IA01-01, IA01-03, IA01-08, IA01-09, IA02-11, IA03-02, IA03-06, IA03-07 |
| Nielsen H5 | IA02-03, IA02-04, IA02-06, IA02-09, IA02-11, IA02-13, IA04-03 |
| Nielsen H6 | IA01-10, IA02-02, IA02-12 |
| Nielsen H7 | IA03-01 |
| Nielsen H8 | IA01-04 |
| Nielsen H9 | IA02-08, IA04-08, IA04-11 |
| Nielsen H10 | IA02-05 |
| Norman P1 | IA03-08 |
| Norman P2 | IA02-05, IA02-07, IA03-12, IA04-09 |
| Norman P3 | IA02-01, IA02-03, IA03-05 |
| Norman P4 | IA02-10 |
| Norman P5 | IA01-03 |
| Norman P6 | IA02-01, IA02-07, IA03-12, IA04-02, IA04-06 |
| Shneiderman R1 | IA01-02 |
| Shneiderman R2 | IA03-01, IA03-07 |
| Shneiderman R3 | IA04-04, IA04-10, IA04-13 |
| Shneiderman R4 | IA04-03 |
| Shneiderman R5 | IA04-03, IA04-11 |
| Shneiderman R6 | IA02-13, IA03-04, IA03-10 |
| Shneiderman R7 | IA04-08 |
| Shneiderman R8 | IA03-09 |
| WCAG SC 1.1.1 | IA01-13 |
| WCAG SC 1.4.3 | IA01-05 |
| WCAG SC 2.2.2 | IA01-10 |
| WCAG SC 2.4.7 | IA01-12 |
| WCAG SC 4.1.2 | IA03-04 |
| WCAG SC 4.1.3 | IA04-12 |

### 2b. By course-slide page

| Slide (S13) | Items grounded |
| --- | --- |
| p.6 | IA02-12 |
| p.7 | IA01-08, IA01-11 |
| p.8 | IA01-13, IA04-12 |
| p.11 | IA02-01, IA02-04, IA02-06, IA02-11, IA04-11 |
| p.12 | IA02-14, IA03-08, IA04-05 |
| p.13 | IA01-12, IA04-02 |
| p.14 | IA03-08 |
| p.16 | IA01-01, IA01-03, IA02-02, IA02-08, IA04-01 |
| p.17 | IA03-01, IA03-03, IA03-11 |
| p.18 | IA02-10, IA03-13 |
| p.26 | IA01-08, IA01-09 |

### 2c. By screenshot — superseded by the live-EMS survey

The v1.2 version of this table mapped items to exact screenshot filenames. That mapping style no
longer matches how the checklist is written: from v1.3 onward (Interactions 5–8, `AI_Audit_Report.md`),
items are grounded primarily in the **live EMS survey** (`EMS_Live_Survey_2026-07-26.md`, 14 pages
inspected) and reference screens by name in the Verification Rule prose (e.g. "the Add/Edit Event
form"), not by embedding a filename. Re-scanning v1.7 for literal filename strings finds only 2
matches (`IA01-04` and `IA04-13`, both citing `Admin_A2_AddEditEvent.png`), which would misrepresent
the grounding as far thinner than it is.

The real per-item grounding evidence is: (1) the framework/slide citations in 2a/2b above, (2) the
survey document for what the live product actually contains, and (3) `check_checklist.py
--evidence-root screenshots` returning **0 unresolved evidence references** against the 14 committed
screenshots — i.e. every image any item does name resolves to a real file, not a broken link.

## 3. AI Prompt Chain

The assignment (§2) requires guiding the AI through each step of the technique rather than issuing one generic prompt. The chain below is the complete record — every prompt that shaped the checklist, in order. It must stay consistent with `../AI_Audit_Report.md`.

### Prompt 1 — Initial generation, grounded in references + real screenshots

- **AI tool**: Claude Code (Sonnet 5, Anthropic)
- **Date**: 2026-07-25
- **Prompt** (verbatim, Vietnamese original):
  ```
  Tôi đã chuẩn bị đầy đủ bộ tài liệu tham chiếu và ảnh chụp giao diện thực tế của hệ thống EMS trong thư mục `docs/`.

  Bây giờ, chúng ta sẽ tiến hành khởi tạo bộ Shared GUI Checklist (>40 items) cho nhóm.

  Hãy thực hiện theo các bước sau:

  1. Đọc và phân tích các file tài liệu trong `docs/`:
     - `docs/requirement.md` (Đặc biệt là Mục 4 & Mục 6)
     - `docs/Nielsen_10_Usability_Heuristics.md`
     - `docs/Norman_6_Principles.md`
     - `docs/Shneiderman_8_Golden_Rules.md`

  2. Quét và phân tích hình ảnh trong thư mục `docs/screenshots/`:
     Hãy xem qua các ảnh chụp giao diện EMS thực tế để nhận diện chính xác cấu trúc layout, các widget (Form, Rich-Text, Modal, Toast, Table, DatePicker, Upload 4:3/24:9, QR code...) và các thành phần UI đang có trên hệ thống.

  3. Sinh bộ Shared GUI Checklist:
     Kết hợp lý thuyết UI/UX với các quan sát thực tế từ ảnh chụp, hãy tạo đúng 48 items (mỗi khía cạnh IA-01, IA-02, IA-03, IA-04 chứa đúng 12 items).
     Ghi trực tiếp kết quả vào file `Shared_Group_Artifacts/Shared_GUI_Checklist.md` dưới dạng Markdown Table với các cột:
     | Item ID | Aspect | Reference Source | Verification Rule (Quy tắc kiểm tra gắn liền với giao diện EMS) | Expected Behavior (Hành vi mong đợi) |

  4. Cập nhật nhật ký tại `Shared_Group_Artifacts/Reference_Sources_and_Prompts.md`:
     - Liệt kê lại toàn bộ nguồn tài liệu & thư mục ảnh đã tham chiếu.
     - Ghi lại câu prompt này.
  ```
- **AI output summary**: Read the four reference files plus §4 and §6 of the requirement, inspected all 14 EMS screenshots, and generated exactly 48 items (12 per IA) with the five requested columns, each citing a Nielsen/Norman/Shneiderman principle and, where applicable, the screenshot it was grounded in. Result → checklist **v1.0**.
- **Human review outcome**: Accepted as a draft. The group then identified four gaps the AI could not see from static images (keyboard focus ring, `alt` text, Enter-to-submit, ESC-to-close) and added them as IA01-13, IA01-14, IA02-13, IA03-13 → checklist **v1.1 (52 items)**.

### Prompt 2 — Conformance review against the assignment text

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date**: 2026-07-26
- **Prompt** (verbatim):
  ```
  mình đang làm hw3 á, hãy đọc yêu cầu hw3 đi, và xem checklist của mình đã bám sát yêu cầu và đúng chưa. feedback cho mình dựa trên tất cả thông tin bạn có được
  ```
- **AI output summary**: Read both the EN and VI requirement files and the two checklist artefacts, then reported: the prompt chain contained only one prompt; the Human Review Notes table was empty while the changelog claimed the review was complete; every referenced path (`docs/`, `Shared_Group_Artifacts/`) was absent from the repository; WCAG was cited by three items but missing from the sources table; the sources table columns were misaligned and ISTQB plus the course slides grounded no item. It also flagged four missing IA elements and a logic error in IA04-07.
- **Human review outcome**: Findings accepted. The scope was narrowed in Prompt 3 to coverage/conformance only, since Tasks 1B–3 had not started.

### Prompt 3 — Coverage audit, clause by clause

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date**: 2026-07-26
- **Prompt** (verbatim):
  ```
  mình chỉ mới làm tới checklist, hãy tập trung check xem checklist của mình có phủ đủ, có tuân thủ các yêu cầu không
  ```
- **AI output summary**: Audited the checklist on five axes — (1) the six explicit clauses of §6 Task 1A, (2) each component named in the §4 IA definitions, (3) per-widget coverage against the widgets the assignment itself names, (4) citation coverage of the three heuristic frameworks, (5) per-item testability. Produced: three §4 elements with zero items (breadcrumbs, drag-and-drop reorder, progress bars); six widgets with zero items (carousel, date picker, dropdown/select, radio/checkbox, table sorting, QR/barcode); the absence of any failure-feedback item across all of IA-04; one factually wrong item (IA04-07); Nielsen H3 and Shneiderman R3/R4/R5 uncited while Norman P4 was used as a catch-all in five items; and the lack of an N/A convention for a checklist shared across four scenarios.
- **Human review outcome**: All findings accepted; the student directed that they be applied to the artefacts.

### Prompt 4 — Apply the fixes

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date**: 2026-07-26
- **Prompt** (verbatim):
  ```
  hãy fix lại cho chuẩn đi, và ghi lại vào file checklist và file AI audit cho mình
  ```
- **AI output summary**: Before editing, extracted the text of `HW03/refs/S13_GUI Testing & Usability Testing.pdf` so that the course slides could be cited by page rather than listed without use — this surfaced slide p.17 (*Breadcrumb Navigation*), p.6 (the GUI element list), p.11 (*Mishandling of server process failures*) and p.26 (*Localization and Internationalization*), which independently confirmed four of the gaps found in Prompt 3. Then rewrote `Shared_GUI_Checklist.md` to **v1.2 / 66 items**: added 14 items, applied 14 corrections, merged the duplicated IA02-03/IA02-04 pair and repurposed IA02-04 to cover upload-constraint enforcement, added the Pass/Fail/N/A convention, a §4 conformance map, a per-widget map and a framework-coverage table. Rewrote this file and created `../AI_Audit_Report.md`. Item IDs were verified programmatically: 17/17/17/15, no duplicates, no gaps.
- **Human review outcome**: _To be completed by the student after reviewing the v1.2 diff — see §5 below._

## 4. Human Review Notes

What the group changed, removed, or added after reviewing raw AI output, and why.

| #  | Round             | Change                                                                                                                                           | Rationale                                                                                                                                                                                                              |
| -- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | v1.1 (2026-07-25) | Added 4 items: IA01-13 keyboard focus ring, IA01-14 image`alt` text, IA02-13 Enter-to-submit, IA03-13 ESC-to-close                             | The AI's grounding was a set of static screenshots. Keyboard interaction and ARIA/HTML attributes have no visual trace in a still image, so this class of defect was structurally invisible to it.                     |
| 2  | v1.2 (2026-07-26) | Removed ISTQB Foundation Level Syllabus from the sources table                                                                                   | It grounded no checklist item. §6 requires the checklist to be*grounded in* its sources; listing a source nothing cites overstates the grounding. Retained as future reading for defect severity in Task 1B.        |
| 3  | v1.2              | Added the course slides as a**page-cited** source instead of a bare title, and added WCAG 2.1 with the five specific success criteria used | v1.1 listed the slides without drawing anything from them, and cited WCAG in three items without listing it at all. Both directions of the inconsistency are now closed.                                               |
| 4  | v1.2              | Corrected IA04-07                                                                                                                                | As written ("summary counts match the number of rows currently shown") the item would fail on any correctly paginated system and would have produced a false bug report in Task 1B.                                    |
| 5  | v1.2              | Merged IA02-03 + IA02-04 into one item; repurposed the freed ID to cover**enforcement** of upload limits                                   | The two items stated one rule twice (4:3 and 24:9 helper text), inflating the count without adding coverage. Meanwhile IA02-07 checked only that limits were*stated*, with nothing checking they were *enforced*.  |
| 6  | v1.2              | Re-sourced four items away from Norman P4 (Mapping) to P6 Signifiers / P3 Constraints / Nielsen H8; added Nielsen H3 and Shneiderman R3/R4/R5    | P4 had become a catch-all across five unrelated items, while H3 and R3/R4/R5 were cited nowhere — an odd gap given that all of IA-04 concerns feedback. All 10 + 6 + 8 principles are now cited at least once.        |
| 7  | v1.2              | Rewrote IA03-12 and IA04-11 as objectively failable rules; made IA01-08 name the exact throttling setting                                        | "No function buried more than one level deep" was a design opinion, and "simulate a scan" was undefined — two testers would have produced different results from the same item.                                       |
| 8  | v1.2              | Added the**Pass / Fail / N/A** result convention                                                                                           | The checklist is shared across scenarios A–D, so items such as IA02-03 (image-ratio helper text) have no referent on, say, the Users list. Recording those as "Pass" would be false and "Fail" would invent a defect. |
| 9  | v1.2              | Added the §4 conformance map, per-widget map, and framework-coverage table                                                                      | Coverage was previously asserted in prose. These three tables make the claim auditable — and building the first of them is what exposed the breadcrumb, drag-and-drop and progress-bar gaps.                          |
| 10 | v1.2              | Added the scenario-assignment table (still to be filled in)                                                                                      | §5's no-duplication rule needs group-level evidence; no artefact recorded who owned which scenario and screens.                                                                                                       |

## 5. Outstanding actions before submission

*Updated 2026-07-30 against the current repository state — items resolved since the v1.2 pass are
marked done rather than left to look outstanding.*

| # | Action | Owner | Status |
| - | --- | --- | --- |
| 1 | Commit the 14 EMS screenshots (`HW03/screenshots/` — not `checklist/screenshots/`, corrected path) to git | Group | **Done** 2026-07-30, commit `32b9346` — the first commit for this assignment, covering the checklist, reference docs and skill suite. |
| 2 | Fill in the scenario-assignment table in `Shared_GUI_Checklist.md` | Group | **Done** — table present, all four members assigned, no overlapping screens (see the checklist's "Scenario assignment" section). |
| 3 | Record the group's review outcome for the v1.2→v1.7 revision passes | Group | **Partially done** — `AI_Audit_Report.md` Interaction 10 records the student's own correction (defect verdicts stripped from the shared artefact). Formal sign-off from the other three members is still pending. |
| 4 | Re-download `HW03/refs/Testing GUI Applications.pdf` — truncated, unreadable | Group | Still open. Nothing cites it; low priority. |
| 5 | Distribute checklist v1.7 to all four members before Task 1B execution | Group | Not verified from this repo — confirm with the group directly. |
| 6 | Pillar-4 gap: only 4 of 53 items grounded in the team's own EMS experience (`AI_Audit_Report.md` Interaction 6) | Group | **Still open**, tracked for v1.8. Each member adds 1–2 items from their own use of EMS. |
