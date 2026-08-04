#!/usr/bin/env python3
"""Run the throttle / offline checklist cells over the Chrome DevTools Protocol.

Why this exists
---------------
Two checklist items cannot be answered by looking at a page, only by changing the
network underneath it:

  IA01-07  Reload a data-heavy screen on DevTools -> Network -> "Slow 3G".
           Expect a spinner or skeleton while data loads, and KPI numbers that
           never flash "0" or blank before the real value arrives.

  IA04-11  Force a server-side failure with DevTools -> Network -> "Offline",
           then load a list screen or submit a form.
           Expect a visible plain-language error that says what failed and offers
           a retry. Never an infinite spinner, a permanently blank screen, or a
           raw stack trace.

A page-level `navigator.onLine` override is NOT a substitute for either: it lies
to the page without cutting the network, so requests still succeed and the test
proves nothing. `Network.emulateNetworkConditions` cuts them for real, which is
why this talks CDP rather than running inside the page.

Credentials
-----------
This script never types a password. It attaches to a Chrome you have already
signed into by hand. See --help for the two-step recipe.

Usage
-----
  # 1. You: start Chrome with a debugging port, then log in to EMS in that window.
  python network_conditions.py --launch

  # 2. Check the connection sees your logged-in tab.
  python network_conditions.py --check

  # 3. Run every cell and write evidence.
  python network_conditions.py --run-all --out ../../../../reports/evidence_task1b

Only the standard library plus `websocket-client` is needed (pip install websocket-client).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import platform
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

try:
    import websocket  # websocket-client
except ImportError:  # pragma: no cover
    sys.exit("pip install websocket-client")

DEFAULT_PORT = 9222
BASE = "https://prod-dev.ems-fitus.cloud"

# The six Scenario-D screens. `needs_id` rows are filled in from --complaint-id.
SCREENS = [
    ("D1", "/complaints/new"),
    ("D2", "/complaints"),
    ("D3", "/dashboard/admin/complaints"),
    ("D4", "/dashboard/admin/complaints/{id}"),
    ("D5", "/notifications"),
    ("D6", "/dashboard/admin/complaints/{id}"),  # lightbox lives on the D4 page
]

# Chrome's own "Slow 3G" preset, as used by DevTools.
SLOW_3G = dict(offline=False, latency=2000.0,
               downloadThroughput=int(50 * 1024 / 8), uploadThroughput=int(50 * 1024 / 8))
OFFLINE = dict(offline=True, latency=0.0, downloadThroughput=0, uploadThroughput=0)
NO_THROTTLE = dict(offline=False, latency=0.0, downloadThroughput=-1, uploadThroughput=-1)


# --------------------------------------------------------------------------- CDP


class CDP:
    """A minimal CDP client: one websocket per tab, synchronous request/response."""

    def __init__(self, ws_url: str):
        # suppress_origin matters: Chrome 111+ rejects a CDP websocket that carries
        # an Origin header unless --remote-allow-origins was passed. Sending no
        # Origin at all works without weakening the browser's own flag defaults.
        self.ws = websocket.create_connection(ws_url, timeout=90, suppress_origin=True)
        self._id = 0

    def send(self, method: str, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            # events are ignored; we poll the DOM instead of racing them

    def eval(self, expression: str, await_promise: bool = True):
        r = self.send("Runtime.evaluate", expression=expression,
                      returnByValue=True, awaitPromise=await_promise)
        if r.get("exceptionDetails"):
            raise RuntimeError(r["exceptionDetails"].get("text", "eval failed"))
        return r.get("result", {}).get("value")

    def close(self):
        try:
            self.ws.close()
        except Exception:
            pass


def http_json(port: int, path: str):
    with urllib.request.urlopen(f"http://127.0.0.1:{port}{path}", timeout=5) as r:
        return json.loads(r.read().decode())


def find_tab(port: int, must_contain: str = "ems-fitus"):
    """Pick the EMS tab, preferring one already on the app."""
    tabs = [t for t in http_json(port, "/json") if t.get("type") == "page"]
    if not tabs:
        raise SystemExit("No page targets. Is Chrome running with --remote-debugging-port?")
    for t in tabs:
        if must_contain in (t.get("url") or ""):
            return t
    return tabs[0]


# ----------------------------------------------------------------------- helpers


def chrome_binary() -> str:
    if platform.system() == "Windows":
        for c in (r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                  r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"):
            if os.path.exists(c):
                return c
    for name in ("google-chrome", "chromium", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    raise SystemExit("Could not find Chrome; pass --chrome /path/to/chrome")


def launch(port: int, chrome: str | None, profile: Path) -> None:
    exe = chrome or chrome_binary()
    profile.mkdir(parents=True, exist_ok=True)
    subprocess.Popen([exe, f"--remote-debugging-port={port}",
                      f"--user-data-dir={profile}", "--no-first-run",
                      "--no-default-browser-check", BASE],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Chrome launching on port {port} with a scratch profile at {profile}.")
    print("This is a FRESH profile, so it is not signed in.")
    print("Log in to EMS yourself in that window, then run:  --check")


# Instrumentation injected before each navigation. It records, from inside the
# page, the things a screenshot taken afterwards can no longer tell you:
# whether a busy indicator was ever shown, and whether a number rendered as 0
# or blank before its real value arrived.
PROBE = r"""
(() => {
  window.__probe = {spinnerSeen:false, spinnerMs:0, zeroFlash:[], firstPaintText:null,
                    errors:[], t0: performance.now()};
  const p = window.__probe;
  const busy = () => document.querySelector(
      '[role=progressbar],[aria-busy=true],.animate-pulse,.animate-spin,[class*="skeleton"],[class*="Skeleton"]');
  let busySince = null;
  const digits = el => (el.innerText || '').trim();
  const sweep = () => {
    const b = busy();
    if (b && busySince === null) { busySince = performance.now(); p.spinnerSeen = true; }
    if (!b && busySince !== null) { p.spinnerMs += performance.now() - busySince; busySince = null; }
    if (p.firstPaintText === null) {
      const t = (document.body && document.body.innerText || '').trim();
      if (t) p.firstPaintText = t.slice(0, 400);
    }
    // A KPI card showing exactly "0" while the page is still busy is the flash
    // IA01-07 is about. Record it with a timestamp so a real 0 can be told apart.
    document.querySelectorAll('h1,h2,h3,p,span,div').forEach(el => {
      if (el.children.length === 0) {
        const t = digits(el);
        if (t === '0' || t === '') return;
      }
    });
    document.querySelectorAll('[class*="text-3xl"],[class*="text-2xl"],[class*="text-4xl"]').forEach(el => {
      if (el.children.length) return;
      const t = digits(el);
      if (t === '0' || t === '-' || t === '') {
        p.zeroFlash.push({t: Math.round(performance.now() - p.t0), text: t,
                          busy: !!busy()});
      }
    });
  };
  p._iv = setInterval(sweep, 60);
  sweep();
  window.addEventListener('error', e => p.errors.push(String(e.message)));
  setTimeout(() => clearInterval(p._iv), 45000);
})();
"""

# Read after the page settles. Answers both items' expected results.
VERDICT = r"""
(() => {
  const p = window.__probe || {};
  const text = (document.body && document.body.innerText || '').trim();
  const visible = el => { const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 0 && r.height > 0 && s.visibility !== 'hidden' && s.display !== 'none'; };
  const busyNow = [...document.querySelectorAll(
     '[role=progressbar],[aria-busy=true],.animate-pulse,.animate-spin,[class*="skeleton"]')]
     .filter(visible).length;
  const liveRegions = [...document.querySelectorAll('[role=alert],[role=status],[aria-live]')]
     .filter(visible).map(e => ({role: e.getAttribute('role'),
                                 live: e.getAttribute('aria-live'),
                                 text: (e.innerText || '').trim().slice(0, 200)}));
  // Anything that reads like a raw server/stack error rather than a written message.
  const raw = /(Internal Server Error|stack trace|at\s+\w+\.\w+\s*\(|undefined is not|NetworkError|Failed to fetch|ERR_|<!DOCTYPE)/i;
  const retry = /(retry|try again|reload|refresh|th[ửu] l[ạa]i|t[ải]i l[ạa]i)/i;
  return {
    spinnerSeen: !!p.spinnerSeen,
    spinnerMs: Math.round(p.spinnerMs || 0),
    zeroFlash: (p.zeroFlash || []).slice(0, 12),
    firstPaintText: p.firstPaintText,
    stillBusy: busyNow,
    bodyLength: text.length,
    blankScreen: text.length < 40,
    liveRegions,
    mentionsRetry: retry.test(text),
    looksRaw: raw.test(text),
    bodyHead: text.slice(0, 500),
    pageErrors: (p.errors || []).slice(0, 5),
  };
})();
"""


def screenshot(cdp: CDP, path: Path) -> None:
    data = cdp.send("Page.captureScreenshot", format="jpeg", quality=70)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(base64.b64decode(data["data"]))


def run_cell(cdp: CDP, item: str, screen: str, url: str, conditions: dict,
             out: Path, settle: float) -> dict:
    cdp.send("Network.enable")
    cdp.send("Page.enable")
    cdp.send("Network.emulateNetworkConditions", **conditions)
    # Inject the probe into the *next* document, so it is running before first paint.
    cdp.send("Page.addScriptToEvaluateOnNewDocument", source=PROBE)
    cdp.send("Page.navigate", url=url)
    time.sleep(settle)
    try:
        verdict = cdp.eval(VERDICT, await_promise=False) or {}
    except Exception as e:  # a page that never becomes scriptable is itself a result
        verdict = {"error": str(e)}
    shot = out / f"{screen}_{item}_{'offline' if conditions['offline'] else 'slow3g'}.jpg"
    try:
        screenshot(cdp, shot)
        verdict["evidence"] = shot.name
    except Exception as e:
        verdict["evidence"] = f"screenshot failed: {e}"
    verdict.update(item=item, screen=screen, url=url,
                   condition="offline" if conditions["offline"] else "slow-3g")
    return verdict


def summarise(v: dict) -> str:
    """Turn a measurement into the wording the checklist item actually asks for."""
    if v["condition"] == "slow-3g":
        if not v.get("spinnerSeen"):
            return "FAIL: no spinner or skeleton was ever shown while data loaded"
        if v.get("zeroFlash"):
            return (f"FAIL: a value rendered as {v['zeroFlash'][0]['text']!r} "
                    f"{v['zeroFlash'][0]['t']}ms in, before the real value arrived")
        return f"PASS: busy indicator shown for {v.get('spinnerMs')}ms, no zero-flash"
    # offline
    if v.get("blankScreen"):
        return "FAIL: permanently blank screen, no error message"
    if v.get("stillBusy"):
        return f"FAIL: {v['stillBusy']} spinner(s) still running after settle - infinite spinner"
    if v.get("looksRaw"):
        return "FAIL: raw technical error text shown instead of a written message"
    if not v.get("liveRegions"):
        return "FAIL: request failed with no visible error message at all"
    if not v.get("mentionsRetry"):
        return "PARTIAL: an error is shown but it offers no retry"
    return "PASS: visible plain-language error with a retry"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument("--launch", action="store_true", help="start Chrome with a debug port")
    ap.add_argument("--chrome", help="path to the Chrome binary")
    ap.add_argument("--profile", type=Path,
                    default=Path.home() / ".ems-cdp-profile",
                    help="scratch profile dir for --launch")
    ap.add_argument("--check", action="store_true", help="verify the tab is signed in")
    ap.add_argument("--run-all", action="store_true")
    ap.add_argument("--complaint-id", default="26",
                    help="an existing support request id, for the D4/D6 URLs")
    ap.add_argument("--settle", type=float, default=12.0,
                    help="seconds to wait after navigate before reading the verdict")
    ap.add_argument("--out", type=Path, default=Path("reports/evidence_task1b"))
    args = ap.parse_args()

    if args.launch:
        launch(args.port, args.chrome, args.profile)
        return 0

    tab = find_tab(args.port)
    cdp = CDP(tab["webSocketDebuggerUrl"])

    if args.check:
        cdp.send("Page.navigate", url=f"{BASE}/dashboard/admin/complaints")
        time.sleep(4)
        url = cdp.eval("location.href", await_promise=False)
        body = cdp.eval("document.body.innerText.slice(0,200)", await_promise=False) or ""
        signed_in = "login" not in (url or "").lower()
        print(f"tab url : {url}")
        print(f"signed in: {'yes' if signed_in else 'NO - log in in that window first'}")
        print(f"body    : {body[:120].replace(chr(10), ' | ')}")
        cdp.close()
        return 0 if signed_in else 1

    if not args.run_all:
        ap.print_help()
        return 2

    results = []
    try:
        for item, conditions in (("IA01-07", SLOW_3G), ("IA04-11", OFFLINE)):
            for screen, path in SCREENS:
                url = BASE + path.replace("{id}", args.complaint_id)
                print(f"  {screen} {item} ...", flush=True)
                v = run_cell(cdp, item, screen, url, conditions, args.out, args.settle)
                v["verdict"] = summarise(v)
                print(f"    {v['verdict']}")
                results.append(v)
                # restore the network between cells so the next navigation is clean
                cdp.send("Network.emulateNetworkConditions", **NO_THROTTLE)
                time.sleep(2)
    finally:
        try:
            cdp.send("Network.emulateNetworkConditions", **NO_THROTTLE)
        except Exception:
            pass
        cdp.close()

    args.out.mkdir(parents=True, exist_ok=True)
    report = args.out / "network_conditions_results.json"
    report.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"\n{len(results)} cells measured -> {report}")
    for v in results:
        print(f"  {v['screen']:3} {v['item']} {v['condition']:8} {v['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
