# Shared GUI Checklist — EMS (Event Management System)

> **Group deliverable — Task 1, Part A**
> **53 items**, sized so one member can execute the whole checklist across ≥ 3 screens within the assignment's time budget.
> Grounded on four pillars: **international standards** (WCAG 2.1) · **recognised heuristics** (Nielsen 10, Norman 6, Shneiderman 8 — all fully cited) · **the real system under test** (14 screenshots + a live survey of 14 running pages) · **the team's own experience** of using EMS.

## Group Information

- **Group ID**: 09
- **Date created**: 2026-07-25
- **Version**: v1.7 (2026-07-26 — every claim re-verified against the 14 screenshots; four survey errors corrected)

**Members**

| # | Student ID | Full Name |
| --- | --- | --- |
| 1 | 23127006 | Trần Nguyễn Khải Luân |
| 2 | 23127128 | Nguyễn Thành Tiến |
| 3 | 23127179 | Nguyễn Bảo Duy |
| 4 | 23127184 | Lê Phạm Kiều Duyên |

## Scenario assignment (§5 no-duplication rule)

| Student ID | Member | Scenario | Screens owned | Account needed |
| --- | --- | --- | --- | --- |
| 23127006 | Trần Nguyễn Khải Luân | **A** — Admin creates and manages events | **A1** Events list (filters, notification dots) · **A2** Add/Edit Event form · **A4** Participants & Reviews | `admin@gmail.com` |
| 23127128 | Nguyễn Thành Tiến | **B** — User registers to attend an event | **B1** Home / events listing · **B2** Event detail · **B3** Registration form · **B4** My Registrations / ticket | **Own student account — must be created first** |
| 23127179 | Nguyễn Bảo Duy | **C** — Admin manages users | **C1** Users list · **C2** Assign Role / Edit user · **C3** Block-Unblock & Reset-Password dialogs · **C4** Export to Excel | `admin@gmail.com` |
| 23127184 | Lê Phạm Kiều Duyên | **D** — User requests Support, Admin resolves | **D1** Create support request · **D2** My Requests + detail · **D3** Admin Support Requests list · **D4** Admin request detail | Both — admin, plus a user account to file the request |

**Compliance with §5:** four members, four distinct scenarios, no shared screens — the no-duplication rule is satisfied by scenario alone; no screen appears twice.

**Why four screens for B, C and D rather than three.** The minimum is three, but the live survey showed that B, C and D each have thin coverage at three screens:
- **B** — B1/B2/B4 contain no substantial form, so most of IA-02 would be N/A. Adding **B3 (registration form)** gives the IA-02 items a referent.
- **C** — the user-administration surface is small (a 7-column table, two filters, Edit/Delete row actions). Taking all four C screens keeps the applicable-item count respectable.
- **D** — D1–D4 span the user and admin sides, which is what the scenario is about; dropping one loses either the filing or the resolving half.

**Scenario B — account blocker RESOLVED (verified v1.7).** The v1.6 survey ran as `admin@gmail.com` and reported that B3/B4/B5 were unreachable, because EMS refuses registration actions to admins ("Admin can view role information only (no registration action)"). The screenshot evidence shows this is no longer the state of play: `User_B3_RegisterForm.png`, `User_B4_MyTicket.png` and `User_B5_PostEvent_StarReview.png` were all captured from the **student account `tien@gmail.com` (avatar `TTN`, role Student)**, and `User_B4_MyTicket.png` shows **Registered Activities: 1** — ICAMM'26, registered at `25/07/2026 21:06`, role "Sinh viên tham dự". The account exists and the registration path works. **No longer on the critical path.**

**Open scope question for B — B2 and B3 may be the same screen.** `User_B3_RegisterForm.png` shows the "Registration roles" block and the **Register (Student)** button rendered *inside the public event-detail page*, not as a separate form. Before Task 1B the owner of B must check whether clicking Register opens a confirmation modal. If it does not, B2 and B3 count as **one** screen and a fourth screen is needed to keep ≥ 3.

> **Action required before Task 1B:** confirm or swap these assignments, then commit the table — §5's no-duplication rule needs group-level evidence.

## How to use this checklist

Each row is one checkable item. For Task 1 Part B, copy the table into your own `Execution_Report.md` and add **Result** + **Notes** columns per screen. Do **not** edit item wording per-member — the checklist must stay identical across the group.

**Result values — Pass / Fail / N/A.** §6 Part B asks for Passed or Failed, but this checklist is shared across scenarios A–D, so some items address widgets that do not exist on a given screen. Marking those "Pass" would be false and "Fail" would invent a defect.

- **Pass** — the item applies here and the expected behaviour was observed.
- **Fail** — the item applies and the expected behaviour was **not** observed. Attach a screenshot and give the reason in Notes.
- **N/A** — the widget the item describes is absent from this screen. **A one-line reason is mandatory.**

Report in `README.md`: *items designed (53) / applicable / executed / passed / failed*. Never count N/A as a pass.

> **This file carries no results.** It is the Task 1A deliverable — verification rules and expected behaviour only. Pass / Fail / N/A, screenshots of failures and bug reports all live in each member's own Task 1B `Execution_Report.md`. See *Why this file contains no findings* below.

## Predicted N/A by scenario

From the live survey. These are **predictions to plan with, not results** — confirm each on your own screens and record the reason in Notes. Items not listed are expected to apply.

| Scenario | Expected N/A | Why |
| --- | --- | --- |
| **A** — event admin | IA01-10, IA01-11, IA03-12, IA04-07 | Spotlight hero and QR ticket are participant-side; no orderable list on A1/A2/A4; the Pending/Resolved cards belong to D3. **IA04-13 is NOT N/A** — corrected in v1.7: `Admin_A4_Participants.png` shows a green **Export** button on the Registrants tab, which is exactly §5 A4's "Export" |
| **B** — participant | IA02-05, IA02-06, IA02-07, IA02-11, IA02-14, IA03-08, IA04-06, IA04-09, IA04-13 | No rich-text editor, date pickers, toggles or upload on the participant screens; no data table; "Important Update" and check-in scanning are admin-side. *(IA04-13 stays N/A only if B does not take `/profile`; the My Activities Export lives there)* |
| **C** — user admin | IA01-10, IA01-11, IA02-03…07, IA02-11, IA02-14, IA03-12, IA04-05, IA04-06, IA04-09, IA04-10 | The user-admin surface has no upload, rich-text, date control, toggle, capacity figure or real-time counter |
| **D** — support | IA01-10, IA01-11, IA02-05, IA02-06, IA02-07, IA02-14, IA03-08, IA04-05, IA04-06, IA04-09 | No rich-text editor or toggle on the support forms; the support **tables** carry no header sort/filter controls. **IA02-11 removed from this list in v1.7** — the Support requests Filters panel has native **From date / To date** inputs, so D does have a date control to test |

**Richest scenarios:** A (the Add/Edit Event form alone exercises most of IA-02) and D (spans user + admin). **Thinnest:** C — its owner should take all four screens and expect a higher N/A count, which is fine as long as every N/A carries a one-line reason.

## Interface Aspects (IA) legend

| Code | Aspect | Description (§4 of the assignment) |
| --- | --- | --- |
| IA-01 | General UI standards | Layout, alignment, typography, colour, consistency, i18n (EN/VI), empty/loading states |
| IA-02 | Forms | Labels, validation, error placement, required-field handling, uploads, rich-text editor |
| IA-03 | Navigation | Menus, breadcrumbs, tabs, sidebar, drag-and-drop reorder, back/return actions, deep links |
| IA-04 | Feedback / state | Toasts, badges, confirmation dialogs, progress bars, status colours, real-time updates |

## Source screenshots referenced

Folder: `../screenshots/` (i.e. `HW03/screenshots/`) — `Admin_A0_Dashboard_KPIs.png` · `Admin_A1_EventsList.png` · `Admin_A2_AddEditEvent.png` · `Admin_A4_Participants.png` · `Admin_C1_UsersList.png` · `Admin_C3_UserDialog.png` · `Admin_D3_D4_SupportManagement.png` · `User_B1_Home_Header_i18n.png` · `User_B2_EventDetail_Banner_Register.png` · `User_B3_RegisterForm.png` · `User_B4_MyTicket.png` · `User_B5_PostEvent_StarReview.png` · `User_D1_CreateSupport_Form.png` · `User_D2_SupportDetail_Response.png`

> **Status (v1.7):** all 14 PNGs are present in `HW03/screenshots/` and every claim in this file has been re-checked against them — the corrections are marked *corrected v1.7* below and listed in the changelog.
>
> **Two files are mis-named — fix before submission.** `User_B4_MyTicket.png` shows **`/profile` → My Profile + My Activities**, not a ticket (and the **QR Code button on it is disabled**, greyed out behind the banner "Please enter your member code to complete your profile"). `User_D2_SupportDetail_Response.png` shows the **My Requests list** (`/complaints`), not the request detail with the official response. The support-request **detail page and its image lightbox have not been captured at all** — IA03-10 currently has no evidence.

## EMS widget inventory (live survey, 2026-07-26)

A **survey pass** over the running EMS to confirm which widgets exist, so items describe the real product. **No item was executed and no Pass/Fail recorded** — that is Task 1B.

Pages surveyed (14): `/login` · `/dashboard` · `/dashboard/admin` · `/dashboard/admin/events` · `/dashboard/admin/categories` · `/dashboard/admin/users` · `/dashboard/admin/complaints` · `…/events/views?id=` · `…/events/edit?id=` · `/events/{id}` · `/complaints` · `/complaints/new` · `/profile` · 404 page. Full detail in `EMS_Live_Survey_2026-07-26.md`.

| Widget | Present? | Consequence |
| --- | --- | --- |
| Admin sidebar, 9 destinations + Collapse | **Yes** — 7 links; *Analytics* and *Settings* are `<button>`, not links | IA03-01 applies; a `<button>` destination cannot be deep-linked |
| Event detail tabs (5, `role="tab"`) | **Yes** | IA03-02, IA03-09 apply |
| Events table, 18 columns | **Yes** | IA03-06, IA03-08 apply |
| Column **sorting** | **Not found** — all 7 header controls are filters; no `aria-sort` | IA03-08 classifies sort vs filter instead of assuming sorting |
| **Breadcrumb** | **Not found on any page surveyed** | IA03-11 checks for any ancestor-path affordance |
| **Back control on admin event detail** | **Present — corrected v1.7.** The v1.6 survey reported "no back control" from a text match on `"back"`; `Admin_A4_Participants.png` shows a **round ← icon button** immediately left of the event title. It is icon-only with no visible text label | IA03-11 no longer treats this page as "neither breadcrumb nor back"; IA03-04 now checks the **accessible name** of an icon-only back control |
| **Drag-and-drop reorder** | **Not found** — no `draggable`; apparent Categories matches were Tailwind classes containing `dat` | IA03-12 checks for an orderable list first, allows justified N/A |
| **Carousel** on home hero | **No** — "SPOTLIGHT EVENT" is a static hero; no slider lib, no controls, no auto-advance over 10 s | IA01-10 rewritten to spotlight-hero correctness |
| **Progress bar / bar meter** | **Present — corrected v1.7.** The v1.6 survey reported "not found" from a `progress,[role=progressbar]` query. `User_B5_PostEvent_StarReview.png` shows a **Rating summary with five horizontal bar meters** (5★…1★), drawn as styled `div`s — invisible to that selector. Capacity figures ("Lecturer 0 / 3") are still text-only | IA04-10 now covers **both**: the rating bars (does the fill match the number?) and the text-only capacity |
| Rich-text editor | **Yes** — ProseMirror/TipTap | IA02-05, IA02-14 apply |
| Upload + ratio helper | **Yes** — "4:3" and "24:9" present; 4 file inputs | IA02-03, IA02-04 apply |
| Selection controls | 7 `role="switch"` · 7 checkboxes · 1 `<select>` · dropdown filter menus. **No radio buttons** | IA02-12 names the kinds that exist |
| Date & time entry | **Mixed — corrected v1.7.** The admin event form uses **custom controls** (0 `input[type=date]` / `datetime-local`). But the Support requests **Filters panel** has native date inputs: `Admin_D3_D4_SupportManagement.png` shows **From date / To date** with a `dd/mm/yyyy` placeholder and the browser's own calendar icon | IA02-11 tests both kinds and treats the mix as a consistency finding. The native placeholder follows the **browser locale**, so it will differ across the Task 3 matrix — record that rather than reporting it as a defect |
| `aria-live` / `role="status"` | **Not found on any page surveyed** | IA04-12 applies; confirm during execution |
| Programmatic `required` | **Inconsistent** — 3 on the user support form, **0** on the admin event edit form despite red asterisks | IA02-01 now compares the two forms |
| Deep-link scheme | **Inconsistent** — events use `?id=14` (`/events/1` → 404); support requests use a path segment (`/complaints/8`) | IA03-07 tests both forms and treats the inconsistency as a finding |
| Users Management | 7 columns (USER · Role · MEMBER CODE · Status · CREATED · UPDATED · ACTIONS); 2 header filters only, no sort; row actions **Edit user** / **Delete user**; toolbar **Export** + **Add User**. No Assign-Role / Block / Reset-Password button at row level — those live inside the Edit dialog | IA02-02, IA03-06, IA03-08, IA04-02, IA04-03 apply; scenario-C members should open the Edit dialog to locate C2/C3 functions |
| Support request management | 5 columns (Requester · Request · Status · Time · Assignee); **Pending / Resolved are `<button>`, not `role="tab"`**, styled as summary cards with the active one outlined amber; a dedicated **Filters card** — search · Member code · Category dropdown · **From date / To date (native)** · clear-filters icon; toolbar **Export Excel**; no header filter or sort controls | IA03-02 widened to compare both tab groups; IA02-11 and IA04-07 apply |
| **Export to Excel** | **Present in FOUR places — corrected v1.7.** Users Management ("Export"), Support requests ("Export Excel"), `/profile` → My Activities ("Export"), and — missed in v1.5/v1.6 — the **Registrants tab of an event** (`Admin_A4_Participants.png`), which is §5 A4's Export | **IA04-13** covers all four; it is **not** N/A for scenario A |
| User-side routes | `/complaints` (My Requests) · `/complaints/new` (create form) · `/profile` · `/notifications`. **None appears in the header nav** — all are behind the avatar "Open menu" button | IA03-01, IA03-07; note the discoverability cost for scenario D |
| Create Support Request form | Labels: Request type (Support / Complaint / Contact / Other) · Issue requiring support · Detailed description · "Add evidence images — JPG, PNG, GIF or WEBP · Up to 5 images · 5 MB each". 1 file input, 2 textareas, 1 select, live counter `0/255`. **`required` = 3** | IA02-01, IA02-03, IA02-04 |
| QR / barcode | Reached via the **QR Code** button on `/profile` (1 canvas element). **Precondition — corrected v1.7:** on an account with no member code the button is **disabled** (`User_B4_MyTicket.png` shows it greyed out under the banner "Please enter your member code to complete your profile"). Fill the member code first | IA01-11 |
| My Requests empty state | "No requests yet" | IA01-06 |
| Event detail (public) | "← Back to events" present; **no breadcrumb**; 3 images, **all carrying `alt`**; role blocks show "Registered 2/80 · Pending 2 · Confirmed 0 · Waitlisted 0" | IA01-13, IA03-04, IA03-11, IA04-05 |

### ✔ Scenario B — the admin-account blocker no longer applies (v1.7)

The v1.6 survey ran as `admin@gmail.com`, where every event detail page reads **"Admin view only"** / **"Admin can view role information only (no registration action)"** and renders no Register button. That observation is accurate **for an admin session** and is worth keeping as a role-based-UI note.

It is **not** a blocker. The screenshot set was captured from a **student account** (`tien@gmail.com`, avatar `TTN`, role Student — also visible as an Active/Student row in `Admin_C1_UsersList.png`), and `User_B4_MyTicket.png` shows **Registered Activities: 1** with ICAMM'26 registered at `25/07/2026 21:06`. B3 and B4 are reachable today. Use the student account, not the admin account, for anything on the B path and for the user half of D.

### ⚠ Why this file contains no findings

**This is a Task 1A artefact. It defines *how* to check and *what* the expected behaviour is — it records no results.** Every Pass / Fail / N/A belongs in each member's own `Execution_Report.md` (Task 1B), produced by running the item against the live system.

Two reasons this matters beyond tidiness:

1. **§18 — the shared checklist is the *only* thing allowed to be identical across the group.** Selection of screens, execution, findings and severities must each be your own. If this file listed defects, four members would file four identical Bug & Usability Findings Logs, and §7 says the TA may cross-check them against the Google Form submissions.
2. **§12 — evidence must come from execution.** A defect written down before anyone ran the item is not an observation, and the dataset behind it drifts anyway (the ngrok instance resets, and the counts recorded during the survey have already changed once).

Earlier drafts of this section listed specific suspected defects. They have been removed. If you noticed something while reading the survey, treat it as a **place to look**, not as a result — then find it yourself, capture your own screenshot, and write it up in your own words.

> Where to look hardest, without prejudging what you will find: page **count labels** against the rows actually rendered · **date and time rendering** across the admin and participant areas · **KPI and summary figures** against the underlying lists · the **`<title>` tag** versus page-body language · **pagination controls** across the five lists that have them.

---

## Checklist (53 items)

### IA-01 — General UI Standards (13 items)

| Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |
| --- | --- | --- | --- | --- |
| IA01-01 | IA-01 | Nielsen H4 — Consistency and Standards / Slides S13 p.16 — Typography, Layout and alignment | Compare across the Events, Users Management and Support requests screens: the page-title treatment (weight, size, underline accent); the padding and vertical rhythm of the white content cards; and the alignment of the four Dashboard KPI cards. | All three are consistent: one page-title style system-wide, one card padding/spacing scale, and KPI cards of equal size, evenly spaced, sharing a baseline. |
| IA01-02 | IA-01 | Shneiderman R1 — Strive for Consistency | Compare the nine sidebar icons (Users Management, Categories, Academic Years, Campuses, Events Management, Support requests, User Guide, Analytics, Settings). | All icons share stroke width, size and alignment; the active item is highlighted the same way everywhere. |
| IA01-03 | IA-01 | Nielsen H4 / Norman P5 — Consistency / Slides S13 p.16 — Color scheme | Check that the primary action colour (cyan/blue fill: "+ Add Event", "+ Add User", "Publish", "Register (Student)") is reserved for primary calls-to-action. | The accent colour marks the single primary action per screen and is never reused decoratively. |
| IA01-04 | IA-01 | Nielsen H8 — Aesthetic and Minimalist Design · *corrected v1.7* | On the Add/Edit Event form, compare the **nine** section headers against field labels ("Event Title", "Start Date & Time"…). The nine, in page order (`Admin_A2_AddEditEvent.png`): "Thumbnail", "Event Banner", "Attachments", "Basic Information", "Date & Time", "Categories", "Registration", "Location & Organization", "Additional Options". *("Lecturer Roles" appears on the **edit** form / once lecturer registration is enabled — count it if your screen shows it.)* | Section headers are visually distinct from field labels, giving a clear two-level typographic hierarchy — and the same treatment is used for **all** of them, including the two below the fold. |
| IA01-05 | IA-01 | WCAG 2.1 SC 1.4.3 — Contrast (Minimum) | With the DevTools contrast inspector (or WebAIM Contrast Checker), measure text-vs-background contrast on every status pill: "Pending", "Active"/"PUBLISHED", "Draft", "Blocked". | Every pill meets **4.5:1** for normal text (**3:1** if ≥ 18.66 px bold / 24 px regular). Record the measured ratio in Notes. |
| IA01-06 | IA-01 | Nielsen H1 — Visibility of System Status | Trigger an empty result: open "Registrants" for an event with zero registrants, search a term with no matches, or open My Requests with none filed ("No requests yet"). | A clear, centred empty-state message appears instead of a blank table with only headers. |
| IA01-07 | IA-01 | Nielsen H1 — Visibility of System Status | Reload a data-heavy screen (Dashboard KPIs, Events list, Users list) with DevTools → Network → "Slow 3G". | A spinner/skeleton shows while data loads; KPI numbers never flash "0" or blank before the real value arrives. |
| IA01-08 | IA-01 | Slides S13 p.26 — Localization and Internationalization / Nielsen H4 / Slides S13 p.7 — prevent text overflow | Switch the header EN/VI toggle on at least three screens (Admin Dashboard, Events list, public Home). Check every static label — **including the browser tab `<title>`** — and check how long Vietnamese titles with diacritics wrap inside cards and table cells. | The toggle sits in the same header position everywhere and switches **all** static labels, leaving no untranslated string or raw translation key — the `<title>` included. Vietnamese diacritics wrap inside their container with no clipping, overlap or horizontal overflow. |
| IA01-09 | IA-01 | Slides S13 p.26 — Localization / Nielsen H4 · *added v1.2* | Switch EN/VI, then compare the same event's date/time and any numeric value on Events list, event detail and My Registrations. | Dates, times and numbers re-render in the selected locale's format (VI `dd/MM/yyyy` vs EN `MM/dd/yyyy`), not one hard-coded format; no raw ISO timestamp leaks into the UI. |
| IA01-10 | IA-01 | Nielsen H6 — Recognition Rather Than Recall / WCAG 2.1 SC 2.2.2 — Pause, Stop, Hide · *added v1.2* | Inspect the "SPOTLIGHT EVENT" hero on the Events dashboard. Watch ~10 s untouched: does it cycle between featured events (prev/next, position dots) or stay fixed? Check the status badge of the event it promotes, then follow "View details". | If it rotates: the user can pause/stop it and reach every slide via visible, keyboard-operable controls. If fixed: the promoted event is still current — an event badged "Ended" in the top promotional slot is a Fail — and "View details" opens exactly that event. |
| IA01-11 | IA-01 | Slides S13 p.7 — "prevent … distorted graphics" / Nielsen H1 · *added v1.2, route confirmed v1.6, precondition added v1.7* | Open a QR/barcode via the **QR Code** button on `/profile`. **Precondition:** on an account with no member code the button is **disabled** and the page shows "Please enter your member code to complete your profile" — fill the member code first, or the item cannot be executed. View the code on desktop and at a phone-width viewport (≤ 400 px), then try to scan it with a phone camera. | The code renders sharp (not upscaled/blurred), keeps its quiet-zone margin, is neither cropped nor overlapped at any width, and actually scans. Separately, note whether the disabled state **explains itself** — a greyed button whose reason sits in a banner elsewhere on the page is a signifier problem worth recording. |
| IA01-12 | IA-01 | WCAG 2.1 SC 2.4.7 — Focus Visible / Slides S13 p.13 — "Focus on objects needing it?" · *team-added v1.1* | Press Tab repeatedly through interactive elements (nav links, buttons, inputs) on any EMS screen without touching the mouse. | Every focused element shows a clearly visible focus ring with sufficient contrast; focus order follows a logical reading order. |
| IA01-13 | IA-01 | WCAG 2.1 SC 1.1.1 — Non-text Content / Slides S13 p.8 — accessibility features · *team-added v1.1* | Inspect the `alt` attribute (DevTools or a screen reader) of banner and avatar images (event thumbnail/banner, user avatar initials). | Every meaningful image carries descriptive `alt`; purely decorative images use `alt=""` so screen readers skip them. |

### IA-02 — Forms (14 items)

| Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |
| --- | --- | --- | --- | --- |
| IA02-01 | IA-02 | Norman P3 — Constraints / Norman P6 — Signifiers / Slides S13 p.11 — "Mandatory fields, not mandatory" · *sharpened v1.6, third form added v1.7* | Check required-field marking on **three** forms, not one — the admin **Add/Edit Event** form, the user **Create Support Request** form, and the **Edit User dialog** (reached from a row's Edit action on Users Management). For each form record two things separately: (a) is the requirement shown **visually**, and by what marker; (b) do the inputs carry `required` / `aria-required="true"` in DevTools? Then submit each form empty to see which fields the system actually enforces. Note that any asterisk may be drawn in CSS and absent from the DOM text — judge (a) by eye and (b) by the accessibility tree, never by searching page text for `*`. | One convention across the whole product for both (a) and (b): no required field unmarked, no optional field falsely marked, and the requirement exposed programmatically as well as visually. **Different conventions between forms is a Fail**, as is any mismatch between what is marked, what is exposed and what is enforced — a screen-reader user cannot see a red `*`, a CSS-drawn asterisk is not in the accessibility tree, and an unmarked mandatory field is discoverable only by failing to submit. |
| IA02-02 | IA-02 | Nielsen H6 — Recognition Rather Than Recall / Slides S13 p.16 — Labels | Type into fields on the Add/Edit Event form and the Edit User dialog. | Labels ("First Name", "Email", "Event Title") stay visible while typing; they are not placeholder-only text that vanishes on input. |
| IA02-03 | IA-02 | Norman P3 — Constraints / Nielsen H5 — Error Prevention | Before choosing any file, check every upload box: the Thumbnail and Event Banner boxes on Add/Edit Event, and the Attachments box on Create Support Request. | All constraints are stated **before** the user picks a file: aspect ratio ("Recommended ratio: 4:3" / "24:9") and accepted types, size and count limits ("JPG, PNG, GIF or WEBP · Up to 5 images · 5 MB each"). |
| IA02-04 | IA-02 | Slides S13 p.11 — "Data validation" / Nielsen H5 · *added v1.2* | Attempt to attach a disallowed file type (`.pdf`/`.exe`), a file over 5 MB, and a 6th image beyond the stated limit. | Each violation is rejected with a message naming the rule broken and the offending filename. The file is never silently dropped and never appears as though it uploaded. |
| IA02-05 | IA-02 | Nielsen H10 — Help and Documentation / Norman P2 — Feedback | Hover every icon in the rich-text toolbar (Bold, Italic, Underline, Strikethrough, link, image, table, font size, alignment, lists, sub/superscript). | Every icon-only toolbar button shows a text tooltip naming its function. |
| IA02-06 | IA-02 | Nielsen H5 — Error Prevention / Slides S13 p.11 — "Data validation" | On Add/Edit Event set "End Date & Time" earlier than "Start Date & Time" (also for the Check-in and Registration Open/Close pairs). | The invalid combination is blocked or flagged inline immediately; an end before its start is never silently accepted. |
| IA02-07 | IA-02 | Norman P6 — Signifiers / Norman P2 — Feedback · *scope corrected v1.7* | Check **every** toggle on Add/Edit Event, not only the Registration block: the five in "Registration" (Allow Student / Lecturer / Guest Registration, Allow Waitlist, Public Event) **and "Allow Additional Role" in the "Additional Options" block further down the page** — that one is §5 A3's *vai trò phụ*, and scoping the item to the Registration block alone would leave it unchecked. | Every toggle, including the one outside the Registration block, carries adjacent helper text explaining its effect (e.g. "Students can register to attend") beneath its label. Record the result per toggle in Notes: a single Pass/Fail for the whole set hides which toggle failed. |
| IA02-08 | IA-02 | Nielsen H9 — Recognize, Diagnose, Recover / Slides S13 p.16 — Error messages | Submit the Add/Edit Event form or the Register form with a required field missing or invalid. | The error appears inline beside the offending field in plain language — not only as one generic banner at the top. |
| IA02-09 | IA-02 | Nielsen H5 — Error Prevention | Attempt Publish / Submit Request / Register while required fields are incomplete. | The submit button is disabled, or submission is blocked with a clear summary of what is missing — never a silent no-op. |
| IA02-10 | IA-02 | Norman P4 — Mapping (keyboard convention) / Slides S13 p.18 — Form Navigation · *team-added v1.1* | Press Enter from a text input in **(a)** a single-field form or search box ("Search events…") and **(b)** the last field of a multi-field form (Add/Edit Event, Register, Create Support Request). | In both cases Enter triggers the primary submit/search action — and never a *different* button (Delete, Cancel) nor a page reload that loses input. |
| IA02-11 | IA-02 | Slides S13 p.11 — "Incorrect field default" / Nielsen H5 / Nielsen H4 · *added v1.2, premise corrected v1.7* | **EMS uses two kinds of date control, so test both** — the Add/Edit Event "Date & Time" fields (**custom controls**, so native browser behaviour cannot be assumed) and the Support requests **Filters** panel (**native date inputs**). First confirm in DevTools which kind each of your fields is, then for each: the value it opens on; whether a past date can be picked for a new event; whether a date can be typed; whether it opens and operates by keyboard alone. | Opens on a sensible default (today or current value, not an arbitrary epoch); invalid dates are visibly disabled rather than selectable-then-rejected; typed input is parsed or rejected with a message, never silently ignored; reachable without a mouse. **Two different date-entry mechanisms in one product is itself a consistency finding** — record it. Note that the native control's format follows the browser locale and will legitimately differ across the Task 3 matrix; that is not a defect. |
| IA02-12 | IA-02 | Slides S13 p.6 — GUI elements (checkboxes, radio buttons, dropdown menus) / Nielsen H6 · *added v1.2* | EMS uses three kinds of selection control: **toggle switches** (`role="switch"` — Registration toggles), **checkboxes** (Categories, Lecturer Roles) and **dropdowns** (Rows-per-page, column filter menus, Status/Time filters). Operate each kind by mouse and by keyboard alone (Tab → Enter/Space → arrows), and click the **text label** rather than the control. | Every control is fully keyboard-operable, shows its current value when closed, keeps long option lists scrollable inside the viewport, and treats its text label as part of the click target. |
| IA02-13 | IA-02 | Nielsen H5 — Error Prevention / Shneiderman R6 — Permit Easy Reversal · *added v1.2* | Fill several fields of the long Add/Edit Event form without saving, then leave by each exit path: the "← Back" control, a sidebar item, and the browser Back button. | Every exit path warns that unsaved changes will be lost and offers a way to stay; entered data is never discarded silently. |
| IA02-14 | IA-02 | Slides S13 p.12 — "Currency of data on screens" / Nielsen H1 · *added v1.2* | In the rich-text editor apply bold, a bulleted list, a hyperlink and a table; save, reload the edit form, then open that event's public detail page. | All formatting survives save + reload in the editor **and** renders identically on the public page — no raw HTML tags, stripped formatting or collapsed tables. |

### IA-03 — Navigation (13 items)

| Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |
| --- | --- | --- | --- | --- |
| IA03-01 | IA-03 | Nielsen H1 — Visibility of System Status / Nielsen H7 — Flexibility and Efficiency / Shneiderman R2 — Shortcuts / Slides S13 p.17 — Main Menu Navigation | Visit Events Management, Users Management and Support requests in turn, watching the sidebar. Then click "Collapse" at the bottom and repeat. | The sidebar item for the current section is visibly highlighted. Collapsed, the sidebar becomes icon-only yet stays fully navigable (icons clickable, tooltips present) and expands again — all nine destinations remain reachable in one click in both states. |
| IA03-02 | IA-03 | Nielsen H4 — Consistency and Standards · *scope widened v1.5* | Compare the two tab groups in EMS: an event's five tabs (Details, Check-in, Registrants, Review Lecturers, Review Students) and the Support request management Pending / Resolved switcher. Note that the event tabs use `role="tab"` while Pending/Resolved are plain `<button>` elements. | The active tab is clearly marked with a fill/colour distinct from inactive ones, **and both tab groups look and behave the same way** — two visually different treatments for the same "switch between filtered views" pattern is a consistency Fail. The non-semantic group should still be reachable and operable by keyboard. |
| IA03-03 | IA-03 | Nielsen H1 — Visibility of System Status / Slides S13 p.17 — Main Menu Navigation | Check pending-item indicators on tabs and sidebar items — the red dot on "Review Students", the red "4" badge on "Support requests". | Any item with pending/unread content shows a badge or dot, and the count matches the actual number of pending items. |
| IA03-04 | IA-03 | Nielsen H3 — User Control and Freedom / Shneiderman R6 — Permit Easy Reversal / WCAG 2.1 SC 4.1.2 — Name, Role, Value · *sharpened v1.7* | On every detail/sub-page find the back control and use it. EMS renders it in more than one form — a text link ("← Back to events"), a text button ("← Back") and a **round icon-only ← button** — so look for an icon as well as for the word "back"; a text search alone will miss it. Record which form each of your screens uses, and for any icon-only one check in DevTools whether the button has an accessible name (`aria-label` or visually-hidden text). | A back control exists on every detail page and returns to the correct originating list — never to an unrelated or blank page. **An icon-only back button with no accessible name is a Fail** even though it works with a mouse: a screen reader announces only "button". Different visual treatments of the same affordance across screens is a separate consistency finding. |
| IA03-05 | IA-03 | Norman P3 — Constraints / Nielsen H1 — Visibility of System Status | On the public Events page click each status filter: Upcoming / Ongoing / Ended. | Filters behave consistently with their visual design (single-select if styled as exclusive), and the active filter is visibly highlighted against the inactive ones. |
| IA03-06 | IA-03 | Nielsen H4 — Consistency and Standards · *sharpened v1.7* | EMS paginates in **five** places and they are not interchangeable — check each one your screens include and **name the list explicitly in Notes**: participant `/dashboard` · admin Events Management · Users Management · Support request management · `/profile` → My Activities. For each, record the rows-per-page option set, the exact wording of the count label, the controls present (page buttons, "Go to page"), and the number of rows actually on screen. | Two things must hold, and they fail independently — score them as **separate** findings, never as one: (a) **each label is arithmetically true** — it states a range matching the rows displayed and the real total; (b) **the five lists agree** — same rows-per-page scale, same label wording, same control set, same position. |
| IA03-07 | IA-03 | Shneiderman R2 — Shortcuts / Nielsen H4 — Consistency and Standards · *corrected v1.5* | Paste a direct URL to a detail page into a fresh tab without going through the list. **EMS is inconsistent here:** events use a query string (`…/events/views?id=14` — the path form `…/events/14` returns 404) while support requests use a path segment (`…/complaints/8`). Test both forms, and also try an id that does not exist. | Each deep link loads the correct record with no detour through the parent list, and a missing or malformed id produces a proper "not found" state rather than a blank screen or crash. Two different URL conventions for the same "open record N" concept within one product is itself a consistency finding — record it in Notes. |
| IA03-08 | IA-03 | Norman P1 — Visibility / Slides S13 p.12 — "Field order" / Slides S13 p.14 — "State of controls aligns with state of data" · *added v1.2* | On the Events list (18 columns) and the Users list, classify every column-header control: does it **sort** or only **filter**? Operate one twice, then apply a filter and go to page 2. | Each control's purpose is unambiguous from its icon (a funnel filters, an arrow sorts — never conflated); the icon changes appearance while a filter is active; any sort applies asc-then-desc with column and direction shown; state survives pagination. For a table this wide, a **complete absence of sorting** is a usability finding, not a pass. |
| IA03-09 | IA-03 | Shneiderman R8 — Reduce Short-Term Memory Load | While on an event's Check-in / Registrants / Reviews tab, check the page header. | The event (or user/request) name stays visible across all sub-tabs, so the admin never has to recall which record they are managing. |
| IA03-10 | IA-03 | Nielsen H3 — User Control and Freedom / Shneiderman R6 — Permit Easy Reversal · *team-added v1.1* | Open a modal/dialog/lightbox (Edit User dialog, an image lightbox on a support-request detail) and press ESC without clicking. | It closes immediately, exactly as clicking "X" would, and focus returns to the element that opened it. |
| IA03-11 | IA-03 | Slides S13 p.17 — "Breadcrumb Navigation: verify that breadcrumb trails accurately reflect the user's path and allow users to backtrack" · *added v1.2, evidence corrected v1.7* | Go two levels deep along two paths — Events Management → an event → Registrants tab, and Support requests → a request detail. Look for a **breadcrumb** specifically. A back control is a *different* affordance and is scored by IA03-04 — do not report the same absence under both items. | On a page reached through two or more levels, an ancestor path is exposed: a breadcrumb whose segments each name a real ancestor, are clickable, and reflect the path taken. **Absence of any breadcrumb across a three-level hierarchy (list → record → tab) is a Fail, not an N/A** — a one-step back control cannot express a path, so the user cannot jump to an intermediate ancestor. |
| IA03-12 | IA-03 | Norman P6 — Signifiers / Norman P2 — Feedback · *added v1.2* | First establish whether the screen has any user-orderable list (candidates: Categories, Campuses, Academic Years, Lecturer Roles). Hover for a grab cursor or grip icon and attempt a drag. If no orderable list exists, record **N/A**. Otherwise drag, drop, then reload. | Where reordering exists: a visible grab affordance, a drop-position indicator while dragging, order persisting after reload, and a keyboard alternative (its absence being an accessibility defect). Where order is fixed and system-defined, N/A is correct — but note whether a user would reasonably expect to reorder that list. |
| IA03-13 | IA-03 | Nielsen H3 — User Control and Freedom / Slides S13 p.18 — "Links and Buttons … lead to the expected screens" · *added v1.2* | On a list screen apply a status filter, go to page 2, open a detail record, then press the browser **Back** button — then **Forward**. | Back returns to the list with filter and page still applied — not to an unfiltered page 1, a blank screen, or out of the app; Forward re-enters the detail record. |

### IA-04 — Feedback / State (13 items)

| Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |
| --- | --- | --- | --- | --- |
| IA04-01 | IA-04 | Nielsen H2 — Match Between System and the Real World / Slides S13 p.16 — Color scheme | Compare badge colours across screens: PUBLISHED/Active/Resolved (green), Pending (yellow/orange), Admin (blue), Blocked (red). | The same status semantics always map to the same colour system-wide (green = positive/complete, yellow = pending, red = blocked/error, blue = informational). |
| IA04-02 | IA-04 | Norman P6 — Signifiers / Slides S13 p.13 — "Correct window modality?" | Open the Edit User dialog and observe the background; try clicking a control behind it. | The background is dimmed/blurred, controls behind it are not interactive, and a visible "X" close control sits in the dialog header. |
| IA04-03 | IA-04 | Nielsen H5 — Error Prevention / Shneiderman R4 — Yield Closure / Shneiderman R5 — Simple Error Handling | Trigger a destructive action: delete an event (trash icon) or delete a user. | A confirmation dialog appears first, names the specific record, and states the consequence ("This cannot be undone"); cancelling leaves the record untouched. |
| IA04-04 | IA-04 | Nielsen H1 — Visibility of System Status / Shneiderman R3 — Offer Informative Feedback | Complete a successful action: Save Changes on Edit User, Publish an event, Submit a support request. | A toast or inline confirmation names what happened ("Event published successfully"); the UI never just silently redirects. |
| IA04-05 | IA-04 | Nielsen H1 — Visibility of System Status / Slides S13 p.12 — "Currency of data on screens" | Register for an event and watch the role slot counters ("Registered 2/80", "Lecturer 0 / 3", plus Pending / Confirmed / Waitlisted). | Counters update immediately and visibly after the user's own action, with no manual page refresh. |
| IA04-06 | IA-04 | Norman P6 — Signifiers | Check an event carrying both a status badge (PUBLISHED) and an "Important Update" flag. | The "Important Update" flag uses a visually distinct warning style (e.g. amber outline) from the status badge, so the two are never confused. |
| IA04-07 | IA-04 | Nielsen H1 — Visibility of System Status · *wording corrected v1.7* | Note each Pending/Resolved summary card's number, then page through **every** page of the Support Requests table counting rows of that status. **First lower rows-per-page to the smallest value the dropdown offers** — at the default of 20 the whole dataset fits on one page and the check cannot fail. (Record counts are volatile: v1.6 saw Pending 4 / Resolved 7, the screenshot shows Pending 4 / Resolved 4 — read the live numbers, never these.) | Each card equals the **total** for that status across all pages — not the rows on the currently displayed page. A card that counts only the visible page is a Fail. |
| IA04-08 | IA-04 | Nielsen H9 — Recognize, Diagnose, Recover / Shneiderman R7 — Internal Locus of Control | Check contextual banners such as "Please enter your member code to complete your profile" and "Event registration period has ended". | Warning banners use a distinct amber style, state the issue in plain language, and do not block the rest of the page. |
| IA04-09 | IA-04 | Norman P2 — Feedback | On the Check-in tab produce three outcomes: (a) a valid registrant's QR, (b) the same QR again (already checked in), (c) an unrelated/invalid QR. | All three give immediate, mutually distinguishable feedback (e.g. green success / amber duplicate / red invalid, each with a message) — not merely a row appearing later in the log. |
| IA04-10 | IA-04 | Nielsen H1 — Visibility of System Status / Shneiderman R3 — Offer Informative Feedback · *added v1.2, corrected v1.7* | Find every bounded quantity and check **both forms EMS uses**. (a) **Bar meters exist** — the "Rating summary" on a public event detail draws five horizontal bars, one per star level, each labelled "n (n%)". Compare each bar's fill against its own number. *(These are styled `div`s, not `<progress>`, which is why a `progress,[role=progressbar]` query reports zero — do not conclude from a DOM query that EMS has no bars.)* (b) **Text-only capacities** — "Lecturer 0 / 3", "Student 1 / 80", "Registered 2/80" on event cards, event detail and Participants & Reviews, plus any upload or Export indicator. | Where a bar exists, its fill is proportional to its own label — a bar reading "0 (0%)" is empty and a bar reading 100 % is full; a determinate bar is used whenever the total is known. **A bar whose fill contradicts the number printed beside it is a Fail**, and must be reported with the number and the measured fill, not "looks wrong". Where a capacity is bare text with no bar, record a usability finding: a fill ratio is exactly what a bar exists for, and "1 / 80" alone forces the user to compute occupancy mentally. |
| IA04-11 | IA-04 | Slides S13 p.11 — "Mishandling of server process failures" / Nielsen H9 / Shneiderman R5 · *added v1.2* | Force a server-side failure — DevTools → Network → **Offline** — then submit a form, publish an event, and load a list screen. | Every failure gives a visible plain-language error stating what failed and offering a retry. Never an infinite spinner, a permanently blank screen, a raw stack trace or HTTP code, or — worst — a **false success** toast for an action that did not persist. |
| IA04-12 | IA-04 | WCAG 2.1 SC 4.1.3 — Status Messages / Slides S13 p.8 — accessibility features · *added v1.2* | With a screen reader running (NVDA / VoiceOver), or DevTools inspecting the toast container, perform a save action and time how long the toast stays. | The toast container carries `role="status"` / `aria-live="polite"` so it is announced without stealing focus, and it stays long enough to read (≥ 5 s, or until dismissed) rather than vanishing after 1–2 s. |
| IA04-13 | IA-04 | Nielsen H1 — Visibility of System Status / Shneiderman R3 — Offer Informative Feedback / Assignment §5 C4 — "Export to Excel — column completeness and download feedback" · *added v1.5, fourth export added v1.7* | Trigger every export on your screens — there are **four** in EMS: **Export** on Users Management, **Export Excel** on Support request management, **Export** on `/profile` → My Activities, and **Export** on an event's **Registrants** tab (`Admin_A4_Participants.png` — this is §5 A4's Export, so **scenario A must run this item, not mark it N/A**). Watch the interval between click and file arrival. Then apply a filter (role/status, or the Pending tab) and export again. Open each downloaded file and compare its columns against the on-screen table (Users: USER · Role · MEMBER CODE · Status · CREATED · UPDATED) and its rows against what was filtered. | The click produces immediate feedback (busy state, progress, or toast) and a clear completion signal — never a dead button with no response. The file arrives with a meaningful, dated filename. Its columns are complete relative to the on-screen table, and the UI makes unambiguous **whether the export covers the current filter/page or the whole dataset** — silently exporting something other than what the user is looking at is a Fail. |

---

## Coverage summary

| Aspect | v1.0 AI-drafted | v1.1 Team-added | v1.2+ Audit-added | Total |
| --- | --- | --- | --- | --- |
| IA-01 General UI standards | 8 | 2 | 3 | **13** |
| IA-02 Forms | 8 | 1 | 5 | **14** |
| IA-03 Navigation | 8 | 1 | 4 | **13** |
| IA-04 Feedback / state | 9 | 0 | 4 | **13** |
| **Total** | **33** | **4** | **16** | **53** |

## The four grounding pillars

| Pillar | How the checklist is grounded in it | Items |
| --- | --- | --- |
| **International standards** | WCAG 2.1, six success criteria applied with their real thresholds | IA01-05 (SC 1.4.3), IA01-10 (SC 2.2.2), IA01-12 (SC 2.4.7), IA01-13 (SC 1.1.1), IA03-04 (SC 4.1.2), IA04-12 (SC 4.1.3) |
| **Recognised heuristics** | Nielsen 10/10, Norman 6/6, Shneiderman 8/8 — every principle cited by at least one item | See framework table below |
| **The real system under test** | 14 screenshots + a live survey of 14 running EMS pages; 16 items name concrete EMS widgets. 6 were rewritten in v1.3 after the survey showed the widget did not exist as assumed — and in **v1.7** a further 4 were corrected in the opposite direction, after the screenshots showed widgets the DOM-query survey had **missed** (bar meters, an icon-only back button, native date inputs, a fourth Export). Both directions are recorded rather than quietly fixed: they are the evidence that a survey by selector and a survey by eye fail differently | IA01-04, IA01-08…11, IA02-03…07, IA02-11, IA02-12, IA02-14, IA03-01, IA03-07, IA03-08, IA03-11, IA03-12, IA04-05…07, IA04-10, IA04-13 |
| **Team experience** | Items the group derived from its own use of EMS rather than from a source — currently the four v1.1 accessibility/keyboard items | IA01-12, IA01-13, IA02-10, IA03-10 |

> **Known weakness — the experience pillar is the thinnest of the four (4 of 53).** Every other item traces to a standard, a heuristic, the slides, or an observation of the product. Before submitting, each member should add **1–2 items from their own frustrations while using EMS** — something no framework would predict. Log them as v1.7 with the member's name, and record in `Reference_Sources_and_Prompts.md` §5 why no source would have produced them. This is the cheapest available gain on criterion 1a, and the only pillar an AI cannot supply.

## Conformance map — every element named in §4

| IA | Element named in §4 | Item(s) |
| --- | --- | --- |
| IA-01 | Layout · Alignment | IA01-01 |
| IA-01 | Typography | IA01-01, IA01-04 |
| IA-01 | Colour | IA01-03, IA01-05 |
| IA-01 | Consistency | IA01-01, IA01-02, IA01-03 |
| IA-01 | i18n EN/VI | IA01-08, IA01-09 |
| IA-01 | Empty states | IA01-06 |
| IA-01 | Loading states | IA01-07 |
| IA-02 | Labels | IA02-02 |
| IA-02 | Validation | IA02-04, IA02-06, IA02-08, IA02-09, IA02-11 |
| IA-02 | Error placement | IA02-08 |
| IA-02 | Required-field handling | IA02-01, IA02-09 |
| IA-02 | Uploads | IA02-03, IA02-04 |
| IA-02 | Rich-text editor | IA02-05, IA02-14 |
| IA-03 | Menus · Sidebar | IA03-01, IA03-03 |
| IA-03 | **Breadcrumbs** | IA03-11 |
| IA-03 | Tabs | IA03-02, IA03-09 |
| IA-03 | **Drag-and-drop reorder** | IA03-12 |
| IA-03 | Back / return actions | IA03-04, IA03-13 |
| IA-03 | Deep links | IA03-07 |
| IA-04 | Toasts | IA04-04, IA04-11, IA04-12 |
| IA-04 | Badges | IA04-01, IA04-06, IA03-03 |
| IA-04 | Confirmation dialogs | IA04-02, IA04-03 |
| IA-04 | **Progress bars** | IA04-10 |
| IA-04 | Status colours | IA04-01, IA04-08 |
| IA-04 | Real-time updates | IA04-05, IA04-09 |
| §5 C4 | **Export to Excel** (column completeness + download feedback) | IA04-13 |

## Per-widget coverage (§6: "the per-widget checklists")

| Widget | Item(s) | Widget | Item(s) |
| --- | --- | --- | --- |
| Buttons / CTAs | IA01-03, IA02-09 | Tables — pagination | IA03-06 |
| Text fields | IA02-02 | Tables — sort / filter headers | IA03-08 |
| Checkboxes · dropdowns · switches | IA02-07, IA02-12 | Tabs | IA03-02, IA03-09 |
| Date picker | IA02-06, IA02-11 | Modal / dialog / lightbox | IA04-02, IA04-03, IA03-10 |
| File upload | IA02-03, IA02-04 | Toast | IA04-04, IA04-11, IA04-12 |
| Rich-text editor | IA02-05, IA02-14 | Progress bar / capacity | IA04-10 |
| Badges / status pills | IA01-05, IA04-01, IA04-06 | Spotlight hero | IA01-10 |
| Breadcrumb | IA03-11 | QR / barcode ticket | IA01-11 |
| Search box | IA02-10 | Error messages | IA02-08, IA04-11 |
| **Export / file download** | **IA04-13** | | |

## Heuristic framework coverage

| Framework | Principles cited |
| --- | --- |
| Nielsen (10 heuristics) | **All 10** — H1, H2, H3, H4, H5, H6, H7, H8, H9, H10 |
| Norman (6 principles) | **All 6** — P1 Visibility, P2 Feedback, P3 Constraints, P4 Mapping, P5 Consistency, P6 Signifiers |
| Shneiderman (8 golden rules) | **All 8** — R1…R8 |
| WCAG 2.1 | SC 1.1.1, 1.4.3, 2.2.2, 2.4.7, **4.1.2** *(added v1.7)*, 4.1.3 |
| Course slides S13 | p.6, 7, 8, 11, 12, 13, 14, 16, 17, 18, 26 |

## Items added beyond the AI output — and why the AI missed them (§6)

### Round 1 — v1.1, team review of the AI draft (2026-07-25)

| ID | Item | Why the AI missed it |
| --- | --- | --- |
| IA01-12 | Keyboard focus indicator | The AI's grounding was static screenshots; focus state leaves no trace in a still image. |
| IA01-13 | Image `alt` text | `alt` lives in the HTML source, not in rendered pixels. |
| IA02-10 | Enter-to-submit | The AI reasoned about mouse clicks on the visible button and could not infer a habitual keyboard pattern. |
| IA03-10 | ESC closes dialog | It saw the visible "X" and overlooked the keyboard-exit convention — a behavioural rule, not a visual element. |

### Round 2 — v1.2, conformance audit against the assignment text (2026-07-26)

Round 1 asked *"what did the AI miss about the screens?"*. Round 2 asked *"what does the assignment require that the checklist lacks?"*. The root cause of every gap: **the v1.0 prompt grounded the AI in screenshots and three heuristic frameworks, but never in the assignment's own IA definitions or the course slides.**

| ID | Item | Why it was missing |
| --- | --- | --- |
| IA03-11 | Breadcrumb | §4 names it and slide p.17 devotes a bullet to it; neither was in the v1.0 prompt, and no screenshot showed a nested page with one. |
| IA03-12 | Drag-and-drop reorder | §4 names it. Reordering is a *gesture* — no static appearance, so screenshot grounding cannot see it. |
| IA03-08 | Sort vs filter on column headers | Slide p.12 lists "Field order". Sort state is a runtime property; the AI catalogued visible controls without knowing what they did. |
| IA03-13 | Browser Back preserves state | The AI produced the deep-link item and treated URL handling as covered; distinguishing deep link from history restoration needs SPA reasoning, not page appearance. |
| IA04-10 | Progress bar | §4 and §5 both name it. The AI folded it into a sub-clause ("and/or upload progress") — a coverage illusion visible only by checking against the spec's word list. |
| IA04-11 | Feedback when an action **fails** | The most consequential gap: v1.0 produced twelve IA-04 items about success and none about failure. Nobody screenshots a 500 error, so screenshot grounding is systematically biased to the happy path. |
| IA04-12 | Toast `aria-live` and dwell time | An ARIA attribute and a timing property are both invisible in a still frame. |
| IA01-10 | Spotlight hero / carousel | §4 and §5 name a carousel. Auto-advance is *motion*; a screenshot freezes one slide. |
| IA01-09 | Locale-aware date/number format | v1.0 read i18n as "does the Vietnamese text fit". Format localisation needs the same value compared across two locales — a comparison never requested. |
| IA01-11 | QR ticket scannability | Whether a code scans is a physical-world property; the screenshot QR *looks* fine. |
| IA02-11 | Date & time control | v1.0 covered date *logic* but not the *widget*. Slide p.11 lists "Incorrect field default". |
| IA02-12 | Selection controls | Slide p.6 lists them; v1.0's per-widget coverage stopped at the visually prominent widgets. |
| IA02-13 | Unsaved-changes warning | Manifests only on an abandoned interaction; no screenshot shows a half-filled form being abandoned. |
| IA02-14 | Rich-text round-trip | Spans three page states (edit → save → public view); single-screenshot grounding cannot represent a multi-state journey. |

### Round 3 — v1.5, after surveying the admin user/support areas

| ID | Item | Why it was missing |
| --- | --- | --- |
| IA04-13 | Export to Excel | §5 C4 names Export as a candidate *screen*, yet the only prior mention of it anywhere in the checklist was a sub-clause of IA04-10. Nobody screenshots a file download, and the Export buttons sit on two screens the original draft never examined. |

## Checklist changelog

| Date | Version | Change | Author |
| --- | --- | --- | --- |
| 2026-07-25 | v1.0 | AI-drafted 48-item checklist (12/IA) grounded in heuristic references + EMS captures. | AI-assisted draft (Claude) |
| 2026-07-25 | v1.1 | Team review. Added 4 human-identified items the AI missed — accessibility/keyboard gaps invisible to screenshot-only analysis. 52 items. | Group (human review) |
| 2026-07-26 | v1.2 | Conformance audit against the assignment text and course slides. Added 14 items closing every §4-named element with no item (breadcrumbs, drag-and-drop, progress bars) plus per-widget gaps and the missing failure-feedback dimension; applied 14 corrections including a factual error in the Pending/Resolved count item. Added the Pass/Fail/N/A convention and the conformance, per-widget and framework tables. 66 items. | AI-assisted audit (Claude Opus 5), reviewed by the group |
| 2026-07-26 | v1.3 | Live survey of the running EMS. Rewrote 6 items that described widgets EMS does not have (carousel, native date picker, breadcrumb, drag-reorder, column sorting, progress bar) and sharpened 4 with observed detail. Added the EMS widget inventory. | AI-assisted survey (Claude Opus 5 via Claude in Chrome) |
| 2026-07-26 | v1.4 | **Reduced 66 → 52 items** for executability: 5 merges and 8 removals of low-yield items, then renumbered contiguously. Verified after reduction that all 10 Nielsen heuristics, 6 Norman principles, 8 Shneiderman rules, 5 WCAG criteria and every §4-named element remain covered. Added the four-pillar grounding table. | AI-assisted reduction (Claude Opus 5) |
| 2026-07-26 | v1.5 | Surveyed Users Management and Support request management. **Added IA04-13 — Export to Excel**, closing §5 C4. Corrected IA03-07 (EMS uses *two* deep-link conventions) and widened IA03-02 (Pending/Resolved are `<button>`, not `role="tab"`). **53 items.** | AI-assisted survey (Claude Opus 5 via Claude in Chrome) |
| 2026-07-26 | v1.7 | **Verification pass — every claim in this file checked against the 14 screenshots.** Corrected **four widget-inventory errors** inherited from the live survey, each of which had left an item describing something EMS does not have or omitting something it does: (1) bar meters **do** exist (the Rating summary), so IA04-10 no longer assumes text-only capacity; (2) the admin event detail **does** have a back control, an icon-only one, so IA03-04 now covers icon-only forms and IA03-11 was narrowed to breadcrumbs alone — the two no longer report the same absence twice; (3) the timestamp evidence behind IA01-09 quoted user-entered content, so the item now specifies comparing rendered timestamps across areas; (4) native date inputs **do** exist on the Support filters, so IA02-11 covers both control types. Five items sharpened against the captures: IA01-04 (nine section headers, not seven) · IA02-07 (extended to the toggle outside the Registration block) · IA02-01 (a third form, the Edit User dialog) · IA03-06 (all five paginated lists named) · IA01-11 (member-code precondition for the QR button). Scope: the **scenario-B account blocker is retired** — the participant screens were captured from a student account that already holds a registration; **Export exists in four places**, so IA04-13 is no longer predicted N/A for scenario A. **Suspected-defect notes removed from this file** — see *Why this file contains no findings*. **Still 53 items**, none added or removed. | Screenshot verification (Claude Opus 5), pending group sign-off |
| 2026-07-26 | v1.6 | Surveyed the participant-side screens — 14 pages in total. **Found that an admin account cannot reach the scenario-B screens** ("Admin can view role information only (no registration action)"), blocking B3/B4 until the owning member registers their own student account per §4. Sharpened IA02-01 (`required` present on the user support form but absent on the admin event form; the asterisk appears CSS-drawn and outside the accessibility tree), IA04-13 (a **third** Export button on `/profile`) and IA01-11 (QR reachable via `/profile`). Recorded the Vietnamese-`<title>`-with-English-body split across all five participant pages. Added the scenario-assignment table and the per-scenario N/A predictions. Still 53 items. | AI-assisted survey (Claude Opus 5 via Claude in Chrome), reviewed by the group |
