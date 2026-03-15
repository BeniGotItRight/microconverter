"""Document conversions: PDF, Word, Text."""

from pathlib import Path

from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from fpdf import FPDF


def pdf_to_word(input_path: Path, output_path: Path) -> None:
    """Convert PDF to Word (.docx) using pdf2docx."""
    from pdf2docx import Converter

    cv = Converter(str(input_path))
    try:
        cv.convert(str(output_path), start=0, end=None)
    finally:
        cv.close()


def word_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert Word (.docx) to PDF using python-docx + fpdf2. No LibreOffice required."""
    doc = Document(str(input_path))
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    for block in doc.iter_inner_content():
        if isinstance(block, Paragraph):
            text = block.text.strip()
            if text:
                safe = text.encode("latin-1", "replace").decode("latin-1")
                pdf.multi_cell(0, 6, safe)
        elif isinstance(block, Table):
            pdf.ln(4)
            for row in block.rows:
                cells = [str(cell.text or "").strip()[:80] for cell in row.cells]
                if any(cells):
                    line = " | ".join(cells)
                    safe = line.encode("latin-1", "replace").decode("latin-1")
                    pdf.multi_cell(0, 6, safe)
            pdf.ln(4)
    pdf.output(str(output_path))


def text_to_pdf(input_path: Path, output_path: Path) -> None:
    """Convert plain text (.txt) to PDF using fpdf2."""
    with open(input_path, "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", size=11)

    for line in content.replace("\r\n", "\n").replace("\r", "\n").split("\n"):
        # FPDF uses latin-1; safely encode non-ASCII for display
        safe = line.encode("latin-1", "replace").decode("latin-1")
        pdf.multi_cell(0, 6, safe)
    pdf.output(str(output_path))
