# SUS Instrument (Vietnamese/English) — Scenario D

> Companion to `docs/usability_testing/Task_Scenario_D.md`. That document already decided **SUS
> over UEQ-S** for Scenario D (a score directly comparable across all four scenario owners'
> reports) — this file does not revisit that choice. This is the actual questionnaire the
> moderator reads aloud to a Vietnamese-speaking participant, plus the exact path from a filled
> answer sheet to a scored result.

## 1. Administration rules

- Administer the SUS **after both Task 1 and Task 2 are finished, and before the four probe
  questions**. Probing first would contaminate the questionnaire — once a participant starts
  narrating what frustrated them, their SUS ratings stop being an independent measurement and
  start echoing whatever they just said out loud.
- Use the **same wording every session** — read directly from the table in §3, do not paraphrase
  on the fly.
- **Read the 1–5 scale aloud once**, at the start, before item 1. Do not re-explain it per item.
- If a participant asks what a specific item "means," **do not explain or paraphrase it** — just
  re-read that item's Vietnamese wording once, exactly as written, and let them answer with
  whatever it means to them. Explaining defeats the point of a standardised instrument: two
  participants must be answering the same question, not two different questions the moderator
  privately tailored.
- The participant answers on a **1–5 scale**: 1 = hoàn toàn không đồng ý, 5 = hoàn toàn đồng ý.

### The scale (read aloud once, verbatim)

> "Với mỗi câu sau, bạn hãy cho biết mức độ đồng ý của bạn theo thang điểm từ 1 đến 5, trong đó:
> **1 = hoàn toàn không đồng ý, 2 = không đồng ý, 3 = trung lập (không đồng ý cũng không phản
> đối), 4 = đồng ý, 5 = hoàn toàn đồng ý.** Không có câu trả lời đúng hay sai, hãy trả lời theo
> cảm nhận thật của bạn về hệ thống vừa rồi."

## 2. The 10 SUS items (bilingual)

English wording is verbatim standard SUS, matching
`docs/usability_testing/session_notes/Session_Notes_TEMPLATE.md` item-for-item and in the same
order. `[R]` marks the 5 reverse-scored items.

| # | English (verbatim) | Vietnamese (read aloud to participant) | |
| --- | --- | --- | --- |
| 1 | I think that I would like to use this system frequently | Tôi nghĩ rằng tôi sẽ muốn sử dụng hệ thống này thường xuyên. | |
| 2 | I found the system unnecessarily complex | Tôi thấy hệ thống này phức tạp một cách không cần thiết. | [R] |
| 3 | I thought the system was easy to use | Tôi thấy hệ thống này dễ sử dụng. | |
| 4 | I think that I would need the support of a technical person to use this system | Tôi nghĩ rằng tôi sẽ cần một người rành kỹ thuật hỗ trợ thì mới dùng được hệ thống này. | [R] |
| 5 | I found the various functions in this system were well integrated | Tôi thấy các chức năng khác nhau trong hệ thống này được kết hợp với nhau khá tốt. | |
| 6 | I thought there was too much inconsistency in this system | Tôi thấy hệ thống này có quá nhiều chỗ thiếu nhất quán. | [R] |
| 7 | I would imagine that most people would learn to use this system very quickly | Tôi nghĩ rằng hầu hết mọi người sẽ học cách dùng hệ thống này rất nhanh. | |
| 8 | I found the system very cumbersome to use | Tôi thấy hệ thống này rất cồng kềnh, bất tiện khi dùng. | [R] |
| 9 | I felt very confident using the system | Tôi cảm thấy khá tự tin khi sử dụng hệ thống này. | |
| 10 | I needed to learn a lot of things before I could get going with this system | Tôi cần phải học khá nhiều thứ trước khi có thể bắt đầu sử dụng được hệ thống này. | [R] |

Every Vietnamese row says "hệ thống này" for consistency, matching the English "this system" —
not "trang web," "ứng dụng," or "nền tảng," so no item quietly narrows or widens what the
participant is rating relative to the others.

**Items 2, 4, 6, 8, 10 are negatively worded on purpose.** This is standard SUS design, not a
translation defect — do not "fix" them into positive phrasing (e.g. turning item 2 into "hệ
thống này đơn giản"). `score_sus.py` reverse-scores exactly these five positions when computing
the total; if the wording were flipped, the score would be silently wrong.

## 3. Printable answer sheet

Hand this to the participant (or the moderator fills it in while reading items aloud). One tick
per row, 1–5.

| # | 1 | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- | --- |
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |
| 6 | | | | | |
| 7 | | | | | |
| 8 | | | | | |
| 9 | | | | | |
| 10 | | | | | |

Thang điểm: 1 = hoàn toàn không đồng ý · 2 = không đồng ý · 3 = trung lập · 4 = đồng ý ·
5 = hoàn toàn đồng ý.

## 4. Probe questions (Vietnamese, asked after the SUS)

Same wording every session, matching `docs/usability_testing/Task_Scenario_D.md` one-for-one.
**Ask exactly the wording below, then stay silent** — give the participant time to think instead
of filling the pause with a hint or a rephrase.

1. **Clarity (Sự rõ ràng)** — "Was there any point where you weren't sure what the platform
   wanted from you, or what would happen next?"
   VI: *"Có lúc nào bạn không chắc chắn platform đang muốn bạn làm gì, hoặc điều gì sẽ xảy ra
   tiếp theo không?"*
2. **Error recovery (Xử lý khi gặp lỗi)** — "If you made a mistake or had to backtrack, how did
   you notice, and how did you get back on track?"
   VI: *"Nếu bạn đã làm sai hoặc phải quay lại bước trước đó, bạn nhận ra điều đó bằng cách nào,
   và bạn đã quay lại đúng hướng như thế nào?"*
3. **Speed (Tốc độ / công sức)** — "Did anything feel slower or more effortful than it should
   have?"
   VI: *"Có điều gì khiến bạn cảm thấy chậm hơn hoặc tốn công sức hơn mức cần thiết không?"*
4. **Trust (Sự tin tưởng)** — "Once you submitted the report, how confident were you that it
   actually went through and someone would see it? Why?"
   VI: *"Sau khi bạn gửi báo cáo đó, bạn tự tin đến mức nào rằng nó đã thực sự được gửi đi và sẽ
   có người xem được? Vì sao?"*

If the participant's answer is too short to be useful, one neutral follow-up is allowed — it must
not lead toward any particular answer:

> *"Bạn nói rõ hơn chỗ đó được không?"*

Do not follow up with anything more specific ("Ý bạn là do màu sắc à?", "Có phải vì cái nút đó
không?") — that supplies the participant an answer rather than eliciting theirs.

## 5. Data entry

One completed answer sheet (§3) becomes **one row** in `docs/usability_testing/SUS_Responses.csv`.

- Enter the **raw 1–5 values exactly as ticked**, including for the reverse-scored items 2, 4, 6,
  8, 10. Do **not** pre-adjust or invert them before entry — `score_sus.py` does the
  reverse-scoring itself, keyed to item position. Entering already-inverted values would cause the
  script to invert them a second time and silently produce the wrong SUS score.
- One row per participant, `participant` column holding their session id (`P1`…`P5`; the pilot's
  row, if kept for the script author's own reference, must not be counted in `Metrics_Table.md`
  per `docs/usability_testing/Task_Scenario_D.md`).

### Worked example (format illustration only — not real data)

The row below exists only to show column order and value shape. `EXAMPLE` is used as the
participant id specifically so it can never be mistaken for a real participant's data. **Delete
this row from the actual `SUS_Responses.csv` before scoring** — it must not appear in any scored
output or in `Metrics_Table.md`.

```
participant,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
EXAMPLE,4,2,5,1,4,2,5,2,4,1
```

## 6. Scoring

Run from `HW03/` (repo-root-relative paths):

```
python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/SUS_Responses.csv --instrument sus --markdown
```

Expected output: a markdown table with one row per participant (`participant`, `SUS score`,
adjective band), a **Mean** row, and a trailing line giving `n`, `SD`, and the `range` (min–max).

Paste that output — table and the `n`/SD/range line together — into
`docs/usability_testing/Metrics_Table.md`. **Report the individual per-participant scores, the
mean, and the range together, not the mean alone** — a mean can look identical whether all five
participants agreed or whether they were split between "loved it" and "hated it," and only the
individual scores and range show which one actually happened.

## 7. Interpretation guardrails

At n = 5, SUS is **descriptive only**. Report the scores and the adjective/grade bands the script
prints, and stop there — do not compute or imply a confidence interval, do not claim statistical
significance for any difference between participants or between this scenario and another, and do
not state a claim like "above/below the industry average" as if it were a measurement (the
Sauro-Lewis curved grade and Bangor adjective bands are useful shorthand labels, not a claim that
this sample was drawn from, or is representative of, the industry-wide benchmark population).
