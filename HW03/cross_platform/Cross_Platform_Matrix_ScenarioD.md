# Task 3 — Cross-Browser / Cross-Platform Matrix — Scenario D — Lê Phạm Kiều Duyên, 23127184

> **Status: NOT YET RUN.** No BrowserStack / LambdaTest trial has been used yet and no cells have
> been captured. This file is the coverage-floor template — fill in real cells only after real
> cloud-lab or real-device sessions. See `.claude/skills/cross-platform-matrix/SKILL.md` for the
> full method (engine-first cell selection, emulator/simulator/real-device distinction, evidence
> discipline).

Screens: **D1** (Create Support Request, user) · **D2** (My Requests + detail, user) · **D3**
(Admin Support Requests list) · **D4** (Admin request detail).
Tooling: BrowserStack or LambdaTest trial (preferred) — record which, and the account used.
Coverage floor required (§6 Task 3), **per screen**: every OS at least once, every browser at
least once, every device class at least once. Not the full 3×5×3 cross-product.

## Required coverage values

- **OS (≥ 3):** Windows · macOS · Android **or** iOS
- **Browsers (≥ 5):** Chrome · Firefox · Safari · Edge · Opera (or Samsung Internet on mobile)
- **Device classes (3):** desktop · tablet · phone

## Engine reminder (do not fill the matrix with one engine wearing five brand names)

| Engine | Browsers in this matrix |
| --- | --- |
| Blink | Chrome, Edge, Opera, Samsung Internet |
| Gecko | Firefox |
| WebKit | Safari (and, by default, every iOS browser regardless of brand, unless the row states an EU/UK BrowserEngineKit exception) |

Force at least one Gecko and one WebKit cell. Note the engine per row.

## Screenshot requirements (§6 Task 3, mandatory)

Every screenshot must show, in the image itself:

1. the EMS URL,
2. the browser / OS / device identity (the lab's own banner, or an about page beside the app),
3. **your student-ID email overlay in the form `MSSV@....edu.vn`** — burn this into the image
   (annotation tool, lab's own overlay feature, or a visible watermark) — this is a hard anti-cheat
   requirement, not optional,
4. the screen in the state being claimed.

Name files: `<Screen>_<OS>_<Browser>_<Device>.png`, saved under `cross_platform/evidence/`.

## Environment kind — record which, per cell

| Kind | What it proves | What it does not prove |
| --- | --- | --- |
| Responsive mode (DevTools) | Layout at a resized viewport, one engine | Nothing engine- or OS-specific |
| Emulator (Android) | Real OS image, virtualised GPU | Real font rendering, real performance |
| Simulator (iOS) | Mac-native reimplementation | Real WebKit build quirks |
| Real device (own or cloud lab) | The actual thing | — |

## Matrix

| # | Screen | OS | Browser | Engine | Device class | Environment | Result | Evidence | Note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | D1 | Windows 11 | Chrome | Blink | desktop | TBD | TBD | | |
| 2 | D1 | macOS | Safari | WebKit | desktop | TBD | TBD | | |
| 3 | D1 | Android | Chrome | Blink | phone | TBD | TBD | | |
| 4 | D2 | Windows 11 | Firefox | Gecko | desktop | TBD | TBD | | |
| 5 | D2 | iOS | Safari | WebKit | phone | TBD | TBD | | |
| 6 | D2 | Windows 11 | Edge | Blink | tablet | TBD | TBD | | |
| 7 | D3 | macOS | Safari | WebKit | desktop | TBD | TBD | | |
| 8 | D3 | Windows 11 | Opera | Blink | desktop | TBD | TBD | | |
| 9 | D3 | Android | Chrome | Blink | tablet | TBD | TBD | | |
| 10 | D4 | Windows 11 | Firefox | Gecko | desktop | TBD | TBD | | |
| 11 | D4 | iOS / Android | Safari / Chrome | WebKit / Blink | phone | TBD | TBD | | |
| 12 | D4 | macOS | Chrome | Blink | desktop | TBD | TBD | | |

**Row plan rationale (covering array, not full cross-product):** 12 cells across 4 screens gives
each screen at least 3 cells, and across the whole matrix every required OS, every required
browser, and every required device class appears at least once **per screen** as required — adjust
concrete rows once real lab availability is known (a trial may not offer every OS/browser/device
combination listed above).

## Coverage achieved (fill in after running)

| Screen | OS covered | Browsers covered | Device classes covered | Engines covered | Missing |
| --- | --- | --- | --- | --- | --- |
| D1 | | | | | |
| D2 | | | | | |
| D3 | | | | | |
| D4 | | | | | |

Verify with:
```bash
python .claude/skills/cross-platform-matrix/scripts/matrix_coverage.py cross_platform/Cross_Platform_Matrix_ScenarioD.md \
  --os "Windows,macOS,Android,iOS" \
  --browsers "Chrome,Firefox,Safari,Edge,Opera" \
  --devices "desktop,tablet,phone" \
  --evidence-root cross_platform/evidence/
```

## Failures (grouped by classification)

Use the fixed vocabulary: `overflow` · `overlap` · `clipping` · `unreadable` ·
`unresponsive-control` · `missing-asset` · `feature-unsupported` · `broken-layout`.
Reproduce any Fail once (ideally a fresh session) before logging it, and cross-check the image
itself — cloud labs can serve a stale screenshot mid-load. _(None recorded yet.)_

## Platform differences observed (not defects)

Record legitimate platform behaviour here so a reviewer sees it was considered, not missed — e.g.
a native `From date`/`To date` input on the Support Requests filter panel (D3) rendering in the
browser's own locale format is expected, not a bug (see `checklist/Shared_GUI_Checklist.md` IA02-11).
_(None recorded yet.)_
