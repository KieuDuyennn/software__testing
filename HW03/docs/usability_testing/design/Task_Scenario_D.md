# Task 2 — Usability test scenario — Scenario D (Support requests)

> Method: moderated think-aloud, target **n = 5** real participants + **1 pilot**.
> Screens under test: **D1** (Create Support Request), **D2** (My Requests list + detail with
> official response). D3/D4 (admin side) are operated by the **moderator**, not the participant —
> a usability *participant* is never given the admin account.
> **Session length: ~20-25 minutes per participant** (consent 1-2 · T1 3-8 · moderator resolves
> 1-2 · T2 2-4 · SUS 2 · probes 3-4). This is the figure promised to candidates in
> `docs/usability_testing/design/Recruiting_Kit.md`; the moderator's internal target is ~20 minutes,
> per `docs/usability_testing/design/Moderator_Runsheet.md` §2.
> Instrument: **SUS** (10 items) — chosen over UEQ-S because the group wants a score directly
> comparable across all four scenario owners' reports.

## Screens under test, and the brief's "≥ 3 screens" rule

§6 opens with *"Tasks 1B, 2, and 3 all operate on the same three (or more) screens of your chosen
scenario,"* and Task 2 says to run the sessions *"on the ≥ 3 screens of your package."* State the
mapping explicitly in the report rather than leaving a grader to count:

| Page the participant actually reaches | Route | Package screen (`docs/02_Task1B_Execution_Report_ScenarioD.md`) | Reached in |
| --- | --- | --- | --- |
| Create Support Request form | `/complaints/new` | **D1** | Task 1 |
| My Requests list | `/complaints` | **D2** (list half) | Task 2 |
| Request detail with the official response | `/complaints/{id}` | **D2** (detail half) | Task 2 |
| Notifications — bell dropdown / list / detail | `/notifications`, `/notifications/{id}` | **D5** | **Only if the participant goes there unprompted** |

That is three distinct user-facing pages across two named package screens, plus a fourth that some
participants will find on their own. **Never steer anyone toward the notification bell** — whether
a participant reaches the response via My Requests or via the bell is itself a findability result.
If they do go there, record the route taken in the session notes; it is legitimate D5 coverage,
observed rather than scripted.

**D3** and **D4** (the admin list and admin detail) are operated by the moderator only and are
never shown to a participant, so they are exercised in these sessions but not *tested* by them.
Say so in the report's Limitations rather than implying user coverage of the admin side.

## Participant profile

Real people **outside this class**, matching the population that actually files EMS support
requests: students or event-goers who have used, or would plausibly use, an FIT@HCMUS event
platform. Do not recruit classmates or teammates — see the assignment's anti-impersonation clause
(§12); the TA may call up to 2 of the 5 to verify them.

## Pilot (run first, 1 extra person, not counted in results)

Same script as below. Purpose: catch an unclear task wording, a broken flow (e.g. OTP email not
arriving), or a task that runs far longer than the 3–8 minute target. Fix the script before
counting real sessions. **Pilot data does not go in the Usability Report's metrics.**

What the pilot *does* go into is `docs/03_Task2_Usability_Report_ScenarioD.md` §4: the date it ran,
what it exposed, and what changed before P1. The brief requires a pilot; a report that never
mentions one reads as though it was skipped. "Nothing needed changing" is a legitimate answer there
— an absent section is not.

## Pre-session setup (moderator does this, not the participant)

1. Confirm the EMS URL loads: `https://prod-dev.ems-fitus.cloud/` (or the currently-live tunnel —
   confirm right before each session; the assignment warns the ngrok/hosted instance resets).
2. Have the admin session (`admin@gmail.com`) ready in a **separate** browser/profile so the
   moderator can resolve the participant's request shortly after they file it, without the
   participant seeing the admin UI.
3. Prepare a realistic support scenario the participant did not write themselves (see Task 1
   wording) so their request content is predictable enough for the moderator to resolve quickly.

## The task (read aloud / handed to the participant — goal only, no click path)

Sessions are run in **Vietnamese**, so the Vietnamese wording below is the one actually spoken and
must be read **verbatim, identically in every session** — the English underneath is a gloss for the
report, not a second script. Improvising a fresh translation per participant would make five
sessions five different studies.

### Task 1 — verbatim Vietnamese (read aloud / hand over on paper)

> *"Bạn hãy tưởng tượng là bạn đã đăng ký tham gia một sự kiện trên trang web này, nhưng tới hôm
> diễn ra sự kiện, lúc bạn check-in thì hệ thống lại báo là bạn chưa hề đăng ký. Bạn muốn chuyện
> này được xử lý. Bạn hãy dùng trang web để báo lại vấn đề đó, theo cách nào bạn thấy là đúng — các
> thông tin chi tiết (tên sự kiện, ngày bạn đăng ký, v.v.) thì bạn cứ tự nghĩ ra thoải mái nhé."*

**English gloss:** *"Imagine you registered for an event on this platform, but when you tried to
check in on the day, the system said you weren't registered at all. You want this fixed. Use the
platform to report the problem, however you think is the right way — you can invent any details you
need (event name, your registration date, etc.)."*

> **Success criterion (defined in advance):** a support/complaint request is successfully submitted
> with a request type, a description of the problem, and at least one attached image (a screenshot
> or any image file counts — the participant should attach *something*, since the form supports
> it). Partial: submitted but missing the image or with an unclear description. Fail: could not
> submit, or gave up.

### Task 2 — verbatim Vietnamese

*(Handed over a few minutes after Task 1, once the moderator has quietly resolved the request from
the admin side.)*

> *"Cái vụ lúc nãy bạn báo đó, giờ bạn thử xem có ai trả lời lại chưa, rồi đọc cho mình nghe họ
> nói gì nhé."*

**English gloss:** *"You submitted that report a little while ago. Go find out whether anyone has
responded to it, and tell me what they said."*

> **Success criterion:** participant locates their own request in "My Requests" (or the
> equivalent menu item — do not name it for them) and correctly reads back the official response
> text. Partial: finds the request but misreads or misses the response. Fail: cannot find where
> their request went.

Keep the product's own vocabulary out of the task wording (the task above says "report the
problem" / "find out whether anyone responded," never "complaints," "My Requests," or "Support" —
those are EMS's own labels, and using them would test nothing about findability). The Vietnamese
wording holds the same line deliberately: it says *"báo lại vấn đề"* and *"có ai trả lời lại chưa"*
and never EMS's own strings *"yêu cầu hỗ trợ"*, *"Yêu cầu của tôi"*, *"loại yêu cầu"* or
*"phản hồi chính thức"*. If a participant asks what a screen label means mid-task, re-read the task
sentence unchanged rather than translating the label for them.

## What to measure (minimum set required by §6 Task 2)

| Metric | How to capture |
| --- | --- |
| Task success | Complete / Partial / Fail per task, against the criteria above |
| Time on task | Start when the participant begins acting on the task prompt; stop at the success criterion. Note any moderator intervention. |
| Errors | Count of wrong actions requiring recovery (e.g. clicked the wrong menu item, submitted with a validation error) |
| Hesitations | Pauses > ~3 s, backtracking, re-reading the screen |
| Post-task SUS | 10-item System Usability Scale, administered once after both tasks |
| Open probe questions | See below — clarity, error recovery, speed, trust |

## Probe questions (same wording every session, asked after the SUS)

The four themes are the ones §6 Task 2 Phase 1 names: **clarity, error recovery, speed, trust** —
one probe each, none droppable. The **Vietnamese wording actually asked** is in
`docs/usability_testing/design/SUS_Instrument_VI_EN.md` §4, one-for-one with the four English probes
below; read it from there.

1. **Clarity** — "Was there any point where you weren't sure what the platform wanted from you, or
   what would happen next?"
2. **Error recovery** — "If you made a mistake or had to backtrack, how did you notice, and how did
   you get back on track?"
3. **Speed** — "Did anything feel slower or more effortful than it should have?"
4. **Trust** — "Once you submitted the report, how confident were you that it actually went
   through and someone would see it? Why?"

## Session script (moderator)

1. **Framing — "I'm testing the product, not you" (required by §6 Task 2 Phase 2).** The
   **Vietnamese wording that is actually spoken** is in
   `docs/usability_testing/design/Moderator_Runsheet.md` §5; read it from there. The English below is the
   gloss of that same framing, kept here so the design document is self-contained:
   *"Thanks for helping out. I'm testing this event-support feature, not
   you — there's no wrong way to do this. Please think out loud as you go: tell me what you're
   looking at, what you expect to happen, and what actually happens. If you get completely stuck,
   let me know and I'll help, but try your own way first."*
2. Get consent to record screen (and audio, if used) before starting.
3. Hand over Task 1. Observe neutrally — no leading hints ("did you see the button at the top?"),
   intervene only if fully stuck. Take structured notes (see `docs/usability_testing/results/session_notes/Session_Notes_TEMPLATE.md`).
4. Once submitted, moderator quietly resolves the request from the admin session (D4: write an
   internal note for the group's own record, plus an official response reusing wording consistent
   with the fictional scenario — e.g. confirming the registration was restored).
5. Hand over Task 2.
6. Close: administer the SUS, then the four probe questions, then stop recording.

## Data files this scenario produces

- `docs/usability_testing/results/Participants_Table.md` — the 5 (+1 pilot) participants, masked contact info
- `docs/usability_testing/results/session_notes/` — one structured, timestamped note file per session
- `docs/usability_testing/results/SUS_Responses.csv` — raw 1–5 answers per participant, scored with
  `python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/results/SUS_Responses.csv --instrument sus --markdown`
- `docs/usability_testing/results/Metrics_Table.md` — task success / time / errors, tabulated across the 5 real sessions
- `docs/03_Task2_Usability_Report_ScenarioD.md` — the final Phase-3 deliverable required by §6 Task 2
