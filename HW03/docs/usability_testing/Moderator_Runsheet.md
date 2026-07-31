# Moderator Runsheet — Task 2 Usability Sessions (Scenario D)

> One sheet, kept open by the moderator (Lê Phạm Kiều Duyên) for all 6 sessions: 1 pilot + 5 real
> (P1–P5). Operational only — the study design, success criteria and probe wording live in
> `docs/usability_testing/Task_Scenario_D.md`; this file does not repeat the "why," only the
> "what to click / say / write, when." Screens under test: **D1** `/complaints/new`, **D2**
> `/complaints`, `/complaints/{id}`. **D3**/**D4** (`/dashboard/admin/complaints`,
> `/dashboard/admin/complaints/{id}`) are operated by the moderator only, never shown to the
> participant.
>
> Items below marked **VERIFY BEFORE PILOT** are not settled by
> `docs/02_Task1B_Execution_Report_ScenarioD.md` or `docs/checklist/EMS_Live_Survey_2026-07-26.md`
> — confirm them live before Session Pilot, do not assume.

## 1. Environment prep — done ONCE before the first session (the pilot)

- [ ] Confirm the EMS URL resolves **right now**, not from memory: try
  `https://prod-dev.ems-fitus.cloud/` first. If it does not load, the hosted instance has moved —
  both the assignment brief and `docs/usability_testing/Task_Scenario_D.md` warn the tunnel
  resets — find the currently-live host and write it at the top of today's notes. This is not a
  one-time check: repeat it at T-15min of every session (§2), because the instance can move again
  between sessions.
- [ ] Open the admin session in a **separate browser profile** (not merely a separate tab), logged
  in as `admin@gmail.com`, so the participant's browser and the admin's browser never share
  cookies/local storage and the participant cannot accidentally see the admin sidebar or URL.
- [ ] Screen-recording tool installed and smoke-tested once end-to-end (record a few seconds,
  play the file back) before the pilot.
- [ ] Recordings destination confirmed writable: `reports/evidence_task2/` (already exists in the
  repo as an empty placeholder folder with a `.gitkeep`). Confirm free disk space for 6 sessions
  of screen video.
- [ ] Decide and document how many participant EMS accounts are needed: **6** — 1 for the pilot
  plus 1 per real participant (P1–P5) — each with a distinct email/member code, so the moderator
  can tell each participant's filed request apart on the admin side purely by member code (§3),
  without relying on the buggy free-text search box (D-005, §4).
- [ ] Decide and document **who creates these accounts and how**: the moderator (Duyên) creates
  all 6 in advance of Day 1, never live during a session, so no participant burns session time on
  sign-up. **VERIFY BEFORE PILOT:** whether the admin's "Add User" dialog
  (`/dashboard/admin/users`) actually lets the moderator set an initial password directly, or
  whether the only working path is self-registration ("Create guest account" on the login page)
  followed by the moderator recording the password. The live survey
  (`docs/checklist/EMS_Live_Survey_2026-07-26.md` §11) only captured the **Edit** User dialog's
  fields (First Name, Last Name, Email, Phone Number, Role, Member Code, Active — no password
  field visible there); the Add-User dialog's own fields were never captured, so this is
  unconfirmed either way.
- [ ] **VERIFY BEFORE PILOT:** that logging into a pre-created account with plain email + password
  does not trigger an OTP step. The login screen's only observed fields are Email and Password
  (`docs/checklist/EMS_Live_Survey_2026-07-26.md` §3); OTP is mentioned in
  `docs/usability_testing/Task_Scenario_D.md` only as a generic pilot-failure risk, most likely
  tied to the guest self-registration path this design deliberately avoids — confirm live rather
  than assuming.
- [ ] **VERIFY BEFORE PILOT:** whether the account-creation path used above lets the moderator set
  a display name that is not the participant's real full name (e.g. "Participant P3" or initials),
  so recordings expose less personal data by construction (see §7).
- [ ] The moderator personally performs every login and every password entry, in setup and in
  every session — never an AI/browser-automation tool, and never the participant typing a
  password on camera. Each participant's dedicated account is pre-authenticated by the moderator
  in their browser tab before they sit down (T-15min, §2), landing on the participant dashboard,
  not on `/complaints/new` — the participant never sees a login screen and no time is spent on
  sign-up or OTP.
- [ ] The moderator privately decides, once, a short admin-side reply script (§3) so resolving
  each participant's request is fast and consistent rather than improvised mid-session. This does
  not touch the Task 1 prompt itself, which stays goal-only per `Task_Scenario_D.md`.

## 2. Per-session run sheet (timed checklist, target ~20 minutes total)

- [ ] **T-24h — confirm slot.** Message/call the participant to confirm date, time and method
  (in-person or remote screen-share); confirm they still meet the recruiting screener in
  `docs/usability_testing/Participants_Table.md`.
- [ ] **T-15min — set up (~10 min for all steps below).**
  - [ ] Re-confirm the EMS URL resolves today (§1).
  - [ ] Pre-authenticate the participant's dedicated account in their browser tab; leave it on the
    participant dashboard, not on any Scenario-D screen.
  - [ ] Confirm the admin profile is logged in and sitting on `/dashboard/admin/complaints` (D3)
    with the Member-code filter cleared and the default Pending tab active — a stale filter from
    the previous participant must not carry over (D-009, §4/§9).
  - [ ] Start the recording tool, confirm an empty buffer (no leftover clip from a previous
    session), do not press "record" yet.
- [ ] **T-0 — framing + consent (~1–2 min).** Deliver the framing verbatim in Vietnamese (§5) —
  this is §6 Task 2 Phase 2's "you are testing the product, not the participant" requirement, plus
  the think-aloud instruction, and both must be said out loud in every session. Read the consent
  script (`docs/usability_testing/Recruiting_Kit.md` §5) and get an **explicit spoken yes** to
  recording the screen, and separately to recording audio, **before** the recorder starts. Then
  start recording and re-state the consent question on tape if the participant is willing, so the
  consent itself is evidenced. If they decline audio, record screen only and note it — do not
  negotiate the consent down and do not run the session without either.
- [ ] **T1 — Task 1 (target 3–8 min per `Task_Scenario_D.md`).** Read the **Vietnamese** Task 1
  prompt verbatim from `docs/usability_testing/Task_Scenario_D.md` §"Task 1 — verbatim Vietnamese"
  (or hand it over on paper) — same wording every session, never a fresh translation. Observe
  neutrally, think-aloud prompts only (§5), take structured notes in `Session_P<n>.md` (§8). Stop
  the clock at submission or at give-up.
- [ ] **Admin-side resolve (~1–2 min, participant not watching).** Moderator switches to the admin
  profile and runs the scripted resolution in §3. The participant can be told something neutral
  like *"Cho mình một chút để xem lại nhé"* ("Give me a moment to look this over") — never that a
  response is being written for them.
- [ ] **T2 — Task 2 (target 2–4 min).** Read the **Vietnamese** Task 2 prompt verbatim from
  `Task_Scenario_D.md` §"Task 2 — verbatim Vietnamese". Same neutral observation rules as T1.
  **Record which route they take to the response** — My Requests, or the notification bell — in the
  session log; do not nudge either way, the choice is a findability result.
- [ ] **SUS (~2 min).** Administer the 10-item scale by reading the **Vietnamese** wording in
  `docs/usability_testing/SUS_Instrument_VI_EN.md` §2, on the printable answer sheet in its §3;
  1 (hoàn toàn không đồng ý) to 5 (hoàn toàn đồng ý). The English-only list in
  `docs/usability_testing/session_notes/Session_Notes_TEMPLATE.md` is for transcribing the answers
  afterwards, not for reading aloud.
- [ ] **Probes (~3–4 min).** Ask the four fixed probe questions from `Task_Scenario_D.md`
  (Clarity, Error recovery, Speed, Trust), same wording every session.
- [ ] **Stop recording.** Confirm the file exists and is playable before the participant leaves.
- [ ] **Immediate write-up (~5–10 min, before the next session, see §8).**

## 3. Admin-side resolution — scripted click path (D3 → D4)

Run this once per participant, right after Task 1, while the participant is not looking at the
admin browser.

1. Switch to the admin profile (already logged in as `admin@gmail.com`), on D3
   (`/dashboard/admin/complaints`).
2. In the **Filters** card, type the participant's assigned **Member code** (not the free-text
   "Search name, email or title" box — that field has a confirmed keystroke-loss defect, D-005,
   while the Member-code field's own filtering applies automatically without it, per
   `docs/02_Task1B_Execution_Report_ScenarioD.md`'s D3 IA02-10 notes).
3. Do **not** switch the Pending/Resolved tab before or during this filter — switching it clears
   the Member-code filter (D-009). Filter first, on the default Pending tab.
4. Confirm exactly one row is returned, matching this participant's account, with a just-now
   timestamp — not a leftover row from the pilot or a different participant.
5. Click the row → opens `/dashboard/admin/complaints/{id}` (D4).
6. In **Internal note**, type an internal-only marker for the group's own record, e.g.:

   > `[Nội bộ] Đã xác minh và khôi phục đăng ký theo yêu cầu hỗ trợ #<id>, phiên kiểm thử usability P<n>.`
   > (Internal: verified and restored the registration for support request #<id>, usability
   > session P<n>.)

   This never reaches the participant's own view — confirmed by
   `docs/02_Task1B_Execution_Report_ScenarioD.md`'s D4 IA04-14 result (internal note does not leak
   to D2).
7. In **Response content**, type the scripted official reply:

   > `Chào bạn, EMS đã kiểm tra và khôi phục lại thông tin đăng ký của bạn cho sự kiện. Bạn có thể đăng nhập lại và kiểm tra mục "Hoạt động của tôi" để xác nhận. Cảm ơn bạn đã phản hồi, mong bạn tham gia sự kiện vui vẻ!`
   > (Hi, EMS has checked and restored your event registration. Please log back in and check "My
   > Activities" to confirm. Thanks for the report — enjoy the event!)

8. Click **Send response** (the single cyan primary button on this screen). Confirm the inline
   green success banner appears and the status pill flips Pending → Resolved.
9. **Wait ~60–90 seconds before handing over Task 2.** Task 1B's own evidence
   (`docs/02_Task1B_Execution_Report_ScenarioD.md`, D3/D4/D5 IA04-05) found the status, sidebar
   badge and notification badge all update immediately with no observed propagation delay, so
   this wait is for pacing/realism ("a little while ago," per `Task_Scenario_D.md`), not a
   technical requirement.

## 4. Known defects that will fire during sessions — RECORD, never fix, never warn

For every row: **RECORD it in the session's Structured observation log, never fix it, never warn
the participant in advance, and never say "that's a known bug" during the session.** Full
descriptions and repro steps are in `docs/05_Bug_Usability_Findings_Log.md`.

Anything that goes wrong and is **not** in this table is a candidate **new** finding — log it in the
session notes with a timestamp, and after the sessions raise it in
`docs/05_Bug_Usability_Findings_Log.md` from **D-020** onwards and submit it to the Google Form
(§7 of the brief). The table below is the known set, not the expected set.

| Finding | Screen / Task hit | What the participant will experience | Moderator's rule | Can fail the task through no fault of the participant? |
| --- | --- | --- | --- | --- |
| D-001 | D1, Task 1 — "Loại yêu cầu" (Request type) dropdown | Picking a value then clicking the next field within ~1 s can revert it to the placeholder, or silently swap it to a different option; the required-field error can then appear even though a value was picked. | Record the exact click sequence and timing. Do not point out what happened. | **Yes** — if this causes the submit to fail, write in the notes that the failure is the product's, not the participant's. |
| D-004 | D1, Task 1 — "← Quay lại" (Back) link | Clicking Back after typing discards all typed text instantly, no warning of any kind. | Record whether the click was deliberate or a misclick/backtrack attempt. | **Yes** — an accidental Back mid-task can turn a near-complete Task 1 into a redo or a Fail; note this explicitly. |
| D-002 | D1, Task 1 — Attachments | A rejected image (wrong type / too large / too many) names the rule broken but never the filename; with more than one attempt the participant may not know which file was rejected. | Record; do not clarify which file was rejected. Watch whether they self-correct. | Possible, if it causes the participant to give up on attaching an image (Partial, per the success criteria). |
| D-003 | D1, Task 1 — empty submit | One generic banner above Submit lists all missing fields; no inline message beside any individual field. | Record as a hesitation/error; do not point at the missing field. | Unlikely alone, but adds time/hesitation. |
| D-005 | D2, Task 2 (occasionally D1) — search/free-text boxes | Fast typing can drop some or all characters, so a search returns nothing or the wrong result even though the record exists. | Record; do not explain why nothing was found. Let the participant retry or abandon search on their own. | Possible on Task 2 if the participant relies on search rather than scanning the (short) list. |
| D-008 | D2/D3 — "Rows per page" | Changing rows-per-page has no visible effect. Low risk for Task 2 since a fresh participant account should hold only their own request. | Record if it happens; note explicitly this is not caused by the participant's account. | Unlikely to affect Task 2 with one record, but record if observed. |
| D-006 | D2 — direct bad URL | Manually editing the URL to a non-existent id shows "Event review not found," wrong-context copy. Unlikely unless the participant types a URL by hand. | Record if it happens; do not correct the message aloud. | Unlikely to occur at all in a normal session. |
| D-007 | D2 detail page — Task 2 | No breadcrumb on the two-levels-deep request-detail page, only a one-step "← Back" link. | Record as a hesitation if the participant looks for an ancestor path. The Back link exists, so this alone should not cause a Fail. | No, on its own. |
| D-012 | D1, Task 1 — description field | Pressing Enter in either text field does nothing (no submit); the participant may press it expecting submission and then wonder if anything happened. | Record as a hesitation. Do not prompt "click Submit instead" unless the intervention rule (§6) is triggered. | No, on its own — but contributes to hesitation count. |

## 5. Neutral-moderation phrasebook (verbatim Vietnamese, with English gloss)

**Framing (T-0, adapt from `Task_Scenario_D.md`'s script):**

> "Cảm ơn bạn đã giúp mình nhé. Mình đang kiểm tra tính năng hỗ trợ sự kiện này, không phải kiểm
> tra bạn — không có cách làm nào là đúng hay sai cả. Bạn cứ nói ra suy nghĩ của mình trong lúc
> làm: bạn đang thấy gì, bạn nghĩ điều gì sẽ xảy ra, và thực tế xảy ra như thế nào. Nếu bạn thực
> sự bị kẹt, cứ nói với mình, mình sẽ hỗ trợ, nhưng hãy thử theo cách của bạn trước đã nhé."
> (Thanks for helping. I'm testing this event-support feature, not you — there's no right or
> wrong way. Please think out loud as you go: what you see, what you expect, what actually
> happens. If you're truly stuck, tell me and I'll help — but try your own way first.)

**When the participant asks "mình làm đúng chưa?" (am I doing this right?):**

> "Không có cách nào đúng hay sai đâu, bạn cứ làm theo cách bạn thấy hợp lý nhất."
> (There's no right or wrong way — just do whatever feels most natural to you.)

**When the participant goes silent (prompt to think aloud):**

> "Bạn đang nghĩ gì vậy? Bạn có thể nói ra những gì bạn đang thấy và đang nghĩ không?"
> (What are you thinking right now? Could you tell me what you're seeing and thinking?)

**When the participant asks for help (not yet a true stall):**

> "Bạn cứ thử theo cách của mình trước đã nhé, nếu thực sự không tìm được thì mình sẽ hỗ trợ."
> (Try it your own way first — if you really can't find it, I'll help.)

**When the participant is truly stuck and the moderator must intervene (§6):**

> "Được rồi, mình sẽ hỗ trợ bạn ở bước này nhé."
> (Okay, I'll help you with this step now.)

**DO-NOT-SAY list — leading phrases, never say these during a task:**

- "Bạn thấy cái nút màu xanh ở trên kia không?" — *Did you see the blue button up there?*
  (points straight at the answer)
- "Không phải chỗ đó đâu, thử chỗ khác đi." — *Not there, try somewhere else.*
  (biases them away from a path before they've finished exploring it)
- "Đúng rồi đó, bấm vào đi." — *That's right, click that.*
  (confirms correctness before the action is taken)
- "Cái này bị lỗi đó, không phải do bạn đâu." — *That's a bug, not your fault.*
  (reveals a known defect mid-session — forbidden under any circumstance, per §4)

## 6. Intervention rule

- Step in only when the participant is genuinely stalled: no visible progress for roughly
  30–45 seconds after a think-aloud prompt, or they explicitly ask for help a second time.
- Always give one more neutral nudge from §5 before intervening — reserve direct help for a real
  stall, honoring the framing script's own promise ("if you're truly stuck, I'll help").
- The moment the moderator gives any task-specific hint, or performs any click/typing for the
  participant, mark **Intervened: Y** in `Session_P<n>.md` and record exactly what was said/done,
  verbatim if possible, in the Structured observation log.
- **An intervened task cannot count as a clean "Complete" for time-on-task purposes.** Score it
  Partial (if the intervention was a small nudge) or note the intervention point and exclude the
  time-on-task figure from any cross-participant averaging in `Metrics_Table.md` — never silently
  fold an assisted run in with unassisted ones.

## 7. Evidence capture and naming

- Every recording and screenshot goes under `reports/evidence_task2/`.
- **Capture a still, not only video, for anything that looks like a finding.** §6 Task 2 Phase 3
  requires the Usability Report's ranked findings to carry **a screenshot each**; a report written
  weeks later cannot manufacture one, and scrubbing six recordings for frames is the slow way to
  get there. The cheap habit: the moment something goes wrong on screen, take the screenshot then —
  during the session if it is unobtrusive, otherwise immediately after the participant leaves by
  reproducing the same state on the moderator's own account (never by staging it on a participant's
  data, and never by editing an image afterwards).
- Naming convention: `P<n>_<task>_<what-it-shows>.<ext>` — e.g. `P2_T1_submit-success.jpg`,
  `P3_T2_response-readback.jpg`, `P1_T1_D-001_requesttype-reverts.mp4`, `Pilot_T1-T2_full-session.mp4`.
- Screen-only recording (no webcam, no participant face in frame). Frame the capture region to the
  browser viewport only — no desktop, chat windows, or other apps visible.
- **Reminder:** the participant's own EMS screen may show their real name (avatar/profile display
  name), since it belongs to their pre-created account. If the account-creation path allows it
  (§1, VERIFY), set the display name to a pseudonym/initials at creation time specifically to
  reduce this exposure; if it does not, this is an accepted, disclosed limitation, not something
  to crop out mid-recording.
- Never capture any other personal data (ID numbers, other participants' rows on an admin screen,
  personal chat).

## 8. Post-session, within 10 minutes

- [ ] Copy `docs/usability_testing/session_notes/Session_Notes_TEMPLATE.md` to
  `docs/usability_testing/session_notes/Session_P<n>.md` (or `Session_Pilot.md`).
- [ ] Fill the Structured observation log and Task outcomes table (Result, Time on task, Error
  count, Hesitation count, Notes) for both tasks.
- [ ] Transcribe the 10 SUS answers (1–5) into `docs/usability_testing/SUS_Responses.csv`, one row
  per participant, columns `participant,q1,...,q10`.
- [ ] Fill in the four probe-question responses (Clarity · Error recovery · Speed · Trust), with at
  least one verbatim quote each where the participant gave one.
- [ ] Fill the "Known defects observed this session" and "Screenshots captured this session" tables
  in `Session_P<n>.md`, and move the stills into `reports/evidence_task2/` under the §7 names.
- [ ] Write the moderator's raw impressions section immediately, before the next session, while
  memory is fresh — this is the one field that cannot be reconstructed later.
- [ ] Move/rename the recording file into `reports/evidence_task2/` per the §7 convention.
- [ ] Pilot session only: note anything to fix in the task wording or script before Session P1;
  pilot data is never merged into `Metrics_Table.md` or the SUS scoring, per
  `docs/usability_testing/Task_Scenario_D.md`.

## 9. Reset checklist between participants

- [ ] Log the participant's account fully out (clear session, not just close the tab) — VERIFY
  logout actually clears cookies/local storage rather than silently re-authenticating on reopen.
- [ ] On the admin side (D3), clear the Member-code filter and any category filter, and return to
  the default Pending tab — do not carry a stale filter into the next participant's search
  (D-009, §4).
- [ ] Confirm the previous participant's request is left Resolved and does not surface again when
  the next participant's distinct account is searched (each account's own member code keeps rows
  distinguishable; `docs/02_Task1B_Execution_Report_ScenarioD.md`'s D4 IA04-14 result already
  confirms no cross-record leakage of internal notes).
- [ ] Confirm the recording buffer is stopped, the file is saved under
  `reports/evidence_task2/`, and a fresh, empty buffer is armed for the next session.
- [ ] Re-confirm the EMS URL still resolves before starting session n+1 (§1).
- [ ] Pre-authenticate the next participant's dedicated account in a clean browser tab, landing on
  the dashboard, not on any Scenario-D screen.
- [ ] Close the previous participant's `Session_P<n>.md` before opening a fresh copy of the
  template for the next session, to avoid cross-writing between participants' notes.

## 10. If it goes wrong

| Situation | Recovery |
| --- | --- |
| EMS is down / URL does not load | Try the currently-live tunnel if already known; if still down, reschedule within 24h and note the outage in `docs/usability_testing/Participants_Table.md` — never run against a stale cached page. |
| Participant no-shows | Wait 10 minutes past the start time, mark the slot missed in `Participants_Table.md`, and move to the reserve candidate rather than merging it into the same day's next session without a break. |
| Recording failed | If caught mid-session, restart recording immediately and note the gap in `Session_P<n>.md`; if only discovered afterward, write the raw impressions from memory right away and flag that session's evidence as incomplete — never fabricate a screenshot after the fact. |
| Participant cannot log in | Should not occur, since the moderator pre-authenticates the account before the session (§1, §2); if it does, the moderator re-enters the credentials personally, without the participant seeing or typing the password, and notes the delay. |
| Session overruns past ~20 min | Let T1/T2 finish naturally if the participant is still genuinely progressing; if time is short, shorten the probes to the single most important one (Trust) rather than cutting the SUS, since a completed SUS is required for every counted participant. |
