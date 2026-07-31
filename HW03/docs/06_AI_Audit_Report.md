# AI Audit Report — HW03 (GUI & Usability Testing on EMS)

> **Mandatory appendix — §10 of the assignment.**
> Scope of this version: **Task 1 Part A (complete)** and **Task 1B (complete — all 60 items × 6 screens)**. Interactions 1-13 are logged below. Task 2 is designed but not run and Task 3 is planned but not run; the AI interactions that produced their planning artefacts, and the reorganisation of this folder on 2026-08-01, are **not yet written up as numbered interactions** — that is an open item, not a claim that they did not happen. The artefacts concerned are listed in the Path note below and in `README.md`.
> Companion files: `docs/01_Task1A_Shared_GUI_Checklist.md` · `docs/checklist/Reference_Sources_and_Prompts.md` · `docs/02_Task1B_Execution_Report_ScenarioD.md` · `docs/05_Bug_Usability_Findings_Log.md` · `README.md` · `docs/07_AI_Critique.md`

> **Path note (2026-08-01).** HW03 was reorganised into `docs/` · `reports/` · `refs/`. Descriptive text in this file uses the new paths. **Verbatim prompt blocks were left exactly as typed** and therefore still name the old locations (`checklist/`, `task1b_execution/`, `docs/screenshots/`); rewriting them would have falsified the record. Mapping: `checklist/Shared_GUI_Checklist.md` → `docs/01_Task1A_Shared_GUI_Checklist.md` · `task1b_execution/` → `docs/02_…` + `reports/evidence_task1b/` · `findings/` → `docs/05_…` · `screenshots/` → `reports/screenshots/` · `requirments/` → `refs/requirements/`.

## 1. Declaration

**I use AI tools for the following tasks:**

| # | Task                                                                                                             | AI tool                                                                                                | Extent of AI involvement                                                                                                                                                                                      |
| - | ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1 | Generating the initial draft of the shared GUI checklist (Task 1A)                                               | Claude Code — Sonnet 5 (Anthropic)                                                                    | AI produced the first 48 items from supplied references and screenshots; the group reviewed and extended them                                                                                                 |
| 2 | Auditing the checklist for conformance and coverage against the assignment text (Task 1A)                        | Claude Code — Opus 5 (Anthropic)                                                                      | AI performed the gap analysis; the student directed the scope and accepted/rejected each finding                                                                                                              |
| 3 | Applying the audit findings to the checklist and the group artefacts (Task 1A)                                   | Claude Code — Opus 5 (Anthropic)                                                                      | AI edited the files under instruction; the group is responsible for the final content                                                                                                                         |
| 4 | Surveying the live EMS to reconcile checklist items with the real product (Task 1A)                              | Claude Code — Opus 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension | AI navigated and inspected the DOM of**14 pages** across three sessions (Interactions 5, 7, 8) to inventory which widgets exist; **no checklist item was executed and no Pass/Fail was recorded** |
| 5 | Splitting the four scenarios across the four members (Task 1A, §5)                                              | Claude Code — Opus 5 (Anthropic)                                                                      | AI proposed the assignment and the per-scenario N/A predictions; the group must confirm or swap them                                                                                                          |
| 6 | Verifying the checklist and survey against the student's 14 screenshots, then applying the corrections (Task 1A) | Claude Code — Opus 5 (Anthropic)                                                                      | AI compared every claim to the images, found four factual errors in the earlier AI-produced survey, and edited the files under instruction; the student authorised each fix                                   |

No other AI tool was used for Task 1A.

**Tool declaration (§9).** The tools §9 permits and requires to be declared here are: an AI tool of the student's choice — **Claude Code (Anthropic), models Sonnet 5 and Opus 5**, the only AI tool used on this assignment; a **BrowserStack / LambdaTest** trial or equivalent cloud cross-browser tool — **not yet used**, Task 3 has not been run, and it must be declared here with the account and session dates once it is; and **Google Forms** for the §7 findings channel — **not yet used**, 0 of 16 findings submitted. The required Bloom-AI level for this homework is **G9.3 (Analyse)** and **G9.4 (Collaborate)**.

**On the checklist prompts (§10).** §10 states that the group's Task 1A checklist prompts belong in this appendix. They are logged as Interactions 1-12 below; `docs/checklist/Reference_Sources_and_Prompts.md` carries the same chain in the group artefact, annotated with the human review outcome per revision. The two are the same prompts, not two different records.

**On the browser survey (Interaction 5):** the student logged in personally — the AI was not given and did not enter any credentials. The survey established *which widgets EMS contains* so that checklist items describe the real product; it did **not** produce test results. All Task 1B execution evidence, and the §12 artefacts generally, remain to be produced by the student against the live system.

> **Fill in before submission:** the *Time* column below is recorded as date-only because exact clock times were not captured during the sessions. Retrieve the real timestamps from the Claude Code session history and complete them — §10 asks for date **and** time.

## 2. Interaction Log

### Interaction 1 — Generate the initial checklist

| Field                       | Value                                        |
| --------------------------- | -------------------------------------------- |
| **AI tool**           | Claude Code — Sonnet 5 (Anthropic)          |
| **Date / time**       | 2026-07-25 ·_time: TBD_                   |
| **Task**              | Task 1A — generate the shared GUI checklist |
| **Artefact produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.0 (48 items)  |

**Prompt (verbatim):**

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

**AI output:** Read the four reference documents and §4/§6 of the requirement, inspected the 14 EMS screenshots, and wrote 48 checklist items — exactly 12 per interface aspect — in the requested five-column format, each citing a Nielsen, Norman or Shneiderman principle and, where relevant, the screenshot that grounded it.

**Human review and action taken:** Accepted as a draft only. The group compared the items against their own experience of the EMS UI and found that every item described something *visible*. Four behavioural/accessibility gaps were added manually, producing v1.1 (52 items); after the v1.4 renumbering they carry the IDs **IA01-12, IA01-13, IA02-10 and IA03-10**. The reason recorded for each — the AI was reasoning from static images — is documented in the checklist.

---

### Interaction 2 — Review the checklist against the assignment requirements

| Field                       | Value                             |
| --------------------------- | --------------------------------- |
| **AI tool**           | Claude Code — Opus 5 (Anthropic) |
| **Date / time**       | 2026-07-26 ·_time: TBD_        |
| **Task**              | Task 1A — conformance review     |
| **Artefact produced** | Review findings (no file edited)  |

**Prompt (verbatim):**

```
mình đang làm hw3 á, hãy đọc yêu cầu hw3 đi, và xem checklist của mình đã bám sát yêu cầu và đúng chưa. feedback cho mình dựa trên tất cả thông tin bạn có được
```

**AI output:** After reading both language versions of the requirement and the two checklist artefacts, reported that the checklist met the structural requirements (52 > 40 items, four aspects covered, the "why the AI missed it" table present and well argued) but that the supporting artefacts did not: the prompt chain contained one prompt where §2 demands step-by-step guidance; the Human Review Notes table was empty while the changelog asserted the review was complete; every path the checklist referenced (`docs/`, `docs/screenshots/`, `Shared_Group_Artifacts/`) was absent from the repository; WCAG grounded three items but was missing from the sources table; the sources table columns were misaligned; and ISTQB and the course slides were listed as sources although no item cited either.

**Human review and action taken:** Findings accepted as accurate — each was independently checkable against the files. The student narrowed the scope for the next step, since Tasks 1B–3 had not begun.

---

### Interaction 3 — Coverage audit, clause by clause

| Field                       | Value                                     |
| --------------------------- | ----------------------------------------- |
| **AI tool**           | Claude Code — Opus 5 (Anthropic)         |
| **Date / time**       | 2026-07-26 ·_time: TBD_                |
| **Task**              | Task 1A — coverage and conformance audit |
| **Artefact produced** | Gap list (no file edited)                 |

**Prompt (verbatim):**

```
mình chỉ mới làm tới checklist, hãy tập trung check xem checklist của mình có phủ đủ, có tuân thủ các yêu cầu không
```

**AI output:** Audited the checklist along five axes — the six explicit clauses of §6 Task 1A; every component named in the §4 IA definitions; per-widget coverage against the widgets the assignment itself names; citation coverage of the three heuristic frameworks; and per-item testability. Findings:

- **§4 elements with no item at all:** breadcrumbs (IA-03), drag-and-drop reorder (IA-03), progress bars (IA-04, present only as a sub-clause of another item).
- **Widgets named by the assignment with no item:** carousel, date picker, dropdown/select, radio/checkbox, table column sorting, QR/barcode ticket.
- **A whole missing dimension:** all twelve IA-04 items addressed *successful* actions; none addressed what the user sees when an action *fails*.
- **A factual error:** IA04-07 compared summary counts against "the number of rows currently shown", which is wrong for any paginated table.
- **Citation problems:** Nielsen H3 and Shneiderman R3/R4/R5 were cited nowhere, while Norman P4 (Mapping) was used as a catch-all across five items, at least three of them incorrectly.
- **A process gap:** no N/A convention, although the checklist is shared across four scenarios and many items have no referent on a given screen.

**Human review and action taken:** All findings accepted; the student instructed that they be applied.

---

### Interaction 4 — Apply the fixes to the artefacts

| Field                        | Value                                                                                                        |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                                            |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                                   |
| **Task**               | Task 1A — revise the checklist and group artefacts                                                          |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.2 (66 items) · `docs/checklist/Reference_Sources_and_Prompts.md` (rewritten) · this file |

**Prompt (verbatim):**

```
hãy fix lại cho chuẩn đi, và ghi lại vào file checklist và file AI audit cho mình
```

**AI output:**

1. Extracted the text of `refs/slides/S13_GUI Testing & Usability Testing.pdf` (55 slides) so the course slides could be cited by page number instead of listed unused. This surfaced slide p.17 (*Breadcrumb Navigation*), p.6 (the GUI element list including checkboxes, radio buttons and dropdown menus), p.11 (*Mishandling of server process failures*) and p.26 (*Localization and Internationalization*) — independently confirming four of the gaps found in Interaction 3.
2. Rewrote the checklist to **v1.2, 66 items**: 14 new items closing the §4 and per-widget gaps, and 14 corrections to existing items (including the IA04-07 factual error, the Norman P4 over-use, and two rules that were not objectively failable).
3. Merged the duplicated IA02-03/IA02-04 pair into one item and repurposed the freed ID to cover enforcement of upload constraints.
4. Added the Pass/Fail/**N/A** result convention, a §4 conformance map, a per-widget coverage map, a framework-coverage table, and a scenario-assignment table for §5's no-duplication rule.
5. Rewrote `docs/checklist/Reference_Sources_and_Prompts.md`: fixed the misaligned sources table, added WCAG 2.1 with its five specific success criteria, added the course slides with per-page citations, removed ISTQB with a documented reason, and filled in the prompt chain and Human Review Notes.
6. Verified the item IDs programmatically: 17 / 17 / 17 / 15 = 66, no duplicates, no gaps.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The v1.2 diff was read in full and all 14 added items and 14 corrections were accepted, with the reasoning recorded as Notes 1-10 there: ISTQB was removed because it grounded no item, IA04-07 was corrected because as written it would have failed on any correctly paginated system and produced a false bug report in Task 1B, IA02-03/IA02-04 were merged because they stated one rule twice, four items were re-sourced away from Norman P4 which had become a catch-all, and IA03-12/IA04-11 were rewritten as objectively failable rules. One objection was raised and upheld: the empty Human Review Notes table had been described in the changelog as a completed review, which is why this file now records an outcome per interaction instead of a blanket claim.

---

### Interaction 5 — Survey the live EMS to reconcile the checklist with the real product

| Field                        | Value                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic), driving the student's Chrome via the Claude in Chrome extension  |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                          |
| **Task**               | Task 1A — verify that checklist items describe widgets EMS actually has                            |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.3 (*EMS widget inventory* section; 5 items rewritten, 5 sharpened) |

**Prompts (verbatim, in order):**

```
ok bật claude-in-chrome đi, mình mở Chrome rồi
```

```
mình chỉ cần bạn xem để tạo ra checklist thôi chưa cần test thật
```

```
claude in chrome để bạn quan sát và viết checklist đúng và hợp lí nhất, chưa test thật để tiết kiệm token
```

**AI output:** Opened the EMS URL and reached the login page, then **stopped and asked the student to log in**, declining to enter the credentials itself. From the authenticated session, surveyed seven pages — user dashboard, admin dashboard, Events Management, Categories, event detail, event edit form, and the 404 page — primarily by querying the DOM rather than by screenshot, at the student's request to conserve tokens. Recorded the results as the *EMS widget inventory* table in the checklist.

The survey showed that **six checklist items described widgets EMS does not have**: there is no carousel (the "SPOTLIGHT EVENT" hero is static — no slider library, no controls, no auto-advance over 10 s); no breadcrumb on any of the seven pages; no drag-and-drop reorder anywhere (the apparent matches on Categories were Tailwind class names containing the substring `dat`, a false positive the AI initially misread); no column sorting (all seven header controls are filters); no native date inputs on the event form (custom controls only); and no progress bar (capacities render as plain text, "Lecturer 0 / 3"). It also found no `aria-live` region and no programmatic `required` attribute on any surveyed page, confirming that **IA04-12** and the extended IA02-01 test something real.

> **Superseded in part — see Interaction 10.** Four of this survey's "not found" results were wrong: EMS *does* have bar meters, an icon-only back control on the admin event detail, and native date inputs on the Support requests filters, and the date-format evidence quoted user-typed content. Three of the four are false negatives from selector-based inspection.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The survey's findings were accepted as the basis for rewriting the EMS-specific items, and then **partly overturned** by Interaction 10 — the outcome that matters here: four "widget not found" results were false negatives from selector-based DOM inspection, caught only because the student supplied 14 real screenshots as independent evidence. The rule taken from this round, and written into `docs/07_AI_Critique.md`, is that an absence claimed from a selector query is a claim about the query, not about the product.

---

### Interaction 6 — Assess the grounding pillars and reduce to an executable size

| Field                        | Value                                                                                                                                                |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                                                                                    |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                                                                           |
| **Task**               | Task 1A — grounding assessment and size reduction                                                                                                   |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.4 (52 items) · `docs/checklist/Reference_Sources_and_Prompts.md` (rewritten) · `docs/checklist/EMS_Live_Survey_2026-07-26.md` (new) |

**Prompts (verbatim):**

```
ghi vào referecne source and prompt cho mình, checklist đó theo như mình học thì phải thiết kế dựa trên
quy tắc chuẩn trên thế giới, các heuristica, web thật cần test và dựa vào kinh nghiệm thfi phải.
Bạn thiết kế checklist cho mình đã phủ đủ hết các yếu tố đó chưa. Giới hạn khoảng 52 test thôi vì nhiều quá làm không hết
```

```
hãy lưu lại các thông tin về web hôm nay bạn đã cap và live, để làm thông tin cho test thật để tiết kiệm token
```

**AI output:** Assessed the checklist against the four grounding pillars the student named — international standards, heuristics, the real system under test, and personal experience — and reported that the first three are strong (5 WCAG criteria; Nielsen 10/10, Norman 6/6, Shneiderman 8/8; 14 screenshots plus the live survey) while the fourth is weak at **4 of 66 items**, since every other item is derivable from a document or an observation and therefore reproducible by an AI.

Reduced the checklist from 66 to **52 items** — 5 merges and 8 removals — selecting removals so that none took the sole carrier of a framework citation or of an element named in §4, then renumbering contiguously and publishing a v1.3 → v1.4 ID map. Verified by script afterwards: 13 / 14 / 13 / 12 = 52, no duplicate or missing IDs, all four frameworks still fully cited.

Saved the live-web observations as `docs/checklist/EMS_Live_Survey_2026-07-26.md` — URL map, per-page widget inventory, the accessibility measurements, the two unscored observations, and a re-runnable DevTools snippet — so Tasks 1B–3 can be planned without browsing the app again.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The reduction to an executable size was accepted. The pillar-4 gap — only 4 of 60 items grounded in the team's own lived use of EMS — is assigned back to the members, each to add 1-2 items from personal experience, signed with their own name and student ID. **Retargeted from v1.8 to v2.0**: v1.8 and v1.9 both added *audit-sourced* items, not personal-experience ones, so neither reduced the gap. Tracked as action 6 in §5 of the group artefact, and explicitly **not closeable on paper** — an AI supplying it on a member's behalf would make the checklist's own grounding claim false.

---

### Interaction 7 — Survey Users Management and Support requests; add the Export item

| Field                        | Value                                                                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic) via Claude in Chrome                                                                                    |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                                                                |
| **Task**               | Task 1A — complete the product survey for scenarios C and D                                                                              |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.5 (53 items) · `docs/checklist/EMS_Live_Survey_2026-07-26.md` §11–13 · `docs/checklist/Reference_Sources_and_Prompts.md` updates |

**Prompts (verbatim):**

```
chưa khảo sát users management và support request là sao, là bạn chưa tạo các TC liên quan tới các phần này á hả
```

```
khảo sát nốt 2 trang đó luôn đi, thêm item Export
```

**AI output:** First clarified that the checklist did contain items for those areas — 17 naming Users-Management widgets and 14 naming Support-request widgets — but that none had been verified against the live product, leaving them exposed to the same failure that had already required six rewrites in v1.3. While counting, found that **Export to Excel was covered by exactly one sub-clause** of another item, although §5 C4 names it as a candidate screen.

Surveyed both areas and added **IA04-13 (Export to Excel)** covering download feedback, filename, column completeness, and whether the export reflects the current filter. Corrected two further items that had been written from the events area alone: support requests use path-segment deep links (`/complaints/8`) where events use `?id=`, and Pending/Resolved are plain `<button>` elements rather than `role="tab"`. Also recorded for scenario-C members that Assign Role, Block/Unblock and Reset Password are **not** row-level actions — only Edit and Delete are.

Re-verified by script: 13 / 14 / 13 / 13 = 53 items, no duplicate or missing IDs, all four frameworks still fully cited.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The added Export item and the Users/Support-request survey results were accepted, subject to the Interaction 5 caveat: any "not found" here rests on selector inspection and was re-checked against real screenshots in Interaction 10 before being relied on.

---

### Interaction 8 — Survey the participant-side screens

| Field                        | Value                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic) via Claude in Chrome                                                                          |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                                                      |
| **Task**               | Task 1A — complete the product survey on the participant side                                                                  |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` v1.6 · `docs/checklist/EMS_Live_Survey_2026-07-26.md` §13–18 · `docs/checklist/Reference_Sources_and_Prompts.md` Prompt 8 |

**Prompt (verbatim):** `khảo sát nốt các trang phía người dùng luôn đi`

**AI output:** surveyed the public event detail page, My Requests, the Create Support Request form and the profile page — 14 pages in total across the session. Nothing was submitted: registering for an event or filing a support request would write to a system shared by the whole class, so the survey stopped at inspection.

The decisive finding was a **blocker rather than a checklist defect**. The session runs as `admin@gmail.com`, and EMS deliberately withholds registration from administrators — every event detail page reads "Admin view only" and "Admin can view role information only (no registration action)", renders no Register button, and the avatar menu offers no My Registrations route. Scenario B's screens (registration form, ticket/QR, post-event review) are therefore unreachable until the member owning B registers their own student/lecturer/guest account, which §4 of the assignment already requires.

Three items were sharpened as a result: IA02-01 (the user support form carries `required` on three fields while the admin event form carries none — one product, two conventions; and the asterisk is absent from text content, so it is likely CSS-drawn and outside the accessibility tree), IA04-13 (a third Export control exists on `/profile`), and IA01-11 (the QR code is reachable via `/profile` → QR Code without holding a ticket). The Vietnamese-`<title>`-with-English-body pattern was confirmed on all five participant pages against English titles on admin pages — a systemic i18n lead rather than the one-off it first appeared to be.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The participant-side survey results were accepted as the grounding for the user-facing items, with the same caveat as Interactions 5 and 7: absence claims from selector inspection were treated as provisional until Interaction 10 re-checked them against real captures. The scenario-B account creation remains assigned to whichever member owns that scenario, and is not this member's to close.

### Interaction 9 — Assign the four scenarios to the four members

| Field                        | Value                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                         |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                |
| **Task**               | Task 1A — §5 no-duplication scope split                                                 |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` — scenario-assignment table and per-scenario N/A predictions |

**Prompt (verbatim):** `chia theo pool cho 34 thành viên luôn giúp mình`

**AI output:** assigned the four members to scenarios A–D with no shared screens, and gave B, C and D four screens each rather than three, because the survey indicated each would otherwise carry too many N/A items. Added a per-scenario N/A prediction table so members could plan effort before executing.

**Human review and action taken:** _The group must confirm or swap these assignments — they were chosen on workload and risk, not on anyone's preference._ **One prediction in this output was later found to be wrong** and is corrected in Interaction 10: IA04-13 was predicted N/A for scenario A on the grounds that the Events list has no Export button, but an Export button exists on the Registrants tab.

---

### Interaction 10 — Verify the checklist against the committed screenshots

| Field                        | Value                                                                                                                                                                                                                                             |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                                                                                                                                                                                 |
| **Date / time**        | 2026-07-26 ·_time: TBD_                                                                                                                                                                                                                        |
| **Task**               | Task 1A — verify every claim against product evidence, then apply the corrections                                                                                                                                                                |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` **v1.7** · `docs/checklist/EMS_Live_Survey_2026-07-26.md` (corrections block + per-section fixes) · `docs/checklist/Reference_Sources_and_Prompts.md` (Prompt 10, Human Review Notes 16–20, revised outstanding actions) · this entry |

**Prompts (verbatim, in order):**

```
mình đang làm HW03, các yêu cầu trong folder requirements, các tài liệu học tập trong references,
folder checklist chứa checklist làm chung cho cả nhóm. Bạn hãy đọc và review giúp mnhf checklist
của mình đã đúng và phù hợp với yêu cầu chưa, có thiếu dư thừa hay có vấn đề gì không
```

```
mình mới cung cấp thêm sceenshot trong folder screenshot ròi đó, và cả EMS_live_survey,
bạn có thể dựa vòa đó để kiểm chứng file checklist
```

```
oki hãy sửa giúp mình
```

**AI output:** the first pass ran without product evidence. It verified the structural claims **by script** rather than by assertion — 53 items at 13/14/13/13 with no duplicate or missing IDs, and the §3a/§3b traceability tables regenerated exactly from the checklist's own *Reference Source* column — and reported process gaps (IA02-04 added but absent from the "why the AI missed it" table; Interaction 9 missing from this file; stale item IDs and page counts here; `TBD` times).

The second pass, once the 14 screenshots were supplied, compared every claim in the checklist and the survey against the images. It found **four factual errors, all originating in the live survey, each of which would have produced a wrong Task 1B result**:

1. **"EMS has no progress bar."** The public event detail carries a **Rating summary with five horizontal bar meters**. They are styled `div`s, so the `progress,[role=progressbar]` query returned zero. Worse, each bar renders full-width while its label reads "0 (0%)" — the survey's error concealed a probable defect.
2. **"No back control on the admin event detail."** There is a round **icon-only ← button** beside the event title. The survey checked by text-matching `"back"`, and the button has no text. IA03-11 would have recorded a Fail for an affordance that exists.
3. **"Support requests renders times as `8:07 25/07`."** That string is the **title of a support request a user typed**, read out of `innerText` as though it were chrome. The real inconsistency is larger — `Jul 25, 2026, 9:15 PM` on the support screens against `25/07/2026 21:01` elsewhere — but a bug report quoting the original string would have been refuted immediately.
4. **"EMS uses no native date inputs."** The Support requests Filters card has native **From date / To date** controls. The input census had been run on one form and generalised to the product.

Three scope corrections followed: the **scenario-B account blocker is spent** (B3–B5 were captured from the student account `tien@gmail.com`, which already holds a registration, so the checklist's "first task on the critical path" was misdirecting the group); **Export exists in four places, not three**, so IA04-13 was wrongly predicted N/A for scenario A; and **§5's C3 does not exist as described** — the Edit User dialog contains Assign Role (a Role dropdown) and Block/Unblock (an "Active" checkbox with no confirmation and no audit), while **Reset Password is absent from the admin UI entirely**.

On instruction, the AI then applied all of the above across the four files, bumping the checklist to **v1.7 — still 53 items**, adding no new items and removing none. Superseded statements were struck through and labelled rather than deleted.

**Human review and action taken:** the student reviewed the findings and authorised the fixes. The student then made an important correction to the AI's work: **the AI had written suspected defects into the shared checklist** — phrasings such as "this is a Fail" and "candidate finding" attached to specific screens. That is out of scope for Task 1A, which designs the instrument; and in a *shared* artefact it is worse than premature, because §18 permits only the checklist itself to be identical across the group, so four members would have filed four identical Findings Logs against the §7 cross-check. On instruction the AI stripped every suspected defect from the group artefacts, leaving verification rules, expected behaviour and the widget inventory, plus a neutral list of *areas to examine*. **No Pass/Fail exists anywhere in the Task 1A deliverables.**

_Group sign-off pending._ The pillar-4 gap (only 4 of 53 items from the team's own experience) remains open and is assigned back to the members as v1.8.

---

## 3. Summary of AI contribution to Task 1A

| Artefact                                            | AI-generated                                                                                             | Human-generated                   | Human-verified         |
| --------------------------------------------------- | -------------------------------------------------------------------------------------------------------- | --------------------------------- | ---------------------- |
| Checklist items — **historical, frozen at v1.7 (53 items)**; the current checklist is v1.9 with 60 items, and its authorship breakdown is the provenance table in `docs/01_Task1A_Shared_GUI_Checklist.md` §"Items added beyond the AI output" | 33 (v1.0) + 16 (v1.2, v1.5) = 49 | 4 (v1.1) | All 53 |
| Item corrections and rewrites                       | 14 (v1.2) + 10 (v1.3) + 2 (v1.5) + 3 (v1.6) + 10 (v1.7) proposed                                         | —                                | Pending group sign-off |
| Corrections of the AI's**own** earlier output | 4 survey errors + 3 scope errors, found in v1.7 by checking AI claims against human-captured screenshots | Screenshots supplied by the group | Student-authorised     |
| Reduction 66 → 52, then +1                         | 5 merges + 8 removals + Export item proposed                                                             | Decision to cap at ~52            | Verified by script     |
| Reference sources                                   | Compiled and page-cited by AI                                                                            | ISTQB removal decision            | All                    |
| Screenshots / EMS evidence                          | **None — AI generated no evidence**                                                               | 14 captures by the group          | —                     |
| Scenario assignment                                 | —                                                                                                       | Group (pending)                   | —                     |

Per §12, no evidence artefact in this homework was produced by AI: the EMS screenshots, the cross-platform captures and the five user-testing participants are all real and group-produced. The AI's contribution is confined to text artefacts.

## 4. Material for the AI Critique (§11)

§11 requires a **200–300 word paragraph, written by the student**, critiquing the AI. This section is the factual raw material for it, not the paragraph itself — the paragraph must be in the student's own words.

Concrete AI failures observed during Task 1A:

1. **The AI covered what it was pointed at, and silently reported full coverage of everything else.** The v1.0 prompt supplied screenshots and three heuristic frameworks; the output was well grounded in exactly those and claimed to cover IA-01…IA-04. It did not, because it was never given the §4 definitions listing what those aspects contain. Breadcrumbs, drag-and-drop reorder and progress bars are named in the assignment and got zero items.
2. **Screenshot grounding produced a systematic happy-path bias.** All twelve original IA-04 items concerned successful actions and none concerned failures — screenshots show populated, working screens, because nobody screenshots a 500 error.
3. **A coverage illusion.** For progress bars the AI wrote "(and/or upload progress)" inside another item's expected behaviour. The word was present, the coverage was not. This is only detectable by checking the checklist against the specification's own vocabulary.
4. **A confidently stated factual error.** IA04-07 asserted that summary counts should equal the rows displayed — wrong for any paginated table, and it would have generated a false bug report during Task 1B.
5. **Plausible-looking but wrong citations.** Norman's "Mapping" was attached to five items, at least three of which are Signifiers or Constraints, while Nielsen H3 and Shneiderman R3/R4/R5 went uncited. The citations read as authoritative and were not.
6. **Padding toward a requested number.** Asked for exactly 48 items, the AI split one rule (upload aspect-ratio helper text) into two items to help reach the count.
7. **Tool-mediated blindness — and it was one-directional.** Given a browser, the AI surveyed EMS almost entirely by CSS selector, then wrote the results up as facts about the product: "no progress bar", "no back control", "no native date inputs". All three were wrong, and wrong the *same way* — `progress,[role=progressbar]` cannot see a bar meter built from styled `div`s, a text match on `"back"` cannot see an icon-only button, and an input census run on one form says nothing about another. The instrument's limits silently became the product's description, and because the bias runs one way, the AI systematically **under-reported what EMS contains**. A fourth error came from the opposite direction: reading `innerText` without separating interface chrome from **user-generated content**, so a support-request title a student had typed (`8:07 25/07`) was written up as a date-format defect.
8. **Only human-captured evidence caught it.** The four errors survived a conformance audit, a coverage audit and two further survey passes — all AI-run. They fell in minutes once screenshots taken by a person were used as the control. That is the sharpest lesson available here: an AI checking its own output reproduces its own blind spot, however the prompt is reframed.
9. **Given evidence, the AI over-ran the task boundary.** Once the screenshots were supplied, it did not stop at correcting the checklist: it began recording verdicts — "this is a Fail", "strong candidate finding" — inside a **Task 1A** artefact whose whole purpose is to define *how* to check, and inside a **shared** file that four people submit. It was fluent about *what* it saw and silent about *whether it was allowed to say so*. The student caught this, not the AI, and neither the assignment brief nor the file's own "no Pass/Fail recorded" header prevented it. The lesson generalises past this homework: an AI optimises for the useful-looking answer and does not police the boundary between the deliverable it was asked for and the next one.
10. **What the AI did well:** it was strong at explaining *why it had missed something* once the gap was pointed out; the second, differently-framed pass ("what does the spec require that this file lacks?") found real defects the first could not; and it verified its structural claims by script rather than by assertion, which is why the item counts and traceability tables held up under checking while the prose claims did not.

The transferable principle: the second AI pass found what the first could not, not because the model changed, but because the *question* changed — from "generate a checklist from these materials" to "verify this checklist against this specification". Generation and verification need to be separate prompts with different grounding, and the human has to supply the standard against which the AI's own output is judged.

Points 7–8 sharpen that principle. Reframing the question is not always enough: when the error comes from the AI's **instrument** rather than its reasoning, no amount of re-asking will surface it, because every pass looks through the same instrument. The four survey errors were only exposed when the **type of evidence** changed — from DOM queries the AI ran to screenshots a person took. So the rule is not merely "verify in a separate pass" but "verify against evidence the AI did not produce". And a claim of **absence** deserves more suspicion than a claim of presence: an AI that reports "EMS has no progress bar" is really reporting "my selector matched nothing", and only a human eye can tell those apart.

### Interaction 11 — Scenario-specific gap audit for D and B, and a fabrication boundary held

| Field                        | Value                                                                                                                                                                           |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                                                                                                               |
| **Date / time**        | 2026-07-30 ·_time: TBD_                                                                                                                                                      |
| **Task**               | Task 1A — add checklist items targeting scenarios D and B specifically                                                                                                         |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` **v1.8** (59 items) · `docs/checklist/Reference_Sources_and_Prompts.md` (Prompt 11, Human Review Note 11, outstanding actions 5–7 updated) · this entry |

**Prompt (paraphrased from a multi-turn exchange):** the student asked whether Task 1A met every
clause of the requirement, then — after being told the checklist's "team experience" pillar was thin
(4 of 53 items) and that the AI could not supply that pillar on a teammate's behalf — pushed back:
they only wanted to focus on the checklist step right now, and asked directly for more items to be
added for their own scenario (D) and a groupmate's scenario (B), to maximise the group's score on
criterion 1a.

**AI output:** Held a boundary the AI had raised a turn earlier — declined to write items *framed as*
personal experience for either the student or a teammate who supplied nothing, since that would
misattribute invented content as someone's real frustration using EMS (the same failure mode
criticised in §4 point 7 below). Instead reframed the request as a legitimate, separate kind of
audit: **scenario-scoped** re-reading of §4 Pool D / Pool B and §5 B3/C4, rather than the
**aspect-scoped** re-reading Rounds 1–3 had already done. This surfaced six gaps invisible to an
aspect-organised pass because each is named only in one scenario's own text: the D4 internal-note vs
official-response boundary (§4 names both fields but nothing tested they stay apart on the user
side); D2/D4 cross-role status consistency (a property that only exists once a scenario spans two
roles, which only D does); D3's two named filters (member code, category) never tested for
correctness; B3's secondary-role selector never checked against the admin-side toggle it should
reflect (IA02-07, added in v1.2, tests the toggle's own helper text, not what it produces on the
other role's screen); waitlist visibility (§4 names the field, no item tested its user-facing
consequence); B1's category-browse-plus-search pairing (§4 names both, only search-adjacent status
filtering had an item). Six items added: IA02-15, IA03-14, IA03-15, IA04-14, IA04-15, IA04-16.
Re-verified by script: 13/15/15/16 = 59 items, no duplicate or missing IDs, all 10+6+8 framework
citations still present, evidence still resolves against the 14 screenshots.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. The six scenario-specific items were accepted as script-verified and traceable. The round's other outcome was accepted as correct behaviour rather than a shortfall: the AI declined to write a defect verdict it had not observed, and that refusal is logged deliberately as the boundary being held. These items remain **AI-proposed and not countersigned** by the other three members. The six items are AI-proposed and
script-verified for structure, but content review (are these real gaps, are the citations right, do
the verification steps match the live product) is still owed — the same standard every other
AI-drafted item in this file has already been through.

### Interaction 12 — Full 55-slide completeness check

| Field                        | Value                                                                                                                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Opus 5 (Anthropic)                                                                                                                       |
| **Date / time**        | 2026-07-30 ·_time: TBD_                                                                                                                              |
| **Task**               | Task 1A — verify checklist coverage and slide-rule conformance                                                                                         |
| **Artefacts produced** | `docs/01_Task1A_Shared_GUI_Checklist.md` **v1.9** (60 items) · `docs/checklist/Reference_Sources_and_Prompts.md` (§2d new, Prompt 12, Human Review Note 12) · this entry |

**Prompt (verbatim):** `checklist có bao phủ đc hết k và có tuân theo các quy tắc như trong slide không`

**AI output:** Instead of answering from the existing audit summary — which only enumerates the 11
slide pages already cited — re-extracted the full 55-page deck with PyPDF2 and checked every bullet
against the citation set. Found **one genuine gap**: p.11's "Wrong fields retrieved by queries" and
p.12's "Window object/DB field correspondence" / "Multiple database rows returned, single row
expected" had no citing item, even though both pages were already cited for *other* bullets — this
is why four earlier audit rounds (organised around cited-vs-uncited pages) had walked past it. Added
**IA04-17**, testing whether a detail screen still shows a previous record's data after navigating
directly to a different record's URL — directly relevant to D4, which is reached by exactly this kind
of per-record deep link. Produced a full page-by-page disposition table (`docs/checklist/Reference_Sources_and_Prompts.md` §2d) classifying every one of the other 54 pages as either already cited, or
process/methodology/technique content with no itemisable per-screen rule, or — for pages 29–55 —
out of scope for a *GUI* checklist because they are the usability-testing-methodology half of the
deck, which grounds Task 2 instead.

**Human review and action taken:** Reviewed by **Lê Phạm Kiều Duyên (23127184)** on 2026-08-01, carried across from §4 Human Review Notes of `docs/checklist/Reference_Sources_and_Prompts.md`, where the same outcome is recorded prompt by prompt. **Not yet countersigned by the other three group members** — that sign-off is action 7 in §5 of that file and remains genuinely open. IA04-17 was accepted: a full re-read of all 55 slide pages found two bullets on pages already marked "done" that no item covered — a different question from the cited-vs-uncited *page* check earlier rounds ran. 59 → 60 items, script-verified, IDs unique and contiguous.

### Interaction 13 — Repo scaffolding + first live Task 1B pass on Scenario D

| Field                        | Value                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **AI tool**            | Claude Code — Sonnet 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension                                                                                                                                                                                                                                                   |
| **Date / time**        | 2026-07-30 ·_time: TBD_                                                                                                                                                                                                                                                                                                                                 |
| **Task**               | Repository scaffolding for §15 (README, Git commit log, AI Critique, Task 2/3 templates, findings log) + a real, live first pass of Task 1B on scenario D (D1–D4)                                                                                                                                                                                        |
| **Artefacts produced** | `README.md`, `docs/07_AI_Critique.md`, `docs/08_Git_Commit_Log.txt`, `docs/02_Task1B_Execution_Report_ScenarioD.md`, `docs/05_Bug_Usability_Findings_Log.md` (finding **D-001**), `docs/usability_testing/*` (templates only), `docs/04_Task3_Cross_Platform_Matrix.md` (template only), and screenshots under `reports/evidence_task1b/` |

**Prompt (verbatim, opening message):**

```
hãy đọc yêu cầu cảu HW3, mình mới làm đc task 1A ròi, giờ hãy tạo một repo thật chính xác hoàn chỉnh và format tốt cho btvn này
```

Follow-up clarifications given during the session (paraphrased, since they were answered through
structured question prompts rather than free text): confirmed Task 1B should be executed for real
("tự tạo user rồi tự chạy làm tự động hết"); confirmed Tasks 2 and 3 had no real data yet and should
be templates only ("Chưa có dữ liệu thật nào"); confirmed the overall scope was the full §15
submission scaffold ("Dựng toàn bộ khung nộp bài đúng chuẩn §15"); mid-session, the student supplied
the current live URL after the original ngrok tunnel went offline (`https://prod-dev.ems-fitus.cloud/login?callbackUrl=%2F — nè dùng lại link này`).

**AI output:**

1. Read the full assignment brief and the existing repo state (checklist v1.9, prior 12 AI-audit
   interactions) to establish that Task 1A was complete and Tasks 1B–3 were not.
2. Attempted to reach the assignment's original EMS URL — it returned `ERR_NGROK_3200` (tunnel
   offline). The student supplied a new working URL, and the session continued there.
3. **Declined to enter any password or OTP itself** (per this session's safety rules on credential
   entry), and explicitly asked the student to perform every login/registration step in the browser
   tab instead — student account creation, admin login, and each re-login needed when switching
   roles in the same cookie-sharing browser tab.
4. Filed a real support request on **D1** as the student's own account. During this, found and
   **reproduced twice** a genuine UI defect: selecting the "Request type" dropdown and clicking
   elsewhere within roughly a second intermittently discards the selection or silently swaps it for
   a different option; did not reproduce with a ~2 s pause inserted. Logged as **D-001** (Bug,
   Major) in `docs/05_Bug_Usability_Findings_Log.md`, with before/after screenshots, after first
   correctly ruling out that the AI's own rushed clicking (rather than the product) was the cause.
5. Verified **D2** (empty state before filing, new request visible with `Pending` status after).
6. Logged in as admin, searched the request on **D3**, opened **D4**, wrote a distinctly-worded
   internal note (containing a unique marker string) and a separate official response, and resolved
   the request — observed an immediate success banner and a live sidebar badge-count update.
7. Re-logged in as the student and confirmed on **D2** that the official response shows correctly
   and the internal note's marker string appears **nowhere** in the requester-facing DOM (checked
   via `get_page_text` and the accessibility tree, not by eye alone) — **IA04-14** and **IA04-15**
   scored Pass with this evidence.
8. Generated `docs/02_Task1B_Execution_Report_ScenarioD.md` programmatically from the 60-item
   checklist (one row per item per screen), pre-filling the checklist's own scenario-D N/A
   predictions as unconfirmed hints, and updated the handful of rows actually executed this session
   to real Pass results with evidence references — leaving the remaining majority honestly marked
   `PENDING` rather than claiming a completed 60×4 pass.
9. Built `docs/usability_testing/` and `docs/04_Task3_Cross_Platform_Matrix.md` as explicit **templates only** — the AI declined
   to fabricate Task 2 participants/sessions or Task 3 cross-browser screenshots, consistent with
   §12 and with `usability-test-study`/`cross-platform-matrix` skill guidance.
10. Wrote `README.md` with an intentionally low self-assessment for Tasks 2/3 (0/25 each) reflecting
    that no real fieldwork has happened yet, and `docs/07_AI_Critique.md` (§11) grounded in this session's
    own reproduced-vs-assumed-bug episode and the checklist's earlier documented false-N/A corrections.

**Human review and action taken:** _To be completed by the student before submission — in
particular, the still-`PENDING` majority of the 60×4 execution matrix, Task 2 recruiting, and Task
3 cloud-lab access all require genuine follow-up work this interaction does not substitute for._

## 5. Sessions still to be logged

| Task                                                              | Status                                                                                                                    |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Task 1B — checklist execution on ≥ 3 screens, bug reports       | **Complete** — all 60 items run against all 6 screens (D1–D6), 360 cells, 108 executed, 16 findings. This row read "partially started" until the full pass finished; corrected 2026-08-01. |
| Task 2 — user testing with 5 real participants, Usability Report | Designed, not run — Phase 1 instruments complete (`docs/usability_testing/`), 0 participants recruited                     |
| Task 3 — cross-browser / cross-platform matrix                   | Planned, not run — 20-cell matrix and run plan ready (`docs/cross_platform/00_Run_Plan.md`), 0 cells captured               |
| §7 — Google Form submissions and the aggregated findings log    | **16 findings logged** (D-001…D-019, with D-013/D-014/D-018 retracted); Google Form submission still TODO for all 16. This row read "1 finding" until the full pass finished; corrected 2026-08-01. |
| §8 — Agent Skill and demo video                                 | Skills built and used (`gui-checklist-execution`, `findings-log`, Interaction 13); demo video links TODO              |

Append an interaction entry to §2 for every AI session on the tasks above, following the same format: tool, date/time, verbatim prompt, AI output, human review and action taken.
