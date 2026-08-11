# HW04 report index

Start with the [main report](../docs/01_Main_Report.md), then use the folders below
for evidence.

## Quick access

| Feature | Chromium | Firefox | WebKit |
|---|---|---|---|
| FR-01 | [Open](final/html/fr01/chromium/index.html) | [Open](final/html/fr01/firefox/index.html) | [Open](final/html/fr01/webkit/index.html) |
| FR-11 | [Open](final/html/fr11/chromium/index.html) | [Open](final/html/fr11/firefox/index.html) | [Open](final/html/fr11/webkit/index.html) |
| FR-13 | [Open](final/html/fr13/chromium/index.html) | [TC](final/html/fr13/firefox/tc/index.html) · [BVA](final/html/fr13/firefox/bva/index.html) · [API](final/html/fr13/firefox/api/index.html) | [TC](final/html/fr13/webkit/tc/index.html) · [BVA](final/html/fr13/webkit/bva/index.html) · [API](final/html/fr13/webkit/api/index.html) |

## Final results

- `final/html/` — final Playwright reports arranged by feature and browser.
- `final/json/` — machine-readable results for the final runs.
- `final/summaries/` — compact execution summaries.

FR-01 and FR-11 each contain one report per browser. The historical FR-13 Firefox
and WebKit executions were produced in three complete case groups (`tc`, `bva`, and
`api`), so those browser folders contain three report entry points.

## Supporting evidence

- `evidence/failure-screenshots/fr01/` — FR-01 assertion evidence.
- `evidence/failure-screenshots/fr11/` — FR-11 assertion evidence.
- `evidence/github-issues/fr01/` — screenshots of filed FR-01 GitHub Issues.
- `evidence/github-issues/fr11/` — 16 screenshots of GitHub Issues #18–#33.
- `evidence/github-issues/fr13/` — 6 screenshots of GitHub Issues #14, #15, #34, #36–#38.

## History

- `history/archived-runs/` — preserved earlier and merged runs cited by the reports.
- `history/raw-artifacts/` — unpacked Playwright traces, videos, and screenshots.
- `history/fr13-partial-runs/` — earlier FR-13 wave and continuation runs.
- `history/general-runs/` — project-wide runs not used as final per-browser evidence.

Files under `history/` support auditability but are not the first files a marker needs
to inspect. Generated HTML and JSON evidence must not be edited manually.
