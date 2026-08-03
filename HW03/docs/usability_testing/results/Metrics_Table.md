# Task 2 — Metrics table — Scenario D

> Five sessions run 2026-08-03. Counts, not percentages, at n = 5 — a percentage implies more
> precision than 5 data points support.
>
> **Provenance of the two columns below.** `Result` and `Route` are reconstructed from each
> participant's **own written answers** to the four probe questions
> (`docs/usability_testing/results/session_notes/Session_P1..P5.md`), which describe what they did in
> their own words. They are therefore **self-reported, not moderator-observed**, and each cell below
> names the sentence it rests on. Confirm them against the recordings in `reports/evidence_task2/`
> before submission and mark the column observed once you have.
>
> **Time on task, errors and hesitations were not measured** — no clock was run and no observation
> log was kept during the sessions, so those columns stay empty rather than being estimated from
> video length. A missing measure is a missing measure.

## Per-participant results (the raw table everything else is derived from)

Transcribed from the five `session_notes/Session_P<n>.md` "Task outcomes" tables — one row per
participant per task, nothing aggregated yet. The pilot is **not** a row here. Mark `Intervened`
`Y` wherever the moderator gave a task-specific hint or clicked for the participant; an intervened
run cannot count as a clean Complete and its time is excluded from the mean below
(`docs/usability_testing/design/Moderator_Runsheet.md` §6).

| P | Task | Result (self-reported) | The participant's own words it rests on | Time | Errors | Hesit. | Route used to reach the response (T2) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P1 | T1 | Complete | *"sau khi gửi có thông báo thành công và yêu cầu xuất hiện trong danh sách với trạng thái"* | — | — | — | — |
| P1 | T2 | Complete | *"khi quay lại danh sách, dòng mới nhất và trạng thái giúp tôi biết mình đang đúng chỗ"* | — | — | — | Danh sách yêu cầu |
| P2 | T1 | Complete, after recovering | *"khi bấm gửi mà ảnh chưa có, phần báo lỗi làm tôi nhận ra và quay lại gắn ảnh"* | — | — | — | — |
| P2 | T2 | Complete, with difficulty | *"lúc tìm phản hồi tôi dùng nút quay lại rồi thử menu khác"*; *"tìm lại yêu cầu hơi lâu vì tên menu chưa giống cách tôi nghĩ"* | — | — | — | Danh sách yêu cầu, sau khi thử nhầm menu |
| P3 | T1 | Complete | *"việc đính ảnh và gửi diễn ra nhanh"*; *"không có bước nào thừa"* | — | — | — | — |
| P3 | T2 | Complete | *"dấu hiệu ở chuông làm tôi đoán có phản hồi mới"*; *"thông báo dẫn tới phản hồi chính thức"* | — | — | — | **Chuông thông báo** |
| P4 | T1 | Complete, after recovering | *"tôi nhận ra mô tả chưa đủ khi biểu mẫu không cho gửi"* | — | — | — | — |
| P4 | T2 | Complete, with difficulty | *"tôi mở nhầm yêu cầu cũ rồi dựa vào ngày và tiêu đề để quay lại"*; *"ở danh sách tôi cũng không biết dòng nào là yêu cầu vừa gửi"* | — | — | — | Danh sách yêu cầu, sau khi mở nhầm |
| P5 | T1 | Complete | *"tôi tự kiểm tra lại trước khi gửi"*; *"yêu cầu có mã và trạng thái trong danh sách"* | — | — | — | — |
| P5 | T2 | Complete, with difficulty | *"tôi thử chuông rồi quay lại vì không thấy đúng thông tin, sau đó tìm trong danh sách yêu cầu"* | — | — | — | Chuông trước, **không dùng được**, rồi danh sách |

## Task success (aggregate — the "success rate, mean time, errors" table §6 Phase 3 asks for)

Success rate is reported as a **count out of 5**, not a percentage: at n = 5 a percentage claims
precision the sample cannot carry, and `4/5` and `80%` are the same fact with different honesty.

| Task | Complete (of 5) | of which: recovered from a self-caught error | Partial | Fail | Mean time | Errors | Hesitations |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 — file the report | **5/5** | 2 (P2 missing image, P4 thin description) | 0/5 | 0/5 | not measured | not counted | not counted |
| T2 — find the response | **5/5** | — | 0/5 | 0/5 | not measured | not counted | not counted |

**Both tasks completed by all five, so success rate is not where the signal is.** Three of the five
reached the response only after a wrong turn (P2 tried a different menu, P4 opened the wrong request,
P5 tried the bell and fell back to the list), and the SUS spread of 27.5–97.5 says the same thing the
success column cannot: the tasks are *achievable* but the path to them is not *discoverable*. A
success-rate-only reading of this study would conclude the product is fine, which none of the four
open-question answers supports.

**Route taken to the response (T2)** — never steered, so this is a findability result: 4 of 5 used
the requests list, 1 (P3) used the notification bell. P5 tried the bell first and abandoned it.

Nothing was excluded from any aggregate. No mean is reported because no time was measured.

## SUS scores

Run: `python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/results/SUS_Responses.csv --instrument sus --markdown`
and paste the output table here.

| Participant | SUS score | Adjective |
| --- | --- | --- |
| P1 | 80.0 | Excellent |
| P2 | 60.0 | OK |
| P3 | 97.5 | Best imaginable |
| P4 | 27.5 | Awful |
| P5 | 70.0 | Good |
| **Mean** | **67.0** | Good |

n = 5, **SD = 26.1, range 27.5–97.5**. Reported descriptively — n is too small for a statistical claim.

**The spread is the finding, not the mean.** A mean of 67 would normally read as "acceptable, room to
improve". At SD 26.1 it describes nobody: no participant scored within 6 points of it. The same
product was rated *Best imaginable* by P3 and *Awful* by P4, and the two ratings are consistent with
what each of them wrote — P3 *"hiểu ngay biểu mẫu cần gì"*, P4 *"không chắc nên tìm ở Hồ sơ, Sự kiện
hay Hỗ trợ"*. Experience here is close to binary: it depends on whether the user guesses the right
menu on the first try. Quoting the mean alone would hide that.

## Interpretation note

Five participants surface most of the *findable* problems in a formative, single-user-group study,
but support no statistical claim (no significance, no confidence interval, no benchmark
comparison). Report "3 of 5 participants hit X," give the SUS mean alongside the five individual
scores, and let the severity ranking in the Usability Report carry the argument.
