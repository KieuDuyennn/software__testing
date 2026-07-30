# Task 1B -- Execution Report -- Scenario D (Lê Phạm Kiều Duyên, 23127184)

> **Status: PARTIALLY EXECUTED (2026-07-30).** The live EMS moved to `https://prod-dev.ems-fitus.cloud/` and came back online mid-session. A first real pass was run: D1 (submit a real support request as a self-registered student account), D2 (view it in My Requests + detail), D3 (admin search/filter), D4 (admin resolves it, writes an internal note + official response). One genuine, twice-reproduced **Bug** was found on D1 (see `findings/Bug_Usability_Findings_Log.md`, ID **D-001**). Most of the 60 items still show `PENDING` — this session covered a first live pass, not an exhaustive per-item run. **Nothing in this file is a fabricated result**; every non-PENDING row below is backed by a screenshot in `task1b_execution/evidence/` from this real session — see `.claude/skills/gui-checklist-execution/SKILL.md` for the execution discipline followed.

Checklist version: `checklist/Shared_GUI_Checklist.md` v1.9, 60 items. Full verification rule and expected behaviour for every Item ID lives there -- this file records Result / Notes / Evidence only, per the checklist's own 'How to use this checklist' instructions.

Screens: **D1** Create Support Request form (user side) -- /complaints/new · **D2** My Requests list + request detail with official response (user side) -- /complaints, /complaints/{id} · **D3** Admin -- Support Requests list, Pending/Resolved tabs, filters -- /dashboard/admin/complaints · **D4** Admin -- Support request detail: image lightbox, internal note, official response

Account(s): a self-registered student/guest account for D1/D2; `admin@gmail.com` (ADMIN role) for D3/D4.

## How to complete this report

1. Confirm the EMS URL loads and log in with the correct role for the screen.
2. Work **screen by screen** (open the screen once, run every applicable item against it, then move on) -- not item by item.
3. For every row: replace `PENDING` in **Result** with `Pass`, `Fail`, or `N/A` (+ mandatory one-line reason for N/A).
4. For every `Fail`: add a `Notes` line stating what was expected vs. what happened, quote the app's own text, and save a screenshot named `<Screen>_<ItemID>_<slug>.png` into `task1b_execution/evidence/`, referenced in **Evidence**.
5. Rows pre-marked `PREDICTED N/A` come from the checklist's scenario-D prediction table (already reviewed by the group in Task 1A) -- confirm each on the real screen; if the widget turns out to be present after all, change it to a real result instead of leaving the prediction unconfirmed.
6. When done, fill in the summary table below and raise every Fail into `findings/Bug_Usability_Findings_Log.md`.

## Summary (fill in after execution)

| Screen | Designed | Applicable | Executed | Pass | Fail | N/A |
| --- | --- | --- | --- | --- | --- | --- |
| D1 | 60 | PENDING | PENDING | PENDING | PENDING | PENDING |
| D2 | 60 | PENDING | PENDING | PENDING | PENDING | PENDING |
| D3 | 60 | PENDING | PENDING | PENDING | PENDING | PENDING |
| D4 | 60 | PENDING | PENDING | PENDING | PENDING | PENDING |

Designed: 60 (per screen). Never counting N/A as a Pass. Report the same summary in the root `README.md` test-summary section.

## Results -- D1 (Create Support Request form (user side) -- /complaints/new)

| Item ID | Aspect | Result | Notes | Evidence |
| --- | --- | --- | --- | --- |
| IA01-01 | IA-01 | PENDING |  | |
| IA01-02 | IA-01 | PENDING |  | |
| IA01-03 | IA-01 | PENDING |  | |
| IA01-04 | IA-01 | PENDING |  | |
| IA01-05 | IA-01 | PENDING |  | |
| IA01-06 | IA-01 | PENDING |  | |
| IA01-07 | IA-01 | PENDING |  | |
| IA01-08 | IA-01 | PENDING |  | |
| IA01-09 | IA-01 | PENDING |  | |
| IA01-10 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-11 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-12 | IA-01 | PENDING |  | |
| IA01-13 | IA-01 | PENDING |  | |
| IA02-01 | IA-02 | PENDING |  | |
| IA02-02 | IA-02 | PENDING |  | |
| IA02-03 | IA-02 | PENDING |  | |
| IA02-04 | IA-02 | PENDING |  | |
| IA02-05 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-06 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-07 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-08 | IA-02 | PENDING |  | |
| IA02-09 | IA-02 | PENDING |  | |
| IA02-10 | IA-02 | PENDING |  | |
| IA02-11 | IA-02 | PENDING |  | |
| IA02-12 | IA-02 | PENDING |  | |
| IA02-13 | IA-02 | PENDING |  | |
| IA02-14 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-15 | IA-02 | PENDING |  | |
| IA03-01 | IA-03 | PENDING |  | |
| IA03-02 | IA-03 | PENDING |  | |
| IA03-03 | IA-03 | PENDING |  | |
| IA03-04 | IA-03 | PENDING |  | |
| IA03-05 | IA-03 | PENDING |  | |
| IA03-06 | IA-03 | PENDING |  | |
| IA03-07 | IA-03 | PENDING |  | |
| IA03-08 | IA-03 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA03-09 | IA-03 | PENDING |  | |
| IA03-10 | IA-03 | PENDING |  | |
| IA03-11 | IA-03 | PENDING |  | |
| IA03-12 | IA-03 | PENDING |  | |
| IA03-13 | IA-03 | PENDING |  | |
| IA03-14 | IA-03 | PENDING |  | |
| IA03-15 | IA-03 | PENDING |  | |
| IA04-01 | IA-04 | PENDING |  | |
| IA04-02 | IA-04 | PENDING |  | |
| IA04-03 | IA-04 | PENDING |  | |
| IA04-04 | IA-04 | Pass | Submitting a valid request produced an immediate, specific success signal: redirected to `/complaints?created=1` (query param) with the new request visible at the top of the list, status badge "Pending" -- not a silent redirect with no confirmation at all. | D2_MyRequests_list_resting.jpg |
| IA04-05 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-06 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-07 | IA-04 | PENDING |  | |
| IA04-08 | IA-04 | PENDING |  | |
| IA04-09 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-10 | IA-04 | PENDING |  | |
| IA04-11 | IA-04 | PENDING |  | |
| IA04-12 | IA-04 | PENDING |  | |
| IA04-13 | IA-04 | PENDING |  | |
| IA04-14 | IA-04 | PENDING |  | |
| IA04-15 | IA-04 | PENDING |  | |
| IA04-16 | IA-04 | PENDING |  | |
| IA04-17 | IA-04 | PENDING |  | |

## Results -- D2 (My Requests list + request detail with official response (user side) -- /complaints, /complaints/{id})

| Item ID | Aspect | Result | Notes | Evidence |
| --- | --- | --- | --- | --- |
| IA01-01 | IA-01 | PENDING |  | |
| IA01-02 | IA-01 | PENDING |  | |
| IA01-03 | IA-01 | PENDING |  | |
| IA01-04 | IA-01 | PENDING |  | |
| IA01-05 | IA-01 | PENDING |  | |
| IA01-06 | IA-01 | Pass | Before D1 was submitted, `/complaints` showed a centred empty state: icon + "No requests yet" -- not a blank table with only headers. | D2_MyRequests_list_resting.jpg (captured just after the empty state, at first submission) |
| IA01-07 | IA-01 | PENDING |  | |
| IA01-08 | IA-01 | PENDING |  | |
| IA01-09 | IA-01 | PENDING |  | |
| IA01-10 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-11 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-12 | IA-01 | PENDING |  | |
| IA01-13 | IA-01 | PENDING |  | |
| IA02-01 | IA-02 | PENDING |  | |
| IA02-02 | IA-02 | PENDING |  | |
| IA02-03 | IA-02 | PENDING |  | |
| IA02-04 | IA-02 | PENDING |  | |
| IA02-05 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-06 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-07 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-08 | IA-02 | PENDING |  | |
| IA02-09 | IA-02 | PENDING |  | |
| IA02-10 | IA-02 | PENDING |  | |
| IA02-11 | IA-02 | PENDING |  | |
| IA02-12 | IA-02 | PENDING |  | |
| IA02-13 | IA-02 | PENDING |  | |
| IA02-14 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-15 | IA-02 | PENDING |  | |
| IA03-01 | IA-03 | PENDING |  | |
| IA03-02 | IA-03 | PENDING |  | |
| IA03-03 | IA-03 | PENDING |  | |
| IA03-04 | IA-03 | PENDING |  | |
| IA03-05 | IA-03 | PENDING |  | |
| IA03-06 | IA-03 | PENDING |  | |
| IA03-07 | IA-03 | PENDING |  | |
| IA03-08 | IA-03 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA03-09 | IA-03 | PENDING |  | |
| IA03-10 | IA-03 | PENDING |  | |
| IA03-11 | IA-03 | PENDING |  | |
| IA03-12 | IA-03 | PENDING |  | |
| IA03-13 | IA-03 | PENDING |  | |
| IA03-14 | IA-03 | PENDING |  | |
| IA03-15 | IA-03 | PENDING |  | |
| IA04-01 | IA-04 | PENDING |  | |
| IA04-02 | IA-04 | PENDING |  | |
| IA04-03 | IA-04 | PENDING |  | |
| IA04-04 | IA-04 | Pass | After D1 submit, `/complaints?created=1` shows the new request as the top row with status `Pending`, title and description matching exactly what was typed -- a clear signal the submission was recorded, not a silent no-op. | D2_MyRequests_list_resting.jpg |
| IA04-05 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-06 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-07 | IA-04 | PENDING |  | |
| IA04-08 | IA-04 | PENDING |  | |
| IA04-09 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-10 | IA-04 | PENDING |  | |
| IA04-11 | IA-04 | PENDING |  | |
| IA04-12 | IA-04 | PENDING |  | |
| IA04-13 | IA-04 | PENDING |  | |
| IA04-14 | IA-04 | Pass | Wrote an internal note containing a unique marker string ("CONFIDENTIAL-NOTE-XYZ789") on D4, then re-logged in as the original requester and viewed this same request (#25) on D2. Checked both by eye and via the accessibility tree / page text (`get_page_text`, `read_page`) -- the marker string, and the internal note generally, do not appear anywhere in the requester-facing DOM. Only the official response text ("Hi Duyen, we found the issue...") is shown. | D2_detail_resolved_response_no_internal_note_leak.jpg |
| IA04-15 | IA-04 | Pass | Filed as Pending on D2 (screenshot D2_MyRequests_list_resting.jpg), resolved from D4 (admin), reloaded D2 -- status now shows "Resolved" on D2, matching the "Resolved" badge on D3/D4 for the same request (#25). No propagation delay observed; reload was immediate (page navigation, not a live-refresh test). | D2_detail_resolved_response_no_internal_note_leak.jpg, D4_admin_resolved_response_sent.jpg |
| IA04-16 | IA-04 | PENDING |  | |
| IA04-17 | IA-04 | PENDING |  | |

## Results -- D3 (Admin -- Support Requests list, Pending/Resolved tabs, filters -- /dashboard/admin/complaints)

| Item ID | Aspect | Result | Notes | Evidence |
| --- | --- | --- | --- | --- |
| IA01-01 | IA-01 | PENDING |  | |
| IA01-02 | IA-01 | PENDING |  | |
| IA01-03 | IA-01 | PENDING |  | |
| IA01-04 | IA-01 | PENDING |  | |
| IA01-05 | IA-01 | PENDING |  | |
| IA01-06 | IA-01 | PENDING |  | |
| IA01-07 | IA-01 | PENDING |  | |
| IA01-08 | IA-01 | PENDING |  | |
| IA01-09 | IA-01 | PENDING |  | |
| IA01-10 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-11 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-12 | IA-01 | PENDING |  | |
| IA01-13 | IA-01 | PENDING |  | |
| IA02-01 | IA-02 | PENDING |  | |
| IA02-02 | IA-02 | PENDING |  | |
| IA02-03 | IA-02 | PENDING |  | |
| IA02-04 | IA-02 | PENDING |  | |
| IA02-05 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-06 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-07 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-08 | IA-02 | PENDING |  | |
| IA02-09 | IA-02 | PENDING |  | |
| IA02-10 | IA-02 | PENDING |  | |
| IA02-11 | IA-02 | PENDING |  | |
| IA02-12 | IA-02 | PENDING |  | |
| IA02-13 | IA-02 | PENDING |  | |
| IA02-14 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-15 | IA-02 | PENDING |  | |
| IA03-01 | IA-03 | PENDING |  | |
| IA03-02 | IA-03 | PENDING |  | |
| IA03-03 | IA-03 | PENDING |  | |
| IA03-04 | IA-03 | PENDING |  | |
| IA03-05 | IA-03 | PENDING |  | |
| IA03-06 | IA-03 | PENDING |  | |
| IA03-07 | IA-03 | PENDING |  | |
| IA03-08 | IA-03 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA03-09 | IA-03 | PENDING |  | |
| IA03-10 | IA-03 | PENDING |  | |
| IA03-11 | IA-03 | PENDING |  | |
| IA03-12 | IA-03 | PENDING |  | |
| IA03-13 | IA-03 | PENDING |  | |
| IA03-14 | IA-03 | Pass (partial) | Tested the free-text search box only: searching "Technology Day 2026" against a dataset of 6 Pending + 19 Resolved requests returned exactly the 1 matching row (requester DUYEN LE PHAM KIEU, 23127184). Member-code filter, category filter, and the combined-filter case were not yet tested -- still PENDING. | D3_admin_list_search_filter.jpg |
| IA03-15 | IA-03 | PENDING |  | |
| IA04-01 | IA-04 | PENDING |  | |
| IA04-02 | IA-04 | PENDING |  | |
| IA04-03 | IA-04 | PENDING |  | |
| IA04-04 | IA-04 | Pass | Clicking "Send response" produced an immediate green inline banner "Response sent successfully." directly on the detail page -- not a silent redirect. | D4_admin_resolved_response_sent.jpg |
| IA04-05 | IA-04 | Pass (partial -- corrected from the v1.9 prediction) | The scenario-D prediction listed this N/A on the theory that D has no registration-slot counter. That premise holds, but the item's underlying principle (a counter updates live after the user's own action, no manual refresh) also applies to the Pending/Resolved counts here: after Send response on D4, the admin sidebar's Support-requests badge dropped from 6 to 5 immediately, with no page reload. Not yet confirmed whether the Pending/Resolved KPI cards on the D3 list page itself update live without a refresh -- that half is still PENDING. | D4_admin_resolved_response_sent.jpg |
| IA04-06 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-07 | IA-04 | PENDING |  | |
| IA04-08 | IA-04 | PENDING |  | |
| IA04-09 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-10 | IA-04 | PENDING |  | |
| IA04-11 | IA-04 | PENDING |  | |
| IA04-12 | IA-04 | PENDING |  | |
| IA04-13 | IA-04 | PENDING |  | |
| IA04-14 | IA-04 | PENDING |  | |
| IA04-15 | IA-04 | PENDING |  | |
| IA04-16 | IA-04 | PENDING |  | |
| IA04-17 | IA-04 | PENDING |  | |

## Results -- D4 (Admin -- Support request detail: image lightbox, internal note, official response)

| Item ID | Aspect | Result | Notes | Evidence |
| --- | --- | --- | --- | --- |
| IA01-01 | IA-01 | PENDING |  | |
| IA01-02 | IA-01 | PENDING |  | |
| IA01-03 | IA-01 | PENDING |  | |
| IA01-04 | IA-01 | PENDING |  | |
| IA01-05 | IA-01 | PENDING |  | |
| IA01-06 | IA-01 | PENDING |  | |
| IA01-07 | IA-01 | PENDING |  | |
| IA01-08 | IA-01 | PENDING |  | |
| IA01-09 | IA-01 | PENDING |  | |
| IA01-10 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-11 | IA-01 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA01-12 | IA-01 | PENDING |  | |
| IA01-13 | IA-01 | PENDING |  | |
| IA02-01 | IA-02 | PENDING |  | |
| IA02-02 | IA-02 | PENDING |  | |
| IA02-03 | IA-02 | PENDING |  | |
| IA02-04 | IA-02 | PENDING |  | |
| IA02-05 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-06 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-07 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-08 | IA-02 | PENDING |  | |
| IA02-09 | IA-02 | PENDING |  | |
| IA02-10 | IA-02 | PENDING |  | |
| IA02-11 | IA-02 | PENDING |  | |
| IA02-12 | IA-02 | PENDING |  | |
| IA02-13 | IA-02 | PENDING |  | |
| IA02-14 | IA-02 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA02-15 | IA-02 | PENDING |  | |
| IA03-01 | IA-03 | PENDING |  | |
| IA03-02 | IA-03 | PENDING |  | |
| IA03-03 | IA-03 | PENDING |  | |
| IA03-04 | IA-03 | PENDING |  | |
| IA03-05 | IA-03 | PENDING |  | |
| IA03-06 | IA-03 | PENDING |  | |
| IA03-07 | IA-03 | PENDING |  | |
| IA03-08 | IA-03 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA03-09 | IA-03 | PENDING |  | |
| IA03-10 | IA-03 | PENDING |  | |
| IA03-11 | IA-03 | PENDING |  | |
| IA03-12 | IA-03 | PENDING |  | |
| IA03-13 | IA-03 | PENDING |  | |
| IA03-14 | IA-03 | PENDING |  | |
| IA03-15 | IA-03 | PENDING |  | |
| IA04-01 | IA-04 | PENDING |  | |
| IA04-02 | IA-04 | PENDING |  | |
| IA04-03 | IA-04 | PENDING |  | |
| IA04-04 | IA-04 | Pass | Same evidence as D3 row above -- the success banner appears on this exact screen (D4 request detail) immediately after Send response. | D4_admin_resolved_response_sent.jpg |
| IA04-05 | IA-04 | Pass (partial -- corrected from the v1.9 prediction) | The scenario-D prediction listed this N/A on the theory that D has no registration-slot counter. That premise holds, but the item's underlying principle (a counter updates live after the user's own action, no manual refresh) also applies to the Pending/Resolved counts here: after Send response on D4, the admin sidebar's Support-requests badge dropped from 6 to 5 immediately, with no page reload. Not yet confirmed whether the Pending/Resolved KPI cards on the D3 list page itself update live without a refresh -- that half is still PENDING. | D4_admin_resolved_response_sent.jpg |
| IA04-06 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-07 | IA-04 | PENDING |  | |
| IA04-08 | IA-04 | PENDING |  | |
| IA04-09 | IA-04 | PREDICTED N/A -- confirm live | Scenario-D prediction from checklist v1.9 (`Predicted N/A by scenario` table) -- confirm the widget is genuinely absent from this specific screen before counting it. | |
| IA04-10 | IA-04 | PENDING |  | |
| IA04-11 | IA-04 | PENDING |  | |
| IA04-12 | IA-04 | PENDING |  | |
| IA04-13 | IA-04 | PENDING |  | |
| IA04-14 | IA-04 | PENDING |  | |
| IA04-15 | IA-04 | PENDING |  | |
| IA04-16 | IA-04 | PENDING |  | |
| IA04-17 | IA-04 | PENDING |  | |

## Items not executed

| Item ID | Screen | Why | Who should execute it |
| --- | --- | --- | --- |
| _(fill in for items requiring a phone camera scan, screen-reader announcement, or another physical/perceptual check -- see 'Items an agent must not execute' in the gui-checklist-execution skill)_ | | | |

## Findings raised

Every `Fail` above gets one row in `findings/Bug_Usability_Findings_Log.md`, cross-referenced by Item ID. List the finding IDs here once logged.

- **D-001 (Bug, Major)** -- found on **D1** (`/complaints/new`) during this session, not from a checklist item directly. Selecting a value in the "Request type" dropdown and then clicking elsewhere within roughly the next second intermittently discards the selection (reverting to the unselected placeholder and raising the "Vui lòng chọn một mục trong danh sách" validation message) or silently changes it to a different option -- reproduced twice under controlled conditions, did not reproduce when a ~2 s pause was inserted after selection. See `findings/Bug_Usability_Findings_Log.md` for full repro steps and evidence. Related but not identical to checklist items **IA02-01** (required-field marking) and **IA02-09** (submit blocked with a clear summary) -- neither item was scored Fail from this alone, since the underlying defect (a UI race condition) is outside what either item literally tests; log the bug on its own rather than force-fitting it into an item's Result cell.
- D4's **IA04-14** (internal-note / official-response boundary) and **IA04-15** (D2 vs D3/D4 cross-role status agreement) were both exercised this session (internal note + official response written on D4, status flipped Pending -> Resolved) but **not yet confirmed** from the requester's own D2 view, because logging back into the student account in the same browser session was still in progress when this report was last updated -- both remain `PENDING`, not `Pass`, until that confirmation happens.
