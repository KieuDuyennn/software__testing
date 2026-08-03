# Task 2 — Recruiting Kit — Scenario D

> Operational kit for going from "nobody recruited" to "6 people scheduled" (1 pilot + 5 real),
> for `docs/usability_testing/design/Task_Scenario_D.md`. This kit does not recruit anyone — an agent
> cannot be a participant, recruit participants, or supply session data (see
> `.claude/skills/usability-test-study/SKILL.md` §"What an agent can and cannot do here"). Every
> table below is a blank template. Fabricating a participant, a session, or a contact detail is
> grounds for **0 points on Task 2** under §12 of the brief.

## 1. Who qualifies / who does not

Screener, applied before anyone is invited to schedule:

**Qualifies (all must be true):**

- A real person, contactable outside this messaging thread (Zalo, phone, or email that actually
  reaches them).
- Outside this class — not a classmate, not a teammate, not enrolled in this course this term.
- Has not already seen this study, this task wording, or the EMS admin resolution flow.
- Plausibly matches the population that files a real EMS support request: a student, lecturer, or
  event-goer who has registered for an event before (does not need to have used EMS specifically).
- Willing to do a ~20–25 minute screen-recorded session and a short questionnaire afterward.
- Comfortable being contacted again by a TA to confirm they took part (see §6 Task 2 Phase 3 of
  `refs/requirements/2026.HW03.GUI Usability EMS_En.md`, restated in its §12: the TA may randomly
  call up to 2 of the 5).

**Disqualifies (any one is enough to drop them):**

- Is a teammate on this HW03 group, or is taking this course this semester.
- Has already seen or discussed Scenario D's task wording, screens, or the group's checklist.
- No verifiable contact method (a contact that only exists inside a group chat with no real name
  behind it does not count).
- Cannot commit ~25 minutes at a fixed time, or refuses to be recorded at all.
- Works for or is closely affiliated with the EMS project itself (would bias findability results).

This screener is intentionally short. Full recruiting criteria already stated in
`docs/usability_testing/results/Participants_Table.md` §"Recruiting criteria (screener)" are the source of
truth; the list above is the same bar phrased as a yes/no gate for a quick decision on each
candidate.

## 2. Where to find 6 such people

| Channel | Why it fits | Recruiting risk |
| --- | --- | --- |
| Friends in a different faculty/department | Outside this class by construction; still a plausible "student" profile | Convenience bias — likely to be similarly tech-comfortable as the recruiter; skews younger/more digitally literate than the full EMS population |
| Dorm-mates / same-building neighbors | Easy to schedule in person, can use their own laptop on the spot | May know each other and compare notes before their sessions, contaminating think-aloud independence |
| Siblings or cousins who are students elsewhere | Verifiable contact already exists (family phone number), low no-show risk | Family members may be reluctant to criticize honestly, or may already know the recruiter is testing "for school" and go easy |
| CLB (club) members from a non-overlapping club | Larger pool than personal friends, plausible "event-goer" profile since CLBs run events | Scheduling friction — CLB members are busy around their own events; may cancel |
| Acquaintances met at past HCMUS events (workshops, orientation, seminars) | Directly matches the "event-goer" persona the scenario targets | Weakest tie, so lowest response rate to the invite; needs a follow-up nudge |

Aim to over-invite (8–10 candidates) against the target of 6, since some will decline or no-show.

## 3. Invite message — verbatim Vietnamese

**Invite message (send as-is, Vietnamese):**

> Chào [tên bạn],
>
> Mình đang làm một bài tập môn Kiểm thử phần mềm ở trường, cần nhờ vài người ngoài lớp mình dùng
> thử một tính năng nhỏ trên một web sự kiện của trường (khoảng 20–25 phút thôi). Bạn sẽ không bị
> đánh giá gì cả — tụi mình đang test cái web, không phải test bạn.
>
> Buổi test sẽ được quay lại màn hình (và có thể ghi âm) để mình xem lại sau, chỉ dùng cho bài
> tập. Sau đó bạn trả lời giúp mình vài câu hỏi ngắn.
>
> Một lưu ý nhỏ: đây là bài tập có kiểm tra chéo, nên đôi khi trợ giảng (TA) của môn học có thể
> gọi điện xác nhận lại với bạn là bạn có thực sự tham gia không — mong bạn thông cảm nếu nhận được
> cuộc gọi đó nhé.
>
> Bạn có rảnh khoảng 20–25 phút trong tuần này không? Nếu được thì mình xin thông tin liên hệ
> (Zalo/SĐT/email) để hẹn lịch nha. Cảm ơn bạn trước!

**English gloss:** Hi [name] — I'm doing a software-testing assignment and need people outside my
class to try a small feature on a school event website (~20-25 min). You're not being evaluated,
the product is. The session will be screen-recorded (and possibly audio-recorded) for the
assignment only. Afterward there are a few short questions. Heads-up: this assignment is spot-
checked, so a TA might call to confirm you actually took part — sorry in advance if that happens.
Are you free ~20-25 min this week? If so, send me a contact method (Zalo/phone/email) to schedule.

**Follow-up / reminder (send as-is, Vietnamese, shorter):**

> Chào [tên bạn], mình nhắn lại về buổi test web mình có nhắn hôm trước á. Bạn còn rảnh khoảng
> 20–25 phút để giúp mình không? Nếu được thì mình xin lịch rảnh của bạn trong 1–2 ngày tới nha,
> cảm ơn bạn nhiều!

**English gloss:** Following up on the test session I mentioned earlier — still free for ~20-25
minutes? If so, let me know your availability in the next day or two. Thanks again.

## 4. Screening questions

Ask before booking a slot. Vietnamese with English gloss; each row states the disqualifying answer.

| # | Question (Vietnamese) | Gloss (English) | Disqualifying answer |
| --- | --- | --- | --- |
| 1 | "Bạn có đang học hoặc từng học chung lớp Kiểm thử phần mềm với mình không?" | Are you currently or previously enrolled in my Software Testing class? | "Có" (Yes) |
| 2 | "Bạn đã từng nghe mình nói về bài test này, hoặc thấy màn hình web mình sắp cho bạn dùng chưa?" | Have you already heard about this study or seen the screens I'm about to show you? | "Rồi" (Yes, already seen it) |
| 3 | "Bạn đã từng đăng ký tham gia một sự kiện nào đó (ở trường hoặc nơi khác) chưa?" | Have you ever registered for an event (at school or elsewhere)? | "Chưa bao giờ" (Never) — weak fit for the target persona |
| 4 | "Mình có thể quay lại màn hình (và âm thanh) trong lúc bạn dùng thử không?" | Can I screen-record (and audio-record) while you try it? | "Không được" (No) |
| 5 | "Bạn có sẵn sàng cho mình một cách liên hệ (Zalo/SĐT/email) để trợ giảng có thể gọi xác nhận nếu cần không?" | Are you willing to give a contact method a TA could use to verify participation if needed? | "Không" (No) |
| 6 | "Bạn có khoảng 20–25 phút liên tục, ở nơi yên tĩnh, trong vài ngày tới không?" | Do you have ~20-25 uninterrupted minutes, somewhere quiet, in the next few days? | "Không thu xếp được" (Cannot arrange it) |

Anyone who fails Q1, Q2, Q4, or Q5 is dropped regardless of the others (hard disqualifiers). Q3 and
Q6 are soft — prefer a better-fitting or more available candidate if one exists, but they alone
don't disqualify.

## 5. Consent script — verbatim Vietnamese

Read aloud at the very start of the session, **before Task 1 is handed over**, and captured on the
recording itself (or in writing if the recording has not started yet).

**Consent script (read aloud, Vietnamese):**

> Trước khi bắt đầu, mình xin phép nói rõ vài điều:
>
> Đây là một buổi kiểm thử usability cho bài tập môn học của mình. Mình đang test một tính năng
> trên web sự kiện của trường, không phải test bạn — không có cách làm nào là "sai" cả.
>
> Buổi này sẽ được quay lại màn hình, và [có/không] kèm ghi âm giọng nói. Bản ghi này chỉ dùng để
> mình xem lại và viết báo cáo cho bài tập, mình sẽ không chia sẻ công khai.
>
> Bạn có thể dừng lại bất cứ lúc nào nếu không muốn tiếp tục, không cần lý do.
>
> Thông tin liên hệ của bạn (Zalo/SĐT/email) sẽ được mình lưu ở dạng che một phần thông tin trong
> báo cáo nộp bài, nhưng trợ giảng của môn học có thể liên hệ với bạn qua thông tin đầy đủ (mình
> giữ riêng, không nộp bản đầy đủ) để xác nhận là bạn có thực sự tham gia buổi test này không.
>
> Bạn đồng ý chứ?

**English gloss:** Before we start: this is a usability test for my coursework, testing the
product, not you — there's no wrong way to do it. This session will be screen-recorded, and
[with/without] audio. The recording is only for my own review and the assignment report, never
shared publicly. You may stop at any time, no reason needed. Your contact info will be stored
masked in the submitted report, but a TA may reach you through the full (unmasked, privately kept)
version to confirm you really took part. Do you agree?

Wait for an explicit spoken "Có" / "Đồng ý" (or written yes) before proceeding to Task 1. If they
hesitate or decline any part (recording, audio, contact retention), stop and do not run the
session — do not substitute a different consent or negotiate it down.

## 6. Scheduling checklist

Confirm before locking in a slot:

- Device: will they use **their own** laptop/phone, or the moderator's? (Their own is preferred —
  matches real-world conditions; note it either way.)
- Browser they'll use (Chrome/Edge/Cốc Cốc/etc.) — record it, it matters for reproducing any bug.
- A quiet place with stable internet (the EMS tunnel is flaky — see
  `docs/usability_testing/design/Task_Scenario_D.md` §"Pre-session setup").
- A backup time slot in case the primary one falls through.
- Confirm the EMS URL is live **right before** the session (moderator responsibility, not the
  participant's).
- Confirm the participant has a working microphone/screen-share tool if the session is remote
  (Zalo call, Google Meet, or in person with screen recording software).

**Booking table template** — fill from real scheduling only; every cell starts as TBD:

| Slot | Role | Contact method | Proposed date/time | Backup date/time | Device (own / moderator) | Confirmed (Y/N) |
| --- | --- | --- | --- | --- | --- | --- |
| Pilot-1 | Pilot | TBD | TBD | TBD | TBD | TBD |
| P1 | Real participant | TBD | TBD | TBD | TBD | TBD |
| P2 | Real participant | TBD | TBD | TBD | TBD | TBD |
| P3 | Real participant | TBD | TBD | TBD | TBD | TBD |
| P4 | Real participant | TBD | TBD | TBD | TBD | TBD |
| P5 | Real participant | TBD | TBD | TBD | TBD | TBD |
| R1 | Reserve | TBD | TBD | TBD | TBD | TBD |
| R2 | Reserve | TBD | TBD | TBD | TBD | TBD |

The two reserve rows are the answer to `docs/usability_testing/design/Moderator_Runsheet.md` §10's
no-show recovery ("move to the reserve candidate"). Screen them like anyone else and hold them;
promoting a reserve into a P-slot means moving their row into
`docs/usability_testing/results/Participants_Table.md`, not inventing one.

Once a row is confirmed, mirror the outcome into
`docs/usability_testing/results/Participants_Table.md` — this table is for booking logistics only; that
file is the record of record for the study.

## 7. After-session message — verbatim Vietnamese

**After-session message (send as-is, Vietnamese):**

> Cảm ơn bạn rất nhiều vì đã dành thời gian giúp mình hôm nay! Buổi test giúp mình rất nhiều cho
> bài tập.
>
> Nhắc lại một chút: như mình có nói trước buổi test, trợ giảng của môn học có thể sẽ gọi điện
> hỏi thăm để xác nhận là bạn có tham gia thật, nên nếu có cuộc gọi lạ hỏi về việc này thì đừng
> ngạc nhiên nha — chỉ là xác nhận thôi. Cảm ơn bạn lần nữa nhé!

**English gloss:** Thank you very much for your time today — the session really helped my
assignment. Quick reminder, as mentioned before we started: a TA from the course may call to
confirm you genuinely took part, so don't be surprised by an unfamiliar call asking about this —
it's just verification. Thanks again.

## 8. Privacy handling

Masking convention — the brief's own wording is *"middle four digits masked"* / *"ẩn 4 số giữa"*
(§6 Task 2 Phase 1 and §12): mask **exactly four** digits in the middle of the number and leave the
rest readable, so `0901234567` becomes `090****567`; for an email, publish the local part only
(`nguyenvana2003@…`). The full rule, including the 11-digit case and why over-masking is
non-conforming rather than cautious, is specified once in
`docs/usability_testing/results/Participants_Table.md` §"Masking rule" — apply it there, not here.

The **unmasked** contact list (real names, full phone numbers/emails) must live outside this repo
entirely — e.g. a personal notes app or a private, non-synced local file — and must never appear
in the submission zip described in §15 of
`refs/requirements/2026.HW03.GUI Usability EMS_En.md`. Only the masked version, inside
`Participants_Table.md`, is submitted. Keep the unmasked list only long enough for the TA
verification window; do not fabricate a placeholder entry there either — an empty personal note
until real recruiting happens is correct.

## Gaps against `docs/usability_testing/design/Task_Scenario_D.md`

Reviewed the study design for consistency with this kit and with §6/§12 of the brief. One gap was
found and has since been **resolved**: the stated session duration disagreed across files
(`Participants_Table.md` said 10-15 minutes, this kit said 15-20), while the moderator run-sheet's
own block budget — consent 1-2 + T1 3-8 + admin resolve 1-2 + T2 2-4 + SUS 2 + probes 3-4 — adds up
to 12-22 minutes of the participant's time before any overrun.

**Settled figure: ~20-25 minutes**, used in every participant-facing message here, in
`docs/usability_testing/results/Participants_Table.md`, and in `docs/usability_testing/00_Run_Plan.md`.
The internal target in `docs/usability_testing/design/Moderator_Runsheet.md` stays **~20 minutes** — the
extra five minutes is the buffer that keeps the promise honest when a participant takes the long
end of T1. Do not quote a shorter number to a candidate to make scheduling easier; a session that
runs 10 minutes past what was promised is how a participant leaves before the SUS is administered,
and an uncompleted SUS costs that whole session.
