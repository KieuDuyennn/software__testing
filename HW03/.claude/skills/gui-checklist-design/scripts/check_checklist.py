#!/usr/bin/env python3
"""Validate a markdown GUI checklist and regenerate its traceability tables.

The checklist is expected to contain one or more markdown tables whose header is

    | Item ID | Aspect | Reference Source | Verification Rule | Expected Behavior |

Column names are matched case-insensitively and only the first three are required, so a
checklist with extra trailing columns still works.

Checks run:
  * item IDs unique, and contiguous within each aspect prefix (IA01-01, IA01-02, ...)
  * per-aspect and total counts
  * citation coverage: which framework principles are cited, which are cited by nobody,
    and which are cited so widely they are probably being used as a catch-all
  * evidence references (image filenames in any column) that do not exist on disk

With --emit-traceability, prints source -> item tables generated from the checklist's own
Reference Source column, ready to paste into the sources document. Regenerating beats
hand-editing: hand-maintained traceability goes stale the first time items are renumbered.

Usage:
    check_checklist.py CHECKLIST.md [--emit-traceability] [--evidence-root DIR]
                                    [--expect N] [--quiet]

Exit code is 1 if any check fails, so it can gate a commit.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

# Principles worth reporting as uncited. Extend for house frameworks; the script also
# reports any citation token it sees that is not in this map, so nothing is silently lost.
KNOWN_PRINCIPLES: dict[str, list[str]] = {
    "Nielsen": [f"H{i}" for i in range(1, 11)],
    "Norman": [f"P{i}" for i in range(1, 7)],
    "Shneiderman": [f"R{i}" for i in range(1, 9)],
}

ID_RE = re.compile(r"^([A-Za-z]+\d*)-(\d+)$")
CITE_RE = re.compile(r"\b(Nielsen|Norman|Shneiderman)\s+([HPR]\d{1,2})\b")
WCAG_RE = re.compile(r"\bSC\s*(\d+\.\d+\.\d+)\b")
SLIDE_RE = re.compile(r"\bp\.\s?(\d{1,3})\b")
IMG_RE = re.compile(r"([\w./-]+\.(?:png|jpe?g|gif|webp))", re.IGNORECASE)


class Item:
    __slots__ = ("item_id", "prefix", "number", "aspect", "source", "rest", "line")

    def __init__(self, cells: list[str], line: int) -> None:
        self.item_id = cells[0]
        self.aspect = cells[1] if len(cells) > 1 else ""
        self.source = cells[2] if len(cells) > 2 else ""
        self.rest = " ".join(cells[3:])
        self.line = line
        m = ID_RE.match(self.item_id)
        self.prefix, self.number = (m.group(1), int(m.group(2))) if m else (self.item_id, -1)


def split_row(raw: str) -> list[str]:
    return [c.strip() for c in raw.strip().strip("|").split("|")]


def parse(path: Path) -> list[Item]:
    """Collect rows from every table that looks like a checklist table."""
    items: list[Item] = []
    in_table = False
    for lineno, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cells = split_row(line)
        lowered = [c.lower() for c in cells]
        if len(cells) >= 3 and lowered[0] in ("item id", "item", "id"):
            in_table = "reference source" in lowered or "aspect" in lowered
            continue
        if set("".join(cells)) <= set("-: "):  # separator row
            continue
        if in_table and ID_RE.match(cells[0]):
            items.append(Item(cells, lineno))
    return items


def check_ids(items: list[Item], problems: list[str]) -> None:
    dupes = [i for i, n in Counter(it.item_id for it in items).items() if n > 1]
    if dupes:
        problems.append(f"duplicate item IDs: {', '.join(sorted(dupes))}")
    by_prefix: dict[str, list[int]] = defaultdict(list)
    for it in items:
        by_prefix[it.prefix].append(it.number)
    for prefix, numbers in sorted(by_prefix.items()):
        expected = set(range(1, len(numbers) + 1))
        missing = sorted(expected - set(numbers))
        extra = sorted(n for n in set(numbers) - expected)
        if missing or extra:
            problems.append(
                f"{prefix} is not contiguous 1..{len(numbers)}: "
                f"missing {missing or 'none'}, unexpected {extra or 'none'}"
            )


def citations(items: list[Item]) -> tuple[dict[str, list[str]], dict[str, list[str]], dict[str, list[str]]]:
    frameworks: dict[str, list[str]] = defaultdict(list)
    wcag: dict[str, list[str]] = defaultdict(list)
    slides: dict[str, list[str]] = defaultdict(list)
    for it in items:
        text = f"{it.source} {it.rest}"
        for fw, code in CITE_RE.findall(text):
            frameworks[f"{fw} {code}"].append(it.item_id)
        for sc in WCAG_RE.findall(text):
            wcag[f"WCAG SC {sc}"].append(it.item_id)
        for page in SLIDE_RE.findall(it.source):
            slides[f"p.{page}"].append(it.item_id)
    return frameworks, wcag, slides


def check_evidence(items: list[Item], root: Path | None, problems: list[str]) -> None:
    if root is None:
        return
    missing: set[str] = set()
    for it in items:
        for name in IMG_RE.findall(f"{it.source} {it.rest}"):
            candidate = (root / name).resolve()
            if not candidate.exists() and not list(root.rglob(Path(name).name)):
                missing.add(name)
    if missing:
        problems.append(
            f"{len(missing)} referenced image(s) not found under {root}: "
            + ", ".join(sorted(missing)[:8])
            + (" ..." if len(missing) > 8 else "")
        )


def emit_traceability(frameworks, wcag, slides) -> None:
    def table(title: str, mapping: dict[str, list[str]]) -> None:
        if not mapping:
            return
        print(f"\n### {title}\n")
        print("| Source | Items citing it |")
        print("| --- | --- |")

        def key(label: str):
            nums = re.findall(r"\d+", label)
            return (re.sub(r"[\d.]", "", label), [int(n) for n in nums])

        for label in sorted(mapping, key=key):
            print(f"| {label} | {', '.join(sorted(set(mapping[label])))} |")

    print("<!-- generated by check_checklist.py --emit-traceability; do not hand-edit -->")
    table("By heuristic framework", frameworks)
    table("By accessibility standard", wcag)
    table("By course-slide page", slides)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("checklist", type=Path)
    ap.add_argument("--emit-traceability", action="store_true", help="print regenerated source->item tables")
    ap.add_argument("--evidence-root", type=Path, help="directory to resolve referenced image filenames against")
    ap.add_argument("--expect", type=int, help="fail if the total item count differs from this")
    ap.add_argument("--quiet", action="store_true", help="print problems only")
    args = ap.parse_args()

    if not args.checklist.is_file():
        print(f"not a file: {args.checklist}", file=sys.stderr)
        return 2

    items = parse(args.checklist)
    if not items:
        print(
            "No checklist rows found. Expected a markdown table whose first column header is "
            "'Item ID' and whose rows start with IDs like IA01-01.",
            file=sys.stderr,
        )
        return 2

    problems: list[str] = []
    check_ids(items, problems)
    check_evidence(items, args.evidence_root, problems)
    frameworks, wcag, slides = citations(items)

    per_prefix = Counter(it.prefix for it in items)
    if not args.quiet:
        counts = "  ".join(f"{p}: {n}" for p, n in sorted(per_prefix.items()))
        print(f"{args.checklist.name}: {len(items)} items   ({counts})")

    if args.expect is not None and len(items) != args.expect:
        problems.append(f"expected {args.expect} items, found {len(items)}")

    # An unreadable citation must never masquerade as a missing one. This parser recognises a
    # specific syntax -- "Nielsen H1", "Norman P3", "Shneiderman R7", "SC 1.4.3" -- so a
    # checklist citing "Nielsen's heuristic #1" would otherwise be reported as citing nothing,
    # and whoever acted on that report would rewrite a perfectly well-grounded checklist.
    unreadable = [
        it.item_id
        for it in items
        if it.source.strip()
        and not CITE_RE.search(f"{it.source} {it.rest}")
        and not WCAG_RE.search(f"{it.source} {it.rest}")
        and not SLIDE_RE.search(it.source)
    ]
    if unreadable:
        problems.append(
            f"{len(unreadable)} item(s) have a Reference Source this parser cannot read: "
            + ", ".join(unreadable[:10])
            + (" ..." if len(unreadable) > 10 else "")
            + ". Expected forms: 'Nielsen H1', 'Norman P3', 'Shneiderman R7', 'WCAG 2.1 SC 1.4.3'"
            ", 'Slides p.17'. Fix the citation FORMAT -- do not read the coverage numbers below "
            "as a real gap until this is zero."
        )

    if not args.quiet:
        print("\nCitation coverage")
        if unreadable:
            print(f"  ! {len(unreadable)} item(s) have unparsed citations -- the counts below are "
                  "therefore a LOWER BOUND, not a coverage measurement")
        for fw, codes in KNOWN_PRINCIPLES.items():
            cited = [c for c in codes if frameworks.get(f"{fw} {c}")]
            uncited = [c for c in codes if not frameworks.get(f"{fw} {c}")]
            print(f"  {fw}: {len(cited)}/{len(codes)} cited" + (f" -- uncited: {', '.join(uncited)}" if uncited else ""))
        if wcag:
            print(f"  Accessibility criteria: {', '.join(sorted(wcag))}")
        if slides:
            print(f"  Slide pages cited: {', '.join(sorted(slides, key=lambda s: int(s[2:])))}")

        heavy = [(label, ids) for label, ids in frameworks.items() if len(set(ids)) >= 5]
        for label, ids in sorted(heavy, key=lambda kv: -len(set(kv[1]))):
            print(
                f"  ! {label} is cited by {len(set(ids))} items ({', '.join(sorted(set(ids)))}) -- "
                "check it is not being used as a catch-all"
            )

    if args.emit_traceability:
        emit_traceability(frameworks, wcag, slides)

    if problems:
        sys.stdout.flush()
        print("\nFAIL", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("\nOK -- IDs unique and contiguous" + (", evidence references resolve" if args.evidence_root else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
