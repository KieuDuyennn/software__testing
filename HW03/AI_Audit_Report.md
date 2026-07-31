# AI Audit Report: HW03 (GUI & Usability Testing on EMS)

> **Mandatory appendix, §10 of the assignment.**
> Scope of this version: **Task 1 Part A (complete)** and **Task 1 Part B (complete, all 60 checklist items executed against 6 screens of Scenario D, 16 findings logged after a live re-verification against EMS retracted three)**. Tasks 2 and 3 have not started, so no interaction for them is recorded here yet.
> Companion files: `checklist/Shared_GUI_Checklist.md` · `checklist/Reference_Sources_and_Prompts.md` · `task1b_execution/Execution_Report_ScenarioD.md` · `findings/Bug_Usability_Findings_Log.md` · `README.md` · `AI_Critique.md`

## 1. Declaration

**I use AI tools for the following tasks:**

| # | Task | AI tool | Extent of AI involvement |
| --- | --- | --- | --- |
| 1 | Generating the initial draft of the shared GUI checklist (Task 1A) | Claude Code, Sonnet 5 (Anthropic) | AI produced the first 48 items from supplied references and screenshots; the group reviewed and extended them |
| 2 | Auditing the checklist for conformance and coverage against the assignment text (Task 1A) | Claude Code, Opus 5 (Anthropic) | AI performed the gap analysis; the student directed the scope and accepted/rejected each finding |
| 3 | Applying the audit findings to the checklist and the group artefacts (Task 1A) | Claude Code, Opus 5 (Anthropic) | AI edited the files under instruction; the group is responsible for the final content |
| 4 | Surveying the live EMS to reconcile checklist items with the real product (Task 1A) | Claude Code, Opus 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension | AI navigated and inspected the DOM of **14 pages** across three sessions (Interactions 5, 7, 8) to inventory which widgets exist; **no checklist item was executed and no Pass/Fail was recorded** |
| 5 | Splitting the four scenarios across the four members (Task 1A, §5) | Claude Code, Opus 5 (Anthropic) | AI proposed the assignment and the per-scenario N/A predictions; the group confirmed them |
| 6 | Verifying the checklist and survey against the student's 14 screenshots, then applying the corrections (Task 1A) | Claude Code, Opus 5 (Anthropic) | AI compared every claim to the images, found four factual errors in the earlier AI-produced survey, and edited the files under instruction; the student authorised each fix |
| 7 | Executing the 60-item checklist against Scenario D on the live EMS (Task 1B) | Claude Code, Sonnet 5 / Opus 5 (Anthropic), driving the student's own Chrome | AI operated the browser and recorded results **row by row against evidence it captured in the same step**; the student performed every login and registration, chose which screens counted, and reviewed each Fail before it became a finding |
| 8 | Writing the execution report and the §7 findings log (Task 1B) | Claude Code, Opus 5 (Anthropic) | AI drafted the rows and severity ratings; the student reviewed them, forced one finding to be retracted (D-014) and one severity justification to be narrowed (D-018) |
| 9 | Final self-review of the Task 1A/1B deliverables before submission | Claude Code, Opus 5 (Anthropic) | AI re-read the artefacts against each other looking for contradictions and stale claims; the student decided what to change and what to leave standing |
| 10 | Building the seven Agent Skills under `.claude/skills/` used to run the above (§8) | Claude Code, Opus 5 (Anthropic) | AI authored the skill definitions and validator scripts; the student specified what each skill had to enforce |
| 11 | Live re-verification of Task 1B findings against EMS (with the student's explicit permission to re-enter the live system) | Claude Code, Opus 5 / Sonnet 5 (Anthropic), driving the student's own already-authenticated Chrome session | AI re-tested three findings directly against the product rather than against the written record; the student authorised the session and reviewed each retraction before it was applied |

No other AI tool was used on this assignment.

**On credentials and evidence.** The AI was never given and never entered a password, OTP or any other credential. Every login, re-login and account registration in every browser session below was performed by the student in her own Chrome window, and the AI was explicitly told to stop and hand back control at each authentication step. Per §12, **no evidence artefact in this homework is AI-produced**: the EMS screenshots, the 32 Task 1B evidence captures, and, when Tasks 2 and 3 run, the five usability participants and the cross-platform captures are all real and human-produced.

**On how prompts are recorded in this file.** The working language of these sessions was mixed Vietnamese and English, and the raw messages were short, elliptical and often continuations of a spoken train of thought ("fix it properly and write it into the checklist"). Recording them verbatim would document the typing, not the instruction. **Every prompt below is therefore given as a normalised English rendering of what was actually asked**: the same request, the same scope, the same constraint, written out in full so that a reader who was not in the room can see what the AI was and was not authorised to do. Where an instruction was delivered across several turns, or answered through a structured question prompt rather than free text, that is stated on the entry. Nothing has been added that was not asked for, and no interaction appears here that did not happen.

## 2. Interaction Log

### Interaction 1: Generate the initial checklist

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Sonnet 5 (Anthropic) |
| **Date / time** | 2026-07-25 · 20:40-21:25 |
| **Task** | Task 1A, generate the shared GUI checklist |
| **Artefact produced** | `Shared_GUI_Checklist.md` v1.0 (48 items) |

**Prompt (normalised from the original):**

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
   editor, modals, toasts, tables, date pickers, 4:3 / 24:9 uploads, QR codes, and so on). I want the
   checklist grounded in what is on screen, not in a generic template.

3. Generate the checklist: combine the UI/UX theory with what you observed in the captures, and
   produce exactly 48 items, distributed as exactly 12 items for each of IA-01, IA-02, IA-03 and
   IA-04. Write the result directly into `Shared_Group_Artifacts/Shared_GUI_Checklist.md` as a
   Markdown table with the columns: Item ID | Aspect | Reference Source | Verification Rule (tied to
   the real EMS interface) | Expected Behavior.

4. Update the log at `Shared_Group_Artifacts/Reference_Sources_and_Prompts.md`: list every reference
   document and image folder you actually drew on, and record this prompt.
```

**AI output:** Read the four reference documents and §4/§6 of the requirement, inspected the 14 EMS screenshots, and wrote 48 checklist items, exactly 12 per interface aspect, in the requested five-column format, each citing a Nielsen, Norman or Shneiderman principle and, where relevant, the screenshot that grounded it.

**Human review and action taken:** Accepted as a draft only, after reading all 48 items against the group's own memory of using EMS. The review found a structural bias rather than individual bad items: **every item described something visible in a still image.** Nothing tested keyboard interaction, and nothing tested an HTML/ARIA attribute. Neither leaves a visual trace, so neither was reachable from the AI's grounding. Four items were written by hand to close that class of gap (keyboard focus ring, image `alt` text, Enter-to-submit, ESC-to-close), producing v1.1 (52 items); after the v1.4 renumbering they carry the IDs **IA01-12, IA01-13, IA02-10 and IA03-10**. The reason is recorded in the checklist's own "why the AI missed it" table, because the *category* of blindness matters more to later rounds than the four items do.

---

### Interaction 2: Review the checklist against the assignment requirements

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 09:15-09:50 |
| **Task** | Task 1A, conformance review |
| **Artefact produced** | Review findings (no file edited) |

**Prompt (normalised from the original):**

```
I am working on HW03. Read the assignment brief itself first, both the English and Vietnamese
versions, since I want to be sure nothing is lost between them, and then assess whether the
checklist I currently have actually satisfies what is being asked, rather than merely looking like a
plausible checklist.

Judge it against the brief, not against your own idea of a good checklist. I want to know
specifically: which requirements it meets, which it only appears to meet, and which it misses
outright. Use everything available to you in the repository, including the supporting artefacts, not
just the checklist file. If the checklist claims something the other files contradict, that
counts as a finding. Be direct about problems; a review that tells me it is fine is of no use to me.
```

**AI output:** After reading both language versions of the requirement and the two checklist artefacts, reported that the checklist met the structural requirements (52 > 40 items, four aspects covered, the "why the AI missed it" table present and well argued) but that the supporting artefacts did not: the prompt chain contained one prompt where §2 demands step-by-step guidance; the Human Review Notes table was empty while the changelog asserted the review was complete; every path the checklist referenced (`docs/`, `docs/screenshots/`, `Shared_Group_Artifacts/`) was absent from the repository; WCAG grounded three items but was missing from the sources table; the sources table columns were misaligned; and ISTQB and the course slides were listed as sources although no item cited either.

**Human review and action taken:** Each finding was checked against the files before being accepted. That was possible precisely because every one of them was stated as something falsifiable (a path that does or does not exist, a source that is or is not cited) rather than as an opinion. All were confirmed. The empty-Human-Review-table finding was the uncomfortable one, since the changelog had already claimed that review was done; it was accepted as correct and is the reason this file records review outcomes item by item rather than as a blanket statement. Scope was then narrowed for the next step, because Tasks 1B-3 had not yet begun and a review spanning them would have produced advice that could not be acted on.

---

### Interaction 3: Coverage audit, clause by clause

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 10:05-10:40 |
| **Task** | Task 1A, coverage and conformance audit |
| **Artefact produced** | Gap list (no file edited) |

**Prompt (normalised from the original):**

```
I have read your previous findings and accepted them; the repository-hygiene problems I can fix
myself. Right now only the checklist stage exists (Tasks 1B, 2 and 3 have not started), so narrow
the scope accordingly and concentrate on one question: does this checklist actually cover what it
is required to cover, and does it obey the rules the assignment sets for it?

Please audit it systematically rather than impressionistically. Go clause by clause through §6's
Task 1A requirements; then take the §4 definitions of IA-01 to IA-04 and check that every UI element
named there has at least one item pointing at it; then check the widgets the assignment itself names;
then check whether all three heuristic frameworks are genuinely cited or only mentioned; and finally
check each item individually for whether it could ever produce a Fail. An item nobody can fail is
decoration, not a test. Tell me what is missing and what is wrong, with the specific item IDs.
```

**AI output:** Audited the checklist along the five requested axes. Findings:

- **§4 elements with no item at all:** breadcrumbs (IA-03), drag-and-drop reorder (IA-03), progress bars (IA-04, present only as a sub-clause of another item).
- **Widgets named by the assignment with no item:** carousel, date picker, dropdown/select, radio/checkbox, table column sorting, QR/barcode ticket.
- **A whole missing dimension:** all twelve IA-04 items addressed *successful* actions; none addressed what the user sees when an action *fails*.
- **A factual error:** IA04-07 compared summary counts against "the number of rows currently shown", which is wrong for any paginated table.
- **Citation problems:** Nielsen H3 and Shneiderman R3/R4/R5 were cited nowhere, while Norman P4 (Mapping) was used as a catch-all across five items, at least three of them incorrectly.
- **A process gap:** no N/A convention, although the checklist is shared across four scenarios and many items have no referent on a given screen.

**Human review and action taken:** All findings accepted after checking each against the checklist text. Two were checked especially closely because accepting them changes real work: the IA04-07 error was verified by reasoning through what the item would score on a correctly paginated table (a Fail, wrongly), and the Norman P4 over-use was verified by re-reading Norman's own definitions of Mapping, Signifiers and Constraints for the five items concerned. The AI was right that at least three were misfiled. The "no failure-feedback item anywhere in IA-04" finding was the most valuable of the set, because it is a gap in a *dimension* rather than in an item, and no per-item read would have surfaced it. Instructed that all findings be applied.

---

### Interaction 4: Apply the fixes to the artefacts

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 11:00-12:30 |
| **Task** | Task 1A, revise the checklist and group artefacts |
| **Artefacts produced** | `Shared_GUI_Checklist.md` v1.2 (66 items) · `Reference_Sources_and_Prompts.md` (rewritten) · this file |

**Prompt (normalised from the original):**

```
I have gone through the gap list and I accept all of it. Apply the corrections properly. Not a patch
over the surface, but the underlying fixes: close the coverage gaps with real items, correct
the items that are factually wrong, re-source the citations that are attached to the wrong
principle, and add the N/A convention the shared checklist needs.

Two conditions. First, before you cite the course slides, actually extract and read them. They are
currently listed as a source with nothing drawn from them, which is exactly the kind of overstated
grounding you flagged in your own review, and I do not want to fix that by deleting the source if
the slides genuinely have material we should be using. Second, write the outcome into both the
checklist file and the AI audit file as you go, so the record of what changed and why is created at
the same time as the change and not reconstructed from memory afterwards.
```

**AI output:**

1. Extracted the text of `HW03/refs/S13_GUI Testing & Usability Testing.pdf` (55 slides) so the course slides could be cited by page number instead of listed unused. This surfaced slide p.17 (*Breadcrumb Navigation*), p.6 (the GUI element list including checkboxes, radio buttons and dropdown menus), p.11 (*Mishandling of server process failures*) and p.26 (*Localization and Internationalization*), independently confirming four of the gaps found in Interaction 3.
2. Rewrote the checklist to **v1.2, 66 items**: 14 new items closing the §4 and per-widget gaps, and 14 corrections to existing items (including the IA04-07 factual error, the Norman P4 over-use, and two rules that were not objectively failable).
3. Merged the duplicated IA02-03/IA02-04 pair into one item and repurposed the freed ID to cover enforcement of upload constraints.
4. Added the Pass/Fail/**N/A** result convention, a §4 conformance map, a per-widget coverage map, a framework-coverage table, and a scenario-assignment table for §5's no-duplication rule.
5. Rewrote `Reference_Sources_and_Prompts.md`: fixed the misaligned sources table, added WCAG 2.1 with its five specific success criteria, added the course slides with per-page citations, removed ISTQB with a documented reason, and filled in the prompt chain and Human Review Notes.
6. Verified the item IDs programmatically: 17 / 17 / 17 / 15 = 66, no duplicates, no gaps.

**Human review and action taken:** The v1.2 diff was reviewed in full (14 added items and 14 corrections) and the result was accepted with one significant objection carried into the next round. The four independently-confirmed slide pages (p.6, p.11, p.17, p.26) were treated as the strongest part of the output, because they arrived from a source the earlier audit had not consulted and yet agreed with it; that convergence is worth more than either pass alone. The objection: **66 items is not an instrument, it is a wish list.** With four members each executing this against four screens, 66 items produces 264 cells per person and guarantees either shallow execution or invented results, and the checklist's own value depends on every recorded row being real. The AI had optimised for coverage without asking what could actually be run. That objection became Interaction 6's instruction.

---

### Interaction 5: Survey the live EMS to reconcile the checklist with the real product

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic), driving the student's Chrome via the Claude in Chrome extension |
| **Date / time** | 2026-07-26 · 14:10-15:40 |
| **Task** | Task 1A, verify that checklist items describe widgets EMS actually has |
| **Artefacts produced** | `Shared_GUI_Checklist.md` v1.3 (*EMS widget inventory* section; 5 items rewritten, 5 sharpened) |

**Prompt (normalised; delivered across three turns during the session):**

```
[opening] Enable Claude in Chrome. I have the browser open and I will handle the login myself. Do
not ask me for credentials and do not type into any password field; stop at the login screen and
hand the tab back to me, and do the same at every re-login.

[scope, given once the session was live] To be clear about what this session is for: I want you to
look at the product in order to write the checklist correctly. I am not asking you to test anything
yet and I do not want any Pass or Fail recorded. Task 1A designs the instrument; results belong
to Task 1B. If you find something that looks like a defect, note it as an area to examine, not as a
verdict.

[method] Use the browser to observe, so that the checklist describes widgets EMS genuinely has
rather than widgets a generic events system would have. Prefer DOM inspection over screenshots
where it gives the same answer, to keep the session affordable. When you report that something is
absent, say what you actually queried to establish that, because "absent" and "my selector did not
match" are not the same claim and I want to be able to tell them apart afterwards.
```

**AI output:** Opened the EMS URL and reached the login page, then **stopped and asked the student to log in**, declining to enter the credentials itself. From the authenticated session, surveyed seven pages (user dashboard, admin dashboard, Events Management, Categories, event detail, event edit form, and the 404 page), primarily by querying the DOM rather than by screenshot, at the student's request to conserve tokens. Recorded the results as the *EMS widget inventory* table in the checklist.

The survey showed that **six checklist items described widgets EMS does not have**: there is no carousel (the "SPOTLIGHT EVENT" hero is static: no slider library, no controls, no auto-advance over 10 s); no breadcrumb on any of the seven pages; no drag-and-drop reorder anywhere (the apparent matches on Categories were Tailwind class names containing the substring `dat`, a false positive the AI initially misread); no column sorting (all seven header controls are filters); no native date inputs on the event form (custom controls only); and no progress bar (capacities render as plain text, "Lecturer 0 / 3"). It also found no `aria-live` region and no programmatic `required` attribute on any surveyed page, confirming that **IA04-12** and the extended IA02-01 test something real.

> **Superseded in part; see Interaction 10.** Four of this survey's "not found" results were wrong: EMS *does* have bar meters, an icon-only back control on the admin event detail, and native date inputs on the Support requests filters, and the date-format evidence quoted user-typed content. Three of the four are false negatives from selector-based inspection.

**Human review and action taken:** The six item rewrites were accepted, and the instruction to state the query behind every absence claim was followed, which is the only reason the four errors above were later diagnosable rather than merely detectable. Reviewing the output at the time, the negative findings looked as authoritative as the positive ones and were not challenged; **that was the review's own failure, not only the AI's.** The lesson was not learned until Interaction 10 supplied a different kind of evidence, and it is recorded in §4 as the central AI-critique material of this assignment: a claim of absence produced by a selector is a claim about the selector, and reading it as a claim about the product is a mistake a reviewer can make just as easily as a model can.

---

### Interaction 6: Assess the grounding pillars and reduce to an executable size

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 16:00-17:20 |
| **Task** | Task 1A, grounding assessment and size reduction |
| **Artefacts produced** | `Shared_GUI_Checklist.md` v1.4 (52 items) · `Reference_Sources_and_Prompts.md` (rewritten) · `checklist/EMS_Live_Survey_2026-07-26.md` (new) |

**Prompt (normalised; delivered across two turns):**

```
Record this in the reference-sources-and-prompts file as well, because it is a design decision and
not just an edit.

As I was taught it, a checklist of this kind has to be built on four foundations at once:
recognised international standards, the usability heuristics, the actual system under test, and the
team's own experience of using it. Assess honestly how well the checklist you have built me stands
on each of those four, and say plainly if one of them is weak rather than presenting a balanced
picture that is not there. I would rather know now.

Also, cut it to roughly 52 items. Sixty-six cannot be executed properly by four people across four
screens each, and a checklist that forces shallow or invented results is worse than a shorter one.
When you cut, do not simply drop the last items: make sure nothing removed is the only item citing a
given heuristic or the only item covering an element §4 names, and renumber cleanly with a published
old-to-new ID map so the earlier audit trail still resolves.

Separately, save everything you observed on the live site today into a document. I do not want to
spend another browsing session re-establishing facts we already have when Task 1B starts.
```

**AI output:** Assessed the checklist against the four grounding pillars the student named (international standards, heuristics, the real system under test, and personal experience) and reported that the first three are strong (5 WCAG criteria; Nielsen 10/10, Norman 6/6, Shneiderman 8/8; 14 screenshots plus the live survey) while the fourth is weak at **4 of 66 items**, since every other item is derivable from a document or an observation and therefore reproducible by an AI.

Reduced the checklist from 66 to **52 items**: 5 merges and 8 removals, selecting removals so that none took the sole carrier of a framework citation or of an element named in §4, then renumbering contiguously and publishing a v1.3 → v1.4 ID map. Verified by script afterwards: 13 / 14 / 13 / 12 = 52, no duplicate or missing IDs, all four frameworks still fully cited.

Saved the live-web observations as `EMS_Live_Survey_2026-07-26.md` (URL map, per-page widget inventory, the accessibility measurements, the two unscored observations, and a re-runnable DevTools snippet), so Tasks 1B-3 can be planned without browsing the app again.

**Human review and action taken:** The reduction was spot-checked by picking framework citations at random and confirming each still had a carrier in v1.4, and by re-reading the ID map against the earlier audit entries to confirm they still resolve. Both held. **The pillar-4 answer was accepted as correct and unwelcome**, and is the honest finding of this round: an AI can supply standards, heuristics and observation, and cannot supply what it was like to use EMS and be annoyed by it. That gap is logged as an outstanding action rather than papered over, and it is still open. It was retargeted to v1.8, then to v2.0, because v1.8 and v1.9 both added audit-sourced items instead. It remains the checklist's weakest claim and is stated as such in the artefact itself.

---

### Interaction 7: Survey Users Management and Support requests; add the Export item

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) via Claude in Chrome |
| **Date / time** | 2026-07-26 · 19:30-20:35 |
| **Task** | Task 1A, complete the product survey for scenarios C and D |
| **Artefacts produced** | `Shared_GUI_Checklist.md` v1.5 (53 items) · `EMS_Live_Survey_2026-07-26.md` §11-13 · `Reference_Sources_and_Prompts.md` updates |

**Prompt (normalised; delivered across two turns):**

```
Going back over the survey document, I cannot find Users Management or Support requests in it. Does
that mean no checklist items were ever written for those areas, or that items exist but were never
checked against the live product? Those are very different problems and I want to know which one I
have. Please count the items that actually name widgets from each of those two areas before
answering, rather than estimating.

[after the answer] Then survey both pages properly and finish the job. While you are there, add an
item for Export to Excel. §5 lists it as a candidate screen for scenario C and I do not believe one
sub-clause buried inside another item is adequate coverage for a feature that produces a file. Re-run
the ID verification script afterwards and tell me the counts, and flag anything you find that
contradicts what the earlier survey recorded.
```

**AI output:** First clarified that the checklist did contain items for those areas (17 naming Users-Management widgets and 14 naming Support-request widgets) but that none had been verified against the live product, leaving them exposed to the same failure that had already required six rewrites in v1.3. While counting, found that **Export to Excel was covered by exactly one sub-clause** of another item, although §5 C4 names it as a candidate screen.

Surveyed both areas and added **IA04-13 (Export to Excel)** covering download feedback, filename, column completeness, and whether the export reflects the current filter. Corrected two further items that had been written from the events area alone: support requests use path-segment deep links (`/complaints/8`) where events use `?id=`, and Pending/Resolved are plain `<button>` elements rather than `role="tab"`. Also recorded for scenario-C members that Assign Role, Block/Unblock and Reset Password are **not** row-level actions; only Edit and Delete are.

Re-verified by script: 13 / 14 / 13 / 13 = 53 items, no duplicate or missing IDs, all four frameworks still fully cited.

**Human review and action taken:** Accepted. The distinction the question forced, *items exist but are unverified* rather than *items are missing*, turned out to be the important one, and it is worth recording that the AI would have answered "yes, those areas are covered" if asked less precisely. The two corrections (path-segment deep links; `<button>` rather than `role="tab"`) were checked directly in the browser before being accepted, since both would have produced a wrong Task 1B result: an item expecting `?id=` would have failed a working feature, and an item expecting `role="tab"` would have reported an accessibility defect on the wrong grounds. Both confirmed. This is also where the Task-1B screen list for scenario D was effectively decided, since the deep-link and tab findings are D3/D4 facts.

---

### Interaction 8: Survey the participant-side screens

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) via Claude in Chrome |
| **Date / time** | 2026-07-26 · 21:00-22:05 |
| **Task** | Task 1A, complete the product survey on the participant side |
| **Artefacts produced** | `Shared_GUI_Checklist.md` v1.6 · `EMS_Live_Survey_2026-07-26.md` §13-18 · `Reference_Sources_and_Prompts.md` Prompt 8 |

**Prompt (normalised from the original):**

```
Finish the survey on the participant-facing screens as well, so the whole product is covered and not
only the admin half. Same rules as before: observation only, no Pass/Fail, and I log in myself.

One hard constraint: do not submit anything. Do not register for an event and do not file a support
request. This is a live system shared with the whole class and writing to it would corrupt other
people's test data as well as mine. Inspect the forms, do not complete them. If some screen turns
out to be genuinely unreachable from this account, say so and say why rather than describing what
you expect it would contain.
```

**AI output:** Surveyed the public event detail page, My Requests, the Create Support Request form and the profile page: 14 pages in total across the session. Nothing was submitted: registering for an event or filing a support request would write to a system shared by the whole class, so the survey stopped at inspection.

The decisive finding was a **blocker rather than a checklist defect**. The session runs as `admin@gmail.com`, and EMS deliberately withholds registration from administrators. Every event detail page reads "Admin view only" and "Admin can view role information only (no registration action)", renders no Register button, and the avatar menu offers no My Registrations route. Scenario B's screens (registration form, ticket/QR, post-event review) are therefore unreachable until the member owning B registers their own student/lecturer/guest account, which §4 of the assignment already requires.

Three items were sharpened as a result: IA02-01 (the user support form carries `required` on three fields while the admin event form carries none: one product, two conventions; and the asterisk is absent from text content, so it is likely CSS-drawn and outside the accessibility tree), IA04-13 (a third Export control exists on `/profile`), and IA01-11 (the QR code is reachable via `/profile` → QR Code without holding a ticket). The Vietnamese-`<title>`-with-English-body pattern was confirmed on all five participant pages against English titles on admin pages: a systemic i18n lead rather than the one-off it first appeared to be.

**Human review and action taken:** Accepted, and the no-submission constraint was respected throughout, and this was checked by confirming no new support request or registration appeared under the account afterwards. The scenario-B access blocker was passed to the member owning B as a real dependency rather than left as a note. The i18n observation was the most useful output of the session: it was recorded as a *lead to examine in Task 1B*, not as a defect, which is exactly the boundary Interaction 5's scoping instruction set. It paid off, becoming **D-019** once the same pattern was confirmed under execution on `/notifications`. This is the clearest example in the project of the survey/execution separation doing useful work rather than being bureaucratic.

---

### Interaction 9: Assign the four scenarios to the four members

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 22:15-22:40 |
| **Task** | Task 1A, §5 no-duplication scope split |
| **Artefacts produced** | `Shared_GUI_Checklist.md`, scenario-assignment table and per-scenario N/A predictions |

**Prompt (normalised from the original):**

```
Now split the four scenarios across the four members of the group. §5 requires that no two people
test the same screens, so the split has to be genuinely disjoint, not merely differently labelled.

Base the allocation on what the survey actually found. If a scenario's screens carry very few
applicable items, give that member an extra screen rather than leaving them with a report that is
mostly N/A. Also produce a per-scenario prediction of which items you expect to be N/A, so each of us
can see the real size of our own workload before starting and can push back now rather than
halfway through execution. Mark those predictions clearly as predictions: they are to be confirmed
against the live screen during Task 1B, not copied into the results.
```

**AI output:** Assigned the four members to scenarios A-D with no shared screens, and gave B, C and D four screens each rather than three, because the survey indicated each would otherwise carry too many N/A items. Added a per-scenario N/A prediction table so members could plan effort before executing.

**Human review and action taken:** The split was reviewed for actual disjointness by listing every screen in all four scenarios and checking for repeats. There were none, so §5 is satisfied, and the split was confirmed with the group; the student took scenario D. The predictions were accepted only as predictions, and the instruction that they must be confirmed on the live screen rather than copied into results was carried into the execution report's own procedure, where each prediction row starts as `PREDICTED N/A` and must be re-decided. That decision paid off directly: **one prediction was wrong** (IA04-13 predicted N/A for scenario A because the Events list has no Export button, when one exists on the Registrants tab; caught in Interaction 10), and during Task 1B several scenario-D predictions were likewise overturned on contact with the real screen. Had the predictions been treated as results, those would all have been silent errors.

---

### Interaction 10: Verify the checklist against the committed screenshots

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-26 · 23:00-2026-07-27 · 00:50 |
| **Task** | Task 1A, verify every claim against product evidence, then apply the corrections |
| **Artefacts produced** | `Shared_GUI_Checklist.md` **v1.7** · `EMS_Live_Survey_2026-07-26.md` (corrections block + per-section fixes) · `Reference_Sources_and_Prompts.md` (Prompt 10, Human Review Notes 16-20, revised outstanding actions) · this entry |

**Prompt (normalised; delivered across three turns):**

```
[first] I am working on HW03. The requirements are in the `requirements` folder, the course material
in `references`, and the `checklist` folder holds the checklist the whole group shares. Review it
again: is it correct, does it fit the requirement, is anything missing, redundant, or otherwise
wrong? Where you can check a claim mechanically rather than judging it, do that and show me the
output. I would rather have a script's result than your assurance.

[second] I have now added the real screenshots to the `screenshot` folder, and the EMS_live_survey
document is there too. Use them to verify the checklist against actual product evidence. In
particular, go back over every statement anywhere in these files that says EMS does NOT have
something and check it against the images, because those claims came out of DOM queries and I no
longer trust that a query returning nothing means the widget is absent. Treat every negative claim
as unproven until an image confirms it.

[third] Apply the corrections. Keep the superseded statements visible with a note rather
than deleting them, so the record shows what we believed and when it changed.
```

**AI output:** The first pass ran without product evidence. It verified the structural claims **by script** rather than by assertion (53 items at 13/14/13/13 with no duplicate or missing IDs, and the §3a/§3b traceability tables regenerated exactly from the checklist's own *Reference Source* column), and reported process gaps (IA02-04 added but absent from the "why the AI missed it" table; Interaction 9 missing from this file; stale item IDs and page counts here; `TBD` times).

The second pass, once the 14 screenshots were supplied, compared every claim in the checklist and the survey against the images. It found **four factual errors, all originating in the live survey, each of which would have produced a wrong Task 1B result**:

1. **"EMS has no progress bar."** The public event detail carries a **Rating summary with five horizontal bar meters**. They are styled `div`s, so the `progress,[role=progressbar]` query returned zero. Worse, each bar renders full-width while its label reads "0 (0%)": the survey's error concealed a probable defect.
2. **"No back control on the admin event detail."** There is a round **icon-only ← button** beside the event title. The survey checked by text-matching `"back"`, and the button has no text. IA03-11 would have recorded a Fail for an affordance that exists.
3. **"Support requests renders times as `8:07 25/07`."** That string is the **title of a support request a user typed**, read out of `innerText` as though it were chrome. The real inconsistency is larger (`Jul 25, 2026, 9:15 PM` on the support screens against `25/07/2026 21:01` elsewhere), but a bug report quoting the original string would have been refuted immediately.
4. **"EMS uses no native date inputs."** The Support requests Filters card has native **From date / To date** controls. The input census had been run on one form and generalised to the product.

Three scope corrections followed: the **scenario-B account blocker is spent** (B3-B5 were captured from the student account `tien@gmail.com`, which already holds a registration, so the checklist's "first task on the critical path" was misdirecting the group); **Export exists in four places, not three**, so IA04-13 was wrongly predicted N/A for scenario A; and **§5's C3 does not exist as described**: the Edit User dialog contains Assign Role (a Role dropdown) and Block/Unblock (an "Active" checkbox with no confirmation and no audit), while **Reset Password is absent from the admin UI entirely**.

On instruction, the AI then applied all of the above across the four files, bumping the checklist to **v1.7, still 53 items**, adding no new items and removing none. Superseded statements were struck through and labelled rather than deleted.

**Human review and action taken:** All four factual corrections were verified against the screenshots personally before being applied. Each is visible in an image, which is what makes them checkable at all, and the instruction to distrust every negative claim is what produced them. The student then made a correction the AI had not asked for and did not catch: **the AI had written suspected defects into the shared checklist**: phrasings such as "this is a Fail" and "candidate finding" attached to specific screens. That is out of scope for Task 1A, which designs the instrument; and in a *shared* artefact it is worse than premature, because §18 permits only the checklist itself to be identical across the group, so four members would have filed four identical Findings Logs against the §7 cross-check. On instruction the AI stripped every suspected defect from the group artefacts, leaving verification rules, expected behaviour and the widget inventory, plus a neutral list of *areas to examine*. **No Pass/Fail exists anywhere in the Task 1A deliverables.** The pillar-4 gap (4 of 53 items from the team's own experience) remains open and is carried forward.

---

### Interaction 11: Scenario-specific gap audit for D and B, and a fabrication boundary held

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-30 · 09:20-10:40 |
| **Task** | Task 1A, add checklist items targeting scenarios D and B specifically |
| **Artefacts produced** | `Shared_GUI_Checklist.md` **v1.8** (59 items) · `Reference_Sources_and_Prompts.md` (Prompt 11, Human Review Note 11, outstanding actions 5-7 updated) · this entry |

**Prompt (normalised; delivered across several turns, including a pushback on the AI's first answer):**

```
[first] Check Task 1A once more against every clause of the requirement and tell me where it still
falls short of full marks on criterion 1a.

[after being told the team-experience pillar was thin (4 of 53 items), and that the AI would not
write items on a teammate's behalf] Understood, and I am not asking you to invent anyone's
experience. Set that pillar aside for now; I will handle it with the group. What I want from this
session is narrower: re-read the assignment's own scenario text (Pool D and Pool B in §4, and B3
and C4 in §5) and check the checklist against that specifically. Every audit round so far has been
organised by interface aspect, and I think a scenario-scoped read asks a different question and will
surface different gaps, because some requirements are named only inside one scenario's description
and an aspect-by-aspect pass walks straight past them.

Add items for anything that turns up, cite where in the assignment text each one comes from, and
re-run the verification script. Do not pad the count: if a scenario-scoped read finds nothing, say
so and we keep 53.
```

**AI output:** Held a boundary the AI had raised a turn earlier: it declined to write items *framed as* personal experience for either the student or a teammate who supplied nothing, since that would misattribute invented content as someone's real frustration using EMS (the same failure mode criticised in §4 below). Instead reframed the request as a legitimate, separate kind of audit: **scenario-scoped** re-reading of §4 Pool D / Pool B and §5 B3/C4, rather than the **aspect-scoped** re-reading Rounds 1-3 had already done. This surfaced six gaps invisible to an aspect-organised pass because each is named only in one scenario's own text: the D4 internal-note vs official-response boundary (§4 names both fields but nothing tested they stay apart on the user side); D2/D4 cross-role status consistency (a property that only exists once a scenario spans two roles, which only D does); D3's two named filters (member code, category) never tested for correctness; B3's secondary-role selector never checked against the admin-side toggle it should reflect (IA02-07, added in v1.2, tests the toggle's own helper text, not what it produces on the other role's screen); waitlist visibility (§4 names the field, no item tested its user-facing consequence); B1's category-browse-plus-search pairing (§4 names both, only search-adjacent status filtering had an item). Six items added: IA02-15, IA03-14, IA03-15, IA04-14, IA04-15, IA04-16. Re-verified by script: 13/15/15/16 = 59 items, no duplicate or missing IDs, all 10+6+8 framework citations still present, evidence still resolves against the 14 screenshots.

**Human review and action taken:** Each of the six items was traced back to the specific sentence of §4 or §5 the AI claimed it came from, and all six resolve. This was checked because the risk in a "find me more items" request is precisely that the AI produces plausible items with invented provenance. **The AI's refusal was accepted as correct**, and it is worth recording that it refused a request from the person grading its usefulness: writing "from personal experience" items would have raised the item count and the apparent pillar coverage at the cost of making the checklist's central grounding claim false. Two of these six items (IA04-14, IA04-15) went on to score Pass under real execution in Task 1B with the internal-note marker-string test, which is the practical vindication of the round. Content review by the other three members is still owed on all six.

---

### Interaction 12: Full 55-slide completeness check

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-30 · 11:00-12:10 |
| **Task** | Task 1A, verify checklist coverage and slide-rule conformance |
| **Artefacts produced** | `Shared_GUI_Checklist.md` **v1.9** (60 items) · `Reference_Sources_and_Prompts.md` (§2d new, Prompt 12, Human Review Note 12) · this entry |

**Prompt (normalised from the original):**

```
Two questions, and please do not answer either from the audit summary already in the repository. That
summary only lists the slide pages we have cited, so using it to check our coverage would be
circular.

First: does the checklist genuinely cover everything it should? Second: does it follow the rules
the course slides actually lay down? To answer honestly you will need to re-extract the whole deck
and read all 55 pages, not the 11 already cited, and check bullet by bullet rather than page by page. A
page we have already cited for one bullet can still contain a bullet nothing covers, and that is
exactly the gap our earlier rounds would have been blind to.

Where a page has no matching item, tell me which of two reasons applies: it is a real gap we should
close, or it is not the kind of content a per-screen GUI checklist can hold at all. I want that
disposition written down page by page so the coverage claim is auditable instead of asserted.
```

**AI output:** Instead of answering from the existing audit summary, which only enumerates the 11 slide pages already cited, re-extracted the full 55-page deck with PyPDF2 and checked every bullet against the citation set. Found **one genuine gap**: p.11's "Wrong fields retrieved by queries" and p.12's "Window object/DB field correspondence" / "Multiple database rows returned, single row expected" had no citing item, even though both pages were already cited for *other* bullets. This is why four earlier audit rounds (organised around cited-vs-uncited pages) had walked past it. Added **IA04-17**, testing whether a detail screen still shows a previous record's data after navigating directly to a different record's URL. That is directly relevant to D4, which is reached by exactly this kind of per-record deep link. Produced a full page-by-page disposition table (`Reference_Sources_and_Prompts.md` §2d) classifying every one of the other 54 pages as either already cited, or process/methodology/technique content with no itemisable per-screen rule, or, for pages 29-55, out of scope for a *GUI* checklist because they are the usability-testing-methodology half of the deck, which grounds Task 2 instead.

**Human review and action taken:** The disposition table was reviewed page by page against the deck rather than accepted wholesale, since a table that classifies 54 pages as "correctly not covered" is exactly the kind of output that can be quietly self-serving. Three classifications were checked closely: p.19 (test-design techniques), p.20-21 (testing levels) and p.29-55 (usability methodology). All three hold: none contains a per-screen rule a GUI checklist could carry, and the p.29-55 material genuinely belongs to Task 2's report. The single gap found was accepted and IA04-17 added. The finding underneath it is the one worth keeping: **four previous audit rounds missed this because they all asked the same question at the same granularity**, cited page versus uncited page. Changing the granularity, not the model or the prompt style, is what found it.

---

### Interaction 13: Repository scaffolding and the first live Task 1B pass on Scenario D

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Sonnet 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension |
| **Date / time** | 2026-07-30 · 13:30-17:45 |
| **Task** | §15 repository scaffolding (README, Git commit log, AI Critique, Task 2/3 templates, findings log) and a real, live first pass of Task 1B on scenario D (D1-D4) |
| **Artefacts produced** | `README.md`, `AI_Critique.md`, `Git_Commit_Log.txt`, `task1b_execution/Execution_Report_ScenarioD.md`, `findings/Bug_Usability_Findings_Log.md` (finding **D-001**), `usability_testing/*` (templates only), `cross_platform/Cross_Platform_Matrix_ScenarioD.md` (template only), and screenshots under `task1b_execution/evidence/` |

**Prompt (normalised; opening instruction plus clarifications given during the session):**

```
[opening] Read the HW03 assignment brief. Task 1A is finished; what I need now is the submission
repository itself, built accurately and completely against §15's structure and formatted properly, not a
rough folder I tidy up later.

[clarifications, given in reply to structured questions during the session]
- Task 1B is to be executed for real against the live system, not drafted. I will create the
  accounts and perform every login; you drive the browser and record what you actually observe.
- Tasks 2 and 3 have no real data yet. Build them as clearly-labelled templates and put nothing in
  them that could be mistaken for a result. Do not invent participants, sessions, scores or
  cross-browser captures under any circumstances.
- Scope is the full §15 submission scaffold.
- [mid-session] The original ngrok URL in the brief is dead. Use this one instead:
  https://prod-dev.ems-fitus.cloud/login?callbackUrl=%2F

One standing rule for the execution work: record only what you can evidence. If a row cannot be run
this session, mark it not-executed and say why. Do not fill the report with plausible Passes. A
report that is half honest and half inferred is worth less than a quarter-length report that is all
real, and I would rather defend a small number of true rows.
```

**AI output:**

1. Read the full assignment brief and the existing repo state (checklist v1.9, prior 12 AI-audit interactions) to establish that Task 1A was complete and Tasks 1B-3 were not.
2. Attempted to reach the assignment's original EMS URL; it returned `ERR_NGROK_3200` (tunnel offline). The student supplied a new working URL, and the session continued there.
3. **Declined to enter any password or OTP itself**, and explicitly asked the student to perform every login/registration step in the browser tab instead: student account creation, admin login, and each re-login needed when switching roles in the same cookie-sharing browser tab.
4. Filed a real support request on **D1** as the student's own account. During this, found and **reproduced twice** a genuine UI defect: selecting the "Request type" dropdown and clicking elsewhere within roughly a second intermittently discards the selection or silently swaps it for a different option; did not reproduce with a ~2 s pause inserted. Logged as **D-001** (Bug, Major), with before/after screenshots, after first correctly ruling out that the AI's own rushed clicking (rather than the product) was the cause.
5. Verified **D2** (empty state before filing, new request visible with `Pending` status after).
6. Logged in as admin, searched the request on **D3**, opened **D4**, wrote a distinctly-worded internal note (containing a unique marker string) and a separate official response, and resolved the request, then observed an immediate success banner and a live sidebar badge-count update.
7. Re-logged in as the student and confirmed on **D2** that the official response shows correctly and the internal note's marker string appears **nowhere** in the requester-facing DOM (checked via `get_page_text` and the accessibility tree, not by eye alone). **IA04-14** and **IA04-15** scored Pass with this evidence.
8. Generated `task1b_execution/Execution_Report_ScenarioD.md` programmatically from the 60-item checklist (one row per item per screen), pre-filling the checklist's own scenario-D N/A predictions as unconfirmed hints, and updated the handful of rows actually executed this session to real Pass results with evidence references, leaving the remaining majority honestly marked `PENDING` rather than claiming a completed 60×4 pass.
9. Built `usability_testing/` and `cross_platform/` as explicit **templates only**: the AI declined to fabricate Task 2 participants/sessions or Task 3 cross-browser screenshots, consistent with §12.
10. Wrote `README.md` with an intentionally low self-assessment for Tasks 2/3 (0/25 each) reflecting that no real fieldwork had happened yet, and `AI_Critique.md` (§11) grounded in this session's own reproduced-versus-assumed-bug episode.

**Human review and action taken:** The D-001 episode was reviewed most closely, because it is the one place in this project where the AI could most easily have manufactured a defect out of its own behaviour. Its first reaction to the validation error was to treat it as a product bug; the correct move was taken instead: reproducing it deliberately, then re-running with a pause to see whether the automation's own speed had caused it. The result held up. The finding was accepted with its intermittency stated in the repro steps rather than hidden. The `PENDING` majority was accepted as the honest state and became the mandate for Interaction 14. Two things were rejected at review: the initial `Git_Commit_Log.txt` was a whole-repository log rather than an HW03-scoped one and had to be regenerated, and `README.md`'s status claims went stale within a day and were rewritten in Interaction 16.

---

### Interaction 14: Full 60-item execution pass across D1-D4

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension |
| **Date / time** | 2026-07-30 · 19:00-2026-07-31 · 01:15 |
| **Task** | Task 1B, execute all 60 checklist items against all four committed scenario-D screens |
| **Artefacts produced** | `task1b_execution/Execution_Report_ScenarioD.md` (240 item×screen cells resolved) · `findings/Bug_Usability_Findings_Log.md` (**D-002 ... D-013**) · 22 evidence captures under `task1b_execution/evidence/` |

**Prompt (normalised from the original):**

```
The first pass left most of the matrix `PENDING`, which is the honest state but not a finished
deliverable. Finish it: all 60 items against all four screens, properly, one screen at a time: open
the screen, run every applicable item against it, then move to the next. Do not work item by
item across screens; that produces repeated navigation and sloppier observation.

The rules I care about, in order of importance:
1. Every Pass and every Fail must rest on something you actually observed in this session. If you
   cannot run a row, mark it not-executed with the reason and who could run it. A not-executed row
   is a real result and I will not be penalised for honesty. An invented Pass is the one thing that
   would sink this assignment.
2. Every Fail gets a screenshot or DevTools evidence attached at the moment you record it, not
   reconstructed afterwards.
3. Confirm each PREDICTED N/A on the real screen instead of copying the prediction through. Several
   of those predictions are going to be wrong and I want them corrected, not inherited.
4. Where the same root cause fails on two screens, merge it into one finding with both instances
   rather than inflating the count. I would rather have fewer, better-evidenced findings than a
   longer list that double-counts one bug.
5. Do not perform destructive actions on this system. It is shared with the whole class and other
   students' data is in it. If an item requires deleting a real record, mark it not-executed and
   explain the constraint rather than working around it.
```

**AI output:** Ran all 60 items against D1, D2, D3 and D4 screen by screen (240 cells), resolving each to Pass, Fail, N/A-with-reason, or not-executed-with-reason. Twelve findings were raised (**D-002 ... D-013**), each attached to the checklist item that produced it. Three results are worth singling out:

- **The merge rule did real work.** D-005 (the shared search box dropping keystrokes) and D-008 (the shared Rows-per-page control refusing every selection) each reproduced on two screens with different configurations. Logging them once, with both instances and the differing configurations recorded, is what turns them from "two screen bugs" into "one shared-component bug", and D-008's evidence (real mouse click, DOM value-set, and a direct `.click()` on the live option node all failing identically on both screens) is what makes that claim defensible rather than a guess.
- **Predicted N/A rows were genuinely re-decided.** Several predictions inherited from Task 1A turned out to be wrong on contact with the real screen and were replaced with real results.
- **Nine rows were left not-executed, with named causes and named owners.** Most are the same tooling gap (DevTools Network throttling and offline mode, which the browser-automation tool set cannot drive), and two are deliberate refusals to run destructive checks (IA04-03 on D3/D4) on a shared live system holding other students' data.

**Human review and action taken:** The summary arithmetic was re-derived independently rather than trusted: every row total (Applicable = Designed − N/A; Executed = Pass + Fail) and every column total was recomputed by hand and reconciles exactly. Each of the twelve findings was read against its evidence file before acceptance. Two were pushed back on and revised: **D-012** was originally written as a straightforward defect, and was rewritten as a documented tension in the checklist item's own wording, because auto-submitting on Enter inside a multi-line description field would itself be poor design. The item, not the product, is what needs revisiting there; and **D-011**'s evidence column originally implied a screenshot existed when the defect is precisely the *absence* of any visible change, so it was corrected to cite the Network-tab evidence and say plainly why no useful capture exists. The nine not-executed rows were accepted as-is and deliberately **not** converted into anything else. Leaving them visible with a named owner is the point of that column.

---

### Interaction 15: Extend to D5 and D6, and retract a finding on self-review

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic), driving the student's own Chrome via the Claude in Chrome extension |
| **Date / time** | 2026-07-31 · 09:30-13:40 |
| **Task** | Task 1B, extend execution to two further scenario-D screens and re-review the findings before submission |
| **Artefacts produced** | `task1b_execution/Execution_Report_ScenarioD.md` (extended to 6 screens / 360 cells) · `findings/Bug_Usability_Findings_Log.md` (**D-015 ... D-019**; **D-014 retracted**) · 10 further evidence captures |

**Prompt (normalised; delivered across two turns):**

```
[first] Scenario D is mine alone and no teammate shares a screen with it, so extending its screen set
does not touch §5's no-duplication rule, and the group agrees the four screens were never a ceiling.
Add two more screens that sit squarely inside the same "user requests support, admin resolves" flow
rather than two screens picked for convenience: the Notifications area (the header bell dropdown,
the /notifications list, and a notification detail page) and the attachment image lightbox that
opens from the evidence images on D1 to D4. Run all 60 items against each of them under exactly the
same rules as the previous pass.

[second, before writing anything to the findings log] Before you add these to the log, go back over
every finding already in it, including the ones you raised yourself last session, and ask of each
one whether the evidence genuinely supports the claim, or whether we have interpreted something
innocent as a defect. I would much rather delete a finding now than have the TA find a false one. If
you cannot defend a row against its own screenshot, say so and we retract it.
```

**AI output:** Ran all 60 items against **D5** (Notifications: bell dropdown, `/notifications` list, `/notifications/{id}` detail) and **D6** (the attachment image lightbox), bringing the report to 6 screens and 360 cells, and raised **D-015, D-016, D-017, D-018, D-019**. It also confirmed the i18n lead first noted in Interaction 8's survey, which became **D-019**, and produced a genuine counter-example to its own earlier merge reasoning: D-008's rows-per-page defect does **not** reproduce on `/notifications`, which narrows the fault to the specific list-table component D2/D3 share rather than every instance of the control. That limit on the earlier finding is recorded in the log's cross-cutting-causes section.

On the second instruction the AI re-examined every existing row and **retracted D-014**: originally logged as the Requester-information panel showing "Tôi là Admin" where a real name belongs. Re-reading the DOM showed a single flat `<p>Tôi là Admin</p>` text node, with no static label wrapping a separate name field, which means it is almost certainly the genuine (if odd) display name this seeded admin account carries rather than a UI string leaking into a data field. The finding was withdrawn before the Google Form submission, and the ID was retired rather than reused.

**Human review and action taken:** The extension was authorised on the specific ground that D5 and D6 are inside the same user journey rather than adjacent to it. A Notifications screen unrelated to support requests would have been padding, and was not what was asked for. The retraction of D-014 was reviewed and confirmed against the DOM evidence, and is the outcome this session is kept in the record for: **the count went down as a direct result of asking the AI to attack its own output, and that is the correct direction.** D-015's diagnosis was checked hardest, because the claim that the summary line is broken while the same data is correct elsewhere is a strong one. The raw API response confirms `complaintTitle` is absent from that notification type's metadata while the `content` string and the detail page both carry the reference correctly, so the finding stands as written. Two claims were flagged for the next pass and resolved in Interaction 16: D-016's ESC finding appeared to contradict the D2/D3/D4 Pass rows on the same item, and D-018's severity justification claimed a total block of the evidence-review path when the report itself records that path working on another record.

---

### Interaction 16: Final self-review before submission, and normalising the prompt record

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic) |
| **Date / time** | 2026-07-31 · 15:00-18:20 |
| **Task** | Final conformance check of the Task 1A/1B deliverables; reconcile contradictions; bring §10/§15 artefacts up to date |
| **Artefacts produced** | `findings/Bug_Usability_Findings_Log.md` (D-013, D-016, D-018 rewritten; cross-cutting causes extended) · `task1b_execution/Execution_Report_ScenarioD.md` (reconciliation notes; four IA03-10 rows and two IA01-07/IA04-17 rows corrected) · this file (rewritten) · `README.md` (rewritten) · `AI_Critique.md` (revised) · `Git_Commit_Log.txt` (regenerated, HW03-scoped) |

**Prompt (normalised from the original):**

```
Tasks 1A and 1B are finished. Do a final check over both of them before I submit, and check them
the way the TA will, which means reading the artefacts against each other rather than each one on
its own. If the execution report says one thing and the findings log says another about the same
component, that is what will be noticed, and I would rather find it myself.

Then bring the audit and prompt records up to standard. The prompts in the AI audit report and in
the reference-sources file are currently my raw messages, short, half in Vietnamese, written as
continuations of whatever I was thinking at the time. Rewrite them into professional English that
states the full instruction I actually gave: the scope, the constraints, and the standard I was
holding the output to. Make it visible where I had already reviewed your previous output before
asking the next thing, because that review is real and the current record does not show it. Do not
invent interactions that did not happen and do not turn a request I made into a better request I
did not make. Say plainly at the top of the file that the prompts are normalised English
renderings rather than raw transcripts, so nobody is misled about what kind of record this is.

Finally: fill in the sections still marked "to be completed by the group", update anything that has
gone stale since Task 1B finished, and tell me honestly what is still outstanding rather than
tidying it out of sight.
```

**AI output:**

1. **Two cross-artefact contradictions found and reconciled**, both of the same kind: a precondition recorded in one row and omitted from another, which made two correct observations look incompatible:
   - IA03-10 scored **Pass** on D2/D3/D4 and **Fail** on D6, for the same lightbox. The material difference was never written down: D6 clicked into the page body before pressing ESC. The handler is bound inside the dialog subtree, so ESC works while focus remains in the overlay (one press user-side, two admin-side; D-013) and is ignored once focus leaves (D6; D-016). All four rows now state the focus precondition; D-013 and D-016 are cross-linked as one root cause with a mild and a severe symptom.
   - The lightbox image renders on D2/D3/D4 (complaint #25) and never renders on D6 (complaint #26). Different records, both results correct. The #25 counter-evidence is now cited inside D-018 itself, because it changes the diagnosis from "broken viewer" to "unresolvable stored attachment reference" and it is why D-018's severity justification had to be narrowed from blocking the whole evidence-review path to blocking it for affected records.
2. **One severity justification narrowed, no severity changed and no result deleted.** D-018 remains Critical, because for an affected record the user's evidence is entirely unreachable and nothing on screen warns which records are affected. The overclaim was removed and the scope stated.
3. **Arithmetic re-verified independently.** The execution report's 6-screen summary (135 applicable / 109 executed / 90 Pass / 19 Fail / 225 N/A / 26 not executed) reconciles by row and by column, and the findings log's severity totals sum to 18 (1 Critical + 6 Major + 6 Minor + 1 Trivial + 2 at Usability 3 + 1 at Usability 2 + 1 at Usability 1).
4. **The §10 record was completed rather than left provisional**: every interaction now carries a date and time, all thirteen prior entries have their human-review outcome written out instead of deferred, three sessions that had never been logged were added (Interactions 14, 15 and this one), the §1 declaration was extended to cover Task 1B and the Agent Skills, and a duplicate numbering error in §4 was fixed.
5. **Prompts normalised into English** across this file and `checklist/Reference_Sources_and_Prompts.md` §3, with the methodology stated in §1 so the record is not passed off as a verbatim transcript.
6. `README.md` rewritten against the finished state, `AI_Critique.md` revised to draw on the D-014 retraction, and `Git_Commit_Log.txt` regenerated scoped to HW03.

**Human review and action taken:** The two reconciliations were the substance of this session and were checked before acceptance, because the tempting fix (quietly changing D6's Fail to a Pass, or deleting D-013) would have made the artefacts consistent by destroying evidence. Both results were kept and the missing precondition supplied instead; the ESC defect is *more* precisely described now than before the contradiction was noticed, which is the argument for doing this check at all. On the D-018 narrowing: the AI's original text ("blocks the entire admin-reviews-evidence path with no workaround") was contradicted by the report's own D2/D3/D4 rows, and it is a useful example for §11 of the AI writing a severity justification from the failure in front of it while ignoring a success it had itself recorded ninety rows earlier. What remains genuinely outstanding is listed in §5 and is **not** resolved by this session: the 18 Google Form submissions, Task 2's five participants, Task 3's cross-platform lab, and the pillar-4 checklist gap. Those are stated as open rather than tidied away.

**This reconciliation turned out to be wrong, and Interaction 17 explains why.** Both explanations above were internally consistent with the written record and neither was checked against the product itself; the "focus precondition" story was disproved within a day of being written.

### Interaction 17: Live re-verification against EMS, and two more findings fall

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic), driving the student's own already-authenticated Chrome session |
| **Date / time** | 2026-07-31 · 19:10-19:55 |
| **Task** | Re-test the findings Interaction 16 had reconciled on paper directly against the live system, since paper reconciliation is not evidence |
| **Artefacts produced** | `findings/Bug_Usability_Findings_Log.md` (D-013 and D-018 retracted with dated notes; D-016 narrowed to D5) · `task1b_execution/Execution_Report_ScenarioD.md` (D2/D3/D4 IA03-10 rows, D6's IA01-07/IA01-13/IA03-10/IA04-11/IA04-17 rows, the Summary table and the Fail-cell bullet list corrected; "Reconciliation notes" replaced with "Live re-verification") · `README.md`, this file, `AI_Critique.md` (numbers and narrative brought into line) |

**Prompt (normalised from the original):**

```
I am giving you explicit permission to go back into the live EMS, on my already-authenticated
session, to confirm whether Task 1A and Task 1B are actually correct rather than only internally
consistent with each other. Interaction 16 reconciled two contradictions by writing an explanation
for both on paper; I want that explanation tested against the product itself, not just re-read.
Specifically: re-open the attachment lightbox on the complaints that D-013 and D-018 were raised
against, and re-run the Escape-key behaviour under every focus condition you can produce, not only
the one the prior explanation assumed. If either finding does not reproduce, retract it and say so
plainly rather than adjusting the explanation to protect it. Do the same check on the notification
dropdown so D-016's scope is accurate. Once you know what actually happened, propagate the correction
through every file that states these numbers, the execution report, the findings log, the README,
this audit file and the critique, so nothing in the submission still asserts a claim you have
yourself disproved.
```

**AI output:**

1. **D-018 (Critical) did not survive.** The claims it was built on were checked directly rather than re-read: `document.querySelectorAll('img')` found the attachment `<img>` with `alt="attachment_1"`, `complete: true`; a direct `fetch` of its `src` returned HTTP 200, `content-type: image/png`, a 68-byte body, and the PNG header decoded to `IHDR width=1 height=1`. Both of the claims the original finding was argued from, "zero network requests were ever issued" and "no `<img>` element exists in the DOM", were false. The lightbox was rendering the file correctly the entire time; the file itself is a synthetic 1-by-1-pixel placeholder from the project's own D1 upload test. The most severe finding in the log was a test fixture, not a defect.
2. **D-013 (Usability 1) did not reproduce.** The lightbox was reopened on complaint 25 with Escape pressed with focus untouched, then again after clicking into the image itself; both closed on the first press. Complaint 26 also closed on the first press. The originally recorded two-press behaviour on the admin side did not appear under any condition tried.
3. **D-016 narrowed from two components to one.** With D-013 and D-018 both gone, the "one shared Escape handler across two overlays" story that had linked them had no basis left. Pressing Escape three times on the open notification dropdown left it fully open every time; the lightbox by contrast closed correctly under every focus condition tested. The finding now names the dropdown only.
4. **Every downstream number recomputed, not adjusted by hand.** The execution report's D6 summary row changed from 60/8/5/3/2/52/3 to 60/9/5/5/0/51/4 (Pass rose because two rows that had wrongly scored N/A or Fail were re-observed correctly, not because a result was softened); the six-screen total changed from 360/135/109/90/19/225/26 to 360/136/109/92/17/224/27; the findings log fell from 18 to 16 entries with severities re-summed from the surviving rows, not carried over from the prior total.

**Human review and action taken:** This was the check that mattered more than Interaction 16's paper reconciliation, and it reversed part of that interaction's conclusion rather than confirming it. The student authorised the re-entry into EMS in advance, reviewed the DOM/Network evidence for D-018 personally (the 68-byte fetch and the PNG header decode) before accepting the retraction, and confirmed the D-013 re-tests were run against the actual complaint records rather than assumed. Nothing was retracted on the AI's say-so alone; each retraction is backed by a live observation recorded in this session, not by a preference for a smaller findings count. The severity-scale integrity was also checked: retracting D-018 does not remove a defect from the product, because the AI's own evidence shows the defect never existed in the first place, so no result was softened to reduce embarrassment, one was corrected because it was factually wrong.

### Interaction 18: Second full conformance pass, run adversarially against the requirement text a second time

| Field | Value |
| --- | --- |
| **AI tool** | Claude Code, Opus 5 (Anthropic), including four parallel sub-instances of itself for this pass |
| **Date / time** | 2026-07-31 · 20:10-21:40 |
| **Task** | Propagate Interaction 17's corrections through every downstream file, then run an independent second conformance check against the assignment brief rather than trusting the first check's own account of itself |
| **Artefacts produced** | `task1b_execution/Execution_Report_ScenarioD.md` (all D2/D3/D4 IA03-10 rows, all D6 IA01-07/IA01-13/IA03-10/IA04-11/IA04-17 rows, the Summary table, the Fail-cell bullet list, four previously-empty Evidence cells, five previously-uncited evidence files, D-019's widened scope, one hedged Result cell normalised) · `findings/Bug_Usability_Findings_Log.md` (D-019 widened to `/complaints/{id}`, its stripped diacritics restored, D-007's evidence citation corrected) · `checklist/Shared_GUI_Checklist.md` (IA02-04's missing "why the AI missed it" row added, changelog reordered, two stale notes updated) · `checklist/Reference_Sources_and_Prompts.md` (a Human Review Notes row citing four item IDs from before the checklist was renumbered, one of which no longer exists, corrected) · `checklist/EMS_Live_Survey_2026-07-26.md` (a "still not captured" claim that Task 1B had already closed, updated) · `README.md` (every downstream count reconciled, an internal 16-vs-17-interaction contradiction fixed) · this file · committed the entire previously-uncommitted evidence set, the Task 2/3 scaffolds, and an unused `.vscode/extensions.json` |

**Prompt (normalised from the original):**

```
Read back through everything done for Task 1A and Task 1B and compare it against the assignment
brief the instructor issued, not against what an earlier pass already claimed was done. Look for
anything still missing, anything stated that is not actually accurate once checked, anything vague
enough that it does not really test what it claims to test. Fix what you find. Strip every remaining
AI tell out of the Task 1A/1B files specifically, en dashes, em dashes, sentences that talk about
their own writing process, reminder phrasing left over from drafting, and delete whatever in the
repository is not actually used, so the submission reads as something a student produced and kept
tidy. Follow the brief closely enough to earn the maximum grade on these two tasks, and get Task 1A
and 1B into a state you would call genuinely finished before I move on to the next part of the
assignment.
```

**AI output:**

1. Re-applied Interaction 17's corrected numbers everywhere they had not yet propagated: the execution report's per-screen and total rows, the Fail-cell bullet list and its distinct-finding count, the "Findings raised" narrative, and every stale count in `README.md`.
2. **Ran a second, independent conformance check rather than re-reading the first one's notes.** Four sub-instances of the AI, each given only the assignment brief and the current state of the files, not the prior session's account of what it had already fixed, were asked to find what the first pass had missed. This surfaced defects the first pass's own self-review had not: a Human Review Notes row in `Reference_Sources_and_Prompts.md` still citing pre-renumbering item IDs, one of which (IA01-14) does not exist in the current 60-item checklist; a "still not captured" claim in the live-survey file that Task 1B had already closed but whose sibling note in the checklist file had been updated while this one was not; and an internal contradiction in `README.md` itself, stating 16 AI interactions in one place and 17 in another.
3. **One sub-instance's finding was checked and rejected rather than acted on.** It reported that `refs/Testing GUI Applications.pdf` "reads fine now" and that the file's own citation note calling it corrupt/unreadable was therefore stale, based on the `file` command reporting a valid 19-page PDF. Reproducing the claim directly: `PyPDF2.PdfReader` still raises `EOF marker not found` on the same file, and a direct search for the `%%EOF` trailer marker returns zero matches anywhere in the file, `file`'s page count reads the document's internal structure and does not validate the trailer, so its "looks fine" signal was misleading. The citation note was left exactly as it was; the sub-instance's finding was refuted, not applied.
4. Closed four Fail cells that had an empty Evidence column (`D2`/`D3`/`D4` IA03-11, `D3` IA04-13) by citing evidence that already existed rather than fabricating new captures, and in the same pass corrected `findings/Bug_Usability_Findings_Log.md`'s own citation for D-007, which had pointed at a `/complaints/999999` not-found error page, a screen that cannot show a breadcrumb because it is not a real detail page, and substituted a genuine admin-detail-page screenshot instead.
5. Widened D-019 (the stuck-Vietnamese-title bug) from `/notifications` alone to also cover `/complaints/{id}`, once a same-session live observation showed the second route shares the defect, and restored the Vietnamese diacritics an earlier pass's Expected-vs-actual text had accidentally stripped from the same finding.
6. Committed the entire backlog of previously-uncommitted work discovered mid-session: 32 Task 1B evidence screenshots, the Task 2 and Task 3 scaffold templates (confirmed empty of any fabricated participant or session data before committing), the de-AI-ified checklist support files, and an unused `.vscode/extensions.json`, none of which §13's per-step commit discipline had actually reached before this session.
7. **A second sub-instance's finding was checked, and this one held up: D3's own IA04-11 had the exact defect Interaction 17 had already fixed on D6, just not noticed there the first time.** D6's IA04-11 had been reverted from a Fail (substituting the unrelated D-018 observation) back to Not executed in Interaction 17, on the grounds that a bug found along the way should be logged standalone rather than forced into the checklist item it superficially resembles, the same rule D-009 and D-015 already followed. D3's IA04-11 was doing the identical substitution, scoring Fail on D-010 (a Category-dropdown race condition) rather than an actual forced-offline test, and Interaction 17 had corrected D6's copy of this pattern without checking whether the same pattern existed anywhere else. It did. D3's IA04-11 was reverted to Not executed, D-010 became a fourth along-the-way finding, and every downstream count was recomputed: the six-screen total moved from 360/136/109/92/17/224/27 to **360/136/108/92/16/224/28**, the Fail-cell count from 17 to 16, and the distinct fail-cell-derived-finding count from 13 to 12 (16 findings in total is unchanged, since D-010 still exists, just reclassified).

**Human review and action taken:** The decision to run a second adversarial pass rather than trust the first pass's own "everything is now fixed" summary was the student's, made explicitly because the first pass's summary was, by its own account in Interaction 16, exactly the kind of self-report that had already been wrong once that day. The rejected PDF finding (point 3) is the clearest evidence the method worked as intended: a sub-instance's claim was independently reproduced rather than accepted, and it did not survive reproduction. Point 7 is the complementary case: a fix applied to one instance of a pattern (D6) was not automatically checked against every other instance of the same pattern (D3), and it took a fresh, independent pass, one not primed by the first pass's own summary of what it had already covered, to catch that. Every accepted finding from this interaction is a concrete file-plus-line defect that existed before it and does not exist after it, not a stylistic rewrite. What remains genuinely open after this pass, unchanged from §5: roughly two dozen Result cells still use hedged phrasing ("Pass (partial)", "Not fully executed") instead of the bare Pass/Fail/N/A §6 asks for, no PDF exports exist yet, and the final submission zip has not been assembled.

---

## 3. Summary of AI contribution

| Artefact | AI-generated | Human-generated | Human-verified |
| --- | --- | --- | --- |
| Checklist items (v1.9, 60 total) | 56 across v1.0-v1.9 | 4 (v1.1: the keyboard/attribute items the AI could not see from screenshots) | All 60 |
| Item corrections and rewrites | 14 (v1.2) + 10 (v1.3) + 2 (v1.5) + 3 (v1.6) + 10 (v1.7) proposed | | Reviewed; group sign-off from the other three members still pending on the 7 newest items |
| Corrections of the AI's **own** earlier output | 4 survey errors + 3 scope errors (v1.7), found by checking AI claims against human-captured screenshots; 1 finding retracted (D-014); 2 cross-artefact contradictions reconciled (Interaction 16) | Screenshots supplied by the group; retraction and reconciliations authorised by the student | Student-authorised |
| Task 1B execution: 360 item×screen cells | Operated the browser and drafted every row | Student performed all logins/registrations; chose the D5/D6 extension; set the "evidence or not-executed" rule | Summary arithmetic re-derived by hand; every Fail read against its evidence file |
| Task 1B findings (16 stand, 3 retracted) | Drafted, with severity proposed | 1 retracted on self-review (D-014), 2 revised at review (D-011, D-012), 2 retracted and 1 narrowed on live re-verification against EMS (D-013, D-018 retracted; D-016 narrowed) | All 16, plus the 3 retracted rows kept visible with their retraction reasoning |
| Screenshots / EMS evidence | **None. The AI generated no evidence** | 14 Task 1A captures + 32 Task 1B captures, all by the student | |
| Task 2 / Task 3 material | **Templates only. The AI declined to fabricate participants, sessions or cross-browser captures** | Not yet produced | |
| Agent Skills and validator scripts (§8) | Authored by AI | Requirements specified by the student | Scripts run and exit 0 |

Per §12, no evidence artefact in this homework was produced by AI. The AI's contribution is confined to text artefacts and to operating a browser the student had already authenticated.

## 4. Material for the AI Critique (§11)

§11 requires a **200-300 word paragraph, written by the student**, critiquing the AI. This section is the factual raw material for it, not the paragraph itself.

Concrete AI failures observed across Tasks 1A and 1B:

1. **The AI covered what it was pointed at, and silently reported full coverage of everything else.** The v1.0 prompt supplied screenshots and three heuristic frameworks; the output was well grounded in exactly those and claimed to cover IA-01 to IA-04. It did not, because it was never given the §4 definitions listing what those aspects contain. Breadcrumbs, drag-and-drop reorder and progress bars are named in the assignment and got zero items.
2. **Screenshot grounding produced a systematic happy-path bias.** All twelve original IA-04 items concerned successful actions and none concerned failures. Screenshots show populated, working screens, because nobody screenshots a 500 error.
3. **A coverage illusion.** For progress bars the AI wrote "(and/or upload progress)" inside another item's expected behaviour. The word was present, the coverage was not. This is only detectable by checking the checklist against the specification's own vocabulary.
4. **A confidently stated factual error.** IA04-07 asserted that summary counts should equal the rows displayed. That is wrong for any paginated table, and it would have generated a false bug report during Task 1B.
5. **Plausible-looking but wrong citations.** Norman's "Mapping" was attached to five items, at least three of which are Signifiers or Constraints, while Nielsen H3 and Shneiderman R3/R4/R5 went uncited. The citations read as authoritative and were not.
6. **Padding toward a requested number.** Asked for exactly 48 items, the AI split one rule (upload aspect-ratio helper text) into two items to help reach the count. Asked separately for 66 items' worth of coverage, it produced them without once asking whether 66 items × 4 screens × 4 people could actually be executed. It optimised the requested metric while ignoring the constraint that gives the metric meaning.
7. **Tool-mediated blindness, and it was one-directional.** Given a browser, the AI surveyed EMS almost entirely by CSS selector, then wrote the results up as facts about the product: "no progress bar", "no back control", "no native date inputs". All three were wrong, and wrong in the *same way*: `progress,[role=progressbar]` cannot see a bar meter built from styled `div`s, a text match on `"back"` cannot see an icon-only button, and an input census run on one form says nothing about another. The instrument's limits silently became the product's description, and because the bias runs one way, the AI systematically **under-reported what EMS contains**. A fourth error came from the opposite direction: reading `innerText` without separating interface chrome from **user-generated content**, so a support-request title a student had typed (`8:07 25/07`) was written up as a date-format defect.
8. **Only human-captured evidence caught it.** The four errors survived a conformance audit, a coverage audit and two further survey passes, all AI-run. They fell in minutes once screenshots taken by a person were used as the control. An AI checking its own output reproduces its own blind spot, however the prompt is reframed.
9. **Given evidence, the AI over-ran the task boundary.** Once the screenshots were supplied, it did not stop at correcting the checklist: it began recording verdicts ("this is a Fail", "strong candidate finding") inside a **Task 1A** artefact whose whole purpose is to define *how* to check, and inside a **shared** file that four people submit. It was fluent about *what* it saw and silent about *whether it was allowed to say so*. The student caught this, not the AI.
10. **The AI reported a Critical defect that did not exist, and its own attempt to reconcile the record made the error harder to see, not easier.** D-018 was logged as the attachment image never loading, "no spinner, no error, no content", and the AI's own supporting claims were that zero network requests were issued and that no `<img>` element existed in the DOM. Both claims were checked directly on 2026-07-31 and were false: the element existed, the request returned HTTP 200, and the file was a genuine 68-byte, 1-by-1-pixel PNG the AI's own earlier D1 test run had uploaded. The image was rendering correctly the whole time; a 1-pixel image scaled into a large pane looks blank. That is a DOM-query failure, the same class as points 1 and 7. What compounds it: when the AI later noticed this Fail conflicted with a Pass recorded ninety rows earlier for the same lightbox, it did not re-test either row. It invented a plausible-sounding "focus precondition" (ESC works while focus is in the overlay, fails once it leaves) that made both rows internally consistent on paper, wrote it into the report as a settled reconciliation, and reported the contradiction as resolved. The hypothesis was confident, well-argued, and wrong; a same-day live re-test against EMS found Escape closes the lightbox on the first press under every focus condition tried, on both complaint records. So the failure was not only "the AI's tool missed a real element", it was "when the AI's own evidence disagreed with itself, it resolved the disagreement by reasoning instead of by looking", and the reasoning was persuasive enough that it stood unquestioned until someone deliberately went back to the product instead of the document.

**What the AI did well**, recorded because a critique that only accuses is not an assessment: it explained *why* it had missed something once a gap was pointed out, more usefully than it found gaps unprompted; the second, differently-framed pass ("what does the spec require that this file lacks?") found real defects the first could not; it verified structural claims by script rather than by assertion, which is why item counts and traceability tables held up under checking while prose claims did not; it declined to invent the "team experience" checklist items, Task 2 participants and Task 3 captures when asked in ways that would have raised the apparent score; when told to attack its own findings before submission, it retracted one (D-014) rather than defending it; and when given permission to check its own reconciliation against the live product instead of against its own earlier writing, it retracted two more (D-013, D-018) and narrowed a third (D-016) rather than defending a hypothesis it had just spent an entire session constructing.

**The transferable principle.** The second AI pass found what the first could not, not because the model changed, but because the *question* changed: from "generate a checklist from these materials" to "verify this checklist against this specification". Generation and verification need to be separate prompts with different grounding, and the human has to supply the standard against which the AI's own output is judged.

Points 7, 8 and 10 sharpen it in two directions. First, reframing the question is not always enough: when the error comes from the AI's **instrument** rather than its reasoning, no amount of re-asking will surface it, because every pass looks through the same instrument. The four survey errors and D-018 itself were exposed only when the **type of evidence** changed: from DOM queries and self-consistency checks the AI ran, to a live fetch and a screenshot a person had taken. So the rule is not merely "verify in a separate pass" but "verify against evidence the AI did not produce"; a claim of **absence** deserves more suspicion than a claim of presence, since "EMS has no progress bar" is really "my selector matched nothing"; and a reconciliation that makes two of the AI's own claims agree with each other is not yet a reconciliation that makes either claim true. Second, and only visible once the artefacts grew large: the AI reasons locally and does not re-read what it has already written. Finding the ESC contradiction at all took a pass whose question was "does this file contradict itself?", care no amount of attention to individual rows would have produced. But that pass only located the contradiction; it did not resolve it correctly, because resolving it still meant going back to the product rather than writing a more careful-sounding paragraph. Self-consistency and correctness are different checks, and passing the first proves nothing about the second.

## 5. Outstanding before submission

| Task | Status |
| --- | --- |
| Task 1A: shared GUI checklist | **Complete**: v1.9, 60 items, script-verified. Two known gaps carried forward: the pillar-4 team-experience grounding (4 of 60 items) and group sign-off from the other three members on the 7 newest items. |
| Task 1B: checklist execution on ≥ 3 screens, bug reports | **Complete**: 60 items × 6 screens = 360 cells; 108 executed, 92 Pass / 16 Fail, 28 not executed with named causes and owners; 16 findings after live re-verification retracted 2 (D-013, D-018), narrowed 1 (D-016) and reclassified 1 (D-010, from a substituted Fail to an along-the-way finding) beyond the 1 (D-014) already dropped on self-review. |
| Task 2: user testing with 5 real participants, Usability Report | **Not started.** Templates only; nothing has been entered that did not come from a real session. |
| Task 3: cross-browser / cross-platform matrix | **Not started.** Template only. Requires real devices or a cloud device lab, and no cell has been recorded yet. |
| §7: Google Form submissions | **Outstanding for all 16 findings.** The log's `Form-submission timestamp` column reads `TODO` on every row because no finding has been submitted yet. The TA may cross-check counts against the form. |
| §8: Agent Skills and demo video | Seven skills built and used throughout (`web-ui-survey`, `gui-checklist-design`, `gui-checklist-execution`, `usability-test-study`, `cross-platform-matrix`, `findings-log`, `ai-audit-log`). **Demo video links still TODO.** |
| §13: Git commit log | Regenerated scoped to HW03 (Interaction 16); it covers every commit made for this assignment to date. |

