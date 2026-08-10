# FR13 bug report (issue filing deferred)

This is the internal FR13 defect assessment. Demo recording and GitHub issue filing are
intentionally deferred.

The 50-case Chromium run produced 29 passes and 21 failed assertions. The failures group
into six distinct root-cause defects:

| ID | Reproductions | Severity | Actual behaviour |
|---|---|---|---|
| BUG-FR13-01 | TC-02, BVA cases, TC-13b, TC-21 | Major | Delivered revenue is multiplied by two. |
| BUG-FR13-02 | TC-13 | Major | `canceled → delivered` returns HTTP 200 and mutates the order. |
| BUG-FR13-03 | TC-11, API-14–17 | Critical | Checkout trusts malformed client `total_amount` values and creates orders. |
| BUG-FR13-04 | TC-04b, API-03/04/06/09 | Critical | Admin endpoints authenticate a token but do not enforce its admin role. |
| BUG-FR13-05 | API-10 | Critical | A signed admin token for a nonexistent user reads global orders. |
| BUG-FR13-06 | TC-19 | Critical | A normal user can promote their own profile to `admin`. |

Evidence: [full Chromium JSON](../../reports/final/json/fr13-chromium.json), [failure grouping](FR13_Failure_Evidence.md),
and the browser wave reports under `reports/history/fr13-partial-runs/json/fr13-*-wave*.json`. The six IDs are
root-cause findings; the 21 failing cases remain separate regression reproductions.
