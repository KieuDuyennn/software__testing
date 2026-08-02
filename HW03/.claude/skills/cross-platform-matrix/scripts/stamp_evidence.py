#!/usr/bin/env python3
"""Stamp a Task 3 capture with the student-ID overlay and file it under its matrix row's name.

The row plan is read from the matrix markdown itself, so the filename this produces can never
drift from the row it belongs to. Run --list to see the rows and the name each one expects.

    python .claude/skills/cross-platform-matrix/scripts/stamp_evidence.py --list
    python .claude/skills/cross-platform-matrix/scripts/stamp_evidence.py --row 1 raw.png

What this does NOT do: take the screenshot. The capture must be a real one, made by a person on
the environment the row claims, with the EMS URL and the browser/OS/device identity already inside
the frame -- this script only burns the overlay in and files the result. An overlay cannot rescue a
capture that is missing the URL or the device identity, because those cannot be added after the
fact without falsifying what the image shows.
"""

import argparse
import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

DEFAULT_OVERLAY = "23127184 · lpkduyen23@clc.fitus.edu.vn"
MATRIX = Path("docs/04_Task3_Cross_Platform_Matrix.md")
EVIDENCE_ROOT = Path("reports/evidence_task3")

# "Windows 11" -> Windows, "iOS 17+" -> iOS: the filename uses the bare OS name.
OS_SHORT = {"Windows 11": "Windows", "iOS 17+": "iOS", "macOS Monterey": "macOS"}

# The row's own Evidence/Note cell is the authority on its filename when it names one; deriving a
# name from the OS and browser columns only works while those columns are single words. Rows like
# "macOS Monterey" + "Safari 15" derive to a name containing spaces, which is not the name the
# capture actually carries -- so read the cell first and derive only as a fallback.
FILENAME_RE = re.compile(r"[A-Za-z0-9][\w.\-]*\.(?:png|jpe?g)", re.I)


def parse_rows(matrix_path):
    """Return {row_number: (screen, os, browser, device, filename)} from the matrix table."""
    rows = {}
    for line in matrix_path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 6 or not cells[0].isdigit():
            continue
        n, screen, os_name, browser, _engine, device = cells[:6]
        stated = FILENAME_RE.search(" ".join(cells[8:10])) if len(cells) >= 9 else None
        if stated:
            fname = stated.group(0)
        else:
            os_short = OS_SHORT.get(os_name, os_name)
            fname = f"{screen}_{os_short}_{browser}_{device}.png".replace(" ", "")
        rows[int(n)] = (screen, os_name, browser, device, fname)
    return rows


def pick_font(width):
    """A watermark that is present but illegible does not satisfy the brief -- scale to the image."""
    size = max(16, width // 55)
    for name in ("arialbd.ttf", "arial.ttf", "segoeui.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def stamp(src, text, corner):
    img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(img)
    font = pick_font(img.width)
    pad = max(8, img.width // 150)

    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    tw, th = right - left, bottom - top
    box_w, box_h = tw + 2 * pad, th + 2 * pad

    # Bottom-left by default: page content and browser chrome both tend to live above it.
    x = pad if corner.endswith("left") else img.width - box_w - pad
    y = pad if corner.startswith("top") else img.height - box_h - pad

    # Opaque plate behind the text -- a low-contrast overlay is treated as no overlay.
    draw.rectangle([x, y, x + box_w, y + box_h], fill=(0, 0, 0))
    draw.text((x + pad - left, y + pad - top), text, font=font, fill=(255, 255, 0))
    return img


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("source", nargs="?", help="the raw capture to stamp")
    ap.add_argument("--row", type=int, help="matrix row number; decides the output filename")
    ap.add_argument("--name", help="output filename, for supporting evidence that has no matrix row "
                                   "(a defect found off the D1-D4 screens). Mutually exclusive "
                                   "with --row: a capture belonging to a row must be named by it.")
    ap.add_argument("--list", action="store_true", help="show every row and the name it expects")
    ap.add_argument("--overlay", default=DEFAULT_OVERLAY, help="overlay text (default: student ID + email)")
    ap.add_argument("--corner", default="bottom-left",
                    choices=["bottom-left", "bottom-right", "top-left", "top-right"])
    ap.add_argument("--matrix", type=Path, default=MATRIX)
    ap.add_argument("--out-dir", type=Path, default=EVIDENCE_ROOT)
    args = ap.parse_args()

    if not args.matrix.exists():
        sys.exit(f"matrix not found: {args.matrix} -- run this from HW03/")
    rows = parse_rows(args.matrix)
    if not rows:
        sys.exit(f"no matrix rows parsed from {args.matrix}")

    if args.list:
        print(f"{len(rows)} rows in {args.matrix}\n")
        for n in sorted(rows):
            screen, os_name, browser, device, fname = rows[n]
            have = "captured" if (args.out_dir / fname).exists() else "--"
            print(f"  {n:>2}  {screen}  {os_name:<11} {browser:<8} {device:<8} {fname:<34} {have}")
        done = sum((args.out_dir / r[4]).exists() for r in rows.values())
        print(f"\n{done}/{len(rows)} captured")
        return

    if args.row and args.name:
        sys.exit("--row and --name are mutually exclusive: a capture that belongs to a matrix row "
                 "must take that row's filename, or the image and the row can drift apart")
    if not args.source or not (args.row or args.name):
        sys.exit("need a source image and either --row N or --name FILE (or use --list)")
    if args.row and args.row not in rows:
        sys.exit(f"row {args.row} is not in the matrix (rows are {min(rows)}-{max(rows)})")
    src = Path(args.source)
    if not src.exists():
        sys.exit(f"no such file: {src}")

    if args.name:
        screen, os_name, browser, device, fname = ("(off-matrix)", "-", "-", "-", args.name)
    else:
        screen, os_name, browser, device, fname = rows[args.row]
    args.out_dir.mkdir(parents=True, exist_ok=True)
    dest = args.out_dir / fname

    img = stamp(src, args.overlay, args.corner)
    img.save(dest)

    label = f"row {args.row}" if args.row else "off-matrix"
    print(f"{label}: {screen} / {os_name} / {browser} / {device}")
    print(f"  overlay -> {args.overlay!r}")
    print(f"  saved   -> {dest}  ({img.width}x{img.height})")
    print("\nOpen it and confirm, in the pixels: the EMS URL, the browser/OS/device identity,")
    print("the overlay legible and not covering the content being judged, and the screen in the")
    print("state the row claims. Then move the filename into the row's Evidence column.")


if __name__ == "__main__":
    main()
