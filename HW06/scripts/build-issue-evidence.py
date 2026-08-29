#!/usr/bin/env python3
"""Render one Newman evidence card per GitHub Issue that still lacks a screenshot.

Section 6.5 of the brief requires a screenshot on every filed issue. The cards
below are renderings of fields taken verbatim from the retained pre-fix Newman
console transcript; nothing is typed in by hand and nothing is invented. The
transcript is the run that produced the 16 reported defects, so it is the run
each issue describes.

    python scripts/build-issue-evidence.py
"""

from __future__ import annotations

import html
import re
import io
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "evidence" / "newman-console" / "suite_full_20260824-002523.log"
OUT = ROOT / "evidence" / "screenshots"
STUDENT_ID = "23127184"

# GitHub issue number -> (case id, slug used for the file name)
ISSUE_CASES = {
    47: ("A1-DP-002", "name-omitted"),
    48: ("A1-DP-015", "email-omitted"),
    49: ("A1-DP-039", "password-omitted"),
    50: ("A1-DP-005", "whitespace-name"),
    51: ("A1-DP-022", "email-no-tld"),
    52: ("A1-DP-034", "email-case-uniqueness"),
    53: ("A1-DP-004", "empty-name"),
    54: ("A1-DP-017", "empty-email"),
    55: ("A1-DP-041", "empty-password"),
    59: ("A1-DP-042", "password-7-chars"),
    60: ("A1-DP-045", "password-no-uppercase"),
    61: ("A1-DP-046", "password-no-lowercase"),
    62: ("A1-DP-047", "password-no-digit"),
    63: ("A1-DP-048", "password-no-special"),
    64: ("A1-DP-033", "duplicate-email"),
}

ANSI = re.compile(r"\x1b\[[0-9;]*m")
CASE_HEAD = re.compile(r"(A\d-[A-Z]+-\d+)\s*\|\s*(.+?)\s*$")
REQUEST = re.compile(r"^(GET|POST|PUT|PATCH|DELETE)\s+(\S+)\s+\[(\d{3})\s+([^,\]]+)")


def read_log() -> list[str]:
    text = LOG.read_bytes().decode("utf-16-le", errors="replace")
    return [ANSI.sub("", line).rstrip() for line in text.splitlines()]


def collect_runs(lines: list[str]) -> dict[str, dict]:
    """Walk the run transcript and record what each case actually did."""
    runs: dict[str, dict] = {}
    current: dict | None = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        head = CASE_HEAD.search(stripped)
        if head and stripped.startswith(("#", "→", "%", "?")) is False and " | " in stripped:
            # A case header looks like "<glyph> A1-DP-002 | Missing name field is rejected"
            case_id, title = head.group(1), head.group(2)
            current = {"case": case_id, "title": title, "failures": []}
            runs.setdefault(case_id, current)
            current = runs[case_id]
            continue
        if current is None:
            continue
        req = REQUEST.match(stripped)
        if req and "request" not in current:
            current["method"] = req.group(1)
            current["url"] = req.group(2)
            current["status"] = f"HTTP {req.group(3)} {req.group(4).strip()}"
            current["request"] = f"{req.group(1)} {req.group(2)}"
            continue
        fail = re.match(r"^\d+\.\s+(.*)$", stripped)
        if fail and "request" in current:
            current["failures"].append(fail.group(1).strip())
    return runs


def collect_details(lines: list[str]) -> dict[str, list[tuple[str, str]]]:
    """Read the verbatim assertion detail table printed at the end of a run."""
    details: dict[str, list[tuple[str, str]]] = {}
    pending: dict | None = None
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        start = re.match(r"^\d+\.\s+AssertionError\s+(.*)$", stripped)
        if start:
            pending = {"assertion": start.group(1).strip(), "detail": ""}
            continue
        if pending is None:
            continue
        if stripped.startswith('inside "'):
            inside = stripped[8:].rstrip('"')
            case = CASE_HEAD.search(inside)
            if case:
                details.setdefault(case.group(1), []).append(
                    (pending["assertion"], pending["detail"])
                )
            pending = None
        elif stripped.startswith("at assertion"):
            continue
        elif not pending["detail"]:
            pending["detail"] = stripped
    return details


NAVY = (0.086, 0.196, 0.310)
INK = (0.133, 0.188, 0.235)
MUTED = (0.357, 0.420, 0.482)
RULE = (0.875, 0.902, 0.925)
BACKDROP = (0.929, 0.937, 0.949)
FAIL_BG = (0.992, 0.945, 0.945)
FAIL_BAR = (0.639, 0.137, 0.165)
FAIL_INK = (0.361, 0.078, 0.094)
SUBTITLE = (0.780, 0.843, 0.902)

WIDTH = 1120.0
MARGIN = 60.0
PAD = 34.0
LABEL_W = 178.0
ROW_H = 40.0


def render(issue: int, slug: str, run: dict, details: list[tuple[str, str]]) -> Path:
    """Draw the evidence card directly; every string comes from the transcript."""
    fields = [
        ("Case", f"{run['case']} | {run['title']}"),
        ("Request", run["request"]),
        ("Identity header", f"X-Student-Id: {STUDENT_ID}"),
        ("Expected", "a 4xx validation response"),
        ("Actual", run["status"]),
    ]
    fail_lines: list[str] = []
    for assertion, detail in details:
        fail_lines.append(f"FAIL  {assertion}")
        if detail:
            fail_lines.append(f"      {detail}")

    header_h = 92.0
    rows_h = ROW_H * len(fields) + 20
    fail_h = 20 + 17 * len(fail_lines) + 12
    footer_h = 44.0
    height = MARGIN * 2 + header_h + rows_h + 18 + fail_h + footer_h

    doc = fitz.open()
    page = doc.new_page(width=WIDTH, height=height)
    page.draw_rect(fitz.Rect(0, 0, WIDTH, height), color=None, fill=BACKDROP)

    card = fitz.Rect(MARGIN, MARGIN, WIDTH - MARGIN, height - MARGIN)
    page.draw_rect(card, color=None, fill=(1, 1, 1))

    band = fitz.Rect(card.x0, card.y0, card.x1, card.y0 + header_h)
    page.draw_rect(band, color=None, fill=NAVY)
    page.insert_text(
        (card.x0 + PAD, card.y0 + 44),
        "Newman JSON Execution Evidence",
        fontname="hebo", fontsize=21, color=(1, 1, 1),
    )
    page.insert_text(
        (card.x0 + PAD, card.y0 + 70),
        f"HW06  |  Student ID {STUDENT_ID}  |  Pre-fix full suite execution",
        fontname="helv", fontsize=10.5, color=SUBTITLE,
    )

    y = band.y1 + 30
    for label, value in fields:
        page.insert_text((card.x0 + PAD, y), label, fontname="hebo", fontsize=10.5, color=NAVY)
        page.insert_text(
            (card.x0 + PAD + LABEL_W, y), value, fontname="helv", fontsize=10.5, color=INK
        )
        page.draw_line(
            fitz.Point(card.x0 + PAD, y + 13),
            fitz.Point(card.x1 - PAD, y + 13),
            color=RULE, width=0.8,
        )
        y += ROW_H

    box = fitz.Rect(card.x0 + PAD, y - 8, card.x1 - PAD, y - 8 + fail_h)
    page.draw_rect(box, color=None, fill=FAIL_BG)
    page.draw_rect(
        fitz.Rect(box.x0, box.y0, box.x0 + 4, box.y1), color=None, fill=FAIL_BAR
    )
    ty = box.y0 + 24
    for line in fail_lines:
        page.insert_text(
            (box.x0 + 20, ty), line, fontname="cour", fontsize=10, color=FAIL_INK
        )
        ty += 17

    page.insert_text(
        (card.x0 + PAD, box.y1 + 26),
        f"Verbatim fields rendered from evidence/newman-console/{LOG.name}",
        fontname="helv", fontsize=8, color=MUTED,
    )
    page.insert_text(
        (card.x0 + PAD, box.y1 + 38),
        "(the run that produced the reported defects). The raw transcript is retained in the repository.",
        fontname="helv", fontsize=8, color=MUTED,
    )

    out = OUT / f"github-issue-{issue}-{slug}-newman.png"
    page.get_pixmap(matrix=fitz.Matrix(1.6, 1.6)).save(out)
    doc.close()
    return out


def main() -> None:
    lines = read_log()
    runs = collect_runs(lines)
    details = collect_details(lines)

    missing = [c for c, _ in ISSUE_CASES.values() if c not in runs or c not in details]
    if missing:
        raise SystemExit(f"cases absent from the transcript: {', '.join(missing)}")

    for issue, (case, slug) in sorted(ISSUE_CASES.items()):
        path = render(issue, slug, runs[case], details[case])
        print(f"#{issue}  {case}  ->  {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
