#!/usr/bin/env python3
"""Build and render the two submission PDFs from their Markdown sources."""

from __future__ import annotations

import html
import re
import shutil
from pathlib import Path

import fitz
from pypdf import PdfReader
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    HRFlowable,
    Image,
    LongTable,
    PageBreak,
    Paragraph,
    Preformatted,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf"
RENDER = ROOT / "tmp" / "pdfs"

FONT_REGULAR = Path(r"C:\Windows\Fonts\arial.ttf")
FONT_BOLD = Path(r"C:\Windows\Fonts\arialbd.ttf")
FONT_MONO = Path(r"C:\Windows\Fonts\consola.ttf")

pdfmetrics.registerFont(TTFont("HWArial", str(FONT_REGULAR)))
pdfmetrics.registerFont(TTFont("HWArial-Bold", str(FONT_BOLD)))
pdfmetrics.registerFont(TTFont("HWConsolas", str(FONT_MONO)))
pdfmetrics.registerFontFamily(
    "HWArial", normal="HWArial", bold="HWArial-Bold", italic="HWArial"
)


def styles():
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "Title",
            parent=base["Title"],
            fontName="HWArial-Bold",
            fontSize=22,
            leading=27,
            textColor=colors.HexColor("#17324D"),
            alignment=TA_CENTER,
            spaceAfter=10 * mm,
        ),
        "h1": ParagraphStyle(
            "H1",
            parent=base["Heading1"],
            fontName="HWArial-Bold",
            fontSize=16,
            leading=20,
            textColor=colors.HexColor("#17324D"),
            spaceBefore=6 * mm,
            spaceAfter=3 * mm,
            keepWithNext=True,
        ),
        "h2": ParagraphStyle(
            "H2",
            parent=base["Heading2"],
            fontName="HWArial-Bold",
            fontSize=13,
            leading=16,
            textColor=colors.HexColor("#245B78"),
            spaceBefore=4 * mm,
            spaceAfter=2 * mm,
            keepWithNext=True,
        ),
        "h3": ParagraphStyle(
            "H3",
            parent=base["Heading3"],
            fontName="HWArial-Bold",
            fontSize=11,
            leading=14,
            textColor=colors.HexColor("#2E6F78"),
            spaceBefore=3 * mm,
            spaceAfter=1.5 * mm,
            keepWithNext=True,
        ),
        "h4": ParagraphStyle(
            "H4",
            parent=base["Heading4"],
            fontName="HWArial-Bold",
            fontSize=9.8,
            leading=12.5,
            textColor=colors.HexColor("#334E5C"),
            spaceBefore=2.5 * mm,
            spaceAfter=1.2 * mm,
            keepWithNext=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="HWArial",
            fontSize=9.2,
            leading=13,
            textColor=colors.HexColor("#17212B"),
            alignment=TA_LEFT,
            spaceAfter=2.2 * mm,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="HWArial",
            fontSize=7.4,
            leading=9.4,
            textColor=colors.HexColor("#17212B"),
        ),
        "quote": ParagraphStyle(
            "Quote",
            parent=base["BodyText"],
            fontName="HWArial",
            fontSize=8.8,
            leading=12,
            leftIndent=7 * mm,
            borderColor=colors.HexColor("#5E8FA3"),
            borderWidth=1,
            borderPadding=5,
            backColor=colors.HexColor("#EEF5F7"),
            spaceAfter=3 * mm,
        ),
        "code": ParagraphStyle(
            "Code",
            fontName="HWConsolas",
            fontSize=7.2,
            leading=9.2,
            leftIndent=3 * mm,
            rightIndent=3 * mm,
            borderPadding=5,
            borderColor=colors.HexColor("#CBD5E1"),
            borderWidth=0.5,
            backColor=colors.HexColor("#F5F7FA"),
            spaceAfter=3 * mm,
        ),
    }


def inline(text: str) -> str:
    value = html.escape(text.strip())
    value = re.sub(r"`([^`]+)`", r'<font name="HWConsolas">\1</font>', value)
    value = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", value)
    value = re.sub(r"\[([^]]+)\]\(([^)]+)\)", r"\1 (\2)", value)
    return value


def table_flowable(rows: list[list[str]], page_width: float, st):
    cols = max(len(row) for row in rows)
    normalized = [row + [""] * (cols - len(row)) for row in rows]
    body_style = st["small"]
    data = [[Paragraph(inline(cell), body_style) for cell in row] for row in normalized]
    first_weight = 1.5 if cols >= 4 else 1.2
    weights = [first_weight] + [1.0] * (cols - 1)
    unit = page_width / sum(weights)
    widths = [unit * weight for weight in weights]
    table = LongTable(data, colWidths=widths, repeatRows=1, hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("FONTNAME", (0, 0), (-1, 0), "HWArial-Bold"),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#F7FAFC")),
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#AAB8C2")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 4),
                ("RIGHTPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )
    return table


def image_flowable(path: Path, max_width: float, max_height: float = 120 * mm):
    img = Image(str(path))
    scale = min(max_width / img.imageWidth, max_height / img.imageHeight, 1.0)
    img.drawWidth = img.imageWidth * scale
    img.drawHeight = img.imageHeight * scale
    img.hAlign = "CENTER"
    return img


def parse_markdown(source: Path, page_width: float):
    st = styles()
    lines = source.read_text(encoding="utf-8-sig").splitlines()
    story = []
    paragraph: list[str] = []
    code: list[str] = []
    in_code = False
    code_lang = ""
    first_heading = True

    def flush_paragraph():
        if paragraph:
            story.append(Paragraph(inline(" ".join(paragraph)), st["body"]))
            paragraph.clear()

    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            flush_paragraph()
            if not in_code:
                in_code = True
                code_lang = stripped[3:].strip()
                code = []
            else:
                if code_lang == "mermaid":
                    story.append(image_flowable(ROOT / "docs" / "assets" / "continuous-performance-flow.png", page_width, 95 * mm))
                else:
                    story.append(Preformatted("\n".join(code), st["code"]))
                in_code = False
                code_lang = ""
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue

        if stripped.startswith("|") and stripped.endswith("|"):
            flush_paragraph()
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                table_lines.append(lines[i].strip())
                i += 1
            rows = []
            for index, raw in enumerate(table_lines):
                cells = [cell.strip() for cell in raw.strip("|").split("|")]
                if index == 1 and all(re.fullmatch(r":?-{3,}:?", c) for c in cells):
                    continue
                rows.append(cells)
            if rows:
                story.append(table_flowable(rows, page_width, st))
                story.append(Spacer(1, 3 * mm))
            continue

        image_match = re.fullmatch(r"!\[([^]]*)\]\(([^)]+)\)", stripped)
        if image_match:
            flush_paragraph()
            image_path = (ROOT / image_match.group(2)).resolve()
            if not image_path.exists():
                raise FileNotFoundError(image_path)
            story.append(image_flowable(image_path, page_width))
            if image_match.group(1):
                caption = ParagraphStyle(
                    "Caption",
                    parent=st["small"],
                    alignment=TA_CENTER,
                    textColor=colors.HexColor("#526574"),
                    spaceAfter=3 * mm,
                )
                story.append(Paragraph(inline(image_match.group(1)), caption))
            i += 1
            continue

        heading = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if heading:
            flush_paragraph()
            level = len(heading.group(1))
            text = heading.group(2)
            if first_heading:
                story.append(Paragraph(inline(text), st["title"]))
                story.append(HRFlowable(width="100%", color=colors.HexColor("#5E8FA3")))
                story.append(Spacer(1, 5 * mm))
                first_heading = False
            else:
                story.append(Paragraph(inline(text), st[f"h{level}"]))
            i += 1
            continue

        if stripped.startswith(">"):
            flush_paragraph()
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip().lstrip("> ").strip())
                i += 1
            story.append(Paragraph(inline(" ".join(quote_lines)), st["quote"]))
            continue

        bullet = re.match(r"^[-*]\s+(.+)$", stripped)
        number = re.match(r"^(\d+)\.\s+(.+)$", stripped)
        if bullet or number:
            flush_paragraph()
            marker = "•" if bullet else f"{number.group(1)}."
            content = bullet.group(1) if bullet else number.group(2)
            story.append(
                Paragraph(
                    f"<b>{marker}</b> {inline(content)}",
                    ParagraphStyle("List", parent=st["body"], leftIndent=5 * mm, firstLineIndent=-4 * mm),
                )
            )
            i += 1
            continue

        if not stripped:
            flush_paragraph()
        else:
            paragraph.append(stripped)
        i += 1

    flush_paragraph()
    while story and isinstance(story[-1], Spacer):
        story.pop()
    return story


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#C9D3DA"))
    canvas.line(18 * mm, 14 * mm, A4[0] - 18 * mm, 14 * mm)
    canvas.setFont("HWArial", 7.5)
    canvas.setFillColor(colors.HexColor("#526574"))
    canvas.drawString(18 * mm, 9 * mm, "HW05 - Student 23127184")
    canvas.drawRightString(A4[0] - 18 * mm, 9 * mm, f"Page {doc.page}")
    canvas.restoreState()


def build(source: Path, target: Path):
    target.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(
        str(target),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=17 * mm,
        bottomMargin=18 * mm,
        title=source.stem,
        author="23127184",
    )
    story = parse_markdown(source, A4[0] - 36 * mm)
    doc.build(story, onFirstPage=footer, onLaterPages=footer)


def render_and_validate(pdf_path: Path, prefix: str, required_terms: list[str]):
    reader = PdfReader(str(pdf_path))
    if not reader.pages:
        raise RuntimeError(f"no pages in {pdf_path}")
    extracted = "\n".join(page.extract_text() or "" for page in reader.pages)
    missing = [term for term in required_terms if term not in extracted]
    if missing:
        raise RuntimeError(f"missing expected text in {pdf_path.name}: {missing}")

    document = fitz.open(pdf_path)
    for page_no, page in enumerate(document, start=1):
        pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5), alpha=False)
        pix.save(RENDER / f"{prefix}-page-{page_no:02d}.png")
    print(f"validated {pdf_path.name}: {len(reader.pages)} pages, {pdf_path.stat().st_size} bytes")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    if RENDER.exists():
        shutil.rmtree(RENDER)
    RENDER.mkdir(parents=True)

    report = OUT / "23127184_HW05_AI_Performance_Report.pdf"
    audit = OUT / "23127184_HW05_AI_Audit_Report.pdf"
    build(ROOT / "23127184_HW05_REPORT.md", report)
    build(ROOT / "docs" / "ai-audit" / "AI_AUDIT.md", audit)
    render_and_validate(report, "report", ["23127184", "Load", "Stress", "Spike", "Soak", "AI Critique"])
    render_and_validate(audit, "audit", ["AI Audit Report", "OpenAI Codex", "Interaction 08"])


if __name__ == "__main__":
    main()
