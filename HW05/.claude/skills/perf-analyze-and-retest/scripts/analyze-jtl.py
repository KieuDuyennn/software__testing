#!/usr/bin/env python3
"""
analyze-jtl.py — Step 7: turn a raw .jtl into the ground-truth numbers.

Why this exists rather than reading the HTML dashboard: the dashboard is a
rendering, and an analysis that disagrees with it has no way to settle the
argument. Every figure printed here is computed from the raw samples, with the
method stated, so a disputed number can be recomputed instead of debated.

Two correctness details this script exists to get right, both of which routinely
produce confidently wrong analyses:

  1. A .jtl is CSV with quoted fields that contain commas. Transaction rows carry
     "Number of samples in transaction : 5, number of failing samples : 0".
     Splitting on commas shifts every later column, and a healthy run gets
     reported as a total failure.

  2. Transaction-controller rows are aggregates of their child samples. Counting
     them alongside the children inflates sample count and throughput. They are
     reported separately here, under transactions passed/failed - which is one of
     the ten metrics the course requires anyway.

Usage:
    python analyze-jtl.py results/run/result.jtl
    python analyze-jtl.py results/run/result.jtl --bucket 30
    python analyze-jtl.py results/run/result.jtl --p95 500 --error-rate 1.0
    python analyze-jtl.py results/run/result.jtl --out docs/phases/04_analysis.md
"""

import argparse
import csv
import math
import os
import sys
from collections import defaultdict

TX_MARKER = "Number of samples in transaction"


def percentile(sorted_values, fraction):
    """Nearest-rank percentile.

    Stated explicitly because JMeter's dashboard interpolates and this does not;
    the two differ by a few milliseconds on small samples. Quoting a percentile
    without naming the method is how two correct analyses end up disagreeing.
    """
    if not sorted_values:
        return 0.0
    rank = max(1, math.ceil(fraction * len(sorted_values)))
    return float(sorted_values[min(rank, len(sorted_values)) - 1])


def summarise(samples):
    """count/error/latency statistics for one group of samples."""
    elapsed = sorted(s["elapsed"] for s in samples)
    errors = sum(1 for s in samples if not s["success"])
    total_bytes = sum(s["bytes"] for s in samples)

    first_start = min(s["ts"] for s in samples)
    last_end = max(s["ts"] + s["elapsed"] for s in samples)
    window_s = max((last_end - first_start) / 1000.0, 0.001)

    return {
        "count": len(samples),
        "errors": errors,
        "error_rate": errors / len(samples) * 100.0,
        "min": elapsed[0],
        "mean": sum(elapsed) / len(elapsed),
        "p50": percentile(elapsed, 0.50),
        "p90": percentile(elapsed, 0.90),
        "p95": percentile(elapsed, 0.95),
        "p99": percentile(elapsed, 0.99),
        "max": elapsed[-1],
        "throughput": len(samples) / window_s,
        "kb_per_s": total_bytes / 1024.0 / window_s,
        "window_s": window_s,
    }


def load(path):
    """Reads a .jtl, splitting request samples from transaction-controller rows."""
    requests, transactions = [], []

    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        if reader.fieldnames is None or "elapsed" not in reader.fieldnames:
            sys.exit(f"{path} does not look like a JMeter CSV .jtl "
                     "(no 'elapsed' column). XML format is not supported.")

        for row in reader:
            try:
                sample = {
                    "ts": int(row["timeStamp"]),
                    "elapsed": int(row["elapsed"]),
                    "label": row["label"],
                    "code": row.get("responseCode", ""),
                    "success": row.get("success", "").strip().lower() == "true",
                    "bytes": int(row.get("bytes") or 0),
                    "threads": int(row.get("allThreads") or 0),
                    "latency": int(row.get("Latency") or 0),
                    "message": row.get("failureMessage", "") or "",
                }
            except (ValueError, KeyError, TypeError):
                continue  # a truncated final line is normal if a run was killed

            if TX_MARKER in (row.get("responseMessage") or ""):
                transactions.append(sample)
            else:
                requests.append(sample)

    return requests, transactions


def load_resources(path):
    """Optional resource samples written alongside the run."""
    if not path or not os.path.exists(path):
        return []
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            try:
                rows.append({
                    "elapsed": float(row["elapsed_s"]),
                    "cpu": float(row["cpu_percent"]),
                    "mem": float(row["working_set_mb"]),
                })
            except (ValueError, KeyError):
                continue
    return rows


def main():
    # Windows consoles default to a legacy codepage, so printing an arrow or an
    # em dash raises UnicodeEncodeError and loses a report that was computed
    # correctly. Written output is always UTF-8; this makes the console agree.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    ap = argparse.ArgumentParser()
    ap.add_argument("jtl")
    ap.add_argument("--bucket", type=int, default=30,
                    help="seconds per time bucket (0 disables the timeline)")
    ap.add_argument("--resources", default=None,
                    help="resources.csv (defaults to one beside the .jtl)")
    ap.add_argument("--p95", type=float, default=None, help="p95 threshold in ms")
    ap.add_argument("--error-rate", type=float, default=None,
                    help="error-rate threshold in percent")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    requests, transactions = load(args.jtl)
    if not requests:
        sys.exit("no request samples found")

    resources_path = args.resources
    if resources_path is None:
        candidate = os.path.join(os.path.dirname(os.path.abspath(args.jtl)), "resources.csv")
        resources_path = candidate if os.path.exists(candidate) else None
    resources = load_resources(resources_path)

    out = []
    out.append(f"# Analysis — `{os.path.basename(args.jtl)}`")
    out.append("")

    overall = summarise(requests)
    out.append("## Overall (request samples)")
    out.append("")
    out.append(f"- Samples: **{overall['count']}** over {overall['window_s']:.1f} s")
    out.append(f"- Requests/second: **{overall['throughput']:.2f}**")
    out.append(f"- Error rate: **{overall['error_rate']:.2f}%** ({overall['errors']} failed)")
    out.append(f"- Response time: mean **{overall['mean']:.1f} ms**, "
               f"p50 {overall['p50']:.0f}, p90 {overall['p90']:.0f}, "
               f"**p95 {overall['p95']:.0f}**, p99 {overall['p99']:.0f}, max {overall['max']:.0f}")
    out.append(f"- Bandwidth: **{overall['kb_per_s']:.1f} KB/s**")
    out.append("")
    out.append("Percentiles use the nearest-rank method; JMeter's dashboard "
               "interpolates, so small differences are expected and not an error.")
    out.append("")

    if transactions:
        tx = summarise(transactions)
        out.append("## Transactions passed/failed")
        out.append("")
        out.append(f"- Transactions: **{tx['count']}**, "
                   f"passed **{tx['count'] - tx['errors']}** "
                   f"({100 - tx['error_rate']:.2f}%), failed **{tx['errors']}**")
        out.append(f"- Transactions/second: **{tx['throughput']:.2f}**")
        out.append(f"- End-to-end journey time: mean **{tx['mean']:.1f} ms**, "
                   f"p95 **{tx['p95']:.0f} ms**, max {tx['max']:.0f}")
        out.append("")
        out.append("Counted separately from request samples: a transaction row is an "
                   "aggregate of its children, so adding the two together would count "
                   "the same work twice.")
        out.append("")

    by_label = defaultdict(list)
    for s in requests:
        by_label[s["label"]].append(s)

    out.append("## Per request label")
    out.append("")
    out.append("| Label | n | Err % | mean | p50 | p90 | p95 | p99 | max | req/s | KB/s |")
    out.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for label in sorted(by_label):
        st = summarise(by_label[label])
        out.append(
            f"| {label} | {st['count']} | {st['error_rate']:.2f} | {st['mean']:.1f} | "
            f"{st['p50']:.0f} | {st['p90']:.0f} | {st['p95']:.0f} | {st['p99']:.0f} | "
            f"{st['max']:.0f} | {st['throughput']:.2f} | {st['kb_per_s']:.1f} |"
        )
    out.append("")

    errors = [s for s in requests if not s["success"]]
    if errors:
        by_code = defaultdict(int)
        for s in errors:
            by_code[s["code"]] += 1
        out.append("## Failures by response code")
        out.append("")
        out.append("| Code | Count | Share of all samples |")
        out.append("|---|---:|---:|")
        for code, n in sorted(by_code.items(), key=lambda kv: -kv[1]):
            out.append(f"| {code} | {n} | {n / overall['count'] * 100:.2f}% |")
        out.append("")
        sample_msg = next((s["message"] for s in errors if s["message"]), "")
        if sample_msg:
            out.append(f"First failure message: `{sample_msg[:160]}`")
            out.append("")

    if args.bucket > 0:
        out.append(f"## Timeline ({args.bucket}s buckets)")
        out.append("")
        out.append("Where throughput stops rising while response time climbs is the knee — "
                   "the capacity limit. It usually appears well before errors do.")
        out.append("")
        start = min(s["ts"] for s in requests)
        # Use sample completion, not only the last start timestamp. A request
        # beginning at a bucket boundary used to make the final bucket appear to
        # span zero seconds and could report thousands of req/s from one sample.
        end = max(s["ts"] + s["elapsed"] for s in requests)
        buckets = defaultdict(list)
        for s in requests:
            buckets[(s["ts"] - start) // (args.bucket * 1000)].append(s)

        out.append("| t (s) | Peak VU | req/s | mean ms | p95 ms | Err % |")
        out.append("|---:|---:|---:|---:|---:|---:|")
        partial_seen = False
        for idx in sorted(buckets):
            group = buckets[idx]
            elapsed_sorted = sorted(s["elapsed"] for s in group)
            errs = sum(1 for s in group if not s["success"])
            peak_vu = max((s["threads"] for s in group), default=0)
            # A run rarely ends on a bucket boundary. Dividing the last bucket's
            # sample count by the nominal width would divide by seconds that were
            # never measured, and the table would show a throughput cliff at the
            # end of every run that no one caused. Divide by the span actually
            # covered, and label the row so the number is read for what it is.
            span = min(args.bucket * 1000, end - (start + idx * args.bucket * 1000)) / 1000
            partial = span < args.bucket * 0.9
            if partial:
                partial_seen = True
            # A sub-second tail does not contain enough observation time for a
            # defensible rate. Report it as n/a rather than dividing one sample
            # by a few milliseconds and presenting the result as throughput.
            width = span if partial else args.bucket
            rate = f"{len(group) / width:.1f}" if width >= 1.0 else "n/a"
            label = f"{idx * args.bucket}*" if partial else f"{idx * args.bucket}"
            out.append(
                f"| {label} | {peak_vu} | {rate} | "
                f"{sum(elapsed_sorted) / len(elapsed_sorted):.1f} | "
                f"{percentile(elapsed_sorted, 0.95):.0f} | {errs / len(group) * 100:.2f} |"
            )
        if partial_seen:
            out.append("")
            out.append("`*` = partial bucket: req/s uses only the observed seconds. Tails "
                       "shorter than one second are reported as `n/a` because their rate is unstable.")
        out.append("")

    if resources:
        peak_cpu = max(r["cpu"] for r in resources)
        mem_start, mem_end = resources[0]["mem"], resources[-1]["mem"]
        mem_peak = max(r["mem"] for r in resources)
        out.append("## Target resource usage")
        out.append("")
        out.append(f"- CPU utilisation: peak **{peak_cpu:.1f}%**, "
                   f"mean {sum(r['cpu'] for r in resources) / len(resources):.1f}% "
                   "(percentage of total machine capacity, not of one core)")
        out.append(f"- Memory: start **{mem_start:.1f} MB** → end **{mem_end:.1f} MB**, "
                   f"peak **{mem_peak:.1f} MB**")
        out.append(f"- Net change: **{mem_end - mem_start:+.1f} MB** over "
                   f"{resources[-1]['elapsed']:.0f} s")
        out.append("")
        if mem_end - mem_start > 0.10 * max(mem_start, 1):
            out.append("> Memory ended more than 10% above its first sample. This is a "
                       "possible accumulation signal, not proof of a leak. Observe a recovery "
                       "period and repeat at a longer duration before classifying the cause.")
            out.append("")

    if args.p95 is not None or args.error_rate is not None:
        out.append("## Verdict against criteria")
        out.append("")
        out.append("| Criterion | Threshold | Measured | Result |")
        out.append("|---|---:|---:|---|")
        if args.p95 is not None:
            ok = "PASS" if overall["p95"] <= args.p95 else "FAIL"
            out.append(f"| p95 response time | {args.p95:.0f} ms | {overall['p95']:.0f} ms | **{ok}** |")
        if args.error_rate is not None:
            ok = "PASS" if overall["error_rate"] <= args.error_rate else "FAIL"
            out.append(f"| Error rate | {args.error_rate:.2f}% | {overall['error_rate']:.2f}% | **{ok}** |")
        out.append("")

    text = "\n".join(out) + "\n"

    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(text)
        print(f"written: {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
