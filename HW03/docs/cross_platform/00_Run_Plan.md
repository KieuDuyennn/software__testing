# Task 3 — Run plan (cross-browser / cross-platform matrix, Scenario D)

> **This is the operating plan, not a deliverable in itself.** It says what has to happen, in what
> order, who does it, and what "done" looks like. The graded artefact is
> `docs/04_Task3_Cross_Platform_Matrix.md`; everything below exists to fill that file with real
> cells. See `.claude/skills/cross-platform-matrix/SKILL.md` for the full method (engine-first cell
> selection, emulator/simulator/real-device distinction, evidence discipline) and
> `.claude/skills/cross-platform-matrix/scripts/matrix_coverage.py` for the verifier.

**Status: not started.** 0 of the planned cells captured, no BrowserStack/LambdaTest trial in use
yet. Task 3 is worth **25 of 100 marks** and is currently self-assessed at **0** in the README — the
same size block as Task 2, and currently the least-started of the three graded tasks.

---

## 1. Status and stakes

- Task 3 (§16 of the brief) carries **25/100** — tied with Task 2 for the single largest mark block
  in this assignment, and larger than Task 1A + Task 1B combined would be if either were still open.
- `README.md` §"Test summary" already records **0 of the planned 20-cell matrix** covered and the
  self-assessment table lists **25 → 0** for Task 3. Nothing in `reports/evidence_task3/` exists yet
  (confirmed: the folder is present but empty).
- **Documents alone cannot earn any of these 25 marks.** §16 criterion 3 grades a matrix of real
  cells; §6 requires a screenshot for every cell; §12 names fabricated cross-platform screenshots as
  a thing TAs verify. Everything in this folder and in `docs/04_Task3_Cross_Platform_Matrix.md` is
  preparation so that no decision has to be made at capture time — but until a person runs the
  sessions and produces the 20 overlaid images, Task 3 scores 0. There is no document-side substitute.
- Nothing here can be simulated or backfilled from Task 1B/Task 2 evidence. Task 1B's screenshots
  are all taken in one browser, on one OS, on one device — they establish *what the screens are*,
  not *whether they render consistently elsewhere*, which is precisely what Task 3 grades.
- §12 (Anti-AI-Cheat Constraints) names the cross-platform screenshots explicitly as something TAs
  verify: each must show the student-ID email overlay **alongside** the EMS URL and the
  browser/OS/device identity. A screenshot without that overlay does not count, and a fabricated one
  is grounds for voiding the task, not just the row.

## 2. What is already decided (do not redesign these)

| Decision | Value | Where it is written |
| --- | --- | --- |
| Screens under test | **D1–D4** — Create Support Request (user), My Requests + detail (user), Admin Support Requests list, Admin request detail | `docs/04_Task3_Cross_Platform_Matrix.md`, this file |
| Screens explicitly excluded | D5 (Notifications) and D6 (attachment lightbox) — Task 1B's extension to 6 screens does **not** carry into Task 3 | brief §6 says "your **three** functions/screens"; Task 2 similarly narrowed off Task 1B's 6-screen extension |
| Deliverable file | `docs/04_Task3_Cross_Platform_Matrix.md` — scaffolded with the coverage-floor template, the engine table, the tooling record, the pre-capture checklist and all **24 rows** marked `Not executed` | existing file |
| Evidence location | `reports/evidence_task3/` | existing empty folder |
| Coverage floor | Per screen: every OS at least once, every browser at least once, every device class at least once — **not** the full 3×5×3 cross-product | brief §6 Task 3 |
| Evidence rule | Every cell needs a screenshot; every screenshot needs the student-ID email overlay `MSSV@....edu.vn` **and** must show the EMS URL and browser/OS/device identity | brief §6, §12 |
| Findings channel | New defects append to `docs/05_Bug_Usability_Findings_Log.md` from **D-020** | brief §7; see §9 below |

**Scope note that must survive into the report:** Task 3 is scoped to **D1–D4**, matching the same
narrowing logic Task 2 applied when it dropped down to D1–D2 — a usability *session* cannot reach
the admin side, but a cross-platform *screenshot pass* can reach all four screens without a real
user, so D1–D4 (not D1–D2, and not D1–D6) is the right cut here. State this explicitly in the
matrix's own header rather than letting a reader assume it matches either sibling task's scope.

## 3. The coverage floor, stated exactly, and the minimum cell count it implies

The brief's own words (§6 Task 3): *"Your matrix does not need every one of the 3×5×3 combinations,
but it must exercise every operating system at least once, every browser at least once, and every
device class at least once, for each of the three [here: four] screens."*

Required values:

- **OS (3):** Windows, macOS, and Android **or** iOS.
- **Browsers (5):** Chrome, Firefox, Safari, Edge, Opera (or Samsung Internet on mobile).
- **Device classes (3):** desktop, tablet, phone.

### Deriving the minimum

This is a covering-array problem, not a cross-product. Each cell (row) contributes exactly one value
to each of the three dimensions (OS, browser, device class). To make every value in a dimension
appear at least once, you need **at least as many rows as the largest dimension** — you cannot cover
5 distinct browsers in fewer than 5 rows, no matter how OS and device class are packed into those
same rows. The OS (3) and device-class (3) requirements are strictly smaller, so they ride along for
free inside those same 5 rows if assigned deliberately.

**Minimum per screen = max(3 OS, 5 browsers, 3 device classes) = 5 cells.**
**This matrix runs 6 per screen, one above the floor** — see "The sixth row" below.
**Minimum total across D1–D4 = 5 × 4 = 20 cells; this matrix runs 6 × 4 = 24** (the coverage requirement is stated per screen, so
it does not shrink by testing screens together — each screen still needs its own 5 rows, even though,
per §6 below, several screens' rows can share the same physical session).

### A concrete 6-cell set: the 5-cell floor, plus one

| # | OS | Browser | Engine | Device class | Rationale |
| --- | --- | --- | --- | --- | --- |
| 1 | Windows 11 | Edge | Blink | desktop | Real local PC, zero cloud-lab cost |
| 2 | Windows 11 | Firefox | Gecko | desktop | Real local PC; the required Gecko cell |
| 3 | macOS | Safari | WebKit | desktop | Cloud lab (no physical Mac); the required WebKit cell |
| 4 | Android | Chrome | Blink | phone | Cloud lab or a real personal Android phone |
| 5 | Android | Opera | Blink | tablet | Cloud lab or a real Android tablet; fills the last device class |

Check against the floor: **OS** {Windows, macOS, Android} — all 3 ✓. **Browser** {Edge, Firefox,
Safari, Chrome, Opera} — all 5 ✓. **Device class** {desktop×3, phone, tablet} — all 3 ✓. **Engines**
{Blink, Gecko, WebKit} — all 3 represented, including the skill's mandatory "at least one Gecko and
one WebKit cell."

Apply the same 5-row template to each of D1–D4 (same OS/browser/device tuples, different screen URL
each time), **plus a sixth row — iOS 17+ · Safari · WebKit · phone, on a cloud-lab real device, not
the Xcode simulator → 24 cells total**, one above the floor on every screen.

### The sixth row, and why it is not padding

At the bare floor the matrix is literally compliant and thin: Chrome, Edge and Opera are all Blink,
so Gecko and WebKit each appear exactly once per screen and **mobile WebKit does not appear at all**.
That is the single combination most likely to break a responsive layout, and it is also where the
brief's own emulator/simulator/real-device distinction has teeth — an iOS *simulator* is a Mac-native
reimplementation, so only a real device proves anything about real WebKit. One extra cloud-lab launch
(~20 minutes) buys a fourth OS, a second WebKit environment, mobile WebKit coverage, and a
demonstrated grasp of that distinction. Note the consequence for verification: `--os` must now list
`iOS` as well, and every value listed in `--os` is treated as required. This
is deliberately not padded: rows beyond this floor should go toward the combinations most likely to
break (WebKit + narrow viewport, per the skill), not toward re-proving brands that share an engine.

### Which brand choices are engine-redundant

Of the 5 required "browsers," only **2 distinct rendering engines beyond Blink** are actually
present: **Edge** and **Opera** are Blink underneath, identical to Chrome for rendering purposes — so
3 of the 5 required brands (Chrome, Edge, Opera) are one engine wearing three names. The two cells
that matter for making an all-Pass matrix credible are **Firefox (Gecko)** and **Safari (WebKit)** —
without them, "5 browsers, all Pass" would really mean "one engine, tested five times." The proposed
set above keeps this: Edge/Opera on Windows/Android (Blink, low marginal value beyond brand-name
literalism), Firefox on Windows (Gecko), Safari on macOS (WebKit).

If the mobile OS chosen is **iOS** instead of Android, apply the skill's WebKit-by-default rule: on
iOS, Safari, Chrome-for-iOS and every other iOS browser are WebKit underneath unless the row states
an EU/UK BrowserEngineKit exception with region and engine build recorded — so an iOS Chrome cell
would need to be logged as WebKit engine, not Blink, unless that exception is documented.

## 4. Decisions the student still owes

| # | Decision | Why it blocks | Recommendation |
| --- | --- | --- | --- |
| 1 | **Cloud lab: BrowserStack or LambdaTest?** | Determines account setup, available OS/browser combinations, and whether "Live" (interactive) or "Automate" access is needed | BrowserStack Live free trial if still available on the student's account; if expired, LambdaTest's free tier (limited monthly minutes) as the brief's own named fallback |
| 2 | **If the trial has expired** — Sauce Labs, CrossBrowserTesting, or real physical devices? | The brief explicitly permits this substitution, but the screenshot rule (URL + browser/OS/device name visible) still applies regardless of tool | Prefer a personal Android phone/tablet + a friend's/family Mac for the macOS/mobile cells over a second unfamiliar cloud tool — fewer new accounts to fight with under time pressure |
| 3 | **Real device vs emulator/simulator for the mobile cells** | The skill and the brief both distinguish these; an Android **emulator** proves the real OS image but not real font rendering/performance, an iOS **simulator** is a Mac-native reimplementation, not real WebKit — neither is "real device" and the matrix's Environment column must say which was used | Use the cloud lab's **real device** inventory where offered (BrowserStack/LambdaTest both advertise real-device farms, not just emulators) — record "real device (cloud)" rather than "emulator"/"simulator" only if that is genuinely what ran |
| 4 | **Which mobile OS — Android or iOS** | The brief only requires one; §3 above assumed Android for realism of cloud-lab/real-device access, but this is not fixed | Android, unless the student already has personal iPhone access — Android real devices are more commonly free on trial tiers |
| 5 | **Which student-ID email is overlaid** | Every screenshot needs the exact same `MSSV@....edu.vn`-form address burned in; this should be the same address already used for the §7 Google Form submissions, for consistency | Confirm the exact official HCMUS student email address (not a placeholder) before the first capture — retrofitting an overlay onto 20 already-taken screenshots is wasted effort |
| 6 | **When to run, given the trial's time limit** | BrowserStack/LambdaTest free tiers meter either session minutes or session count; running cold without a session plan burns the trial before the matrix is done | Do a **dry run first** (no captures) to confirm login, EMS reachability from the cloud lab (ngrok tunnels can be flaky through corporate/lab proxies), and screenshot/overlay mechanics — then run the real 3 timed cloud sessions in one sitting per §6 below |

## 5. The mandatory screenshot rule

Every one of the 24 cells needs one screenshot. Each image must show, **in the pixels themselves**,
not just the filename or a caption written elsewhere:

1. the EMS URL (the lab's own browser-chrome/address-bar frame, kept in the capture, satisfies this),
2. the browser / OS / device identity — the cloud lab's own banner/frame (BrowserStack and
   LambdaTest both stamp this on Live sessions) or a visible `about:` page/device-info readout beside
   the app if using a real personal device,
3. **the student-ID email overlay, in the form `MSSV@....edu.vn`**, burned into the image — not a
   caption in the markdown table, not a filename, the pixels themselves,
4. the screen in the state being claimed (resting state for a Pass; the defective state for a Fail).

**Producing the overlay:** use whichever is least friction and still legible —
BrowserStack/LambdaTest's own screenshot-annotation feature if it supports adding text, or a
lightweight screenshot annotator (Windows Snipping Tool's markup, macOS Preview's markup, or any
image editor) to stamp the email in a corner that does not cover the content being evaluated. A
watermark that is technically present but illegibly small, low-contrast, or cropped off does **not**
satisfy the rule — the skill's own evidence discipline says "verify by opening the image, not by
trusting the filename," and a TA will do exactly that.

A screenshot missing the overlay does not count as evidence for that cell, full stop — the cell
reverts to "Not executed," it is not scored as Pass/Fail on the strength of the rest of the image.

**Naming convention** (already stated in `docs/04_Task3_Cross_Platform_Matrix.md` and the skill):

```
<Screen>_<OS>_<Browser>_<Device>.png
```

e.g. `D1_Windows_Edge_desktop.png`, `D3_macOS_Safari_desktop.png`, `D4_Android_Opera_tablet.png`.
Save all 24 under `reports/evidence_task3/`. **All 24 filenames are already pre-assigned**, one per
row, in the Note cell of `docs/04_Task3_Cross_Platform_Matrix.md` — name each capture from its row
rather than inventing a name at capture time. When a cell is captured, move that filename from the
Note cell into the row's **Evidence** column and reuse the Note for the defect description (Fails
only). Leaving Evidence empty until a real image exists is deliberate: `matrix_coverage.py` then
only ever flags a reference that is genuinely broken, and the matrix never claims evidence it does
not have. The unrun matrix already passes the verifier clean (exit 0, floor met on all four
screens) — confirmed by running it, so any later failure is a real regression, not scaffolding noise.

## 6. Run order — minimising cloud-lab minutes

The expensive resource is **cloud-lab session launches**, not screenshots — once a session is open on
a given OS/browser/device, all four screens (D1–D4) can be captured without relaunching. Group by
environment, not by screen:

**Every one of the 20 shots below must pass the same five checks before you move on** (the identical
list sits directly above the matrix table in `docs/04_Task3_Cross_Platform_Matrix.md`, which is where
you will be looking at capture time): **(1)** EMS URL visible in the image · **(2)** browser / OS /
device identity visible in the image · **(3)** `MSSV@....edu.vn` overlay burned into the pixels,
legible, not covering the content being judged · **(4)** the screen in the state the row claims ·
**(5)** saved under `reports/evidence_task3/` with the row's pre-assigned filename. Fix an overlay in
the session that produced it — retrofitting overlays onto a batch of finished screenshots, or
relaunching a metered cloud session to redo one shot, is the expensive failure mode here.

```
BLOCK 0 — LOCAL, no cloud lab, no time pressure   (rows 1-2 of the template, ×4 screens = 8 shots)
  [ ] Own Windows PC, Edge     -> D1, D2, D3, D4   (4 screenshots)
  [ ] Own Windows PC, Firefox  -> D1, D2, D3, D4   (4 screenshots)

BLOCK 1 — CLOUD LAB, one session, macOS + Safari  (row 3 of the template, ×4 screens = 4 shots)
  [ ] Launch BrowserStack/LambdaTest Live: macOS, Safari, desktop
  [ ] Navigate D1 -> screenshot+overlay -> D2 -> D3 -> D4, all in the same session

BLOCK 2 — CLOUD LAB (or real device), Android phone + Chrome  (row 4, ×4 screens = 4 shots)
  [ ] Launch/connect: Android, Chrome, phone
  [ ] D1 -> D2 -> D3 -> D4, same session

BLOCK 3 — CLOUD LAB (or real device), Android tablet + Opera  (row 5, ×4 screens = 4 shots)
  [ ] Launch/connect: Android, Opera (or Samsung Internet), tablet
  [ ] D1 -> D2 -> D3 -> D4, same session

BLOCK 4 — CLOUD LAB, iOS phone + Safari, REAL DEVICE  (row 6, ×4 screens = 4 shots)
  [ ] Launch a real iPhone from the lab's device farm, NOT the Xcode simulator —
      a simulator is a Mac-native reimplementation and proves nothing about real WebKit.
      Record `real device (cloud)` in the Environment column, and if only a simulator
      is available on your tier, record `simulator` honestly rather than upgrading it.
  [ ] D1 -> D2 -> D3 -> D4, same session
```

Total: **4 cloud-lab session launches** (not 24) cover 16 of the 24 cells; the remaining 8 run free
and untimed on a local machine. This is the single biggest lever on trial-minute budget — collapsing
24 cells into 4 timed launches rather than 24.

**Time estimate:** each cloud session — login, navigate 4 screens, screenshot, overlay each — runs
roughly 15–25 minutes; call it 20 minutes × 3 sessions ≈ **60 minutes of metered cloud-lab time**,
plus the local block (unmetered, budget 30–40 minutes for 8 screenshots) and setup/account
verification overhead. **Whole matrix: realistically a single 2–3 hour sitting**, assuming the trial
is live and EMS is reachable from the lab on the first attempt. Do the dry run (§4, item 6) on a
separate earlier sitting so this window is spent capturing, not troubleshooting login.

## 7. What to record per cell

For every row in `docs/04_Task3_Cross_Platform_Matrix.md`:

| Column | What goes in it |
| --- | --- |
| Result | `Pass` or `Fail` only (no hedging — see the repo's own past correction commit on this) |
| Environment | `real device (local)`, `real device (cloud)`, `emulator`, or `simulator` — never left blank |
| Evidence | the pre-assigned filename moved over from the row's Note cell once the image exists; must resolve under `reports/evidence_task3/` |
| Note (Fail only) | the defect classification from the fixed vocabulary — `overflow` · `overlap` ·
`clipping` · `unreadable` · `unresponsive-control` · `missing-asset` · `feature-unsupported` ·
`broken-layout` — plus one line describing what was seen |

Before logging any Fail as final: **reproduce it once**, ideally in a fresh session, per the skill's
own cloud-lab caution — stale sessions, mid-load captures and DPI-scaled screenshots on cloud labs
routinely masquerade as product defects. Also separate genuine incompatibility from legitimate
platform difference (native date-input locale formatting, platform scrollbars, system font
substitution, the mobile URL bar changing viewport height) — record the latter under "Platform
differences observed," not as a Fail.

## 8. Verification

Run from `HW03/` once cells are filled in:

```bash
python .claude/skills/cross-platform-matrix/scripts/matrix_coverage.py docs/04_Task3_Cross_Platform_Matrix.md \
  --os "Windows,macOS,Android,iOS" \
  --browsers "Chrome,Firefox,Safari,Edge,Opera" \
  --devices "desktop,tablet,phone" \
  --evidence-root reports/evidence_task3/
```

**`--os` must list exactly the three operating systems the rows actually use — no more.** Every value
passed is treated as *required*, so an earlier version of this command that listed
`Windows,macOS,Android,iOS` "to future-proof it" reported `OS not covered: iOS` on all four screens
and exited 1 against a matrix that is in fact correct (verified: exit 1, four problems). If the
mobile-OS decision in §4 item 4 changes from Android to iOS, change the matrix rows, their filenames
**and** this `--os` list in the same edit.

A clean run prints, per screen, `OS`, `browser` and `device class` each showing `X/X covered` with
no `MISSING` line, at least 2 distinct engines identified per screen, no `! Fail with no evidence
reference` problem, no `evidence file not found` problem, and ends with:

```
OK -- coverage floor met on every screen, evidence resolves
```

Exit code 0. Any `FAIL (N problem(s))` on stderr means at least one required value is still
uncovered somewhere, or a Fail row lacks a working evidence reference — fix before treating the
matrix as submittable.

## 9. Handoff to §7 (findings)

Every genuine incompatibility found — not a legitimate platform difference — becomes a row in
`docs/05_Bug_Usability_Findings_Log.md`, typed `Bug`, with the matrix cell (screen, OS, browser,
device) as its reproduction context and the screenshot as evidence.

- **New IDs start at D-020.** D-001…D-019 are already taken (Task 1B). **D-013, D-014 and D-018 are
  retired and must never be reused** — they were retracted on live re-verification and self-review,
  and the findings log's own retraction notes document why; reusing those numbers for unrelated Task
  3 findings would corrupt that history.
- **Task 2 also draws from D-020 onward** (`docs/usability_testing/00_Run_Plan.md` §4.6). Coordinate:
  whichever task's findings are written up and submitted to the Google Form first claims the next
  sequential ID. **Allocate an ID only at the moment a finding is actually written**, not in advance
  — reserving a block for Task 3 ahead of time risks a collision if Task 2's session analysis lands
  first, and the brief's own cross-check (§7: "the aggregated file and the form submissions must be
  consistent") means a reserved-but-unused ID is itself a discrepancy a TA can catch.
- Each new finding is **also submitted to the Google Form** (https://forms.gle/CJQFQCAXcsDbXDMM9)
  from the student-ID email, per §7 of the brief. Then re-run the findings-log checker:

```bash
python .claude/skills/findings-log/scripts/check_findings.py docs/05_Bug_Usability_Findings_Log.md --evidence-root reports/evidence_task3
```

## 10. Definition of done

- [ ] Cloud lab (or real-device fallback) chosen and account/trial confirmed working (§4 item 1-2)
- [ ] Mobile OS decided (Android or iOS) and stated in the matrix header
- [ ] Student-ID email overlay confirmed exact and consistent with the §7 Google Form address
- [ ] Dry run completed: login, EMS reachability from the lab, overlay mechanics all verified before
      the timed capture sessions
- [ ] All 24 cells captured (6 per screen × D1–D4), each screenshot showing URL + browser/OS/device
      identity + student-ID email overlay + the claimed screen state
- [ ] The matrix's **Tooling** record table filled in (tool actually used, trial identity and window,
      mobile OS decided, the exact overlaid student-ID email)
- [ ] `docs/04_Task3_Cross_Platform_Matrix.md` filled in: Result, Environment, Evidence and Note
      (Fails only) for every row — no `Not executed` left
- [ ] The matrix's **Failures** table filled in: one row per `Fail` cell, with its classification from
      the fixed vocabulary, a short note on the defect, its screenshot and its findings-log ID
- [ ] Every Fail reproduced once before being logged as final
- [ ] "Coverage achieved" table and "Platform differences observed" section filled in
- [ ] `matrix_coverage.py` run clean (exit 0, no `MISSING`, ≥ 2 engines per screen, no evidence
      problems)
- [ ] New findings appended to `docs/05_Bug_Usability_Findings_Log.md` from D-020, coordinated with
      Task 2's own D-020+ allocation, each also submitted to the Google Form
- [ ] `.claude/skills/findings-log/scripts/check_findings.py` run clean against `reports/evidence_task3`
- [ ] The Task 3 AI interactions appended to `docs/06_AI_Audit_Report.md`, stating explicitly that
      the captures were produced by a person on real environments/cloud-lab sessions, not AI-generated
- [ ] README §"Test summary" and §16 self-assessment updated off 0
