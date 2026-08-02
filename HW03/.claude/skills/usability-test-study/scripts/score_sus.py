#!/usr/bin/env python3
"""Score SUS or UEQ-S questionnaire responses from a CSV.

Hand-scoring SUS gets the reverse-scored even items wrong often enough that it is worth
automating. UEQ-S needs a -3..+3 transform and a pragmatic/hedonic split.

CSV format -- one row per participant, first column the participant label:

    participant,q1,q2,q3,q4,q5,q6,q7,q8,q9,q10
    P1,4,2,5,1,4,2,5,2,4,1

  SUS   expects 10 columns of 1..5 (1 strongly disagree .. 5 strongly agree),
        odd items positively worded, even items negatively worded.
  UEQ-S expects 8 columns of 1..7, each item presented with the NEGATIVE term on the
        left (1 = obstructive .. 7 = supportive). Items 1-4 are pragmatic quality,
        items 5-8 hedonic quality. If your form presented some items flipped, pass
        --reverse with their 1-based positions.

Usage:
    score_sus.py responses.csv --instrument sus
    score_sus.py responses.csv --instrument ueq-s [--reverse 3,7]
    score_sus.py responses.csv --instrument sus --markdown
"""

from __future__ import annotations

import argparse
import csv
import statistics
import sys
from pathlib import Path

# Sauro & Lewis curved grading, for context only -- with five participants these are
# descriptive labels, not measurements. Do not report them as benchmarked results.
SUS_GRADES = [
    (84.1, "A+"), (80.8, "A"), (78.9, "A-"), (77.2, "B+"), (74.1, "B"),
    (72.6, "B-"), (71.1, "C+"), (65.0, "C"), (62.7, "C-"), (51.7, "D"), (0.0, "F"),
]
# Bangor's adjective figures are the MEAN SUS score of respondents choosing each adjective
# (Worst imaginable 12.5, Awful 20.3, Poor 35.7, OK 50.9, Good 71.4, Excellent 85.5, Best
# imaginable 90.9) -- they are anchors, not band floors. Using them as floors biases every
# label downward: a perfectly neutral questionnaire (all 3s = 50.0) would come out "Poor".
# So bands are the midpoints between adjacent anchors, i.e. nearest-anchor labelling.
SUS_ADJECTIVES = [
    (88.2, "Best imaginable"), (78.5, "Excellent"), (61.2, "Good"), (43.3, "OK"),
    (28.0, "Poor"), (16.4, "Awful"), (0.0, "Worst imaginable"),
]
UEQ_S_ITEMS = [
    "obstructive / supportive", "complicated / easy", "inefficient / efficient",
    "confusing / clear", "boring / exciting", "not interesting / interesting",
    "conventional / inventive", "usual / leading edge",
]


def band(value: float, table: list[tuple[float, str]]) -> str:
    for threshold, label in table:
        if value >= threshold:
            return label
    return table[-1][1]


def read_rows(path: Path, expected: int) -> list[tuple[str, list[float]]]:
    with path.open(newline="", encoding="utf-8-sig") as fh:
        rows = [r for r in csv.reader(fh) if r and any(c.strip() for c in r)]
    if not rows:
        raise SystemExit("empty CSV")
    # Drop a header row if its data cells are not numeric.
    try:
        [float(c) for c in rows[0][1 : expected + 1]]
    except ValueError:
        rows = rows[1:]
    out: list[tuple[str, list[float]]] = []
    for row in rows:
        label = row[0].strip() or f"P{len(out) + 1}"
        cells = [c.strip() for c in row[1 : expected + 1]]
        if len(cells) != expected or any(c == "" for c in cells):
            raise SystemExit(
                f"{label}: expected {expected} response values, got {len([c for c in cells if c])}"
            )
        try:
            values = [float(c) for c in cells]
        except ValueError:
            raise SystemExit(f"{label}: non-numeric response value in {cells}")
        out.append((label, values))
    if not out:
        raise SystemExit(
            f"{path}: header row only, no participant responses yet -- nothing to score. "
            "Add one row per real session; never a placeholder or example row."
        )
    return out


def score_sus(values: list[float]) -> float:
    for i, v in enumerate(values, 1):
        if not 1 <= v <= 5:
            raise SystemExit(f"SUS item {i} value {v} out of range 1..5")
    total = 0.0
    for i, v in enumerate(values, 1):
        total += (v - 1) if i % 2 == 1 else (5 - v)
    return total * 2.5


def score_ueq_s(values: list[float], reverse: set[int]) -> tuple[float, float, float, list[float]]:
    for i, v in enumerate(values, 1):
        if not 1 <= v <= 7:
            raise SystemExit(f"UEQ-S item {i} value {v} out of range 1..7")
    transformed = [
        (8 - v) - 4 if i in reverse else v - 4 for i, v in enumerate(values, 1)
    ]
    pragmatic = statistics.fmean(transformed[:4])
    hedonic = statistics.fmean(transformed[4:])
    overall = statistics.fmean(transformed)
    return overall, pragmatic, hedonic, transformed


def summarise(name: str, scores: list[float]) -> dict[str, float]:
    return {
        "mean": statistics.fmean(scores),
        "sd": statistics.stdev(scores) if len(scores) > 1 else 0.0,
        "min": min(scores),
        "max": max(scores),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("responses", type=Path)
    ap.add_argument("--instrument", choices=("sus", "ueq-s"), required=True)
    ap.add_argument("--reverse", default="", help="UEQ-S only: 1-based item positions presented flipped, e.g. 3,7")
    ap.add_argument("--markdown", action="store_true", help="emit markdown tables for pasting into a report")
    args = ap.parse_args()

    if not args.responses.is_file():
        print(f"not a file: {args.responses}", file=sys.stderr)
        return 2

    if args.instrument == "sus":
        rows = read_rows(args.responses, 10)
        scored = [(label, score_sus(values)) for label, values in rows]
        stats = summarise("SUS", [s for _, s in scored])
        if args.markdown:
            print("| Participant | SUS score | Adjective |")
            print("| --- | --- | --- |")
            for label, s in scored:
                print(f"| {label} | {s:.1f} | {band(s, SUS_ADJECTIVES)} |")
            print(f"| **Mean** | **{stats['mean']:.1f}** | {band(stats['mean'], SUS_ADJECTIVES)} |")
            print(f"\nn = {len(scored)}, SD = {stats['sd']:.1f}, range {stats['min']:.1f}-{stats['max']:.1f}. "
                  f"Curved grade of the mean: {band(stats['mean'], SUS_GRADES)}. "
                  "Reported descriptively; n is too small for a statistical claim.")
        else:
            print(f"SUS -- {len(scored)} participants\n")
            for label, s in scored:
                print(f"  {label:<12} {s:6.1f}   {band(s, SUS_ADJECTIVES)}")
            print(f"\n  mean {stats['mean']:.1f}   SD {stats['sd']:.1f}   "
                  f"range {stats['min']:.1f}-{stats['max']:.1f}")
            print(f"  grade band of mean: {band(stats['mean'], SUS_GRADES)}  "
                  f"({band(stats['mean'], SUS_ADJECTIVES)})")
            print("\n  Report the individual scores alongside the mean -- with a handful of\n"
                  "  participants the spread carries more information than the average.")
        return 0

    reverse = {int(x) for x in args.reverse.split(",") if x.strip()}
    bad = [r for r in reverse if not 1 <= r <= 8]
    if bad:
        print(f"--reverse positions out of range 1..8: {bad}", file=sys.stderr)
        return 2

    rows = read_rows(args.responses, 8)
    scored = [(label, *score_ueq_s(values, reverse)) for label, values in rows]
    overall = summarise("overall", [r[1] for r in scored])
    prag = summarise("pragmatic", [r[2] for r in scored])
    hed = summarise("hedonic", [r[3] for r in scored])

    def verdict(v: float) -> str:
        return "positive" if v > 0.8 else "negative" if v < -0.8 else "neutral"

    header = "| Participant | Overall | Pragmatic | Hedonic |"
    if args.markdown:
        print(header)
        print("| --- | --- | --- | --- |")
        for label, ov, pr, he, _ in scored:
            print(f"| {label} | {ov:+.2f} | {pr:+.2f} | {he:+.2f} |")
        print(f"| **Mean** | **{overall['mean']:+.2f}** | {prag['mean']:+.2f} | {hed['mean']:+.2f} |")
        print(f"\nn = {len(scored)}. Scale -3..+3; above +0.8 counts as a positive evaluation, "
              f"below -0.8 negative. Overall: {verdict(overall['mean'])}.")
    else:
        print(f"UEQ-S -- {len(scored)} participants" + (f", items reversed: {sorted(reverse)}" if reverse else "") + "\n")
        for label, ov, pr, he, _ in scored:
            print(f"  {label:<12} overall {ov:+.2f}   pragmatic {pr:+.2f}   hedonic {he:+.2f}")
        for name, s in (("overall", overall), ("pragmatic", prag), ("hedonic", hed)):
            print(f"\n  {name:<10} mean {s['mean']:+.2f}   SD {s['sd']:.2f}   "
                  f"range {s['min']:+.2f}..{s['max']:+.2f}   -> {verdict(s['mean'])}")
        print("\n  Per-item means (scale -3..+3):")
        for idx, name in enumerate(UEQ_S_ITEMS):
            col = statistics.fmean(r[4][idx] for r in scored)
            group = "pragmatic" if idx < 4 else "hedonic"
            print(f"    {idx + 1}. {name:<30} {col:+.2f}  ({group})")
        print("\n  A high pragmatic score with a low hedonic one means the product works but is\n"
              "  dull; the reverse means it appeals but obstructs. They call for different fixes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
