# Usability Report — EMS Scenario D (Support requests) — Lê Phạm Kiều Duyên, 23127184

> **Status: run. 5 of 5 participants, 5 sessions held 2026-08-03,** all recruited and moderated by
> Lê Phạm Kiều Duyên. Every participant is a real, contactable person from a university other than
> this one; the masked contact list is in `docs/usability_testing/results/Participants_Table.md`.
> No number, quote or answer in this file comes from anywhere except those five sessions.
>
> **Evidence.** Two independent records per participant: the completed questionnaire (10-item SUS +
> four open probes) in `docs/usability_testing/results/session_notes/`, and a screen recording,
> `reports/evidence_task2/Session_P1..P5.mp4`. The five recordings were checked to be genuinely
> distinct before being relied on — **0 % of frames are shared between any pair**, and each shows that
> participant writing their own scenario (Tech Talk Data & Cloud, Giải chạy FIT, Workshop Kỹ năng
> phỏng vấn, AI Career Day, Câu lạc bộ 27/07). Findings citing a screenshot use a still cut from the
> recording of the participant who hit the problem.
>
> **Headline: both tasks were completed by all five, and the product still has a findability
> problem.** SUS mean **67.0**, but with **SD 26.1 across a 27.5–97.5 range** — no participant scored
> within 6 points of the mean. Three of the five reached the official response only after a wrong
> turn, and the five reported **7 error episodes between them — 5 of the 7 are "I was in the wrong
> place"**. Success rate alone would have reported this product as fine; it is not what the five people
> described.

**Section map against the brief.** §6 Task 2 Phase 3 requires the report to contain: the scenario
(§3 below) · the participant table, 5 people, masked (§5) · the metrics tables (§6 task metrics,
§7 SUS) · the findings ranked by severity **with a screenshot each** (§9) · a prioritised list of
concrete recommendations (§11). §7 of the brief requires genuine bugs to be logged through the
findings channel (§13 below).
Nothing here may be deleted as "not applicable"; each one is separately marked in the rubric.

---

## 1. Method and what was measured

| | |
| --- | --- |
| Method | Moderated think-aloud, one participant at a time |
| Participants | **n = 5** counted, all outside this class, plus **one pilot (Pilot-01) run before P1** whose data enters no result — see §4 |
| Session length | ~20–25 minutes per participant |
| Session language | Vietnamese (all participant-facing wording; this report is in English) |
| Mode / device | Moderated, one participant at a time, screen recorded; recordings in `reports/evidence_task2/` |
| Dates | **2026-08-03**, all five sessions |
| Instrument | **SUS**, 10 items, administered after both tasks and **before** the probe questions |
| Recording | Screen **and** audio, all five; consent to each asked separately and captured before recording started |
| Moderator | Lê Phạm Kiều Duyên |

Measures collected, the minimum set named in §6 Task 2 Phase 1:

| Measure | Definition used | Where it lands |
| --- | --- | --- |
| Task success | Complete / Partial / Fail against criteria fixed **before** the sessions (§3) | §6 |
| Time on task | Defined as: from the participant beginning to act on the prompt until the success criterion, intervened runs excluded from means. **No clock was run, so this measure was not collected** — §6 note 3, §11b | — |
| Errors | An action that moved the participant off the success path and had to be undone. **Counted from what each participant wrote about their own session**, one episode = 1: 7 episodes, 3 of 5 people | §6 |
| Hesitations | Points of uncertainty the participant states in their own words. **Not** the ≥3 s pause count, which needs a clock on the recording: 7, 4 of 5 people | §6 |
| Perceived effort | Ordinal rank from probe 3, standing in for time on task in the analysis and nowhere claimed to be it | §6 |
| SUS | 10 items, 1–5, reverse-scored at positions 2/4/6/8/10 by `score_sus.py` | §7 |
| Open probes | Four fixed questions: clarity · error recovery · speed · trust | §8 |

## 2. Screens under test

| Page the participant reaches | Route | Package screen | Reached in |
| --- | --- | --- | --- |
| Create Support Request form | `/complaints/new` | **D1** | Task 1 |
| My Requests list | `/complaints` | **D2** (list) | Task 2 |
| Request detail with the official response | `/complaints/{id}` | **D2** (detail) | Task 2 |
| Notifications bell / list / detail | `/notifications`, `/notifications/{id}` | **D5** | Unprompted, by **P3** (succeeded) and **P5** (tried, could not use it, fell back to the list) |

Three distinct user-facing pages across the same package screens tested in Task 1B
(`docs/02_Task1B_Execution_Report_ScenarioD.md`), plus a fourth reached only by participants who
chose that route. **D3** and **D4** (admin list and admin detail) are operated by the moderator to
resolve each request mid-session and are never shown to a participant — exercised, not user-tested.
See §12 (Limitations).

## 3. Task scenario

Full design, success criteria and moderator script: `docs/usability_testing/design/Task_Scenario_D.md`.
Goal-oriented, no click path given, and deliberately avoiding EMS's own vocabulary so the task
tests findability rather than reading comprehension.

**Task 1 (verbatim, as spoken):**

> *"Bạn hãy tưởng tượng là bạn đã đăng ký tham gia một sự kiện trên trang web này, nhưng tới hôm
> diễn ra sự kiện, lúc bạn check-in thì hệ thống lại báo là bạn chưa hề đăng ký. Bạn muốn chuyện
> này được xử lý. Bạn hãy dùng trang web để báo lại vấn đề đó, theo cách nào bạn thấy là đúng — các
> thông tin chi tiết (tên sự kiện, ngày bạn đăng ký, v.v.) thì bạn cứ tự nghĩ ra thoải mái nhé."*

English gloss: *"Imagine you registered for an event here, but on the day the check-in said you
were never registered. You want it fixed. Use the platform to report the problem, however you think
is right — invent whatever details you need."*

*Success:* a support request submitted with a request type, a description, and at least one image
attached. *Partial:* submitted but missing the image, or with an unclear description. *Fail:* could
not submit, or gave up.

**Task 2 (verbatim, handed over after the moderator has quietly resolved the request):**

> *"Cái vụ lúc nãy bạn báo đó, giờ bạn thử xem có ai trả lời lại chưa, rồi đọc cho mình nghe họ
> nói gì nhé."*

English gloss: *"That thing you reported earlier — check whether anyone has replied, and read me
what they said."*

*Success:* the participant finds their own request without being told the menu name and reads the
official response back correctly. *Partial:* finds the request but misses or misreads the response.
*Fail:* cannot find where the request went.

## 4. Pilot

Required by §6 Task 2 Phase 1: one extra person, run before the counted sessions, to catch unclear
wording or a broken flow. **Pilot data never enters §6, §7 or §8** — no metric, no SUS score and no
finding in this report is computed from it.

| | |
| --- | --- |
| Pilot run on | **2026-08-03, before P1.** Session code Pilot-01. |
| Participant | Nguyễn Kháng Chiến — Kinh tế Luật, Đại học Kinh tế – Luật (UEL). Outside this class: **Y**. Contact `034****512`, middle four masked per §12. Consent to recording: **Y**. Sixth person, not one of the counted five. |
| Evidence | `reports/evidence_task2/Session_Pilot01.mp4` — 35.2 s captured, 1280×720. Verified a **distinct** recording: 0 % frame overlap against every one of `Session_P1..P5.mp4`, 485 unique frames. |
| Write-up | `docs/usability_testing/results/session_notes/Session_Pilot01.md` |
| Outcome | T1 **Partial** — first submit rejected, recovered unaided. T2 **Complete** — one back-track, no moderator intervention. |
| Durations and counts | Moderator-reported (18:42 total; T1 6:18, T2 1:36; 2 errors, 4 hesitations). The recording is a 35-second excerpt and **does not corroborate them**; they are attributed rather than asserted, and enter no calculation anywhere in this report. |

**What the pilot changed before P1.** Three of the eight adjustments in `Session_Pilot01.md` §6 were
carried through and are visible in the run of the counted five: a valid image file was staged for every
session, login state and submit capability were checked before each session, and the task wording was
left untouched — no function name and no click path was added to the prompt, which is why §6's
findability result means anything.

**What the pilot recommended and the counted sessions did not do.** Items 1–3 and 5 of that list — fix
the clock start/stop convention, and have the moderator log errors, back-tracks and pauses over three
seconds — were agreed and then **not implemented across P1–P5**. That is why §6 carries no time on task
and why the error and hesitation counts there are participant-reported rather than observer-recorded.
The pilot did its job and identified the gap; the process failure was downstream of it. Stated here
rather than in §12 alone, because a pilot whose recommendations were dropped is a weaker pilot than one
whose recommendations were followed.

**One pilot observation is still open.** §5.1 reports a required field losing its value after the image
upload, forcing a re-entry before the form would submit. Nothing equivalent appears in the five counted
sessions, and it has **not been reproduced against the live product**, so it carries **no finding ID**
and is not counted among the 24 in `docs/05_Bug_Usability_Findings_Log.md`. It is a lead to re-test,
not a result.

## 5. Participants

Five real people, all outside this class, contacts masked per §12 (middle four digits). The
unmasked list is held privately by the moderator and is **not** in this repository or the
submission zip. Source of record: `docs/usability_testing/results/Participants_Table.md` — keep the two
copies identical.

| P | Name | Profile | Outside this class | Contact (masked) | Session date | Consent: screen / audio |
| --- | --- | --- | --- | --- | --- | --- |
| P1 | Đoàn Tú Uyên | Y đa khoa, ĐH Y Dược TP.HCM | Y | `034****161` | 2026-08-03 | Y / Y |
| P2 | Huỳnh Thế Vũ | Cơ khí, ĐH Bách Khoa | Y | `036****675` | 2026-08-03 | Y / Y |
| P3 | Lê Khôi Nguyên | Công nghệ thực phẩm, ĐH Bách Khoa | Y | `091****789` | 2026-08-03 | Y / Y |
| P4 | Nguyễn Thành Tiến | Cơ khí, ĐH Công nghiệp | Y | `093****120` | 2026-08-03 | Y / Y |
| P5 | Trần Nguyễn Ngọc An | Marketing, ĐH Kinh tế TP.HCM (UEH) | Y | `083****721` | 2026-08-03 | Y / Y |

Five students from four universities across medicine, mechanical engineering, food technology and
marketing. None is enrolled in this course, and none works in software — so the sample is not skewed
toward users who would find a technical interface unusually easy.

Recruiting channel and screener: `docs/usability_testing/design/Recruiting_Kit.md` §1–§4. Masking format:
`0901234567` → `090****567`, exactly four digits hidden.

## 6. Metrics — task success, time, errors

Tabulated in `docs/usability_testing/results/Metrics_Table.md`, which carries the per-participant
breakdown this table is derived from. Counts out of 5, not percentages — at n = 5 a percentage claims
precision the sample cannot carry.

| Task | Complete (of 5) | of which: recovered from a self-caught error | Partial | Fail | Mean time | Errors (self-reported) | Hesitations (self-reported) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T1 — file the report | **5/5** | 2 (P2, P4) | 0/5 | 0/5 | not measured | **4 episodes, 2 of 5** | **4, 4 of 5** |
| T2 — find the response | **5/5** | — | 0/5 | 0/5 | not measured | **3 episodes, 3 of 5** | **3, 3 of 5** |
| **Both** | 10/10 runs | 2 | 0 | 0 | not measured | **7, 3 of 5** | **7, 4 of 5** |

Every one of the seven error episodes is listed with the participant sentence it is counted from, in
`docs/usability_testing/results/Metrics_Table.md` §"Where each error episode comes from". Read that
way the seven split **5 findability errors** (wrong page, wrong menu, wrong request, unusable bell
route) against **2 blocked submissions** — and the blocked submissions are the form doing its job, not
failing. That split is the argument of §9 and §10 in one line.

**Three provenance statements this table depends on, made once here rather than implied.**

1. **Task outcomes are self-reported.** They are reconstructed from each participant's own written
   answers to the four probe questions, and the per-participant table in
   `docs/usability_testing/results/Metrics_Table.md` quotes the sentence each cell rests on. They are
   not moderator observations, and confirming them against the recordings in
   `reports/evidence_task2/` is the next step on this task.
2. **The error and hesitation counts are participant-reported and are a lower bound.** Each episode is
   one the participant described in writing; an error they made without noticing, or noticed and did
   not mention, is not in the count. A moderator-observed count would be equal or higher, never lower.
   The hesitation column counts self-declared uncertainty points (*"phân vân"*, *"không chắc"*,
   *"dừng lại một chút"*) — it is **not** the ≥3 s pause count §6 defines, which needs a clock on the
   recording. Counting rules are written out in `docs/usability_testing/results/Metrics_Table.md`.
3. **Time on task was not measured.** No clock was run, and the recordings are 18.8–26.0 s excerpts,
   so a duration taken from them would measure the clip and not the task. It is the one required
   measure this study does not carry, and it is not silently replaced: what stands in its place is an
   ordinal **perceived-effort rank**, taken from each participant's own answer to probe 3, and labelled
   as ordinal wherever it is used.

**Perceived effort, error count and SUS agree in rank order for all five participants** — P3 (0 errors,
97.5) · P1 (0, 80.0) · P5 (1, 70.0) · P2 (3, 60.0) · P4 (3, 27.5), no inversion. Nobody who hit an
error scored above 70; both zero-error participants scored 80 or better. That is internal consistency
rather than corroboration — all three come from the same person in the same sitting — but it does mean
the SUS spread in §7 is not an artefact of how people felt about filling in a questionnaire: it tracks
what they actually reported doing.

**Success rate is not where the signal is.** Everyone finished both tasks; the product is usable in
the sense that a determined person gets through it. What separates the five is *how much guessing it
took* — see §7 and §8, and the four findings in §9 that come out of them. A report that stopped at
5/5 and 5/5 would conclude the interface is fine, and none of the twenty open-question answers
supports that conclusion.

**Route taken to the response (T2), never steered — a findability result in its own right:** 4 of 5
used the requests list, 1 (P3) used the notification bell. P5 tried the bell first, could not use
what it showed, and fell back to the list.

## 7. Metrics — SUS

Scored with
`python .claude/skills/usability-test-study/scripts/score_sus.py docs/usability_testing/results/SUS_Responses.csv --instrument sus --markdown`.
Report all five individual scores, the mean **and** the range — a mean alone cannot distinguish
five participants who agreed from five who were split.

| Participant | SUS score | Adjective |
| --- | --- | --- |
| P1 | 80.0 | Excellent |
| P2 | 60.0 | OK |
| P3 | 97.5 | Best imaginable |
| P4 | 27.5 | Awful |
| P5 | 70.0 | Good |
| **Mean** | **67.0** | Good |

n = 5, **SD = 26.1**, range **27.5–97.5**. Descriptive only: no confidence interval, no significance
claim, no "above/below the industry average" stated as a measurement.

**The spread is the result; the mean is nearly meaningless here.** 67.0 would ordinarily read as
"acceptable, some room to improve". At SD 26.1 it describes none of the five — no participant scored
within 6 points of it, and the distribution is not a cluster with an outlier but a genuine split.
The same two tasks on the same product produced *Best imaginable* (P3, 97.5) and *Awful* (P4, 27.5).

Each score is consistent with what that participant wrote, which is why the split is credible rather
than noise:

- **P3, 97.5** — *"Tôi hiểu ngay biểu mẫu cần gì"*, *"Không có bước nào thừa"*. Guessed right first
  time, including using the bell to reach the response.
- **P4, 27.5** — *"Tôi không chắc nên tìm ở Hồ sơ, Sự kiện hay Hỗ trợ"*, *"ở danh sách tôi cũng không
  biết dòng nào là yêu cầu vừa gửi"*. Guessed wrong twice and recovered both times by reasoning from
  dates and titles.

Both finished both tasks. The difference between 97.5 and 27.5 is entirely the cost of finding the
way, which is precisely what §9's findings address.

## 8. Probe question responses

Asked after the SUS, same wording every session (Vietnamese wording in
`docs/usability_testing/design/SUS_Instrument_VI_EN.md` §4). Summarise across the five participants and
quote verbatim where a quote carries the point; attribute each quote to P1–P5 and to a timestamp in
that session's notes.

| Probe | What the five said | Quotes (attributed, verbatim) | Feeds finding |
| --- | --- | --- | --- |
| **Clarity** — unsure what the platform wanted, or what would happen next | Splits cleanly in two. P3 understood the form immediately. The other four each name a specific moment of doubt, and they are not the same moment: **where to start** (P2, P4), **which request type to pick** (P1, P5), and **which row in the list is mine** (P4). | P4: *"Tôi không chắc nên tìm ở Hồ sơ, Sự kiện hay Hỗ trợ, và ở danh sách tôi cũng không biết dòng nào là yêu cầu vừa gửi."* · P2: *"Ban đầu tôi tìm trong trang Sự kiện vì nghĩ vấn đề đăng ký sẽ nằm ở đó; tôi không đoán ngay phải vào hỗ trợ."* · P1: *"Ở phần chọn loại yêu cầu tôi dừng lại một chút vì chưa chắc trường hợp mất đăng ký thuộc mục nào."* · P5: *"tôi phân vân giữa hai loại yêu cầu và không chắc đổi lựa chọn có làm mất nội dung đã nhập không."* · P3: *"Tôi hiểu ngay biểu mẫu cần gì."* | **D-024**, **D-025**, **D-026** |
| **Error recovery** — noticing a mistake and getting back on track | Recovery worked, and worked *because of validation*, not because of navigation. Both people who erred on T1 were caught by the form refusing to submit and fixed it unaided. Recovery on T2 was worse: it meant re-reading list rows. | P2: *"Khi bấm gửi mà ảnh chưa có, phần báo lỗi làm tôi nhận ra và quay lại gắn ảnh."* · P4: *"Tôi nhận ra mô tả chưa đủ khi biểu mẫu không cho gửi; về sau tôi mở nhầm yêu cầu cũ rồi dựa vào ngày và tiêu đề để quay lại."* · P1: *"khi quay lại danh sách, dòng mới nhất và trạng thái giúp tôi biết mình đang đúng chỗ."* | **D-025** (T2 half); the T1 half is a **strength**, see §10 |
| **Speed** — anything slower or more effortful than it should be | Nobody said the *system* was slow. Every complaint is about effort spent searching, not waiting. | P4: *"Tốn công nhất là dò nhiều menu và đọc từng yêu cầu để tìm đúng cái mới."* · P2: *"Tìm chỗ báo vấn đề và tìm lại yêu cầu hơi lâu vì tên menu chưa giống cách tôi nghĩ."* · P5: *"tôi phải kiểm tra các trường và làm mới trang để chắc phản hồi đã cập nhật."* · P3: *"việc đính ảnh và gửi diễn ra nhanh."* | **D-024**, **D-025** |
| **Trust** — confidence that the report went through and someone would see it | All five ended up confident, but only two were confident *at the moment of submitting*. The other three needed to go and look at the list or the detail page first — trust came from persistent state, not from the confirmation. | P4: *"Tôi chưa thật sự tin ngay sau khi gửi vì thông báo biến mất nhanh; chỉ khi mở được chi tiết và thấy trạng thái hoặc phản hồi tôi mới yên tâm."* · P2: *"Tôi tin ở mức vừa; có thông báo đã gửi nhưng chỉ yên tâm hơn khi thấy yêu cầu nằm trong danh sách."* · P5: *"Tôi khá tin vì yêu cầu có mã và trạng thái trong danh sách."* · P3: *"Tôi rất tin vì có xác nhận gửi, mục yêu cầu lưu lại nội dung, và thông báo dẫn tới phản hồi chính thức."* | **D-027** |

## 9. Findings, ranked by severity

Severity scale (Nielsen 0–4, as required by §6 Task 2 Phase 3):

| | |
| --- | --- |
| 0 | Not a usability problem |
| 1 | Cosmetic — fix if time permits |
| 2 | Minor |
| 3 | Major — high priority |
| 4 | Catastrophe — fix before release |

Rules applied when turning observations into the rows below, per
`docs/usability_testing/00_Run_Plan.md` §4.3:

- Group by **cause, not symptom** — three participants stumbling in three places for one underlying
  reason is **one** finding.
- **Systemic** (a finding): hit in **≥ 2 of 5** sessions, *or* once with a structural cause that can
  be named. **Isolated slip** (not a finding): one participant, once, no structural explanation —
  those go in §10, not here.
- Every row carries **a screenshot**; the brief asks for one per ranked finding by name. Files live
  in `reports/evidence_task2/`; an inline image embed from this file is written
  `![alt](../reports/evidence_task2/<file>)`.
- Distinguish a **product defect** (goes to the findings log as a Bug) from a **design problem**
  (goes as Usability) in the Type column.

| # | Severity | Type | Finding | Affected (of 5) | Evidence | Root cause | Recommendation | Log ID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **F1** | **3** — Major | Usability | **Nothing on the platform tells a user that "I have a problem with my registration" is handled under Support.** Two of five began the task somewhere else entirely, and neither reached the support form by recognition — they reached it by elimination after the pages they expected turned out not to offer it. | 2/5 (P2, P4) | P2: *"Ban đầu tôi tìm trong trang Sự kiện vì nghĩ vấn đề đăng ký sẽ nằm ở đó; tôi không đoán ngay phải vào hỗ trợ."* · P4: *"Tôi không chắc nên tìm ở Hồ sơ, Sự kiện hay Hỗ trợ"*, *"Tốn công nhất là dò nhiều menu"* · **Recordings** `Session_P2.mp4`, `Session_P4.mp4`. *No single-frame still: this finding is about movement across pages, which one frame cannot show.* | The entry point is named after the *organisation's* internal category ("Hỗ trợ") rather than after the user's situation. A registration problem is mentally filed under the event, and the event page offers no route onward. | On the event / registration page, add a visible "Báo vấn đề về đăng ký này" action that deep-links into `/complaints/new` with the event pre-filled. Failing that, at minimum surface Support from the event context. | **D-024** |
| **F2** | **3** — Major | Usability | **A user cannot tell which row in their request list is the one they just filed.** The list gives no "just submitted" cue, so identifying your own newest request means reading rows and reasoning from dates and titles. One participant opened the wrong request; a second described the same search as slow. | 2/5 (P4 hit it, P2 describes it) | P4: *"ở danh sách tôi cũng không biết dòng nào là yêu cầu vừa gửi"*, *"tôi mở nhầm yêu cầu cũ rồi dựa vào ngày và tiêu đề để quay lại"* · P2: *"tìm lại yêu cầu hơi lâu vì tên menu chưa giống cách tôi nghĩ"* · **Screenshot** `D-025_P4_two_pending_rows_same_timestamp.png` — P4's own list showing two Pending requests both stamped *Aug 3, 2026, 1:40 PM*, with nothing marking which one he had just filed; recording `Session_P4.mp4`. | After submitting, the user is returned to a list with no continuity from the action they just performed — no highlight, no anchor, no "mới nhất" marker. Default ordering alone does not communicate recency to someone who does not know the ordering. | Return the user to the **detail page of the request just created**, not to the list. If the list must be the landing page, highlight the new row and anchor to it. | **D-025** |
| **F3** | **2** — Minor | Usability | **The request-type choice is guesswork, and users fear that changing it will discard what they have typed.** Two participants stalled at the same control, and one of them was reasoning about data loss rather than about categories. | 2/5 (P1, P5) | P1: *"Ở phần chọn loại yêu cầu tôi dừng lại một chút vì chưa chắc trường hợp mất đăng ký thuộc mục nào"* · P5: *"tôi phân vân giữa hai loại yêu cầu và không chắc đổi lựa chọn có làm mất nội dung đã nhập không"* · **Screenshot** `D-026_P2_request_type_options_unexplained.png` — the open dropdown, all four options as bare labels (Support · Complaint · Contact · Other), no example or description on any of them | Type options are unexplained labels with no examples, so the user cannot map their situation to one. The data-loss fear is a separate, second-order cost of that same uncertainty. | Add one line of example text per request type ("ví dụ: đã đăng ký nhưng không check-in được"). Guarantee — visibly — that switching type preserves entered content. | **D-026** |
| **F4** | **2** — Minor | Usability | **The submission confirmation is too transient to establish trust.** Three of five did not believe the request had been filed until they navigated somewhere else and saw it persisted. The toast disappears before it has done its job. | 3/5 (P2, P4, P5) | P4: *"Tôi chưa thật sự tin ngay sau khi gửi vì thông báo biến mất nhanh; chỉ khi mở được chi tiết và thấy trạng thái hoặc phản hồi tôi mới yên tâm"* · P2: *"có thông báo đã gửi nhưng chỉ yên tâm hơn khi thấy yêu cầu nằm trong danh sách"* · P5: *"yêu cầu có mã và trạng thái trong danh sách"* · **Recordings** `Session_P4.mp4`, `Session_P5.mp4`. *No still: every post-submit frame in P1, P4 and P5 was searched and none contains the confirmation toast — consistent with the finding, but absence of a frame is not offered as proof of it.* | A time-limited toast is the only acknowledgement of a state-changing action the user cares about. Trust is being carried by *persistent* artefacts (the ID, the status pill) that the confirmation itself never shows. | Replace the transient toast with a persistent confirmation that names the request ID and its status, on the page the user lands on after submitting. Pairs naturally with F2's fix. | **D-027** |

**Corroboration of an existing Task 1B finding.** P5 tried the notification bell first and abandoned
it: *"lúc xem phản hồi tôi thử chuông rồi quay lại vì không thấy đúng thông tin, sau đó tìm trong
danh sách yêu cầu."* That is the user-side consequence of **D-015** (notification summaries carry a
permanently empty complaint title), already logged from Task 1B checklist execution. It is recorded
here as independent confirmation from a real user rather than as a new finding — the root cause is
already logged, and merging by cause is the rule this project applies everywhere else.

## 10. Observations that are not findings

Single-participant slips with no structural cause, and anything interesting that does not meet the
bar in §9. Recorded so the evidence is complete, explicitly **not** counted as findings and not
ranked — padding the finding count with these is how a small study starts overclaiming.

| Observation | Participant | Why it is not promoted to a finding |
| --- | --- | --- |
| Refreshed the page to be sure the response had updated: *"tôi phải kiểm tra các trường và làm mới trang để chắc phản hồi đã cập nhật"* | P5 | One participant, once. Plausibly the same root cause as F4 (trust carried by persistent state, not by feedback), but a single instance with a second possible explanation — ordinary caution — does not meet the ≥ 2 bar, and folding it into F4 would overstate F4's reach. |
| Reached the response via the notification bell without difficulty | P3 | Not a problem at all. Recorded because it is the *only* successful bell route in five sessions and is the counterexample to P5's failed one — worth keeping when D-015 is fixed and re-tested. |

**A strength worth stating, since it is a real result and not padding.** Form validation on D1 did
its job in both cases where it mattered: P2 submitted without an image and P4 with too thin a
description, and **both noticed the problem and fixed it unaided, from the form's own error message**
— *"phần báo lỗi làm tôi nhận ra và quay lại gắn ảnh"* (P2), *"Tôi nhận ra mô tả chưa đủ khi biểu mẫu
không cho gửi"* (P4). Error prevention and recovery on the form itself is the part of this flow that
works, and no recommendation below asks for it to be changed.

## 11. Prioritised recommendations

Concrete and actionable — name the screen, the control, and the change. Ordered by severity first,
then by cost to fix, so the top of the list is what to do on Monday morning. Each row must trace
back to a finding number in §9; a recommendation with no finding behind it is an opinion.

| Priority | From | Screen / control | Concrete change | Severity | Effort |
| --- | --- | --- | --- | --- | --- |
| **1** | **F2** (D-025) | D1 → post-submit redirect | After a successful submit, land the user on `/complaints/{id}` — the request they just created — instead of the list. Removes the "which row is mine" problem at source rather than decorating around it. | 3 | **S** |
| **2** | **F1** (D-024) | Event / registration page → D1 | Add a "Báo vấn đề về đăng ký này" action on the event context, deep-linking to `/complaints/new` with the event pre-filled. Puts the entry point where users already look. | 3 | **M** |
| **3** | **F4** (D-027) | D1 confirmation | Replace the transient toast with a persistent confirmation block showing the request ID and status. If priority 1 ships, this is where it lands anyway — the two fixes combine. | 2 | **S** |
| **4** | **F3** (D-026) | D1 request-type select | One line of example text under each type option; guarantee and state that switching type preserves entered content. | 2 | **S** |
| **5** | **D-015** (Task 1B, confirmed by P5) | D5 notification summary | Populate the complaint title in notification summaries. Currently the bell is a dead end for anyone who tries it — P3 succeeded through it only because the surrounding cues were enough. | — | **S** |

**Priorities 1 and 3 are the same change.** Landing the user on the detail page of the request they
just created both identifies the request (F2) and provides a persistent confirmation (F4). One small
fix addresses a Major and a Minor finding, which is why it is first despite F1 also being Major.

## 11b. Conformance against §6 Task 2, item by item

Stated as a table so nothing has to be inferred. Every row names where the requirement is met, or
says plainly that it is not and why it cannot be recreated after the fact.

| §6 requirement | State | Where / why |
| --- | :-: | --- |
| **Phase 1** — goal-oriented task scenario, no click path | Met | §3; wording avoids EMS's own vocabulary so the task tests findability |
| Measure: **task success** | Met | §6, per participant in `results/Metrics_Table.md` |
| Measure: **time on task** | **Not met** | No clock was run during the sessions. The recordings are short excerpts (18.8–26.0 s of captured footage), not full sessions, so a duration read off them would not be time on task. §6 carries an ordinal **perceived-effort rank** in its place, from probe 3, labelled as ordinal — it is a substitute for the analysis, not for the measure. Cannot be recreated without re-running the study. |
| Measure: **error / hesitation count** | **Partly met** | **Errors: 7 episodes counted**, 3 of 5 participants, each traced to the participant's own sentence in `results/Metrics_Table.md`. **Hesitations: 7**, 4 of 5 participants. Both are participant-reported and therefore a **lower bound**, and the hesitation figure counts self-declared uncertainty points, not the ≥3 s pauses §6 defines — that needs a clock on the recording. Counted honestly from the data that exists; an observer-recorded count was never taken. |
| Measure: **post-task SUS or UEQ-S** | Met | SUS, 10 items, §7; scored by `score_sus.py` |
| **Open probes** covering clarity · error recovery · speed · trust | Met | §8, all four asked of all five, same wording |
| **5 real participants**, target profile, verifiable contacts, middle four digits masked, outside this class | Met | §5; four universities, none in this course, none in software |
| **Pilot** with one extra person | Met | Pilot-01, a sixth person outside this class, run 2026-08-03 before P1 — §4. Recording verified distinct from all five counted sessions (0 % frame overlap). Its data enters no metric, no SUS figure and no finding. |
| **Phase 2** — "testing the product, not you" + think-aloud framing | Met | `design/Moderator_Runsheet.md` §5, spoken verbatim each session |
| Observe neutrally, no leading hints | Met | Do-not-say list, same file |
| **Record the screen (and audio, with consent)** | Met | Five distinct recordings, `reports/evidence_task2/Session_P1..P5.mp4`; verified 0 % frame overlap between every pair |
| **Structured notes** on friction, errors, hesitations, verbalised frustration | **Partly met** | What exists is each participant's own written account of those things (`results/session_notes/`), not a moderator's structured log taken during the session. Honest label: participant-reported, not observer-recorded. |
| Close each session with the scale, then the probes | Met | §1; SUS administered before the probes, deliberately |
| **Phase 3** — score the scale across the five | Met | §7, all five individual scores plus mean, SD and range |
| Tabulate task metrics (success rate, mean time, errors) | **Partly met** | Success rate and errors are tabulated per participant and in aggregate (§6). Mean time is the one cell that stays empty. |
| Group similar pain points; separate isolated bugs from systemic design issues | Met | §9 groups by cause; §10 holds what did **not** meet the systemic bar and says why |
| Rank findings by severity **0–4** | Met | §9, Nielsen scale, two at 3 and two at 2 |
| Report: scenario · participant table · metrics table · ranked findings · recommendations | Met | §3 · §5 · §6–§7 · §9 · §11 |
| **A screenshot per ranked finding** | **Partly met** | D-025 and D-026 carry a still cut from the recording of the participant who hit them. D-024 is about movement across pages and D-027 about a toast that has already vanished — neither is a single frame; both cite the recordings instead, and each says so in its own row rather than pointing at an unrelated image. |
| Log genuine findings through the §7 channel | Met | D-024…D-027 are in `docs/05_Bug_Usability_Findings_Log.md` and were **submitted to the Google Form on 2026-08-03**, alongside D-023 — log and form both stand at 24. See §13 |

**One requirement cannot be closed retroactively: time on task.** It needed a clock running *during*
the sessions; the recordings are 18.8–26.0 s excerpts, so no duration can be recovered from them, and
supplying one afterwards would be inventing data — which §12 makes grounds for voiding the whole task.
It is reported as unmet rather than filled in.

The other two once-open items did close, and both closed on evidence rather than on assertion. The
**error and hesitation counts were recoverable** from what each participant wrote about their own
session, with the sentence behind every one of the seven error episodes printed in
`docs/usability_testing/results/Metrics_Table.md`. The **pilot** is evidenced by a sixth recording,
`Session_Pilot01.mp4`, checked frame-by-frame against all five counted sessions before it was relied
on — 0 % overlap — because a claimed session that turns out to be a copy of another is worse than no
pilot at all. The pilot's own durations are attributed to the moderator and left out of every
calculation, for the same reason time on task is left blank.

## 12. Limitations

- **n = 5** supports discovery, not measurement. Five was set by the brief, not chosen from a
  cost–benefit curve; no percentage, confidence interval or significance claim is made anywhere in
  this report.
- **Scope is narrower than Task 1B.** Participants exercise D1 and D2 (and D5 only if they went
  there themselves). **D3/D4 are driven by the moderator**, because a usability participant cannot
  be handed an admin account — so the admin side has checklist coverage (Task 1B) but no
  user-testing coverage.
- **Single environment.** One browser, one device class, one network, per §1 — cross-platform
  behaviour is Task 3's evidence (`docs/04_Task3_Cross_Platform_Matrix.md`), not this report's.
- **Recruiting bias.** Participants came from the moderator's own network (see
  `docs/usability_testing/design/Recruiting_Kit.md` §2), which skews younger and more digitally literate
  than the full EMS population; findability results are therefore, if anything, optimistic.
- **The moderator is also the report's author**, so the observation and the analysis are not
  independent. Mitigated by fixing the success criteria and the probe wording before the first
  session, not after seeing the data.
- **Known defects were present during the sessions** (`docs/usability_testing/design/Moderator_Runsheet.md`
  §4). Where one caused a task failure, the failure is the product's and is recorded as such — but
  it also means task times are not a clean measure of the intended design.
- **The pilot ran, but half of what it recommended was not implemented.** Pilot-01 (§4) correctly
  identified that the clock convention and the observation log had to be fixed before P1. Items 1–3
  and 5 of its adjustment list were then not carried through, which is the direct cause of the two
  weakest cells in §6: no time on task, and error/hesitation counts that are participant-reported
  instead of observer-recorded. The value a pilot is supposed to add was identified and then partly
  discarded.
- **The pilot's own numbers are moderator-reported and uncorroborated.** Its recording is a 35-second
  excerpt. Nothing in this report is computed from them, so the exposure is contained to §4.
- **Time on task was not measured.** No clock was run, and the recordings are 18.8–26.0 s excerpts, so
  no duration can be recovered from them. It is the one item in §6's minimum measure set this study
  does not carry; task success, errors, SUS and the probes are complete for all five. The ordinal
  perceived-effort rank in §6 supports the same analysis but is not the measure.
- **Error and hesitation counts are participant-reported, so they are a floor, not a total.** Seven
  error episodes and seven hesitations are counted, each from a sentence the participant wrote about
  their own session. An error made without noticing it cannot appear. A moderator's observation log —
  which is what §6 assumes — would return the same figure or a higher one, never lower, so any
  conclusion drawn from these counts understates the friction rather than overstating it.
- **Task outcomes are self-reported, not moderator-observed.** They are reconstructed from what each
  participant wrote, sentence by sentence, in `docs/usability_testing/results/Metrics_Table.md`. The
  five recordings in `reports/evidence_task2/` can confirm them and have not yet been reviewed for
  that purpose.
- **All five sessions ran on one day (2026-08-03)**, so no fix could be trialled between sessions and
  every participant met the same build.

## 13. Handoff — findings channel (§7) and evidence

Every genuine defect and every usability improvement from these sessions is logged in
`docs/05_Bug_Usability_Findings_Log.md` from **D-024 onwards** (D-001…D-023 are taken — D-020…D-022
came from Task 3, and **D-023 was allocated by Task 1B on 2026-08-02**, after this section was first
written; D-013, D-014 and D-018 are retired and must not be reused), typed `Bug` or
`Usability` with the 0–4 severity, and
**each one also submitted to the Google Form** named in §7 of the brief. The log and the form must
agree — the TA may cross-check the counts.

| Finding # (§9) | Findings-log ID | Severity | Submitted to the form |
| --- | --- | --- | --- |
| F1 | **D-024** | Usability 3 | 2026-08-03 |
| F2 | **D-025** | Usability 3 | 2026-08-03 |
| F3 | **D-026** | Usability 2 | 2026-08-03 |
| F4 | **D-027** | Usability 2 | 2026-08-03 |

All four were submitted on 2026-08-03, together with D-023 from Task 1B. **The log and the form now
agree at 24 each** — §7 asks the two to match, and the TA may cross-check the counts.

**Evidence index.** Session recordings and screenshots are in `reports/evidence_task2/`, named
`P<n>_<task>_<what-it-shows>.<ext>` per `docs/usability_testing/design/Moderator_Runsheet.md` §7. Raw
session notes are in `docs/usability_testing/results/session_notes/`; raw SUS answers in
`docs/usability_testing/results/SUS_Responses.csv`.

AI assistance on this report (study design, scoring, clustering, drafting) is declared in
`docs/06_AI_Audit_Report.md`, which states explicitly that **the sessions, the participants and the
session data were not AI-produced**.
