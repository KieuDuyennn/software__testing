# FR13 bug report

This is the FR13 defect assessment. The six root-cause findings have been filed as
GitHub Issues and their issue-page screenshots are preserved under
`reports/evidence/github-issues/fr13/`.

The 50-case Chromium run produced 29 passes and 21 failed assertions. The failures group
into six distinct root-cause defects:

| ID | Reproductions | Severity | Actual behaviour |
|---|---|---|---|
| BUG-FR13-01 | TC-02, BVA cases, TC-13b, TC-21 | Major | Delivered revenue is multiplied by two. Filed as [#15](https://github.com/KieuDuyennn/software__testing/issues/15). |
| BUG-FR13-02 | TC-13 | Major | `canceled → delivered` returns HTTP 200 and mutates the order. Filed as [#38](https://github.com/KieuDuyennn/software__testing/issues/38). |
| BUG-FR13-03 | TC-11, API-14–17 | Critical | Checkout trusts malformed client `total_amount` values and creates orders. Filed as [#34](https://github.com/KieuDuyennn/software__testing/issues/34). |
| BUG-FR13-04 | TC-04b, API-03/04/06/09 | Critical | Admin endpoints authenticate a token but do not enforce its admin role. Filed as [#14](https://github.com/KieuDuyennn/software__testing/issues/14). |
| BUG-FR13-05 | API-10 | Critical | A signed admin token for a nonexistent user reads global orders. Filed as [#36](https://github.com/KieuDuyennn/software__testing/issues/36). |
| BUG-FR13-06 | TC-19 | Critical | A normal user can promote their own profile to `admin`. Filed as [#37](https://github.com/KieuDuyennn/software__testing/issues/37). |

Evidence: [full Chromium JSON](../../reports/final/json/fr13-chromium.json), [failure grouping](FR13_Failure_Evidence.md),
and the browser wave reports under `reports/history/fr13-partial-runs/json/fr13-*-wave*.json`. The six IDs are
root-cause findings; the 21 failing cases remain separate regression reproductions.
