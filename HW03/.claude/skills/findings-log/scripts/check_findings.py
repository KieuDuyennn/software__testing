#!/usr/bin/env python3
"""Validate a markdown findings log.

Reads EVERY markdown table whose header has an ID column and a Severity column -- a log
usually has a summary table plus per-finding detail, separated by prose, and a parser that
stopped at the first break would silently ignore most of the file. Rows describing the same
ID across tables are merged (non-empty cells win) so the summary and the detail are treated
as one record.

Checks:
  * IDs unique within each table, and non-empty
  * required columns present and non-empty per record (configurable with --require)
  * severity values legal for the record's Type (Bug -> blocker..trivial, Usability -> 0..4)
  * evidence filenames resolve on disk under --evidence-root, which may be repeated when one log
    aggregates findings whose screenshots live in more than one folder (a name resolving under any
    one of the roots is accepted)
  * counts by type and severity, so a header total can be checked against reality

A record is exempted from field and severity checks only when an explicit Status column says
withdrawn. Earlier versions looked for the substring "withdraw" anywhere in the row, which
silently disabled validation for any finding whose description happened to mention
withdrawing money, a Withdraw button, or a withdrawal form.

Column matching is fuzzy by substring so slightly different column names still work. Because
that can mis-resolve, the resolved mapping is printed -- check it if a result surprises you.

Usage:
    check_findings.py LOG.md [--evidence-root DIR]... [--expect N]
                             [--require "Description,Severity,Evidence"] [--quiet]

Exit code 1 if any check fails.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

BUG_SEVERITIES = {"blocker", "critical", "major", "minor", "trivial"}
USABILITY_SEVERITIES = {"0", "1", "2", "3", "4"}
EMPTY = {"", "-", "--", "n/a", "na", "tbd", "todo", "?", "—"}
IMG_RE = re.compile(r"([\w./ -]+?\.(?:png|jpe?g|gif|webp|mp4|webm))", re.IGNORECASE)


def split_row(raw: str) -> list[str]:
    """Split a markdown row, honouring \\| as an escaped literal pipe."""
    placeholder = "\x00"
    return [
        c.strip().replace(placeholder, "|")
        for c in raw.strip().strip("|").replace(r"\|", placeholder).split("|")
    ]


def find_col(headers: list[str], *needles: str) -> int | None:
    for idx, head in enumerate(headers):
        low = head.lower()
        if any(n in low for n in needles):
            return idx
    return None


def is_label(cell: str) -> bool:
    """A header cell is a short label, never a sentence."""
    return len(cell) <= 40 and cell.count(" ") <= 5


def is_findings_header(cells: list[str]) -> bool:
    # Every cell of a real header is a short label. Without this test, a DATA row whose prose
    # happens to contain "severity" and "ID" -- e.g. a not-logged table explaining that an
    # unverified report would put "a severity" in front of developers and "gets an ID when it
    # is seen" -- is read as a header, re-arms the parser, and swallows every row after it.
    # Rejecting a genuine header is loud (exit 2, "no findings table found"); accepting a fake
    # one is silent, so this errs towards strict.
    if not cells or not all(is_label(c) for c in cells):
        return False
    low = [c.lower() for c in cells]
    return find_col(low, "id") is not None and find_col(low, "sever") is not None


def parse(path: Path) -> tuple[list[str], list[tuple[int, list[str]]]]:
    """Return (headers of the first findings table, [(table_index, cells), ...])."""
    headers: list[str] = []
    rows: list[tuple[int, list[str]]] = []
    table_idx = -1
    in_table = False
    for raw in path.read_text(encoding="utf-8-sig").splitlines():
        line = raw.strip()
        if not line.startswith("|"):
            in_table = False
            continue
        cells = split_row(line)
        if set("".join(cells)) <= set("-: "):
            continue
        if is_findings_header(cells):
            # Re-arm on every header-shaped row, so tables after prose are not dropped.
            if not headers:
                headers = cells
            table_idx += 1
            in_table = True
            continue
        if in_table and headers:
            rows.append((table_idx, cells + [""] * (len(headers) - len(cells))))
    return headers, rows


def merge(records: dict[str, list[str]], key: str, cells: list[str], width: int) -> None:
    """Merge a row into an existing record for the same ID, preferring non-empty cells."""
    existing = records.get(key)
    if existing is None:
        records[key] = cells[:width] + [""] * max(0, width - len(cells))
        return
    for i in range(width):
        if existing[i].strip().lower() in EMPTY and i < len(cells):
            existing[i] = cells[i]


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("log", type=Path)
    ap.add_argument("--evidence-root", type=Path, action="append", dest="evidence_roots")
    ap.add_argument("--expect", type=int, help="fail if the finding count differs")
    ap.add_argument(
        "--require",
        default="description,sever,evidence",
        help="comma-separated header substrings that must be non-empty in every record",
    )
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    if not args.log.is_file():
        print(f"not a file: {args.log}", file=sys.stderr)
        return 2

    headers, raw_rows = parse(args.log)
    if not headers:
        print(
            "No findings table found. Expected a markdown table with an 'ID' column and a "
            "'Severity' column.",
            file=sys.stderr,
        )
        return 2
    if not raw_rows:
        print("Findings table has a header but no rows.", file=sys.stderr)
        return 2

    width = len(headers)
    id_col = find_col(headers, "id")
    type_col = find_col(headers, "type", "loại")
    sev_col = find_col(headers, "sever", "mức")
    ev_col = find_col(headers, "evidence", "ảnh", "screenshot")
    status_col = find_col(headers, "status", "trạng thái")

    problems: list[str] = []

    # Duplicate IDs are only a defect within one table -- the same ID in a summary table and a
    # detail table is one finding described twice, which is normal.
    per_table: dict[int, list[str]] = {}
    for table_idx, cells in raw_rows:
        per_table.setdefault(table_idx, []).append(cells[id_col])
    for table_idx, ids in per_table.items():
        for dupe, n in Counter(i for i in ids if i.strip()).items():
            if n > 1:
                problems.append(f"duplicate finding ID within one table: {dupe} ({n} rows)")
    if any(not c[id_col].strip() or c[id_col].strip().lower() in EMPTY for _, c in raw_rows):
        problems.append("one or more rows have no ID")

    records: dict[str, list[str]] = {}
    for _, cells in raw_rows:
        key = cells[id_col].strip()
        if key:
            merge(records, key, cells, width)

    required_cols: list[tuple[str, int]] = []
    for needle in [n.strip() for n in args.require.split(",") if n.strip()]:
        col = find_col(headers, needle)
        if col is None:
            problems.append(f"required column matching '{needle}' not found in the table header")
        else:
            required_cols.append((needle, col))

    types: Counter[str] = Counter()
    severities: Counter[str] = Counter()
    withdrawn_ids: list[str] = []

    for fid, row in records.items():
        row_type = row[type_col].strip().lower() if type_col is not None else ""
        withdrawn = status_col is not None and "withdraw" in row[status_col].strip().lower()
        if withdrawn:
            withdrawn_ids.append(fid)
        types[row_type or "unspecified"] += 1

        for _, col in required_cols:
            if row[col].strip().lower() in EMPTY and not withdrawn:
                problems.append(f"{fid}: column '{headers[col]}' is empty")

        if sev_col is not None:
            sev = row[sev_col].strip().lower()
            sev_token = re.sub(r"[^a-z0-9]", "", sev.split()[0]) if sev else ""
            severities[sev_token or "empty"] += 1
            if withdrawn or not sev_token:
                continue
            if row_type.startswith("bug"):
                if sev_token not in BUG_SEVERITIES:
                    problems.append(
                        f"{fid}: Bug severity '{row[sev_col]}' is not one of "
                        f"{'/'.join(sorted(BUG_SEVERITIES))}"
                    )
            elif row_type.startswith("usab"):
                if sev_token not in USABILITY_SEVERITIES:
                    problems.append(
                        f"{fid}: Usability severity '{row[sev_col]}' is not 0-4 "
                        "(Nielsen severity scale)"
                    )
            elif sev_token not in BUG_SEVERITIES | USABILITY_SEVERITIES:
                # Type unrecognised, so the scale is unknown -- still reject a value that is
                # legal on neither scale rather than passing it silently.
                problems.append(
                    f"{fid}: severity '{row[sev_col]}' is legal on neither scale, and Type "
                    f"'{row[type_col] if type_col is not None else ''}' was not recognised as "
                    "Bug or Usability, so the intended scale cannot be checked"
                )

    if ev_col is not None and args.evidence_roots:
        roots = args.evidence_roots
        bad = [r for r in roots if not r.is_dir()]
        for r in bad:
            problems.append(f"--evidence-root is not a directory: {r}")
        roots = [r for r in roots if r.is_dir()]
        if roots:
            for fid, row in records.items():
                cell = row[ev_col]
                if cell.strip().lower() in EMPTY:
                    continue
                for name in IMG_RE.findall(cell):
                    name = name.strip()
                    # A cell may name a file by bare filename or by a repo-relative path; either
                    # form counts as resolved if it lands under any one of the roots given.
                    if any((r / name).exists() or list(r.rglob(Path(name).name)) for r in roots):
                        continue
                    where = " or ".join(str(r) for r in roots)
                    problems.append(f"{fid}: evidence file not found under {where}: {name}")

    if args.expect is not None and len(records) != args.expect:
        problems.append(f"expected {args.expect} findings, found {len(records)}")

    if not args.quiet:
        print(f"{args.log.name}: {len(records)} findings "
              f"({len(raw_rows)} rows across {len(per_table)} table(s))")
        resolved = {
            "ID": id_col, "Type": type_col, "Severity": sev_col,
            "Evidence": ev_col, "Status": status_col,
        }
        print("  columns resolved: " + ", ".join(
            f"{k}->{headers[v] if v is not None else 'MISSING'}" for k, v in resolved.items()
        ))
        print("  by type:     " + ", ".join(f"{k}={v}" for k, v in sorted(types.items())))
        print("  by severity: " + ", ".join(f"{k}={v}" for k, v in sorted(severities.items())))
        if withdrawn_ids:
            print(f"  withdrawn (checks skipped): {', '.join(sorted(withdrawn_ids))}")
        if status_col is None:
            print("  note: no Status column, so no record can be exempted as withdrawn. Add one\n"
                  "        if you need to keep a withdrawn finding's row without failing checks.")

    if problems:
        sys.stdout.flush()
        print(f"\nFAIL ({len(problems)} problem(s))", file=sys.stderr)
        for p in problems:
            print(f"  - {p}", file=sys.stderr)
        return 1
    if not args.quiet:
        print("\nOK -- IDs unique per table, required fields present, severities legal"
              + (", evidence resolves" if (ev_col is not None and args.evidence_roots) else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
