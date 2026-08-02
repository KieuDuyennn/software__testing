# Reference Sources & AI Prompts: Shared GUI Checklist

> Group deliverable supporting **Task 1, Part A**. Documents the sources the checklist is grounded in and the full prompt chain used to generate and refine it (required by §6 and §15 of the assignment).
> Companion files: `docs/01_Task1A_Shared_GUI_Checklist.md` (the checklist itself) · `docs/06_AI_Audit_Report.md` (§10 mandatory appendix).
> Checklist version covered: **v2.0, 62 items** (2026-07-30; documentation-only conformance pass
> 2026-08-01, no item added, removed or reworded). Prompt 1 produced v1.0; Prompts 2-4 produced the
> v1.2/66-item conformance pass; Prompts 5-10 reduced and corrected the set via the live-EMS survey
> and the screenshot-verification pass (v1.3 to v1.7); Prompt 11 added 6 scenario-specific items for
> D and B (v1.8); Prompt 12 added 1 item after a full 55-slide completeness check (v1.9).
>
> **§3 below carries the complete chain, all twelve prompts, with nothing delegated to another
> file.** §15 submits this file as the group-level *"AI prompts used to build the checklist"*
> artefact, separately from any individual report, so a reader holding only the group folder must be
> able to see every prompt that shaped the checklist without opening `docs/06_AI_Audit_Report.md`
> (which is an individual §10 appendix). Prompts 5-10 were previously cross-referenced there rather
> than reproduced here; they are now inlined. The two records are the same prompts, not two different
> ones, and `docs/06_AI_Audit_Report.md` remains the fuller log of AI *output* for those rounds.

## 1. Reference Sources

Every source below is cited by at least one checklist item. Sources that grounded no item have been removed, see §4 Human Review Notes for what was removed and why.

| # | Source                                                                 | Type                | Sections / criteria actually used                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Citation                                                                                               |
| - | ---------------------------------------------------------------------- | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| 1 | Nielsen, J., *10 Usability Heuristics for User Interface Design*    | **Article** (heuristic framework) | All ten: H1 Visibility of system status · H2 Match between system and real world · H3 User control and freedom · H4 Consistency and standards · H5 Error prevention · H6 Recognition rather than recall · H7 Flexibility and efficiency of use · H8 Aesthetic and minimalist design · H9 Help users recognize/diagnose/recover from errors · H10 Help and documentation                                                                                                                                                                                                                                                                                                                                                                                                                          | Nielsen Norman Group, 1994 (rev. 2024), https://www.nngroup.com/articles/ten-usability-heuristics/   |
| 2 | Norman, D. A., *The Design of Everyday Things* (Revised & Expanded) | **Book**            | All six principles: P1 Visibility · P2 Feedback · P3 Constraints · P4 Mapping · P5 Consistency · P6 Signifiers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Basic Books, 2013                                                                                      |
| 3 | Shneiderman, B. et al., *Eight Golden Rules of Interface Design*    | **Book** (heuristic framework) | All eight: R1 Strive for consistency · R2 Enable shortcuts for frequent users · R3 Offer informative feedback · R4 Design dialogs to yield closure · R5 Offer simple error handling · R6 Permit easy reversal of actions · R7 Support internal locus of control · R8 Reduce short-term memory load                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | *Designing the User Interface*, 6th ed., Pearson, 2016                                               |
| 4 | **Course slides: `S13_GUI Testing & Usability Testing.pdf`** | **Course slides**   | p.6 GUI elements to test (buttons, checkboxes, radio buttons, dropdown menus, text fields, error messages) · p.7 visual consistency, text overflow, distorted graphics · p.8 accessibility features · p.11-14 Common GUI bugs (data validation · incorrect field default · mishandling of server process failures · mandatory fields not mandatory · field order · currency of data on screens · window modality · focus on objects needing it · state of controls aligns with state of data) · p.16 Checklist testing categories (GUI standards, colour scheme, typography, layout and alignment, labels, error messages) · p.17-18 Navigation testing (main menu,**breadcrumb**, links and buttons, form navigation and focus order) · p.26 Localization and Internationalization | Local file:`refs/slides/S13_GUI Testing & Usability Testing.pdf`                                       |
| 5 | **W3C: Web Content Accessibility Guidelines (WCAG) 2.1**       | **Standard**        | SC 1.1.1 Non-text Content · SC 1.4.3 Contrast (Minimum) · SC 2.2.2 Pause, Stop, Hide · SC 2.4.7 Focus Visible · SC 4.1.3 Status Messages                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | W3C Recommendation, 5 June 2018, https://www.w3.org/TR/WCAG21/                                       |
| 6 | Assignment specification                                               | Assignment spec     | §4 SUT (EMS feature pools A to D; IA-01 to IA-04 definitions, used as the conformance map in the checklist) · §5 suggested screens · §6 Task 1 Part A requirements                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Local file:`refs/requirements/2026.HW03.GUI Usability EMS_En.md` (+ `_Vi.md`)                       |
| 7 | Real EMS interface captures: 14 screenshots, plus the live-EMS survey (14 pages) | Product evidence    | Grounded the EMS-specific items and, from v1.3 onward, superseded six items the survey had gotten wrong (see `docs/06_AI_Audit_Report.md` Interaction 10 for the four factual errors this caught) | Local folder: `reports/screenshots/` · `docs/checklist/EMS_Live_Survey_2026-07-26.md` (both committed to git) |

**Against §6's own list.** §6 Task 1 Part A asks the group to submit "the list of reference sources
you drew on (books, articles, standards, the course slides)". Each of those four categories is
present above and each is cited by at least one item: **books** = rows 2 and 3 (Norman; Shneiderman
et al., *Designing the User Interface*, 6th ed.), **articles** = row 1 (Nielsen, NN/g),
**standards** = row 5 (WCAG 2.1, six success criteria), **course slides** = row 4 (S13, eleven pages
cited individually). Rows 6 and 7 are the assignment text and the product evidence; they are
additional grounding, not substitutes for any of the four.

**Slide-page citations verified against the file, 2026-08-01.** Every page number the checklist
cites was re-extracted from `refs/slides/S13_GUI Testing & Usability Testing.pdf` (55 pages) and the
quoted bullet checked against the extracted text, so no item cites a page that does not exist or a
bullet that is not on it. Spot-values confirmed: p.6 "buttons, checkboxes, radio buttons, dropdown
menus, text fields, and error messages" · p.7 "text overflow, misalignment, and distorted graphics"
· p.8 "checks for accessibility features" · p.11 "Mandatory fields, not mandatory" and "Wrong fields
retrieved by queries" · p.12 "Field order", "Currency of data on screens", "Window object/DB field
correspondence" · p.13 "Correct window modality?", "Focus on objects needing it?" · p.14 "State of
controls aligns with state of data in window?" · p.16 "Color scheme", "Typography", "Layout and
alignment", "Labels", "Error messages" · p.17 "Breadcrumb Navigation: Verify that breadcrumb trails
accurately reflect the user's path and allow users to backtrack" · p.18 "Links and Buttons",
"Form Navigation" · p.26 "Localization and Internationalization".

### Sources considered but not used

| Source                                                                                    | Why it is not in the table above                                                                                                                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| ISTQB Foundation Level Syllabus                                                           | Listed in §17 of the assignment as general course reading, but it contains no GUI-checklist or per-widget material, and**no checklist item cites it**. Listing an uncited source would misrepresent the grounding. It is expected to be relevant later for defect-severity terminology in the Task 1B bug reports, not for Task 1A. |
| `refs/slides/EN.UsabilityTesting.pdf`, `refs/slides/GUI-VulqUpdated.UsabilityTesting.pdf` | Cover usability-testing method (test plan format, task selection, Likert/semantic-differential questionnaires, performance vs preference data, severity × probability analysis). These ground**Task 2**, not the Task 1A checklist, and are cited in the Task 2 report instead.                                                     |
| `refs/slides/Testing GUI Applications.pdf`                                                | The file could not be opened during the v1.2 audit (`PdfReadError: EOF marker not found`; the PDF appears truncated). Nothing was cited from it because nothing could be read from it. Re-downloading it is tracked as §5 action 4.                                                                                                     |

## 2. Source-to-Item Traceability

> Tables 2a and 2b below are **machine-regenerated** from `docs/01_Task1A_Shared_GUI_Checklist.md`'s own
> *Reference Source* column, using `.claude/skills/gui-checklist-design/scripts/check_checklist.py
> --emit-traceability`, the same command re-derives them from any future version, so drift like
> the v1.2→v1.7 staleness this file previously had cannot happen silently again. Regenerated
> **2026-08-01** against **v1.9 (60 items)**, after the one citation change of that date (IA01-04
> gained its S13 p.16 *Typography* citation); script exit 0, IDs unique and contiguous, all 10+6+8
> framework citations present, evidence resolves against `reports/screenshots/`.

### 2a. By framework

| Source | Items citing it |
| --- | --- |
| Nielsen H1 | IA01-06, IA01-07, IA01-11, IA02-14, IA03-01, IA03-03, IA03-05, IA04-04, IA04-05, IA04-07, IA04-10, IA04-13, IA04-16 |
| Nielsen H2 | IA04-01, IA04-14 |
| Nielsen H3 | IA03-04, IA03-10, IA03-13 |
| Nielsen H4 | IA01-01, IA01-03, IA01-08, IA01-09, IA02-11, IA03-02, IA03-06, IA03-07, IA03-14, IA04-15 |
| Nielsen H5 | IA02-03, IA02-04, IA02-06, IA02-09, IA02-11, IA02-13, IA04-03 |
| Nielsen H6 | IA01-10, IA02-02, IA02-12, IA03-15 |
| Nielsen H7 | IA03-01 |
| Nielsen H8 | IA01-04 |
| Nielsen H9 | IA02-08, IA04-08, IA04-11 |
| Nielsen H10 | IA02-05 |
| Norman P1 | IA03-08 |
| Norman P2 | IA02-05, IA02-07, IA03-12, IA04-09 |
| Norman P3 | IA02-01, IA02-03, IA03-05, IA04-14 |
| Norman P4 | IA02-10, IA02-15 |
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
| p.11 | IA02-01, IA02-04, IA02-06, IA02-11, IA04-11, IA04-17 |
| p.12 | IA02-14, IA03-08, IA04-05, IA04-17 |
| p.13 | IA01-12, IA04-02 |
| p.14 | IA03-08 |
| p.16 | IA01-01, IA01-03, IA01-04, IA02-02, IA02-08, IA04-01 |
| p.17 | IA03-01, IA03-03, IA03-11 |
| p.18 | IA02-10, IA03-13 |
| p.26 | IA01-08, IA01-09 |

The 6 v1.8 items (IA02-15, IA03-14, IA03-15, IA04-14, IA04-15, IA04-16) cite Nielsen/Norman and the
assignment's own §4/§5 text rather than a slide page, none introduces a new slide citation, so this
table is unchanged in which pages appear, only in which items each Nielsen/Norman row now includes.

### 2d. Full 55-page slide-deck coverage check (v1.9)

The student asked directly whether the checklist covers everything and follows the slides' rules.
Rather than answer from memory, the deck was re-extracted page by page (`PyPDF2`, all 55 pages) and
checked against the citation set above. Result: **one genuine gap found and closed (IA04-17, see
Round 5 in the checklist)**; everything else on pages 1-28 (the GUI-testing half of the deck) is
either already cited or is not an itemisable per-screen rule:

| Pages | Content | Disposition |
| --- | --- | --- |
| p.1-5, 9 | Title, agenda, definitions, purpose, brand/compliance rationale for GUI testing | Conceptual framing, not a testable rule, nothing to cite |
| p.6, 7, 8 | Common elements; visual consistency; usability/accessibility | **Cited** (IA02-12; IA01-08, IA01-11; IA01-13, IA04-12) |
| p.10 | Section header only | No content |
| p.11 | Data validation, incorrect field default, mishandling of server failures, mandatory fields, **wrong fields retrieved by queries** | First four bullets **cited**; fifth was the v1.9 gap, now **IA04-17** |
| p.12 | Incorrect search criteria, field order, **multiple rows returned single expected**, currency of data, **window/DB field correspondence** | "Field order" and "currency of data" **cited**; the two bold bullets were the other half of the v1.9 gap, now **IA04-17**. "Incorrect search criteria" is partially covered by IA03-14 (D3 filters) and IA02-10 (search-box Enter behaviour), though neither is a full match, a candidate for a future round if search-result correctness itself needs its own item |
| p.13, 14 | Window modality, control/menu state vs data state, focus | **Cited** (IA01-12, IA04-02); the near-duplicate p.13/p.14 bullets about control state are covered jointly by IA03-08 and IA04-05/07 |
| p.15 | Section header only | No content |
| p.16, 17, 18 | Low-level checklist categories; navigation testing (menu, breadcrumb, links, form focus order) | **Cited.** p.16 → IA01-01 (Typography, Layout and alignment), IA01-03 + IA04-01 (Color scheme), IA01-04 (Typography, citation added 2026-08-01), IA02-02 (Labels), IA02-08 (Error messages) · p.17 → IA03-01, IA03-03 (Main Menu Navigation), IA03-11 (Breadcrumb Navigation) · p.18 → IA02-10 (Form Navigation), IA03-13 (Links and Buttons) |
| p.19 | Test-design **techniques** (equivalence partitioning, BVA, decision tables, state-transition) | Technique catalogue for functional testing generally, not a GUI-checklist rule, out of scope for this artefact |
| p.20, 21 | Integration level, non-functional level (soak, compatibility, platform/environment) | Testing-**level** categories, not per-screen rules; compatibility/platform testing is Task 3's concern (`cross-platform-matrix` skill), not Task 1A's |
| p.22-25, 27 | Challenges in GUI testing: platforms, UI churn, coverage, test data/environment, backend integration | Process/methodology guidance for running a testing *effort*, not itemisable per-screen rules |
| p.26 | Localization / internationalization challenge | **Cited** (IA01-08, IA01-09) |
| p.28 | Automation in GUI testing (manual vs automated mapping) | Process guidance on *how* to execute, not a UI rule to check |
| p.29-55 | Usability-testing methodology: test types, test plans, evaluator selection, performance/preference data, questionnaires (Likert, semantic differential, branching), data analysis | **Out of scope for this Task 1A checklist by design**. This half of the deck grounds **Task 2** (the `usability-test-study` skill already cites the relevant method literature). Nothing here is a GUI-checklist item; citing it here would blur what each task's report should ground itself in. |

**Answer to "does it cover everything":** for the half of the deck this checklist is actually meant
to ground itself in (GUI testing, p.1-28), yes, after v1.9: every bullet that names a checkable
per-screen property has a citing item, and every uncited bullet is conceptual framing, a technique
catalogue, or process guidance rather than a rule. The usability-testing half (p.29-55) is
deliberately not covered here; it belongs to Task 2's report, not Task 1A's checklist.

### 2c. By screenshot: superseded by the live-EMS survey

The v1.2 version of this table mapped items to exact screenshot filenames. That mapping style no
longer matches how the checklist is written: from v1.3 onward (Interactions 5-8, `docs/06_AI_Audit_Report.md`),
items are grounded primarily in the **live EMS survey** (`docs/checklist/EMS_Live_Survey_2026-07-26.md`, 14 pages
inspected) and reference screens by name in the Verification Rule prose (e.g. "the Add/Edit Event
form"), not by embedding a filename. Re-scanning v1.7 for literal filename strings finds only 2
matches (`IA01-04` and `IA04-13`, both citing `Admin_A2_AddEditEvent.png`), which would misrepresent
the grounding as far thinner than it is.

The real per-item grounding evidence is: (1) the framework/slide citations in 2a/2b above, (2) the
survey document for what the live product actually contains, and (3) `check_checklist.py
--evidence-root reports/screenshots` returning **0 unresolved evidence references** against the 14 committed
screenshots: every image any item does name resolves to a real file, not a broken link.

## 3. AI Prompt Chain

The assignment (§2) requires guiding the AI through each step of the technique rather than issuing one generic prompt. The chain below is the complete record: every prompt that shaped the checklist, in order. It stays consistent with `docs/06_AI_Audit_Report.md`.

> **How these prompts are recorded, and which are verbatim.** The working language of these sessions
> was mixed Vietnamese and English. Two conventions are used below and each prompt says which
> applies to it:
>
> - **Prompts 1-4, 11 and 12 are normalised English renderings.** The raw messages for those rounds
>   were long, multi-step instructions typed partly in Vietnamese; they are written out in full
>   English so the scope, the constraints and the standard the output was held to are all visible.
>   Nothing has been added that was not asked for, and no prompt appears here for an exchange that
>   did not happen. The original Vietnamese of Prompt 1 is preserved verbatim in
>   `docs/06_AI_Audit_Report.md`, Interaction 1.
> - **Prompts 5-10 are reproduced verbatim, exactly as typed, in the original Vietnamese**, with a
>   literal English gloss beside each. Those rounds were driven by short, elliptical one-line
>   messages, and normalising a one-liner into a paragraph would document the intent rather than the
>   instruction. They match `docs/06_AI_Audit_Report.md` Interactions 5-10 character for character.
>
> The verbatim prompts still name the folder layout as it stood in July (`checklist/`, `docs/`,
> `Shared_Group_Artifacts/`, `screenshots/`); HW03 was reorganised into `docs/` · `reports/` ·
> `refs/` on 2026-08-01 and rewriting a verbatim prompt to match would falsify the record. The
> mapping is given in `docs/06_AI_Audit_Report.md`'s Path note.

### Prompt 1: Initial generation, grounded in references and real screenshots

- **AI tool**: Claude Code (Sonnet 5, Anthropic)
- **Date / time**: 2026-07-25, 20:40 to 21:25
- **Prompt** (normalised from the original):
  ```
  I have assembled the full set of reference material and real EMS interface captures under `docs/`.
  We are now going to produce the group's Shared GUI Checklist (more than 40 items). Please work
  through the following steps in order rather than generating the whole thing in one pass:

  1. Read and analyse the reference documents in `docs/`:
     - `docs/requirement.md` (in particular Section 4 and Section 6)
     - `docs/Nielsen_10_Usability_Heuristics.md`
     - `docs/Norman_6_Principles.md`
     - `docs/Shneiderman_8_Golden_Rules.md`

  2. Examine the images in `docs/screenshots/`: go through the real EMS screen captures and identify
     the actual layout structure and the widgets the product genuinely contains (forms, rich-text
     editor, modals, toasts, tables, date pickers, 4:3 / 24:9 uploads, QR codes, and so on). I want
     the checklist grounded in what is on screen, not in a generic template.

  3. Generate the checklist: combine the UI/UX theory with what you observed in the captures, and
     produce exactly 48 items, distributed as exactly 12 items for each of IA-01, IA-02, IA-03 and
     IA-04. Write the result directly into `Shared_Group_Artifacts/Shared_GUI_Checklist.md` as a
     Markdown table with the columns: Item ID | Aspect | Reference Source | Verification Rule (tied
     to the real EMS interface) | Expected Behavior.

  4. Update the log at `Shared_Group_Artifacts/Reference_Sources_and_Prompts.md`: list every
     reference document and image folder you actually drew on, and record this prompt.
  ```
- **AI output summary**: Read the four reference files plus §4 and §6 of the requirement, inspected all 14 EMS screenshots, and generated exactly 48 items (12 per IA) with the five requested columns, each citing a Nielsen/Norman/Shneiderman principle and, where applicable, the screenshot it was grounded in. Result: checklist **v1.0**.
- **Human review outcome**: Accepted as a draft only, after reading all 48 items against the group's own memory of using EMS. The review found a *structural* bias rather than individual bad items: every item described something visible in a still image, so nothing tested keyboard interaction and nothing tested an HTML/ARIA attribute. Neither leaves a visual trace, so neither was reachable from the AI's grounding. Four items were written by hand to close that class of gap (keyboard focus ring, `alt` text, Enter-to-submit, ESC-to-close), giving checklist **v1.1 (52 items)**. The category of blindness is recorded in the checklist's own "why the AI missed it" table, because it mattered to every later round more than the four items did.

### Prompt 2: Conformance review against the assignment text

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26, 09:15 to 09:50
- **Prompt** (normalised from the original):
  ```
  I am working on HW03. Read the assignment brief itself first, both the English and Vietnamese
  versions, since I want to be sure nothing is lost between them, and then assess whether the
  checklist I currently have actually satisfies what is being asked, rather than merely looking like
  a plausible checklist.

  Judge it against the brief, not against your own idea of a good checklist. I want to know
  specifically: which requirements it meets, which it only appears to meet, and which it misses
  outright. Use everything available to you in the repository, including the supporting artefacts,
  not just the checklist file. If the checklist claims something the other files contradict, that
  counts as a finding. Be direct about problems; a review that tells me it is fine is of no use.
  ```
- **AI output summary**: Read both the EN and VI requirement files and the two checklist artefacts, then reported: the prompt chain contained only one prompt; the Human Review Notes table was empty while the changelog claimed the review was complete; every referenced path (`docs/`, `Shared_Group_Artifacts/`) was absent from the repository; WCAG was cited by three items but missing from the sources table; the sources table columns were misaligned and ISTQB plus the course slides grounded no item. It also flagged four missing IA elements and a logic error in IA04-07.
- **Human review outcome**: Each finding was checked against the files before being accepted, which was possible precisely because every one was stated as something falsifiable (a path that does or does not exist, a source that is or is not cited) rather than as an opinion. All confirmed. The empty Human Review Notes finding was the uncomfortable one, since the changelog had already claimed the review was done; accepting it is why this file now records review outcomes prompt by prompt instead of as a blanket statement. Scope was narrowed in Prompt 3, because Tasks 1B to 3 had not started and a review spanning them would have produced advice nobody could act on.

### Prompt 3: Coverage audit, clause by clause

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26, 10:05 to 10:40
- **Prompt** (normalised from the original):
  ```
  I have read your previous findings and accepted them; the repository-hygiene problems I can fix
  myself. Right now only the checklist stage exists, Tasks 1B, 2 and 3 have not started, so narrow
  the scope accordingly and concentrate on one question: does this checklist actually cover what it
  is required to cover, and does it obey the rules the assignment sets for it?

  Please audit it systematically rather than impressionistically. Go clause by clause through §6's
  Task 1A requirements; then take the §4 definitions of IA-01 to IA-04 and check that every UI
  element named there has at least one item pointing at it; then check the widgets the assignment
  itself names; then check whether all three heuristic frameworks are genuinely cited or only
  mentioned; and finally check each item individually for whether it could ever produce a Fail. An
  item nobody can fail is decoration, not a test. Tell me what is missing and what is wrong, with
  the specific item IDs.
  ```
- **AI output summary**: Audited the checklist on the five requested axes. Produced: three §4 elements with zero items (breadcrumbs, drag-and-drop reorder, progress bars); six widgets with zero items (carousel, date picker, dropdown/select, radio/checkbox, table sorting, QR/barcode); the absence of any failure-feedback item across all of IA-04; one factually wrong item (IA04-07); Nielsen H3 and Shneiderman R3/R4/R5 uncited while Norman P4 was used as a catch-all in five items; and the lack of an N/A convention for a checklist shared across four scenarios.
- **Human review outcome**: All findings accepted after checking each against the checklist text. Two were checked especially closely, because accepting them changes real work: IA04-07 was verified by reasoning through what it would score on a correctly paginated table (a Fail, wrongly), and the Norman P4 over-use by re-reading Norman's own definitions of Mapping, Signifiers and Constraints for the five items concerned. At least three were genuinely misfiled. The most valuable finding was the missing *failure-feedback dimension* across all of IA-04, because it is a gap in a dimension rather than in an item, and no per-item read would have surfaced it. Applied in Prompt 4.

### Prompt 4: Apply the fixes

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26, 11:00 to 12:30
- **Prompt** (normalised from the original):
  ```
  I have gone through the gap list and I accept all of it. Apply the corrections properly, not a
  patch over the surface, but the underlying fixes: close the coverage gaps with real items, correct
  the items that are factually wrong, re-source the citations attached to the wrong principle, and
  add the N/A convention the shared checklist needs.

  Two conditions. First, before you cite the course slides, actually extract and read them. They
  are currently listed as a source with nothing drawn from them, which is exactly the kind of
  overstated grounding you flagged in your own review, and I do not want to fix that by deleting the
  source if the slides genuinely have material we should be using. Second, write the outcome into
  both the checklist file and the AI audit file as you go, so the record of what changed and why is
  created at the same time as the change and not reconstructed from memory afterwards.
  ```
- **AI output summary**: Before editing, extracted the text of `refs/slides/S13_GUI Testing & Usability Testing.pdf` so that the course slides could be cited by page rather than listed without use. This surfaced slide p.17 (*Breadcrumb Navigation*), p.6 (the GUI element list), p.11 (*Mishandling of server process failures*) and p.26 (*Localization and Internationalization*), which independently confirmed four of the gaps found in Prompt 3. Then rewrote `docs/01_Task1A_Shared_GUI_Checklist.md` to **v1.2 / 66 items**: added 14 items, applied 14 corrections, merged the duplicated IA02-03/IA02-04 pair and repurposed IA02-04 to cover upload-constraint enforcement, added the Pass/Fail/N/A convention, a §4 conformance map, a per-widget map and a framework-coverage table. Rewrote this file and created `docs/06_AI_Audit_Report.md`. Item IDs were verified programmatically: 17/17/17/15, no duplicates, no gaps.
- **Human review outcome**: The v1.2 diff was reviewed in full, 14 added items and 14 corrections, and accepted, with one objection carried into the next round. The four independently-confirmed slide pages were treated as the strongest part of the output, because they came from a source the earlier audit had not consulted and yet agreed with it. The objection: **66 items is not an instrument, it is a wish list.** Four members by four screens by 66 items is 264 cells each, which guarantees either shallow execution or invented results, and the checklist's whole value depends on every recorded row being real. That objection became the size-reduction instruction recorded as Interaction 6 in `docs/06_AI_Audit_Report.md`.

### Prompt 5: Survey the live EMS so items describe the real product

- **AI tool**: Claude Code (Opus 5, Anthropic), driving the student's own Chrome via the Claude in Chrome extension
- **Date / time**: 2026-07-26 (exact clock time not captured; see the outstanding-actions note)
- **Prompt** (verbatim, in order, three messages):
  ```
  ok bật claude-in-chrome đi, mình mở Chrome rồi
  ```
  ```
  mình chỉ cần bạn xem để tạo ra checklist thôi chưa cần test thật
  ```
  ```
  claude in chrome để bạn quan sát và viết checklist đúng và hợp lí nhất, chưa test thật để tiết kiệm token
  ```
  *English gloss:* "turn on claude-in-chrome, I have Chrome open" / "I only need you to look, in order to
  build the checklist, not to run real tests yet" / "claude in chrome is so you can observe and write the
  most correct and sensible checklist; no real testing yet, to save tokens."
- **AI output summary**: Opened the EMS URL, reached the login page and **stopped, asking the student to log in**; it was given no credentials and entered none. From the authenticated session it surveyed seven pages (participant dashboard, admin dashboard, Events Management, Categories, event detail, event edit form, 404), mainly by DOM query rather than screenshot at the student's explicit request. Reported that **six checklist items described widgets EMS does not have** (no carousel, no breadcrumb, no drag-and-drop reorder, no column sorting, no native date input on the event form, no progress bar) and that no `aria-live` region and no programmatic `required` existed on the surveyed pages. Result: checklist **v1.3**, EMS widget inventory added.
- **Human review outcome**: Accepted and applied at the time. **Partly overturned five rounds later, and the reversal is the outcome of record**: Prompt 10's screenshot check found four of this survey's "not found" results to be wrong (bar meters, an icon-only back control, native date inputs on the Support filters, plus a user-typed string misread as a rendered date). Three of the four are false negatives in the same direction: a DOM selector proves presence but never absence. Nothing from this round survives unchecked; every claim it produced was re-verified against human-captured screenshots in Prompt 10, and the ones that failed are listed in the corrections block at the top of `docs/checklist/EMS_Live_Survey_2026-07-26.md`.

### Prompt 6: Grounding-pillar assessment and reduction to an executable size

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26 (exact clock time not captured)
- **Prompt** (verbatim, in order, two messages):
  ```
  ghi vào referecne source and prompt cho mình, checklist đó theo như mình học thì phải thiết kế dựa trên
  quy tắc chuẩn trên thế giới, các heuristica, web thật cần test và dựa vào kinh nghiệm thfi phải.
  Bạn thiết kế checklist cho mình đã phủ đủ hết các yếu tố đó chưa. Giới hạn khoảng 52 test thôi vì nhiều quá làm không hết
  ```
  ```
  hãy lưu lại các thông tin về web hôm nay bạn đã cap và live, để làm thông tin cho test thật để tiết kiệm token
  ```
  *English gloss:* "write it into reference source and prompt for me; as I was taught, that checklist has to
  be designed on international standard rules, the heuristics, the real web under test, and on experience.
  Has the checklist you designed covered all of those factors? Limit it to about 52 tests, any more and we
  cannot finish them." / "save the information about the site you captured and viewed live today, as input
  for the real testing, to save tokens."
- **AI output summary**: Assessed the checklist against the **four grounding pillars the student named** (international standards, heuristics, the real system under test, personal experience) and reported the first three strong and the fourth weak at **4 of 66 items**. Reduced 66 → **52 items** (5 merges, 8 removals) choosing removals so that none took the sole carrier of a framework citation or of a §4-named element, renumbered contiguously, published a v1.3→v1.4 ID map, and verified by script (13/14/13/12 = 52). Saved the live-web observations as `docs/checklist/EMS_Live_Survey_2026-07-26.md`.
- **Human review outcome**: The ~52 cap was the student's own instruction, not the AI's proposal, and it came from the objection recorded under Prompt 4: 66 items × 4 screens × 4 members guarantees either shallow execution or invented results. The reduction was accepted after checking that the framework and §4 coverage tables still held. **The pillar-4 finding was accepted and assigned back to the members rather than closed by the AI** — that assignment is still open, see §5 action 6, and it is the one finding from this round that no later round has discharged.

### Prompt 7: Complete the survey for scenarios C and D; add the Export item

- **AI tool**: Claude Code (Opus 5, Anthropic) via Claude in Chrome
- **Date / time**: 2026-07-26 (exact clock time not captured)
- **Prompt** (verbatim, in order, two messages):
  ```
  chưa khảo sát users management và support request là sao, là bạn chưa tạo các TC liên quan tới các phần này á hả
  ```
  ```
  khảo sát nốt 2 trang đó luôn đi, thêm item Export
  ```
  *English gloss:* "what do you mean users management and support request have not been surveyed, does that
  mean you have not created the test cases related to those parts?" / "go ahead and survey those two pages
  as well, and add an Export item."
- **AI output summary**: First corrected the student's inference: the checklist *did* contain items naming Users-Management (17) and Support-request (14) widgets, but none had been verified against the live product, leaving them exposed to the same failure that had already forced six rewrites in v1.3. While counting it found that **Export to Excel was covered by exactly one sub-clause** of another item although §5 C4 names it as a candidate screen. Surveyed both areas, added **IA04-13 (Export to Excel)**, corrected IA03-07 (support requests use path-segment deep links where events use `?id=`) and widened IA03-02 (Pending/Resolved are plain `<button>`, not `role="tab"`). Also recorded for scenario C that Assign Role, Block/Unblock and Reset Password are **not** row-level actions. Result: **v1.5, 53 items**, script-verified 13/14/13/13.
- **Human review outcome**: The Export gap was accepted immediately, because it is checkable against the assignment's own §5 C4 wording rather than against an opinion. The AI's correction of the student's premise was also accepted: "has an item" and "has a *verified* item" are different claims, and conflating them is exactly what produced the v1.3 rewrites. The scenario-C note (no row-level Assign Role / Block / Reset Password) was later confirmed in Prompt 10 to go further than recorded here — **Reset Password is absent from the admin UI entirely** — which is a discrepancy against §5's own C3 description and is owed to whoever owns scenario C.

### Prompt 8: Survey the participant-side screens

- **AI tool**: Claude Code (Opus 5, Anthropic) via Claude in Chrome
- **Date / time**: 2026-07-26 (exact clock time not captured)
- **Prompt** (verbatim, single message):
  ```
  khảo sát nốt các trang phía người dùng luôn đi
  ```
  *English gloss:* "go ahead and survey the user-side pages as well."
- **AI output summary**: Surveyed the public event detail page, My Requests, the Create Support Request form and `/profile`, bringing the session total to **14 pages**. **Nothing was submitted**: filing a support request or registering for an event would write to a system shared by the whole class, so the survey stopped at inspection. Reported a scope blocker rather than a checklist defect: the session ran as `admin@gmail.com`, and EMS withholds registration from administrators ("Admin can view role information only (no registration action)"), so scenario B's screens appeared unreachable. Sharpened IA02-01 (`required` on three fields of the user form, zero on the admin event form despite red asterisks, the asterisk likely CSS-drawn and outside the accessibility tree), IA04-13 (a third Export, on `/profile`) and IA01-11 (QR reachable via `/profile`). Result: **v1.6**, still 53 items.
- **Human review outcome**: The three item sharpenings were accepted and remain in the current checklist. **The blocker was accepted at the time and later retired**: Prompt 10 established from the screenshot set that the participant screens had in fact been captured from a student account (`tien@gmail.com`) that already held a registration, so the "first task on the critical path" this round created was misdirecting the group. The lesson kept from it is the narrower true statement, that an *admin* session cannot exercise the B path, which survives as a role-based-UI note rather than as a scheduling constraint. The refusal to submit anything into a shared system was the correct call and was not overridden.

### Prompt 9: Split the four scenarios across the four members (§5)

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26 (exact clock time not captured)
- **Prompt** (verbatim, single message):
  ```
  chia theo pool cho 34 thành viên luôn giúp mình
  ```
  *English gloss:* "please also split it by pool for the 3-4 members" (`34` is a typo for "3-4", the group
  size §1 of the assignment allows).
- **AI output summary**: Assigned the four members to scenarios A-D with no shared screens, and gave B, C and D **four** screens each rather than the minimum three, on the grounds that the survey indicated each would otherwise carry too many N/A items. Produced the per-scenario N/A prediction table so members could size the work before executing. Result: the *Scenario assignment* and *Predicted N/A by scenario* sections of the checklist.
- **Human review outcome**: The split was reviewed against §5's no-duplication rule (four members, four distinct scenarios, no screen appearing twice) and adopted as the group's committed assignment; the justification for taking four screens on B, C and D is written into the checklist rather than left implicit, because §5 requires a stated reason for choosing screens beyond the suggested set. **One prediction in this output was later found wrong** and is corrected in the checklist: IA04-13 was predicted N/A for scenario A on the grounds that the Events list has no Export button, but an Export button exists on the Registrants tab, which is §5 A4's own Export. Confirmation of the assignment by the other three members is tracked as §5 action 7.

### Prompt 10: Verify every claim against the committed screenshots, then apply the corrections

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-26 (exact clock time not captured)
- **Prompt** (verbatim, in order, three messages):
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
  *English gloss:* "I am doing HW03; the requirements are in the requirements folder, the study material in
  references, and the checklist folder holds the checklist shared by the whole group. Please read and review
  whether my checklist is correct and appropriate for the requirements, whether anything is missing or
  redundant, or whether there is any problem." / "I have now also supplied the screenshots in the screenshot
  folder, and EMS_live_survey; you can use those to verify the checklist file." / "ok, please fix it."
- **AI output summary**: The first pass ran **without product evidence** and verified the structural claims by script rather than by assertion (53 items at 13/14/13/13, no duplicate or missing IDs, traceability tables regenerated from the checklist's own citation column), reporting process gaps: IA02-04 added but absent from the "why the AI missed it" table, a missing interaction entry, stale IDs and page counts, `TBD` times. The second pass, once the 14 screenshots were supplied, compared every claim against the images and found **four factual errors, all originating in the AI's own earlier live survey**, each of which would have produced a wrong Task 1B result: (1) EMS *does* have bar meters (the Rating summary), (2) the admin event detail *does* have an icon-only ← back control, (3) `8:07 25/07` is a user-typed request title, not a rendered date, (4) the Support filters *do* use native date inputs. Three scope corrections followed: the scenario-B account blocker is spent; Export exists in **four** places, not three; and §5's C3 does not exist as described (Reset Password is absent from the admin UI). Applied across the four files as **v1.7, still 53 items**, none added or removed.
- **Human review outcome**: The student authorised each fix after checking it against the images, and then **made a correction to the AI's work that the AI had not caught**: it had written suspected defects into the *shared* checklist, phrasings such as "this is a Fail" and "candidate finding" attached to named screens. That is out of scope for Task 1A, which designs the instrument and records no results, and in a shared artefact it is worse than premature, because §18 permits only the checklist itself to be identical across the group, so four members would have filed four identical Findings Logs against §7's cross-check. On instruction every suspected defect was stripped from the group artefacts, leaving verification rules, expected behaviour, the widget inventory and a neutral list of areas to examine. **No Pass/Fail exists anywhere in the Task 1A deliverables**, which is what the *Why this file contains no findings* section of the checklist now states explicitly. The transferable finding, and the one carried into the §11 AI Critique: four AI-run passes had failed to catch these four errors, and they fell in minutes once evidence the AI had not produced was used as the control.

### Prompt 11: Scenario-specific gap audit for D and B

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-30, 09:20 to 10:40
- **Prompt** (normalised; delivered across several turns, including a pushback on the AI's first
  answer):
  ```
  [first] Check Task 1A once more against every clause of the requirement and tell me where it still
  falls short of full marks on criterion 1a.

  [after being told the team-experience pillar was thin, 4 of 53 items, and that the AI would not
  write items on a teammate's behalf] Understood, and I am not asking you to invent anyone's
  experience. Set that pillar aside for now; I will handle it with the group. What I want from this
  session is narrower: re-read the assignment's own scenario text, Pool D and Pool B in §4, and B3
  and C4 in §5, and check the checklist against that specifically. Every audit round so far has
  been organised by interface aspect, and I think a scenario-scoped read asks a different question
  and will surface different gaps, because some requirements are named only inside one scenario's
  description and an aspect-by-aspect pass walks straight past them.

  Add items for anything that turns up, cite where in the assignment text each one comes from, and
  re-run the verification script. Do not pad the count: if a scenario-scoped read finds nothing, say
  so and we keep 53.
  ```
- **AI output summary**: Declined to invent items framed as the checklist's "team experience" pillar
  (personal frustration is not something an AI can supply on a teammate's behalf, see
  `docs/06_AI_Audit_Report.md` §4, points 7-8, on why fabricating that pillar would misrepresent the
  checklist's own grounding claim). Instead ran a **scenario-specific audit pass**: re-reading §4
  Pool B / Pool D and §5 B3/C4 against the current 53-item checklist to find what a *scenario-scoped*
  re-read surfaces that the earlier *aspect-scoped* Rounds 1-3 did not. Found and added 6 items:
  D4 internal-note/official-response boundary (IA04-14), D2/D4 cross-role status consistency
  (IA04-15), D3 member-code+category filter correctness (IA03-14), B3 secondary-role selector
  reflecting the admin-side toggle (IA02-15), waitlist visibility (IA04-16), B1 category+search
  (IA03-15). Checklist: **v1.8, 59 items**. Re-verified by script: 13/15/15/16 = 59, no duplicate or
  missing IDs, all 10+6+8 framework citations still present, evidence still resolves.
- **Human review outcome**: Each of the six items was traced back to the specific sentence of §4 or
  §5 the AI claimed it came from, and all six resolve. This was checked deliberately, because the
  risk in a "find me more items" request is exactly that the AI returns plausible items with
  invented provenance. **The AI's refusal to write personal-experience items was accepted as
  correct**, and is recorded here rather than quietly dropped: writing them would have raised the
  item count and the apparent pillar coverage at the cost of making the checklist's central
  grounding claim false. Two of the six (IA04-14, IA04-15) later scored Pass under real execution in
  Task 1B via the internal-note marker-string test, which is the practical vindication of the round.
  Content review by the other three members is still owed on all six, see §5 action 7.

### Prompt 12: Full slide-deck completeness check

- **AI tool**: Claude Code (Opus 5, Anthropic)
- **Date / time**: 2026-07-30, 11:00 to 12:10
- **Prompt** (normalised from the original):
  ```
  Two questions, and please do not answer either from the audit summary already in the repository.
  That summary only lists the slide pages we have cited, so using it to check our coverage would be
  circular.

  First: does the checklist genuinely cover everything it should? Second: does it follow the rules
  the course slides actually lay down? To answer honestly you will need to re-extract the whole deck
  and read all 55 pages, not the 11 already cited, and check bullet by bullet rather than page by
  page. A page we have already cited for one bullet can still contain a bullet nothing covers, and
  that is exactly the gap our earlier rounds would have been blind to.

  Where a page has no matching item, tell me which of two reasons applies: it is a real gap we
  should close, or it is not the kind of content a per-screen GUI checklist can hold at all. I want
  that disposition written down page by page so the coverage claim is auditable instead of asserted.
  ```
- **AI output summary**: Rather than answer from the existing audit summary (which only lists the 11
  pages already cited), re-extracted all **55 pages** of `S13_GUI Testing & Usability Testing.pdf`
  with PyPDF2 and checked every bullet against the checklist's citation set. Found one real gap split
  across two already-cited pages: p.11 "Wrong fields retrieved by queries" and p.12 "Window
  object/DB field correspondence" / "Multiple database rows returned, single row expected", missed
  by every earlier round because those rounds tracked cited-vs-uncited *pages*, not cited-vs-uncited
  *bullets within a page*. Added **IA04-17**. Checklist → **v1.9, 60 items**. Also produced the
  page-by-page disposition table in §2d above, and confirmed pages 29 to 55 (usability-testing
  methodology) are correctly out of scope for this checklist, since they ground Task 2 instead.
- **Human review outcome**: The disposition table was reviewed page by page against the deck rather
  than accepted wholesale, since a table classifying 54 pages as "correctly not covered" is exactly
  the kind of output that can be quietly self-serving. Three classifications were checked closely,
  p.19 (test-design techniques), p.20 to 21 (testing levels) and p.29 to 55 (usability methodology),
  and all three hold: none contains a per-screen rule a GUI checklist could carry, and the p.29 to
  55 material genuinely belongs to Task 2's report. The single gap was accepted and IA04-17 added.
  The finding underneath it is what is worth keeping: four previous audit rounds missed this because
  they all asked the same question at the same granularity (cited page versus uncited page), and
  changing the granularity, not the model, not the prompt style, is what found it.

## 4. Human Review Notes

What the group changed, removed, or added after reviewing raw AI output, and why.

| #  | Round             | Change                                                                                                                                           | Rationale                                                                                                                                                                                                              |
| -- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 1  | v1.1 (2026-07-25) | Added 4 items: IA01-12 keyboard focus ring, IA01-13 image`alt` text, IA02-10 Enter-to-submit, IA03-10 ESC-to-close                             | The AI's grounding was a set of static screenshots. Keyboard interaction and ARIA/HTML attributes have no visual trace in a still image, so this class of defect was structurally invisible to it.                     |
| 2  | v1.2 (2026-07-26) | Removed ISTQB Foundation Level Syllabus from the sources table                                                                                   | It grounded no checklist item. §6 requires the checklist to be*grounded in* its sources; listing a source nothing cites overstates the grounding. Retained as future reading for defect severity in Task 1B.        |
| 3  | v1.2              | Added the course slides as a**page-cited** source instead of a bare title, and added WCAG 2.1 with the five specific success criteria used | v1.1 listed the slides without drawing anything from them, and cited WCAG in three items without listing it at all. Both directions of the inconsistency are now closed.                                               |
| 4  | v1.2              | Corrected IA04-07                                                                                                                                | As written ("summary counts match the number of rows currently shown") the item would fail on any correctly paginated system and would have produced a false bug report in Task 1B.                                    |
| 5  | v1.2              | Merged IA02-03 + IA02-04 into one item; repurposed the freed ID to cover**enforcement** of upload limits                                   | The two items stated one rule twice (4:3 and 24:9 helper text), inflating the count without adding coverage. Meanwhile IA02-07 checked only that limits were*stated*, with nothing checking they were *enforced*.  |
| 6  | v1.2              | Re-sourced four items away from Norman P4 (Mapping) to P6 Signifiers / P3 Constraints / Nielsen H8; added Nielsen H3 and Shneiderman R3/R4/R5    | P4 had become a catch-all across five unrelated items, while H3 and R3/R4/R5 were cited nowhere, an odd gap given that all of IA-04 concerns feedback. All 10 + 6 + 8 principles are now cited at least once.        |
| 7  | v1.2              | Rewrote IA03-12 and IA04-11 as objectively failable rules; made IA01-08 name the exact throttling setting                                        | "No function buried more than one level deep" was a design opinion, and "simulate a scan" was undefined; two testers would have produced different results from the same item.                                       |
| 8  | v1.2              | Added the**Pass / Fail / N/A** result convention                                                                                           | The checklist is shared across scenarios A to D, so items such as IA02-03 (image-ratio helper text) have no referent on, say, the Users list. Recording those as "Pass" would be false and "Fail" would invent a defect. |
| 9  | v1.2              | Added the §4 conformance map, per-widget map, and framework-coverage table                                                                      | Coverage was previously asserted in prose. These three tables make the claim auditable, and building the first of them is what exposed the breadcrumb, drag-and-drop and progress-bar gaps.                          |
| 10 | v1.2              | Added the scenario-assignment table                                                                                      | §5's no-duplication rule needs group-level evidence; no artefact recorded who owned which scenario and screens.                                                                                                       |
| 11 | v1.8 (2026-07-30) | Added 6 scenario-specific items (IA02-15, IA03-14, IA03-15, IA04-14, IA04-15, IA04-16) for D and B | Rounds 1-3 audited by IA aspect, which finds generic gaps but misses anything named only in one scenario's own text (§4 Pool B/D, §5 B3/C4). A scenario-scoped re-read is a different question from an aspect-scoped one, and finds a different set of gaps, same principle as the earlier "reframe the question" lesson in `docs/06_AI_Audit_Report.md` §4. |
| 12 | v1.9 (2026-07-30) | Added IA04-17 (record identity / stale data on direct navigation) | A full re-read of all 55 slide pages, not just the 11 already cited, found two bullets on already-cited pages (p.11, p.12) that no item covered. Earlier rounds checked cited-vs-uncited pages; nobody had checked cited-vs-uncited bullets within a page already marked "done." |
| 13 | 2026-08-01 conformance pass (documentation only, no item added, removed or reworded) | Inlined Prompts 5-10 here instead of cross-referencing them; corrected the recording-convention disclosure (5-10 are verbatim Vietnamese, not normalised English); mapped the source table onto §6's own "books, articles, standards, the course slides" wording; re-verified every S13 page citation against the PDF; added the S13 p.16 *Typography* citation to IA01-04 and regenerated §2b; corrected §2d's p.16 item list; corrected action 3, which claimed a review record in `docs/06` that is not there; added actions 8 and 9 | §15 submits this file as the **group-level** artefact for "the AI prompts used to build the checklist", separately from any individual report. Six of the twelve prompts were reachable only through `docs/06_AI_Audit_Report.md`, an individual §10 appendix, so a marker holding just the group folder would have seen half a chain. The remaining fixes are traceability accuracy: a claim that a page grounds an item, or that a review outcome exists, has to be true when the marker checks it, and two of them were not. |

## 5. Outstanding actions before submission

*Updated 2026-08-01 against the current repository state; items resolved since the v1.2 pass are
marked done rather than left to look outstanding. Task 1B is now complete (see
`docs/02_Task1B_Execution_Report_ScenarioD.md`), which closes action 5 and changes nothing
about actions 4, 6 and 7. Actions 8 and 9 were added by the 2026-08-01 conformance pass.*

| # | Action | Owner | Status |
| - | --- | --- | --- |
| 1 | Commit the 14 EMS screenshots (`reports/screenshots/`, not `checklist/screenshots/`, corrected path) to git | Group | **Done** 2026-07-30, commit `32b9346`, the first commit for this assignment, covering the checklist, reference docs and skill suite. |
| 2 | Fill in the scenario-assignment table in `docs/01_Task1A_Shared_GUI_Checklist.md` | Group | **Done**: table present, all four members assigned, no overlapping screens (see the checklist's "Scenario assignment" section). |
| 3 | Record the group's review outcome for the v1.2 to v1.7 revision passes | Group | **Done in this file** (2026-07-31, completed 2026-08-01): all twelve prompts in §3 above now carry a written review outcome stating what was checked, what was accepted, what was later overturned and what was rejected — including the defect verdicts stripped from the shared artefact in Prompt 10. **Not yet done in `docs/06_AI_Audit_Report.md`**: seven of its interaction entries (4, 5, 6, 7, 8, 11, 12) still read *"To be completed by the group"* under *Human review and action taken*. The substance for those rounds is in §3 above and can be carried across, but that file is owned by its author, not by this artefact. Formal sign-off from the other three members remains pending and is tracked as action 7. |
| 4 | Re-download `refs/slides/Testing GUI Applications.pdf`, truncated, unreadable | Group | Still open. Nothing cites it; low priority. |
| 5 | Distribute checklist v1.9 to all four members before Task 1B execution | Group | **Done for this member**: scenario D was executed against v1.9 in full (60 items across 6 screens, `docs/02_Task1B_Execution_Report_ScenarioD.md`). Whether A, B and C executed against the same version is not verifiable from this repository; confirm with the group before the group-level §7 cross-check. |
| 6 | Pillar-4 gap: **5 of 62** items grounded in the team's own experience of EMS (`docs/06_AI_Audit_Report.md` Interactions 6 and 15) | Group, per member | **Partly closed in v2.0 (2026-08-02); still open for three of the four members.** v1.8 and v1.9 both added *audit-sourced* items, not personal-experience ones, so neither reduced the gap. v2.0 reduced it by exactly one: **IA04-18**, whose origin is the D-018 misdiagnosis during this group's own Task 1B execution — a lived episode documented in `docs/02_Task1B_Execution_Report_ScenarioD.md` and `docs/05_Bug_Usability_Findings_Log.md` before that round, so the provenance is checkable rather than asserted. **IA03-16**, written in the same round, is counted under pillar 3 instead, because it came from a survey note; folding it in would have made the grounding table false.<br><br>What remains owed is **1-2 items from each of the other three members**; see the note in the checklist's *four grounding pillars* section. **Concrete form of the action:** each of the four members, having used EMS themselves, writes 1-2 items in the checklist's five-column format describing something that annoyed or misled *them* while using the product, signs each with their own name and student ID in the *Items added beyond the AI output* section, and states there why no document, heuristic, slide or survey would have produced it. An AI cannot supply this on a member's behalf and must not: the checklist's own grounding claim would become false, which is the reason the AI declined in Prompt 11 and again in the 2026-08-01 pass. |
| 7 | Group review of the 7 new v1.8/v1.9 items (IA02-15, IA03-14, IA03-15, IA04-14, IA04-15, IA04-16, IA04-17), and confirmation of the §5 scenario split from Prompt 9 | Group | **Open.** AI-proposed, script-verified, executed in Task 1B by scenario D's owner only, not yet reviewed or countersigned by the other three members. The scenario split in the checklist is described as "committed" on the strength of one member's word; the other three have not recorded agreement anywhere in this repository. |
| 8 | Fill the seven `To be completed by the group` placeholders in `docs/06_AI_Audit_Report.md` (Interactions 4, 5, 6, 7, 8, 11, 12) | Owner of `docs/06` | **Open.** §2 of the assignment makes human review of every AI result mandatory and §10 requires the process to be logged completely; an interaction entry whose review field is a placeholder reads as review not done. The substance exists in §3 of this file and can be carried across. |
| 9 | Recover the exact clock times for the Task 1A sessions | Group | **Open.** §10 asks for the date **and time** of each interaction. Prompts 5-10 above and the corresponding entries in `docs/06_AI_Audit_Report.md` carry a date but `TBD` for the time; retrieve them from the Claude Code session history. Prompts 1-4, 11 and 12 already carry real start-end times. |
