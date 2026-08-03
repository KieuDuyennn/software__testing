# Task 2 — Participants — Scenario D

> **Status: 5 of 5 recruited and run.** Recruited and run by Lê Phạm Kiều Duyên; the details below
> were supplied by her from her own private contact list, not produced by any agent.
> §12 anti-cheat clause: participants must be **real people outside this class**, with
> **verifiable** contact details; the TA may randomly call up to **2 of the 5** to confirm. An
> agent cannot recruit participants or supply session data — see
> `.claude/skills/usability-test-study/SKILL.md` §"What an agent can and cannot do here".
>
> **Two things to confirm before submitting.** (1) The answer sheets are headed 03/08/2026 while the
> sessions ran 2026-08-01; the session date is entered below, so align the sheets to it. (2) The
> P-code ↔ name mapping follows the order the participants were listed in — worth one check against
> the recordings, since P4's row carries the lowest score.

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

| Pilot | Name (or initials) | Profile | Outside this class (Y/N) | Contact (masked) | Date | Consent: screen / audio | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Pilot-1 | — | — | — | — | — | — | Not run; the five counted sessions went ahead directly. |

The instruments were desk-checked against the brief instead. Noted once in the report's Limitations.

## The 5 real participants

Every row must describe a real person you actually sat with. `Outside this class` is the §12
eligibility check and must read `Y` for all five — a `N` or a blank means that person cannot be
counted toward the five. `Consent` records what the participant agreed to be recorded, screen and
audio separately, matching the consent script in `docs/usability_testing/design/Recruiting_Kit.md` §5.

| P | Name | Profile | Outside this class (Y/N) | Contact (masked, phone) | Session date | Consent: screen / audio | Recording file in `reports/evidence_task2/` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | Đoàn Tú Uyên | Sinh viên Y đa khoa, Đại học Y Dược TP.HCM | Y | `034****161` | 2026-08-01 | Y / TBD | `P1_full_session.avi` |
| P2 | Huỳnh Thế Vũ | Sinh viên Cơ khí, Đại học Bách Khoa | Y | `036****675` | 2026-08-01 | Y / TBD | `P2_full_session.avi` |
| P3 | Lê Khôi Nguyên | Sinh viên Công nghệ thực phẩm, Đại học Bách Khoa | Y | `091****789` | 2026-08-01 | Y / TBD | `P3_full_session.avi` |
| P4 | Nguyễn Thành Tiến | Sinh viên Cơ khí, Đại học Công nghiệp | Y | `093****120` | 2026-08-01 | Y / TBD | `P4_full_session.avi` |
| P5 | Trần Nguyễn Ngọc An | Sinh viên Marketing, Đại học Kinh tế TP.HCM (UEH) | Y | `083****721` | 2026-08-01 | Y / TBD | `P5_full_session.avi` |

Five students from four different universities (Y Dược, Bách Khoa, Công nghiệp, UEH), across
medicine, mechanical engineering, food technology and marketing — none enrolled in this course, so
§12's "outside this class" bar is met by construction, and none of the five works in software, so
the set is not skewed toward technical users.

Screen consent is evidenced by the five recordings. Audio consent is a separate question in the
consent script and is left `TBD` until confirmed per participant.

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
