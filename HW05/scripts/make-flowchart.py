#!/usr/bin/env python3
"""Generate the continuous-performance flowchart used by the PDF report."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "assets" / "continuous-performance-flow.png"
REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")


def main():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    canvas = Image.new("RGB", (1800, 720), "white")
    draw = ImageDraw.Draw(canvas)
    title_font = ImageFont.truetype(str(BOLD), 34)
    box_font = ImageFont.truetype(str(BOLD), 25)
    note_font = ImageFont.truetype(str(REGULAR), 22)
    navy, teal = "#17324D", "#2E6F78"

    draw.text((60, 30), "Commit-aware performance regression gate", font=title_font, fill=navy)

    def box(x, y, w, h, text, fill="#EAF3F6"):
        draw.rounded_rectangle((x, y, x + w, y + h), 16, fill=fill, outline=teal, width=4)
        lines = text.split("\n")
        sizes = [draw.textbbox((0, 0), line, font=box_font) for line in lines]
        total = sum(rect[3] - rect[1] for rect in sizes) + (len(lines) - 1) * 6
        cy = y + (h - total) / 2
        for line, rect in zip(lines, sizes):
            width, height = rect[2] - rect[0], rect[3] - rect[1]
            draw.text((x + (w - width) / 2, cy), line, font=box_font, fill=navy)
            cy += height + 6

    def arrow(x1, y1, x2, y2, label=""):
        draw.line((x1, y1, x2, y2), fill=navy, width=5)
        if abs(x2 - x1) >= abs(y2 - y1):
            direction = 1 if x2 > x1 else -1
            tip = [(x2, y2), (x2 - direction * 22, y2 - 14), (x2 - direction * 22, y2 + 14)]
        else:
            direction = 1 if y2 > y1 else -1
            tip = [(x2, y2), (x2 - 14, y2 - direction * 22), (x2 + 14, y2 - direction * 22)]
        draw.polygon(tip, fill=navy)
        if label:
            draw.text(((x1 + x2) / 2 + 8, (y1 + y2) / 2 - 28), label, font=note_font, fill=teal)

    top_y, w, h = 150, 260, 110
    xs = [40, 340, 640, 940, 1240]
    for x, text in zip(xs, ["Commit / PR", "Risky paths?", "Seed + smoke", "Short Load", "SLO or p95\nregression?"]):
        box(x, top_y, w, h, text)
    for left, right in zip(xs, xs[1:]):
        arrow(left + w, top_y + h / 2, right - 10, top_y + h / 2)

    box(1240, 390, w, h, "Pass + update\nhistory", "#E6F4EA")
    box(900, 390, w, h, "Confirmation\nrun")
    box(560, 390, w, h, "Reproduced?")
    box(220, 390, w, h, "Block + attach\nraw evidence", "#FCE8E6")
    arrow(1370, top_y + h, 1370, 380, "No")
    arrow(1240, top_y + h / 2, 1170, 445, "Yes")
    arrow(900, 445, 830, 445)
    arrow(560, 445, 490, 445, "Yes")
    arrow(690, 500, 690, 585, "No")
    draw.text((535, 610), "Mark as noise; do not block", font=note_font, fill=teal)
    draw.text((40, 665), "Scheduled lane: nightly Stress + Spike; release-candidate Soak", font=note_font, fill=navy)
    canvas.save(OUT, format="PNG", optimize=True)
    print(f"written: {OUT}")


if __name__ == "__main__":
    main()
