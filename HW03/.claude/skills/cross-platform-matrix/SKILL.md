---
name: cross-platform-matrix
description: Plan, execute and verify a cross-browser / cross-platform compatibility matrix — choosing OS × browser × device cells by rendering engine rather than brand, telling real devices apart from emulators, simulators and DevTools responsive mode, capturing evidence per cell, and checking the coverage floor was genuinely met. Use whenever behaviour must be compared across browsers, OSes, screen sizes or devices, whenever a device/browser matrix needs designing or auditing, whenever a defect appears on one platform but not another, and whenever a cloud device-lab result needs interpreting. Trigger on "cross-browser", "cross-platform", "compatibility matrix", "ma trận tương thích", "test trên nhiều trình duyệt", "test trên nhiều thiết bị", "BrowserStack", "LambdaTest", "broken on Safari", "lỗi trên iPhone nhưng Chrome thì không". Do NOT use for a GUI review in one browser (gui-checklist-execution) or to write responsive CSS — this verifies coverage, it does not author styles.
---

# Cross-platform matrix

The goal is coverage you can defend, not cells you can count. A matrix of ten Chromium browsers is
ten cells and roughly one test.

## Choose cells by engine, not by brand

Rendering differences come from the engine. Brands sharing an engine mostly share behaviour:

| Engine | Browsers |
| --- | --- |
| Blink | Chrome, Edge, Opera, Samsung Internet, Brave |
| Gecko | Firefox |
| WebKit | Safari — and, in most regions, every browser on iOS whatever its brand |

So a five-browser matrix of Chrome / Edge / Opera / Chrome-mobile / Samsung Internet is five brands
and one engine. **Force at least one Gecko and one WebKit cell**, and note the engine per row — that
is what makes an all-pass matrix meaningful and what makes a single Fail interpretable.

The iOS rule is the one that trips people, and it is now a default rather than a law. Historically
every iOS browser was WebKit underneath, so "Chrome on iPhone" was a Safari test wearing different
chrome. That is still what you will get almost everywhere — but Apple has permitted alternative
browser engines for EU users since iOS 17.4 (BrowserEngineKit), and the UK CMA has ruled that iOS
must open to them as well, so a genuine Blink-on-iOS cell is possible and becoming more so.

Treat it as: **on iOS, record WebKit unless the row documents otherwise**, and where it does, record
the region and the engine build alongside the browser version — because a reader cannot otherwise
tell an exceptional cell from a mislabelled one. Never let a brand name alone decide the engine.

## Design the matrix

Where a required coverage floor exists — say every OS, every browser and every device class at least
once, per screen — you do **not** need the full cross-product. Treat it as a covering array: pick
cells so that each required value appears at least once, then spend the remaining budget on the
combinations most likely to break.

Where breakage actually concentrates:

- **WebKit** — date/time inputs, `gap` in older versions, sticky positioning, `100vh` versus the
  dynamic viewport with the URL bar in play.
- **Narrow viewports** — wide tables, fixed-width containers, modals taller than the screen,
  horizontal overflow.
- **Font substitution** — a stack that resolves differently per OS changes every text metric, which
  is how "the same layout" ends up wrapping differently.
- **Touch versus pointer** — hover-only affordances (tooltips on icon-only buttons), targets under
  the 44 px guidance, drag interactions.
- **Locale-driven native controls** — a native date input renders in the browser's locale. This is
  correct behaviour, not a defect. Record it and move on.

## Say what kind of environment each cell was

These are not interchangeable and a matrix that does not distinguish them cannot be trusted:

| | What it is | What it will not tell you |
| --- | --- | --- |
| **Responsive mode** (DevTools) | One engine, resized viewport | Anything engine- or OS-specific. It is a layout check, not a compatibility cell. |
| **Emulator** (Android) | Runs the real OS image, virtualised GPU | Real font rendering, real performance, real device chrome |
| **Simulator** (iOS) | Mac-native reimplementation, not iOS | Real WebKit build quirks, real text metrics |
| **Real device** (own or cloud) | The actual thing | Nothing — but is slowest and scarcest |

Put the environment kind in its own column. If a required OS was only covered in responsive mode,
say so plainly instead of letting the cell imply a device test.

## Cloud device labs wobble

BrowserStack, LambdaTest and equivalents produce artefacts that look exactly like product defects:
stale sessions serving a previous page, screenshots captured mid-load, DPI-scaled captures that
appear blurry, device labels not matching the hardware, and tunnel latency that makes a
still-loading page look broken.

Two rules follow. **Reproduce any Fail once before logging it** — ideally in a fresh session. And
**read what the screenshot actually shows** rather than trusting the cell label: confirm the browser
and OS identity are visible in the image and match the row.

## Evidence per cell

Each capture must show, in the image itself:

- the application URL,
- the browser / OS / device identity (the lab's own banner, or an about page beside the app),
- any overlay the engagement requires,
- the screen in the state being claimed.

Verify by opening the image, not by trusting the filename. A mislabelled capture is the single
easiest thing for a reviewer to catch and the most damaging to find.

Name files predictably: `<Screen>_<OS>_<Browser>_<Device>.png`.

## Classify failures precisely

"Broken" is not actionable. Use a fixed vocabulary so failures cluster:

`overflow` (content escapes horizontally) · `overlap` (elements collide) · `clipping` (content cut
off) · `unreadable` (contrast or size at this viewport) · `unresponsive-control` (works elsewhere,
not here) · `missing-asset` (image, font, icon absent) · `feature-unsupported` (API or CSS the
engine lacks) · `broken-layout` (structural collapse).

Then separate **genuine incompatibility** from **legitimate platform difference**. Platform
differences to leave alone: native control appearance and locale format, platform scrollbars, system
font substitution, safe-area insets, the mobile URL bar changing viewport height. Log the
*inconsistency* if the app mixes native and custom controls for the same job — that is a product
decision. Do not log the platform for behaving like itself.

## Output

```markdown
# Compatibility matrix — <product>
Screens: <S1 · S2 · S3>   Dates: <range>   Tooling: <lab / real devices>
Coverage floor required: <e.g. 3 OS, 5 browsers, 3 device classes, per screen>

| # | Screen | OS | Browser | Engine | Device class | Environment | Result | Evidence | Note |
| 1 | S1 | Windows 11 | Firefox 128 | Gecko | desktop | real | Pass | S1_Win_FF_desktop.png | |
| 2 | S1 | iOS 17 | Safari | WebKit | phone | real device (cloud) | Fail | S1_iOS_Safari_phone.png | overflow: table forces 180 px horizontal scroll |

## Coverage achieved
Per screen: which OS / browsers / device classes / engines were covered, and which were not.

## Failures
Grouped by classification, with the cells affected and whether it reproduced.

## Platform differences observed (not defects)
So a reviewer sees they were considered rather than missed.
```

## Verify coverage with the script

```bash
python .claude/skills/cross-platform-matrix/scripts/matrix_coverage.py matrix.md \
  --os "Windows,macOS,Android" \
  --browsers "Chrome,Firefox,Safari,Edge,Opera" \
  --devices "desktop,tablet,phone" \
  --evidence-root screenshots/
```

It reports, per screen, which required values are still uncovered, how many engines are represented,
whether any Fail row lacks evidence, and whether any evidence file is missing from disk. Claiming
coverage in prose is exactly the claim that quietly breaks when a cell gets dropped — and it is the
first thing a reviewer recounts.

## Handing off

Each genuine incompatibility becomes a record in `findings-log`, with the cell as its reproduction
context. Log AI assistance with `ai-audit-log` — and state that the captures were produced by a
person on real environments, since a compatibility matrix is worthless if its evidence could have
been generated.
