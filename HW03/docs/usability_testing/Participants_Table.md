# Task 2 — Participants — Scenario D

> **Status: EMPTY — no participants recruited yet.** Fill in once real people are recruited.
> §12 anti-cheat clause: participants must be **real people outside this class**, with
> **verifiable** contact details; the TA may randomly call up to **2 of the 5** to confirm. An
> agent cannot recruit participants or supply session data — see
> `.claude/skills/usability-test-study/SKILL.md` §"What an agent can and cannot do here". This
> table must be filled in by the student from real recruiting, never invented.

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
| Pilot-1 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | Run first; fix the script before the 5 real sessions |

## The 5 real participants

Every row must describe a real person you actually sat with. `Outside this class` is the §12
eligibility check and must read `Y` for all five — a `N` or a blank means that person cannot be
counted toward the five. `Consent` records what the participant agreed to be recorded, screen and
audio separately, matching the consent script in `docs/usability_testing/Recruiting_Kit.md` §5.

| P | Name (or initials) | Profile | Outside this class (Y/N) | Contact (masked, Zalo/email/phone) | Session date | Consent: screen / audio | Recording file in `reports/evidence_task2/` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | TBD |
| P2 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | TBD |
| P3 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | TBD |
| P4 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | TBD |
| P5 | TBD | TBD | TBD | TBD | TBD | TBD / TBD | TBD |

## Reserve candidates (used only if a booked slot falls through)

`docs/usability_testing/Moderator_Runsheet.md` §10 sends a no-show to "the reserve candidate" —
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
