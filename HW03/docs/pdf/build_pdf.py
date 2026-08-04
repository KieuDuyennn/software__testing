#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_pdf.py - regenerate the PDF deliverables required by HW03 §15.

USAGE (from the HW03 repository root):

    python docs/pdf/build_pdf.py                 # rebuild every PDF in DOCUMENTS
    python docs/pdf/build_pdf.py --keep-html     # also leave the intermediate .html next to the PDFs
    python docs/pdf/build_pdf.py --list          # show the Markdown -> PDF mapping and exit

Pipeline: Markdown --(python-markdown, `tables` extension)--> self-contained HTML
(UTF-8, inline print stylesheet, images embedded as base64 data URIs)
--(headless Google Chrome `--print-to-pdf`)--> A4 PDF.

Requirements: Python 3.8+, `markdown` (pip install --user markdown), and Google Chrome
installed at one of the usual Windows locations (auto-detected, see find_chrome()).
No pandoc / wkhtmltopdf / LaTeX / admin rights needed.

The Markdown files are the source of truth; everything in docs/pdf/*.pdf is generated.
"""

import argparse
import base64
import glob
import mimetypes
import os
import re
import shutil
import subprocess
import sys
import tempfile

try:
    import markdown
except ImportError:  # pragma: no cover
    sys.exit("Missing dependency: run  pip install --user markdown")

from markdown.extensions import Extension
from markdown.inlinepatterns import SimpleTagInlineProcessor

# --------------------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------------------

# Repository root = two levels up from this file (docs/pdf/build_pdf.py).
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT_DIR = os.path.join(ROOT, "docs", "pdf")

# (source markdown, output pdf basename)
DOCUMENTS = [
    ("README.md", "00_Main_Report.pdf"),
    ("docs/01_Task1A_Shared_GUI_Checklist.md", "01_Task1A_Shared_GUI_Checklist.pdf"),
    ("docs/02_Task1B_Execution_Report_ScenarioD.md", "02_Task1B_Execution_Report_ScenarioD.pdf"),
    # §15 lists the Usability Report and the cross-platform report as parts of the main report,
    # so both need a PDF too. They are templates until Tasks 2 and 3 are actually run; rebuild
    # after filling them in.
    ("docs/03_Task2_Usability_Report_ScenarioD.md", "03_Task2_Usability_Report_ScenarioD.pdf"),
    ("docs/04_Task3_Cross_Platform_Matrix.md", "04_Task3_Cross_Platform_Matrix.pdf"),
    ("docs/05_Bug_Usability_Findings_Log.md", "05_Bug_Usability_Findings_Log.pdf"),
    # §15 submits the reference-sources list and the AI prompt chain as a GROUP artefact
    # alongside the checklist, so it needs a PDF of its own.
    ("docs/checklist/Reference_Sources_and_Prompts.md", "01b_Reference_Sources_and_Prompts.pdf"),
    ("docs/06_AI_Audit_Report.md", "06_AI_Audit_Report.pdf"),
    ("docs/07_AI_Critique.md", "07_AI_Critique.pdf"),
]

# Directories searched (by file basename) when an image link does not resolve relative
# to its own Markdown file. Several reports link evidence as `evidence/<name>.jpg`
# while the files actually live under reports/evidence_task*/.
IMAGE_SEARCH_ROOTS = ["reports", "docs", "refs"]

CHROME_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.join(os.environ.get("LOCALAPPDATA", ""), r"Google\Chrome\Application\chrome.exe"),
    os.path.join(os.environ.get("PROGRAMFILES", ""), r"Google\Chrome\Application\chrome.exe"),
    os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), r"Google\Chrome\Application\chrome.exe"),
    r"C:\Program Files\Google\Chrome Beta\Application\chrome.exe",
    r"C:\Program Files\Chromium\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
]

# --------------------------------------------------------------------------------------
# Print stylesheet
# --------------------------------------------------------------------------------------
# Font stack leads with Segoe UI / Arial, both of which carry the full Vietnamese
# diacritic set on Windows. Tables use auto layout plus `overflow-wrap: anywhere`, so
# wide tables (up to 16 columns in the findings log) wrap instead of running off the
# right edge; the per-column-count classes shrink the type as the table gets wider.

CSS = r"""
@page { size: A4; margin: 20mm 18mm 18mm 18mm; }

/* Tables with many columns get their own landscape pages (Chrome named pages), so a
   16-column findings table has 273mm of usable width instead of 174mm and no column
   is squeezed down to one character per line. */
@page rotated { size: A4 landscape; margin: 14mm 12mm; }
.landscape { page: rotated; }

html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }

body {
  font-family: "Segoe UI", "Segoe UI Variable Text", Arial, "Helvetica Neue",
               "Noto Sans", "Liberation Sans", sans-serif;
  font-size: 10.5pt;
  line-height: 1.45;
  color: #14181d;
  margin: 0;
  overflow-wrap: break-word;
}

/* ---------- headings ---------- */
h1, h2, h3, h4, h5, h6 {
  font-weight: 600;
  line-height: 1.25;
  margin: 1.1em 0 0.45em;
  page-break-after: avoid;
  break-after: avoid-page;
}
h1 { font-size: 19pt; margin-top: 0; padding-bottom: 6px; border-bottom: 2px solid #2f5b8c; color: #1d3f63; }
h2 { font-size: 14.5pt; padding-bottom: 3px; border-bottom: 1px solid #c6d2df; color: #1d3f63; }
h3 { font-size: 12pt; color: #23425f; }
h4 { font-size: 11pt; color: #33445a; }
h5, h6 { font-size: 10.5pt; color: #445366; }

p { margin: 0.5em 0; orphans: 2; widows: 2; }

/* ---------- lists ---------- */
ul, ol { margin: 0.45em 0; padding-left: 1.5em; }
li { margin: 0.18em 0; }
li > ul, li > ol { margin: 0.15em 0; }

/* ---------- blockquotes / callouts ---------- */
blockquote {
  margin: 0.7em 0;
  padding: 0.4em 0.9em;
  border-left: 3px solid #2f5b8c;
  background: #f2f6fa;
  page-break-inside: avoid;
}
blockquote p { margin: 0.3em 0; }

/* ---------- tables ---------- */
table {
  width: 100%;
  max-width: 100%;
  border-collapse: collapse;
  table-layout: auto;
  margin: 0.7em 0;
  font-size: 8.6pt;
  line-height: 1.3;
}
th, td {
  border: 0.6pt solid #96a3b2;
  padding: 3px 4px;
  text-align: left;
  vertical-align: top;
  overflow-wrap: anywhere;
  word-break: break-word;
  hyphens: auto;
}
th { background: #e3eaf3; font-weight: 600; }
tr:nth-child(even) td { background: #f7f9fc; }
thead { display: table-header-group; }   /* repeat header row on every page */
tr { page-break-inside: avoid; break-inside: avoid; }

/* narrower type as the column count grows, so nothing is squeezed off the page */
table.cols-sm  { font-size: 9.2pt; }
table.cols-md  { font-size: 8.4pt; }
table.cols-lg  { font-size: 7.3pt; }
table.cols-xl  { font-size: 7.0pt; }
table.cols-xxl { font-size: 6.4pt; }
table.cols-xxl th, table.cols-xxl td,
table.cols-xl  th, table.cols-xl  td { padding: 2px 3px; hyphens: none; }
/* keep short identifier-style cells on one line rather than stacking them vertically */
table.cols-xl  td:first-child, table.cols-xl  th:first-child,
table.cols-xxl td:first-child, table.cols-xxl th:first-child { white-space: nowrap; }
/* floor on column width so short-worded columns ("Type", "Severity") are not squeezed
   down to one character per line; 16 x 4.6em still fits the 273mm landscape text box */
table.cols-xl  th, table.cols-xl  td,
table.cols-xxl th, table.cols-xxl td { min-width: 4.6em; }

/* ---------- code ---------- */
code, kbd, samp {
  font-family: Consolas, "Cascadia Mono", "Courier New", monospace;
  font-size: 0.88em;
  background: #f0f2f5;
  border: 0.5pt solid #dde1e6;
  border-radius: 2px;
  padding: 0 2px;
  overflow-wrap: anywhere;
}
pre {
  background: #f6f8fa;
  border: 0.6pt solid #d7dde4;
  border-radius: 3px;
  padding: 7px 9px;
  margin: 0.7em 0;
  white-space: pre-wrap;
  overflow-wrap: anywhere;
  font-size: 8.6pt;
  line-height: 1.35;
  page-break-inside: avoid;
}
pre code { background: none; border: none; padding: 0; font-size: 1em; }

/* ---------- links, images, rules ---------- */
a { color: #14508c; text-decoration: none; overflow-wrap: anywhere; }
img {
  max-width: 100%;
  max-height: 200mm;
  height: auto;
  border: 0.6pt solid #ccd3da;
  page-break-inside: avoid;
  break-inside: avoid;
}
hr { border: none; border-top: 1px solid #c6d2df; margin: 1.1em 0; }
del { color: #7a828b; }
strong { font-weight: 600; }

/* ---------- generated cover strip ---------- */
.doc-source {
  font-size: 8pt;
  color: #6b7581;
  border-bottom: 0.6pt dotted #c3ccd6;
  padding-bottom: 4px;
  margin-bottom: 14px;
}
"""

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
<div class="doc-source">HW03 &middot; generated from <code>{source}</code> &middot; Markdown is the source of truth</div>
{body}
</body>
</html>
"""


# --------------------------------------------------------------------------------------
# Markdown extensions / helpers
# --------------------------------------------------------------------------------------

class StrikethroughExtension(Extension):
    """GitHub-flavoured ``~~deleted~~`` -> ``<del>deleted</del>`` (not in core Markdown)."""

    def extendMarkdown(self, md):
        md.inlinePatterns.register(
            SimpleTagInlineProcessor(r"(~{2})(.+?)(~{2})", "del"), "gfm_del", 175
        )


def find_chrome():
    """Return the path to a Chrome/Chromium binary, or exit with a clear message."""
    for path in CHROME_CANDIDATES:
        if path and os.path.isfile(path):
            return path
    for name in ("chrome", "chrome.exe", "chromium", "msedge"):
        found = shutil.which(name)
        if found:
            return found
    sys.exit(
        "Google Chrome was not found. Checked:\n  "
        + "\n  ".join(p for p in CHROME_CANDIDATES if p)
        + "\nInstall Chrome or edit CHROME_CANDIDATES in this script."
    )


def build_image_index():
    """basename -> absolute path, for every image under the search roots."""
    index = {}
    exts = (".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp")
    for root in IMAGE_SEARCH_ROOTS:
        base = os.path.join(ROOT, root)
        if not os.path.isdir(base):
            continue
        for path in glob.glob(os.path.join(base, "**", "*"), recursive=True):
            if path.lower().endswith(exts) and os.path.isfile(path):
                index.setdefault(os.path.basename(path).lower(), path)
    return index


def to_data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "application/octet-stream"
    with open(path, "rb") as fh:
        return "data:%s;base64,%s" % (mime, base64.b64encode(fh.read()).decode("ascii"))


def inline_images(md_text, md_path, image_index, report):
    """Rewrite ``![alt](src)`` to embed the image, so the HTML is fully self-contained.

    Resolution order: relative to the Markdown file -> relative to the repo root ->
    by basename anywhere under IMAGE_SEARCH_ROOTS. Unresolved links are left untouched
    and reported.
    """
    md_dir = os.path.dirname(os.path.abspath(md_path))

    def repl(match):
        alt, src = match.group(1), match.group(2).strip()
        if src.startswith(("http://", "https://", "data:")):
            return match.group(0)
        src_clean = src.split(" ")[0].strip("<>")
        candidates = [
            os.path.normpath(os.path.join(md_dir, src_clean)),
            os.path.normpath(os.path.join(ROOT, src_clean)),
        ]
        resolved = next((c for c in candidates if os.path.isfile(c)), None)
        if resolved is None:
            resolved = image_index.get(os.path.basename(src_clean).lower())
            if resolved:
                report["relinked"].add(src_clean)
        if resolved is None:
            report["missing"].add(src_clean)
            return match.group(0)
        report["embedded"] += 1
        return "![%s](%s)" % (alt, to_data_uri(resolved))

    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+(?:\s+\"[^\"]*\")?)\)", repl, md_text)


_TABLE_RE = re.compile(r"<table>(.*?)</table>", re.DOTALL)
_CELL_RE = re.compile(r"<(?:th|td)[ >]")


# Tables at or above this column count are moved onto landscape pages.
LANDSCAPE_MIN_COLS = 9


def classify_tables(html):
    """Tag each <table> with a size class based on its widest row (column count).

    Tables of LANDSCAPE_MIN_COLS or more columns are additionally wrapped in a
    ``.landscape`` block, which puts them on rotated A4 pages.
    """

    def repl(match):
        inner = match.group(1)
        widest = max(
            (len(_CELL_RE.findall(row)) for row in re.findall(r"<tr>(.*?)</tr>", inner, re.DOTALL)),
            default=0,
        )
        if widest <= 3:
            cls = "cols-sm"
        elif widest <= 5:
            cls = "cols-md"
        elif widest <= 8:
            cls = "cols-lg"
        elif widest <= 12:
            cls = "cols-xl"
        else:
            cls = "cols-xxl"
        table = '<table class="%s">%s</table>' % (cls, inner)
        if widest >= LANDSCAPE_MIN_COLS:
            table = '<div class="landscape">%s</div>' % table
        return table

    return _TABLE_RE.sub(repl, html)


def md_to_html(md_path, source_label, image_index, report):
    with open(md_path, "r", encoding="utf-8") as fh:
        md_text = fh.read()

    md_text = inline_images(md_text, md_path, image_index, report)

    converter = markdown.Markdown(
        extensions=[
            "tables",        # GFM pipe tables -> real <table> markup (acceptance criterion)
            "fenced_code",
            "sane_lists",
            "attr_list",
            "md_in_html",
            StrikethroughExtension(),
        ],
        output_format="html5",
    )
    body = classify_tables(converter.convert(md_text))

    title_match = re.search(r"^#\s+(.+)$", md_text, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else os.path.basename(md_path)
    title = re.sub(r"[*`_]", "", title)

    return HTML_TEMPLATE.format(title=title, css=CSS, source=source_label, body=body)


def html_to_pdf(chrome, html_path, pdf_path):
    """Print a local HTML file to PDF with headless Chrome."""
    profile = tempfile.mkdtemp(prefix="hw03-chrome-")
    url = "file:///" + os.path.abspath(html_path).replace("\\", "/")
    cmd = [
        chrome,
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--no-first-run",
        "--no-default-browser-check",
        "--disable-extensions",
        "--hide-scrollbars",
        "--user-data-dir=" + profile,           # never touch the user's real Chrome profile
        "--run-all-compositor-stages-before-draw",
        "--virtual-time-budget=20000",
        "--no-pdf-header-footer",
        "--print-to-pdf-no-header",              # older-flag alias; harmless if unknown
        "--print-to-pdf=" + os.path.abspath(pdf_path),
        url,
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if not os.path.isfile(pdf_path) or os.path.getsize(pdf_path) < 1024:
            raise RuntimeError(
                "Chrome did not produce a usable PDF for %s\nstdout: %s\nstderr: %s"
                % (html_path, proc.stdout[-2000:], proc.stderr[-2000:])
            )
    finally:
        shutil.rmtree(profile, ignore_errors=True)


def page_count(pdf_path):
    """Page count without any third-party dependency (falls back to pypdf if present)."""
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf_path).pages)
    except Exception:
        with open(pdf_path, "rb") as fh:
            data = fh.read()
        counts = [int(m.group(1)) for m in re.finditer(rb"/Count\s+(\d+)", data)]
        return max(counts) if counts else -1


def main():
    parser = argparse.ArgumentParser(description="Build the HW03 PDF deliverables.")
    parser.add_argument("--keep-html", action="store_true",
                        help="keep the intermediate HTML files in docs/pdf/")
    parser.add_argument("--list", action="store_true",
                        help="print the Markdown -> PDF mapping and exit")
    args = parser.parse_args()

    if args.list:
        for src, dst in DOCUMENTS:
            print("%-48s -> docs/pdf/%s" % (src, dst))
        return 0

    chrome = find_chrome()
    print("Chrome:  %s" % chrome)
    print("Root:    %s" % ROOT)
    os.makedirs(OUT_DIR, exist_ok=True)

    image_index = build_image_index()
    work_dir = OUT_DIR if args.keep_html else tempfile.mkdtemp(prefix="hw03-html-")
    failures = []

    try:
        for src_rel, pdf_name in DOCUMENTS:
            src = os.path.join(ROOT, src_rel)
            if not os.path.isfile(src):
                failures.append("%s: source not found" % src_rel)
                print("MISSING  %s" % src_rel)
                continue

            report = {"embedded": 0, "missing": set(), "relinked": set()}
            html = md_to_html(src, src_rel.replace("\\", "/"), image_index, report)

            html_path = os.path.join(work_dir, pdf_name[:-4] + ".html")
            with open(html_path, "w", encoding="utf-8") as fh:
                fh.write(html)

            pdf_path = os.path.join(OUT_DIR, pdf_name)
            html_to_pdf(chrome, html_path, pdf_path)

            size_kb = os.path.getsize(pdf_path) / 1024.0
            note = ""
            if report["embedded"]:
                note += "  [%d image(s) embedded" % report["embedded"]
                if report["relinked"]:
                    note += ", %d relinked by filename" % len(report["relinked"])
                note += "]"
            if report["missing"]:
                note += "  [WARN unresolved images: %s]" % ", ".join(sorted(report["missing"]))
            print("OK       docs/pdf/%-42s %8.1f KB  %3d pages%s"
                  % (pdf_name, size_kb, page_count(pdf_path), note))
    finally:
        if not args.keep_html:
            shutil.rmtree(work_dir, ignore_errors=True)

    if failures:
        print("\nFAILED:\n  " + "\n  ".join(failures))
        return 1
    print("\nDone. %d PDF(s) in %s" % (len(DOCUMENTS), OUT_DIR))
    return 0


if __name__ == "__main__":
    sys.exit(main())
