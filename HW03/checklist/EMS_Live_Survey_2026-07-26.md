# EMS Live Survey: captured 2026-07-26

> **Purpose.** A **widget inventory** of the running EMS, taken so that Task 1A's checklist items describe the real product instead of a generic web app. Nothing here was executed and no Pass/Fail was assigned.
>
> **Scope limit, read this first.** This file answers *"what controls does EMS have, and where?"*. It does **not** answer *"what is broken?"*. That is Task 1B, it is **individual** work under §18, and it must come from your own run against the live system with your own screenshots. Where an entry below notes that something looked odd, treat it as **a place to look**, never as a finding to copy: four members submitting the same defect list would collapse §7's cross-check between the Findings Log and the Google Form. The instance also resets periodically, so any count or value recorded here may already be stale.
> **Method.** Claude Opus 5 driving the student's own Chrome (Claude in Chrome extension); the student logged in personally. Mostly DOM queries rather than screenshots, to conserve tokens.
> **Session state.** Logged in as **`admin@gmail.com`** (display name "Tôi là Admin", initials `TLA`), the admin account named in §4. Because EMS blocks registration actions for admins, the scenario-B participant screens could not be reached; see §13.
> **Caution.** §4 of the assignment warns the ngrok tunnel resets data periodically. Record counts (22 events, 4 pending support requests) will drift; treat them as indicative, not fixed.
>
> ## ⚠ Corrections applied 2026-07-26 (v1.7), read before using this file
>
> This survey was taken almost entirely by **DOM query**. Cross-checking it against the 14 screenshots found **four places where a selector returned zero for something that is plainly on the page**. Each is corrected in place below and flagged *corrected v1.7*; they are listed together here because the failure mode matters more than the individual facts.
>
> | # | This file said | Reality | Why the query missed it |
> |---|---|---|---|
> | 1 | No progress bar anywhere | Public event detail has a **Rating summary with five bar meters** | They are styled `div`s; `progress,[role=progressbar]` cannot see them |
> | 2 | No "← Back" on the admin event detail | There **is** a round **icon-only ← button** left of the title | The check was a text match on `"back"`; the button has no text |
> | 3 | Support renders times as `8:07 25/07` | That string is a **request title a user typed**, not a rendered date | Page text was read without distinguishing user content from chrome |
> | 4 | EMS has no native `input[type=date]` | Support requests' **Filters** panel has native **From date / To date** | The input census was run on the event form, then generalised to the product |
>
> All four are corrections to **what EMS contains**: the input to writing accurate checklist items. None of them is a test result, and this file still records no Pass/Fail.
>
> **Transferable lesson (feeds the §11 AI Critique):** a DOM query proves presence reliably and absence only for the exact selector asked. Three of the four errors are *false negatives* pointing the same way, the survey under-reported what EMS has, and the fourth is user content misread as UI. Every "not found" in this file should be treated as "not found **by this selector**" until a screenshot confirms it.

## 1. Access

| Item | Value |
| --- | --- |
| Base URL | `https://promoter-starboard-prude.ngrok-free.dev/` |
| ngrok interstitial | Yes, a "You are about to visit..." page with a **Visit Site** button appears first in a normal browser (bypassed by non-browser user agents). Expect it on every fresh session and in every cross-browser run in Task 3. |
| Login redirect | `/` → `/login?callbackUrl=%2F` |
| After login | `/dashboard` |

## 2. URL map

| Area | URL |
| --- | --- |
| Login | `/login?callbackUrl=%2F` |
| Participant dashboard (events listing) | `/dashboard` |
| Calendar | `/calendar` |
| Saved events | `/my-favorites` |
| User guide (participant) | `/manual` |
| Public event detail | `/events/{id}`, observed ids 1, 2, 6, 7, 10, 12, 14, 18, 25 |
| Admin home | `/dashboard/admin` |
| Users Management | `/dashboard/admin/users` |
| Categories | `/dashboard/admin/categories` |
| Academic Years | `/dashboard/admin/academic-contexts` |
| Campuses | `/dashboard/admin/campuses` |
| Events Management | `/dashboard/admin/events` |
| Support requests | `/dashboard/admin/complaints` |
| User Guide (admin) | `/dashboard/admin/manual` |
| Event detail (admin) | `/dashboard/admin/events/views?id={id}` |
| Event edit (admin) | `/dashboard/admin/events/edit?id={id}` |

**Deep-link scheme:** records are addressed by **query string**, not path segment. `/dashboard/admin/events/1` returns 404; `/dashboard/admin/events/views?id=14` works. Relevant to IA03-07.

**404 page:** branded EMS card, heading "404 / Page Not Found", body "The page you are looking for does not exist or has been moved.", buttons **Go Back** and **Back to Dashboard**. Useful as the expected-state reference for IA03-07 and IA04-11.

## 3. Login page

- Left panel: EMS logo art + "EVENT MANAGEMENT SYSTEM". Right panel: `fit@hcmus` logo, "VNUHCM - UNIVERSITY OF SCIENCE / FACULTY OF INFORMATION TECHNOLOGY".
- Fields: **Email\*** (placeholder "Enter your email"), **Password\*** (placeholder "Enter your password", eye toggle). Button **Login**. Links: **Forgot password?**, **Create guest account**. Divider "OR CONTINUE WITH" + Google / Microsoft buttons.
- Language flag control top-right.
- **Observation (not scored):** the page `<title>` is Vietnamese, `Đăng nhập | HCMUS EMS`, while the entire visible body is English. Relevant to **IA01-08**; note that `<title>` never appears in a screenshot, so this is invisible to screenshot-only review.

## 4. Participant dashboard: `/dashboard`

**Header:** `fit@hcmus` · "EVENT MANAGEMENT SYSTEM / Faculty of Information technology" · nav **Events · Calendar · Saved Events · User guide** · language flag · apps/grid icon · notification bell (badge `0`) · avatar `TLA`.

**Language control:** `aria-label="Switch language"`; opens a dropdown with two options, **Tiếng Việt** (VN flag) and **English** (US flag), current one highlighted. Relevant to IA01-08 / IA01-09.

**Spotlight hero:** label "SPOTLIGHT EVENT", a status badge, event title, description, location, date range, and a **View details** link.
- **No carousel.** No slider-library markup (`carousel|slider|swiper|slick|embla` → 0 matches), no prev/next controls, no position dots, and no slide change after 10 s untouched.
- **Observation (not scored):** the promoted event was badged **"Ended"**: "Chương trình: Gặp gỡ & Trò chuyện cùng Ban chủ nhiệm Khoa CNTT", 28/06/2026. Relevant to IA01-10.

**Controls:** search box "Search events by title..." · status filters **Upcoming / Ongoing / Ended** · **Filters** button · a second filter icon.

**Left rail:** "Categories" panel (14 categories: Movement & Campaign Activities, Culture & Performing Arts, Physical Education & Sports, Volunteering & Community Service, Academic Competitions, Career Orientation & Enterprise Networking, Skills Training & Workshops, Internship & Field Practice, Job Opportunities, Scientific Research, Innovation & Creativity, Thesis / Project Defense, Conferences & Seminars, Other Activities) · "Academic Context" (Standard Program / Special Program → 2025-2026 → Semester 1 / Semester 2) · **Collapse** button.

**Event cards:** status badge (Upcoming / Ongoing / Ended) · title · description · "Event time:" · location · "Registration deadline:" · "Organizer:" · category chips · academic-context chips · campus chip · role capacity blocks **"Lecturer 0 / 3"**, **"Student 1 / 80"** · rating "0.0 (0)" on ended events · **Save** button (`aria-label="Save event"`).

**Pagination:** "Rows per page:" with options **4 / 8 / 12 / 16**; page buttons **1 2 3**; count label **"Showing 1 of 22 events"**.
- **Observation (not scored):** the label reads "Showing 1 of 22 events" while **8 cards** are displayed. Expected wording would be a range ("Showing 1-8 of 22"). Relevant to **IA03-06**.

**Date rendering:** `dd/MM/yyyy HH:mm` (e.g. `28/06/2026 08:30`) while the interface language is English. Whether this changes on switching to VI is **untested**: that is exactly IA01-09.

**Other links present:** `mailto:info@fit.hcmus.edu.vn`; footer with campus addresses, related systems and social links.

## 5. Admin area: `/dashboard/admin`

Page title `Admin Management | HCMUS EMS`; heading "Admin Dashboard".

**Sidebar, 9 destinations + Collapse:**

| Destination | Element type | Note |
| --- | --- | --- |
| EMS Admin (root) | link `/dashboard/admin` | |
| Users Management | link `/dashboard/admin/users` | |
| Categories | link `/dashboard/admin/categories` | |
| Academic Years | link `/dashboard/admin/academic-contexts` | |
| Campuses | link `/dashboard/admin/campuses` | |
| Events Management | link `/dashboard/admin/events` | |
| Support requests | link `/dashboard/admin/complaints` | carries badge **4** |
| User Guide | link `/dashboard/admin/manual` | |
| **Analytics** | **`<button>`, not a link** | cannot be deep-linked or opened in a new tab |
| **Settings** | **`<button>`, not a link** | same |
| Collapse | `<button>` | |

Relevant to IA03-01 (all nine reachable in one click) and IA03-07 (two of them have no URL).

## 6. Events Management: `/dashboard/admin/events`

**Table: 18 columns**: EVENT · EVENT TYPES · TIME · REGISTRATION · CHECK-IN · TYPE · PUBLIC · ACADEMIC CONTEXT · CAMPUS · LOCATION · STATUS · TIME STATUS · LECTURERS · STUDENTS · ORGANIZER · CREATED · UPDATED · ACTIONS.

**Header controls: 7 buttons, all filters, no sorting.** Labels: "Filter by event types", "Filter by event start date", "Filter by public event", "Filter by academic context", "Filter by campus", "Filter by lecturer registration...", "Filter by student registration...". `aria-sort` → **0 occurrences**. Relevant to IA03-08.

**Toolbar:** "All Status" dropdown · "All Time" dropdown · rows-per-page "5" · pages "1 2".

**Row actions:** links to `views?id=` and `edit?id=`; buttons **"Important update"** and **"Delete event"** (the latter likely opens a confirm dialog, relevant to IA04-03; do not trigger it accidentally during automation).

## 7. Categories: `/dashboard/admin/categories`

Table columns: **ICON · CATEGORY · Enabled · ACTIONS**. Button **Add Category**.

**No drag-and-drop reorder.** `draggable="true"` → 0. An initial query for drag-library markup returned 5 hits, but inspecting their class names showed they were `<th>` elements whose Tailwind classes contain the substring `dat`, a **false positive**. Relevant to IA03-12 (N/A is justified here).

## 8. Event detail (admin): `/dashboard/admin/events/views?id=14`

- **5 tabs** with `role="tab"`: **Details · Check-in · Registrants · Review Lecturers · Review Students**. Relevant to IA03-02, IA03-09.
- Headings observed: the event title (twice, page header and content), then the event's own Vietnamese rich-text sections ("1. THÔNG TIN CHƯƠNG TRÌNH", "2. HỌC BỔNG HỖ TRỢ", "3. ĐIỀU KIỆN THAM GIA", "4. THỦ TỤC VÀ HỒ SƠ ĐĂNG KÝ", "5. THỜI GIAN NỘP HỒ SƠ"), plus "Lecturer Roles".
- **No breadcrumb** (`nav[aria-label*=breadcrumb]` and `[class*=breadcrumb]` → 0). Confirmed against the screenshots.
- ~~No "← Back" control found on this page~~, **corrected v1.7.** There **is** a back control: a round **icon-only ← button** immediately left of the event title, visible in `Admin_A4_Participants.png` and again on Create Event in `Admin_A2_AddEditEvent.png`. The original check was a text match for `"back"`, and the button carries no text. Relevant to **IA03-04** (does it have an accessible name?) rather than to IA03-11.
- **No `aria-live`.** ~~No progress bar~~, **corrected v1.7**, see §14: bar meters exist on the public event detail, they are just not `<progress>`.

## 9. Event edit form: `/dashboard/admin/events/edit?id=14`

| Property | Observed |
| --- | --- |
| Section headers | Thumbnail · Attachments · Basic Information · Date & Time · Categories · Registration · Lecturer Roles |
| `input[type=text]` | 20 |
| `input[type=date]` / `datetime-local` | **0**: date & time use custom controls |
| `<select>` | 1 |
| `input[type=radio]` | **0**: EMS has no radio buttons here |
| `input[type=checkbox]` | 7 |
| `role="switch"` | 7 (the Registration toggles) |
| `input[type=file]` | 4 (thumbnail, banner, attachments) |
| Rich-text editor | **ProseMirror / TipTap**: 1 `contenteditable`, 2 ProseMirror nodes (not Quill, not TinyMCE) |
| Aspect-ratio helper text | **"4:3"** and **"24:9"** both present |
| `required` / `aria-required` | **0**: required fields are signalled by the red `*` only |
| `aria-live` | 0 |
| Breadcrumb | 0 |

Relevant to IA02-01, IA02-03, IA02-05, IA02-07, IA02-11, IA02-12, IA02-14, IA01-04.

## 10. Cross-cutting accessibility observations

Measured on all seven pages surveyed (`/dashboard`, `/dashboard/admin`, `/dashboard/admin/events`, `/dashboard/admin/categories`, event views, event edit, 404):

| Property | Result |
| --- | --- |
| `[aria-live]` | **0 on every page** |
| `[role="status"]` / `[role="alert"]` | **0 on every page** |
| `[aria-sort]` | **0** (Events table) |
| `[required]` / `[aria-required]` | **0** (event edit form) |

These make **IA04-12** and the programmatic half of **IA02-01** meaningful tests rather than formalities. Confirm them during execution, do not copy this table into an Execution Report as a result.

## 11. Users Management: `/dashboard/admin/users` (scenario C)

| Property | Observed |
| --- | --- |
| Columns (7) | USER · Role · MEMBER CODE · Status · CREATED · UPDATED · ACTIONS |
| Header controls | 2 only, "Filter by role", "Filter by status". **No sorting**; `aria-sort` = 0 |
| Row actions | **Edit user** · **Delete user**: that is all |
| Toolbar | **Export** · **Add User** · rows-per-page `5` · pages `1 2` · a `7` control |
| Inputs | 1 text (search) · 1 `<select>` · 0 checkbox · 0 `role="switch"` |
| Tabs | none (`role="tab"` = 0) |
| Breadcrumb · `aria-live` · progress bar | 0 · 0 · 0 |

**Mapping against §4 Pool C.** The assignment describes the Users list as "Avatar+Name, Role, Member Code, **Active**, **Audit** columns". The real table has **Status** where the spec says Active, and **CREATED / UPDATED** where it says Audit. Not a defect, just note the naming difference so a Task 1B report does not claim a missing column.

**Important for scenario C, answered by the screenshots (v1.7).** §5 lists C2 *Assign Role* and C3 *Block-Unblock and Reset-Password dialogs*. None is a row-level button; only Edit and Delete are. `Admin_C3_UserDialog.png` shows what the **Edit User** dialog actually contains:

| §5 function | Where it is |
| --- | --- |
| **C2 Assign Role** | Present, a **Role dropdown** inside the Edit User dialog |
| **C3 Block / Unblock** | Present as an **"Active" checkbox** at the bottom of the same dialog, there is no separate Block/Unblock dialog. Whether toggling it raises a confirmation step or an audit prompt is what **IA04-03** asks; execute the item rather than assuming from the static capture |
| **C3 Reset Password** | **Not present anywhere in the dialog.** Fields are First Name · Last Name · Email · Phone Number · Role · Member Code · Active, then Cancel / Save Changes |

**Consequence for the C owner:** C3 as §5 describes it does not exist as a screen. A defensible set of three is **C1 Users list · C2 Edit User dialog · C4 Export**: state in the report that C3's functions were located inside C2 and that Reset Password is absent from the admin UI. Also note the dialog carries **no required-field markers at all**, a third convention feeding IA02-01.

## 12. Support request management: `/dashboard/admin/complaints` (scenario D)

| Property | Observed |
| --- | --- |
| Page heading | "Support request management" |
| Columns (5) | Requester · Request · Status · Time · Assignee |
| Header controls | **none**: no filter and no sort buttons in `<th>`; `aria-sort` = 0 |
| Pending / Resolved | **`<button>` elements, not `role="tab"`**: labelled "Pending4" and "Resolved7" (count baked into the label) |
| Filters | A dedicated **Filters card** (not header controls): "Search name, email or title" · "Member code" · "Category / All categories" dropdown · **"From date" and "To date", native date inputs, `dd/mm/yyyy` placeholder + the browser's own calendar icon (corrected v1.7; the original census was run on the event form and generalised)** · a clear-filters icon top-right |
| Toolbar | **Export Excel** · rows-per-page `20` · page `1` · count label "1-4 of 4 results" |
| Pending / Resolved | Rendered as two **summary cards**, the active one outlined amber, not a tab strip |
| Detail links | `/dashboard/admin/complaints/8`, `/7`, `/6`, `/5`, **path segment**, unlike events which use `?id=` |
| Breadcrumb · `aria-live` · progress bar | 0 · 0 · 0 |
| Sample rows | "Test Support Request" · "Test support request - 23127097 - 8:02 25/07" · "fessefsewfsefsef", the dataset contains obvious test junk |

**Two observations (not scored):**
- **Timestamp rendering, the earlier entry here was wrong, corrected v1.7.** It cited `8:07 25/07` as this screen's date format. That string is the **title of a support request a user typed**, shown in bold in the REQUEST column, `innerText` was read without separating interface chrome from user content. Timestamps on this screen and on the events/users screens do use different styles; **compare them yourself at execution time and quote what you see then** (IA01-01, IA01-09). Do not carry the old string into a report: it quotes another student's data, not the product.
- **IA04-07 is not meaningful at the default page size.** Pending 4 + Resolved 7 = 11 rows with rows-per-page at 20, so everything fits on one page and the "counts must match totals across all pages" check cannot fail. Lower rows-per-page to 5 before running that item.

**Export exists on both admin lists**: "Export" on Users Management and "Export Excel" here. This is what prompted new checklist item **IA04-13**, since §5 C4 ("Export to Excel, column completeness and download feedback") previously had no item covering it.

## 13. Participant side: session identity and the scenario-B blocker

The avatar menu ("Open menu" button) identifies the session as **`admin@gmail.com`**, display name "Tôi là Admin" (hence the `TLA` initials). This is the admin account named in §4 of the assignment.

**Routes exposed only through the avatar menu**: none of them appears in the header nav:

| Route | Purpose |
| --- | --- |
| `/complaints` | My Requests (user side of scenario D) |
| `/complaints/new` | Create support request |
| `/profile` | My Profile + My Activities |
| `/notifications` | Notifications |

Menu contents: Events · Calendar · Saved Events · User guide · Admin dashboard · Support requests · View profile · Notifications · Language · Logout.

### An admin account cannot reach the scenario-B screens

On `/events/10` (an Upcoming event with registration still open until 01/08/2026) the page renders **no Register button**: only "Back to events", "Save event", "Share event". The Registration-roles block states:

> **Admin view only** ... Student roles → Học viên tham dự · Registered **2/80** · Pending **2** · Confirmed **0** · Waitlisted **0** · Lecturer roles → Giảng viên hướng dẫn · Registered **0/10** · Pending 0 · Approved 0 · Guest roles → No roles available · **"Admin can view role information only (no registration action)"**

So **B3, B4 and B5 are unreachable from this account**, and there is no "My Registrations" entry in the menu.

> **Resolved, v1.7.** This is a property of the *admin role*, not a blocker on the group. The screenshot set was captured from a **student account**: `tien@gmail.com`, avatar `TTN`, role Student (it also appears as an Active/Student row in `Admin_C1_UsersList.png`). `User_B3_RegisterForm.png` shows the live **Register (Student)** button and role checkbox; `User_B4_MyTicket.png` shows **Registered Activities: 1**: ICAMM'26, registered at `25/07/2026 21:06`, role "Sinh viên tham dự". The B path is open today. Keep the observation above as a **role-based-UI note** (does EMS explain *why* the action is withheld from an admin?), not as a scheduling constraint.
>
> **Note for whoever owns B:** registration happens **inline on the event detail page**: the "Registration roles" block and Register button are part of `/events/{id}`, not a separate form. Check whether a confirmation modal follows the click; if not, B2 and B3 are one screen, not two.

The capacity figures above are still useful: they confirm the shape of the data IA04-05 checks (Registered / Pending / Confirmed / Waitlisted per role).

## 14. Public event detail: `/events/{id}`

| Property | Observed |
| --- | --- |
| Title | `Chi tiết sự kiện | HCMUS EMS`, **Vietnamese title, English body** |
| Back control | **"Back to events"** present |
| Breadcrumb | 0 |
| Tabs | 0 (`role="tab"`) |
| Headings | Event title · "Detailed content" · the event's own Vietnamese rich-text sections · "Registration roles" |
| Buttons | Back to events · Save event · Share event |
| Images | 3, **all carrying an `alt` attribute** (0 missing, 0 empty) |
| **Rating summary** | **Corrected v1.7, bar meters exist here.** An aggregate score ("★ 0.0 (0)") above **five horizontal bars**, one per star level, each with its own count and percentage label. They are styled `div`s, not `<progress>`, which is why `progress,[role=progressbar]` returned 0 and the product was wrongly recorded as having no bar meter. **This is the referent for IA04-10**: compare each bar's fill against its own label when you execute |
| Other controls on this page | "Back to events" text link · "Save event" · "Share event" · a floating share button, plus scroll-to-top buttons at the right edge and bottom-right |
| `aria-live` | 0 |
| Dates | `01/10/2026 08:00`, `31/03/2027 17:00`, `29/06/2026`, `dd/MM/yyyy` under an English UI |

## 15. My Requests: `/complaints`

Title `Yêu cầu hỗ trợ | HCMUS EMS` (Vietnamese). Heading "Support requests". Empty state **"No requests yet"** (the admin has filed none), a clean reference case for IA01-06. One status filter ("All statuses"), 1 text input, 1 `<select>`. Link to `/complaints/new`. No tabs, no breadcrumb, no `aria-live`.

## 16. Create Support Request: `/complaints/new`

Title `Gửi yêu cầu hỗ trợ | HCMUS EMS` (Vietnamese).

| Property | Observed |
| --- | --- |
| Labels | Request type (options **Support · Complaint · Contact · Other**) · Issue requiring support · Detailed description · "Add evidence images" |
| Upload helper text | **"JPG, PNG, GIF or WEBP · Up to 5 images · 5 MB each"**: matches the checklist wording exactly |
| Inputs | 1 text · 1 file · 1 select · 2 textarea · 0 radio · 0 checkbox |
| Character counter | **`0/255`** live counter present |
| Placeholders | "For example: Unable to register for an event" · "For example: I tried to register for Technology Day 2026 as a Participant. After selecting the role and clicking Register, the system displayed "Registration failed"..." |
| Buttons | **Submit request** · Cancel · Back |
| `required` / `aria-required` | **3** |
| `aria-live` | 0 |

**Two points worth carrying into IA02-01:**
1. **`required` is inconsistent across the product**: 3 on this user form, **0** on the admin event-edit form despite that form showing red asterisks. Same product, two standards.
2. **No `*` appears in this page's text content**, although the reference screenshot shows "Request type *". The asterisk is therefore most likely drawn by CSS (`::after`), which means it is not in the accessibility tree. Confirm visually during execution before recording a result.

> Nothing was submitted on this form. The survey stopped at inspection, creating a support request would write to a shared system.

## 17. Profile: `/profile`

Title `Hồ sơ cá nhân | HCMUS EMS` (Vietnamese). Headings "My Profile", "Tôi là Admin", "My Activities".

Buttons: **QR Code** · **Edit Profile** · **Change Password** · **Filters** · **Export**.
- The **QR Code** button renders a code (1 `canvas`) without needing a ticket, the practical route for IA01-11. **Precondition, corrected v1.7:** on an account with no member code the button is **disabled** (greyed out in `User_B4_MyTicket.png`, under the amber banner "Please enter your member code to complete your profile"). Fill the member code first.
- **A third Export button** lives here. **Corrected v1.7, there is a fourth**, on an event's **Registrants** tab (`Admin_A4_Participants.png`), which is §5 A4's Export. IA04-13 covers all four, and is **not** N/A for scenario A.
- This page is what `User_B4_MyTicket.png` actually shows. Rows-per-page on My Activities is **10**: a fifth distinct pagination scale (dashboard `4/8/12/16` · admin Events `5` · Users `5` · Support `20` · here `10`).
- `required` 0 · `aria-live` 0 · no tabs.

## 18. Still not surveyed

Updated v1.7 against the screenshot set:

| Was listed as unsurveyed | Status now |
| --- | --- |
| Registration form · ticket · post-event review | **Covered**: captured from the student account (§13). Registration is inline on the event detail page |
| Admin **Edit-user dialog** | **Covered**: `Admin_C3_UserDialog.png`, contents in §11 |
| Support-request **detail** page + image lightbox | **Still not captured.** `User_D2_SupportDetail_Response.png` is mis-named: it shows the **My Requests list** (`/complaints`), not the detail with the official response. **IA03-10 (ESC closes the lightbox) has no evidence at all**: the D owner must capture this |
| Admin support-request detail (internal note, official response) | **Still not captured**: §5 D4 |

Also unsurveyed and worth a look before Task 1B: the **Check-in tab** (IA04-09 depends on it), and the `Analytics` / `Settings` sidebar accordions.

## 19. Re-running the survey

The whole inventory came from one DOM query per page. To refresh it after a data reset, run this in DevTools console on any EMS page:

```js
const n = s => document.querySelectorAll(s).length;
const t = s => [...document.querySelectorAll(s)].map(e => e.textContent.trim().replace(/\s+/g, ' ')).filter(Boolean);
({
  path: location.pathname,
  breadcrumb: n('nav[aria-label*=readcrumb i],[class*=breadcrumb i]'),
  tabs: t('[role=tab]'),
  tableCols: t('th'),
  headerCtrls: [...document.querySelectorAll('th button')].map(b => b.getAttribute('aria-label')),
  ariaSort: n('[aria-sort]'),
  draggable: n('[draggable=true]'),
  progress: n('progress,[role=progressbar]'),
  ariaLive: n('[aria-live],[role=status],[role=alert]'),
  required: n('[required],[aria-required=true]'),
  inputs: { text: n('input[type=text]'), date: n('input[type=date]'), dtl: n('input[type=datetime-local]'),
            select: n('select'), radio: n('input[type=radio]'), checkbox: n('input[type=checkbox]'),
            file: n('input[type=file]'), switchRole: n('[role=switch]') },
  editor: n('[contenteditable=true].ql-editor,[class*=ProseMirror i]'),
  pagination: (document.body.innerText.match(/Showing[^\n]*|Rows per page[^\n]*/g) || [])
})
```

> Note: a query containing `location.search` was blocked by the browser extension's data guard. Use `location.pathname` instead.

**Known blind spots of this snippet (v1.7)**: the four corrections at the top of this file all came from them. Do not treat a `0` here as proof of absence:
- `progress,[role=progressbar]` misses **bar meters built from styled `div`s** (the Rating summary). Check visually.
- Text matching misses **icon-only controls** (the round ← back button). Query `button:not(:has(*:not(svg)))` or just look at the page.
- `tableCols` / `headerCtrls` only inspect `<th>`; EMS puts the Support filters, including the **native date inputs**: in a card **above** the table, so they were never counted. Run the `inputs` census on every page, not one representative form.
- `document.body.innerText` mixes **user-generated content with UI chrome**. The `8:07 25/07` error came from reading a request title as a date format.
