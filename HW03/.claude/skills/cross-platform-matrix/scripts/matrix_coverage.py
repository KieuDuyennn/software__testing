#!/usr/bin/env python3
"""Verify a cross-browser / cross-platform matrix actually meets its coverage floor.

Reads the first markdown table that has OS, Browser and Result columns, then per screen
reports which required OS / browser / device-class values are uncovered. Also flags the
common credibility problems: a Fail row with no evidence, evidence that is not on disk, and
a matrix whose browsers all share one rendering engine.

Column names are matched by substring and case-insensitively, so "OS / Platform",
"Browser (version)" and "Device type" all resolve.

Usage:
    matrix_coverage.py matrix.md --os "Windows,macOS,Android" \
        --browsers "Chrome,Firefox,Safari,Edge,Opera" \
        --devices "desktop,tablet,phone" [--evidence-root DIR] [--quiet]

Exit code 1 if any required value is uncovered on any screen, or any evidence check fails.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ENGINES = {
    "Blink": ("chrome", "chromium", "edge", "opera", "samsung", "brave", "vivaldi"),
    "Gecko": ("firefox", "gecko"),
    "WebKit": ("safari", "webkit", "epiphany"),
}
EMPTY = {"", "-", "--", "n/a", "na", "tbd", "todo", "?"}
IMG_RE = re.compile(r"([\w./ -]+?\.(?:png|jpe?g|gif|webp|mp4|webm))", re.IGNORECASE)


def split_row(raw: str) -> list[str]:
    return [c.strip() for c in raw.strip().strip("|").split("|")]


def find_col(headers: list[str], *needles: str) -> int | None:
    for idx, head in enumerate(headers):
        low = head.lower()
        if any(n in low for n in needles):
            return idx
    return None


def engine_of(browser: str, os_name: str, declared: str = "") -> str:
    """Resolve the rendering engine for a cell.

    An explicitly declared Engine cell always wins: iOS is WebKit by default but no longer by
    law -- Apple permits alternative engines for EU users on iOS 17.4+, and the UK CMA has
    ruled iOS must open to them -- so silently overriding a row that says "Blink" would erase
    the very cell that makes a matrix interesting.
    """
    for engine in ENGINES:
        if engine.lower() in declared.lower():
            return engine
    if any(tok in os_name.lower() for tok in ("ios", "iphone", "ipad")):
        return "WebKit"
    low = browser.lower()
    for engine, tokens in ENGINES.items():
        if any(t in low for t in tokens):
            return engine
    return "unknown"


def parse(path: Path) -> tuple[list[str], list[list[str]]]:
    headers: list[str] = []
    rows: list[list[str]] = []
    in_table = False
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cells = split_row(line)
        if set("".join(cells)) <= set("-: "):
            continue
        low = [c.lower() for c in cells]
        # Every cell of a real header is a short label. Without this test a DATA row whose Note
        # cell says something like "passes on this platform in every browser" is read as a
        # header, re-arms the parser and swallows the rows after it -- silently.
        is_label = all(len(c) <= 40 and c.count(" ") <= 5 for c in cells)
        if is_label \
                and find_col(low, "os", "platform") is not None \
                and find_col(low, "browser") is not None \
                and find_col(low, "result", "pass", "status") is not None:
            # Re-arm on every header-shaped row. A per-screen report puts prose and headings
            # between its matrices, and a parser that stopped at the first break would report
            # a partial matrix as fully covered -- the exact false all-clear this checks for.
            if not headers:
                headers = cells
            in_table = True
            continue
        if in_table and headers:
            rows.append(cells + [""] * (len(headers) - len(cells)))
    return headers, rows


def covered(required: list[str], seen: set[str]) -> tuple[list[str], list[str]]:
    """Match required values against observed cells by case-insensitive substring."""
    hit, miss = [], []
    joined = " | ".join(seen).lower()
    for req in required:
        (hit if req.lower() in joined else miss).append(req)
    return hit, miss


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("matrix", type=Path)
    ap.add_argument("--os", default="", help="comma-separated required operating systems")
    ap.add_argument("--browsers", default="", help="comma-separated required browsers")
    ap.add_argument("--devices", default="", help="comma-separated required device classes")
    ap.add_argument("--evidence-root", type=Path)
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.matrix.is_file():
        print(f"not a file: {args.matrix}", file=sys.stderr)
        return 2

    headers, rows = parse(args.matrix)
    if not headers:
        print(
            "No matrix table found. Expected a markdown table with columns for OS/Platform, "
            "Browser and Result.",
            file=sys.stderr,
        )
        return 2
    if not rows:
        print("Matrix table has a header but no rows.", file=sys.stderr)
        return 2

    c_screen = find_col(headers, "screen", "page", "màn")
    c_os = find_col(headers, "os", "platform")
    c_browser = find_col(headers, "browser")
    c_device = find_col(headers, "device", "form factor", "thiết bị")
    c_result = find_col(headers, "result", "pass", "status")
    c_ev = find_col(headers, "evidence", "screenshot", "ảnh")
    c_env = find_col(headers, "environment", "real", "emulat")
    c_engine = find_col(headers, "engine")

    req_os = [s.strip() for s in args.os.split(",") if s.strip()]
    req_br = [s.strip() for s in args.browsers.split(",") if s.strip()]
    req_dev = [s.strip() for s in args.devices.split(",") if s.strip()]

    per_screen: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: {"os": set(), "browser": set(), "device": set(), "engine": set()}
    )
    problems: list[str] = []
    results: dict[str, int] = defaultdict(int)

    for n, row in enumerate(rows, 1):
        screen = row[c_screen].strip() if c_screen is not None else "(all)"
        screen = screen or "(unnamed)"
        os_name = row[c_os].strip()
        browser = row[c_browser].strip()
        bucket = per_screen[screen]
        bucket["os"].add(os_name)
        bucket["browser"].add(browser)
        if c_device is not None:
            bucket["device"].add(row[c_device].strip())
        declared = row[c_engine].strip() if c_engine is not None else ""
        bucket["engine"].add(engine_of(browser, os_name, declared))

        verdict = row[c_result].strip().lower() if c_result is not None else ""
        results[verdict or "empty"] += 1
        is_fail = verdict.startswith("fail")

        if is_fail and c_ev is not None and row[c_ev].strip().lower() in EMPTY:
            problems.append(f"row {n} ({screen} / {os_name} / {browser}): Fail with no evidence reference")
        if c_ev is not None and args.evidence_root and row[c_ev].strip().lower() not in EMPTY:
            for name in IMG_RE.findall(row[c_ev]):
                name = name.strip()
                if not (args.evidence_root / name).exists() \
                        and not list(args.evidence_root.rglob(Path(name).name)):
                    problems.append(f"row {n}: evidence file not found under {args.evidence_root}: {name}")

    if not args.quiet:
        print(f"{args.matrix.name}: {len(rows)} cells across {len(per_screen)} screen(s)")
        print("  results: " + ", ".join(f"{k}={v}" for k, v in sorted(results.items())))
        if c_env is None:
            print("  ! no Environment column -- a reviewer cannot tell real device from emulator,\n"
                  "    simulator or DevTools responsive mode. Add one.")

    for screen in sorted(per_screen):
        bucket = per_screen[screen]
        if not args.quiet:
            print(f"\n  {screen}")
        for label, required, seen in (
            ("OS", req_os, bucket["os"]),
            ("browser", req_br, bucket["browser"]),
            ("device class", req_dev, bucket["device"]),
        ):
            if not required:
                continue
            hit, miss = covered(required, seen)
            if not args.quiet:
                print(f"    {label:<13} {len(hit)}/{len(required)} covered"
                      + (f"  -- MISSING: {', '.join(miss)}" if miss else ""))
            if miss:
                problems.append(f"{screen}: {label} not covered: {', '.join(miss)}")

        engines = {e for e in bucket["engine"] if e != "unknown"}
        if not args.quiet:
            print(f"    engines       {', '.join(sorted(engines)) or 'unknown'}")
        if len(engines) < 2:
            print(f"    ! {screen}: only {len(engines) or 'no identified'} rendering engine(s). "
                  "Browsers sharing an engine mostly share behaviour -- add a Gecko and a WebKit cell.")

    if problems:
        sys.stdout.flush()
        print(f"\nFAIL ({len(problems)} problem(s))", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("\nOK -- coverage floor met on every screen"
              + (", evidence resolves" if (c_ev is not None and args.evidence_root) else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
