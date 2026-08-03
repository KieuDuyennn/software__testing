# Task 2 — Participants — Scenario D

> **Status: 5 of 5 recruited and run.** Recruited and run by Lê Phạm Kiều Duyên; the details below
> were supplied by her from her own private contact list, not produced by any agent.
> §12 anti-cheat clause: participants must be **real people outside this class**, with
> **verifiable** contact details; the TA may randomly call up to **2 of the 5** to confirm. An
> agent cannot recruit participants or supply session data — see
> `.claude/skills/usability-test-study/SKILL.md` §"What an agent can and cannot do here".
>
> **One thing to confirm before submitting.** The P-code ↔ name mapping follows the order the
> participants were listed in, and has not been checked against the recordings. Worth one pass, since
> P4's row carries the lowest score and the TA may call two of the five.

## Masking rule — exactly four digits, no more, no fewer

The brief specifies the format twice and both say the same thing: §6 Task 2 Phase 1, *"verifiable
contact details (Zalo / email / phone, **middle four digits masked**)"*, and §12, *"name plus Zalo
/ phone, **middle four digits masked**"* (Vietnamese: *"ẩn 4 số giữa"*). So:

- **Phone.** Take the number as a plain digit string, replace **exactly four digits in the middle**
  with `*`, and leave every other digit visible. A Vietnamese 10-digit mobile `0901234567` becomes
  **`090****567`** — three visible, four masked, three visible, still ten characters. Count the
  asterisks before committing: four, never five, never a whole block. Do not also mask the last two
  digits, do not collapse the number into `090xxxxxxx`, and do not add spaces that change the digit
  positions. An 11-digit number keeps the extra digit visible on the left: `01234567890` →
  `0123****890` (four visible, four masked, three visible).
- **Email.** The brief's four-digit rule is written for a phone number, so for an email publish the
  local part and drop the domain: `nguyenvana2003@gmail.com` → **`nguyenvana2003@…`**. Prefer a
  phone/Zalo number as the listed contact wherever the participant gave one, because that is the
  form §12 names and the form a TA can dial.
- **Zalo** is a phone number — mask it as a phone.

A masked value that hides more than four digits is not "safer," it is non-conforming: the TA must
still be able to see enough of the number to recognise it against the unmasked list you hold
privately when they call to verify (§12).

## Pilot (not counted in Task 2 results)

| Pilot | Name | Profile | Outside this class (Y/N) | Contact (masked) | Date | Consent: recording | Recording |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pilot-01 | Nguyễn Kháng Chiến | Sinh viên Kinh tế Luật, Đại học Kinh tế – Luật (UEL) | Y | `034****512` | 2026-08-03 | Y | `reports/evidence_task2/Session_Pilot01.mp4` |

Run **before P1** on the same day. A sixth person, not one of the counted five — a pilot participant
has already seen the tasks and the screens, so their session can never also be counted. Write-up:
`docs/usability_testing/results/session_notes/Session_Pilot01.md`; what it changed and what it
recommended-but-did-not-get is in the report's §4.

**Verified before being relied on.** `Session_Pilot01.mp4` was frame-hashed against all five counted
recordings: **0 % shared frames** with every one of them, 485 unique frames over 35.2 s at 1280×720.
A claimed sixth session that turned out to be a copy of a counted one would be worse than no pilot, so
the check ran first. Its **durations and error counts are moderator-reported and uncorroborated** — the
recording is an excerpt — and they enter no table, no SUS figure and no finding.

**One field to confirm before submitting:** the university was given as an abbreviation and is recorded
here as Đại học Kinh tế – Luật (UEL), inferred from the stated major. The TA may call, so check the
spelling against your own record.

## The 5 real participants

Every row must describe a real person you actually sat with. `Outside this class` is the §12
eligibility check and must read `Y` for all five — a `N` or a blank means that person cannot be
counted toward the five. `Consent` records what the participant agreed to be recorded, screen and
audio separately, matching the consent script in `docs/usability_testing/design/Recruiting_Kit.md` §5.

| P | Name | Profile | Outside this class (Y/N) | Contact (masked, phone) | Session date | Consent: screen / audio | Recording file in `reports/evidence_task2/` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Đoàn Tú Uyên | Sinh viên Y đa khoa, Đại học Y Dược TP.HCM | Y | `034****161` | 2026-08-03 | Y / Y | `Session_P1.mp4` |
| P2 | Huỳnh Thế Vũ | Sinh viên Cơ khí, Đại học Bách Khoa | Y | `036****675` | 2026-08-03 | Y / Y | `Session_P2.mp4` |
| P3 | Lê Khôi Nguyên | Sinh viên Công nghệ thực phẩm, Đại học Bách Khoa | Y | `091****789` | 2026-08-03 | Y / Y | `Session_P3.mp4` |
| P4 | Nguyễn Thành Tiến | Sinh viên Cơ khí, Đại học Công nghiệp | Y | `093****120` | 2026-08-03 | Y / Y | `Session_P4.mp4` |
| P5 | Trần Nguyễn Ngọc An | Sinh viên Marketing, Đại học Kinh tế TP.HCM (UEH) | Y | `083****721` | 2026-08-03 | Y / Y | `Session_P5.mp4` |

Five students from four different universities (Y Dược, Bách Khoa, Công nghiệp, UEH), across
medicine, mechanical engineering, food technology and marketing — none enrolled in this course, so
§12's "outside this class" bar is met by construction, and none of the five works in software, so
the set is not skewed toward technical users.

All five consented to screen **and** audio recording, asked as two separate questions per the consent
script, before recording started.

## Reserve candidates (used only if a booked slot falls through)

`docs/usability_testing/design/Moderator_Runsheet.md` §10 sends a no-show to "the reserve candidate" —
screen and hold two, so a cancellation does not cost a session. A reserve who is never used stays
here and never appears in the table above.

| R | Name (or initials) | Profile | Outside this class (Y/N) | Contact (masked) | Screened on | Used for |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | TBD | TBD | TBD | TBD | TBD | (unused / P_) |
| R2 | TBD | TBD | TBD | TBD | TBD | (unused / P_) |

## Recruiting criteria (screener)

Use this to decide who to invite before scheduling:

1. Outside this course/class.
2. Has plausibly used, or would plausibly use, an event-registration platform (student, event-goer,
   or lecturer) — matches the population that would file a real EMS support request.
3. Able to do a ~20–25 minute screen-recorded session and answer a short questionnaire afterward.
4. Provides a contact method the TA could reach to verify participation (Zalo, phone, or email).

## Unmasked contact log (private — do NOT include in the submitted zip)

Keep full, unmasked contact details somewhere private (not in this repo / not in the submission
zip) in case the TA needs to reach a participant. This table only ever holds the masked version.
