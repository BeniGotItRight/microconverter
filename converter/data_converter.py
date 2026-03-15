"""Data conversions: CSV, Excel, PDF to Excel, Excel to PDF."""

from pathlib import Path

import pandas as pd

# Try chardet for encoding detection
try:
    import chardet
    HAS_CHARDET = True
except ImportError:
    HAS_CHARDET = False


def _detect_encoding(file_path: Path) -> str:
    """Detect file encoding for CSV. Fallback to utf-8."""
    if not HAS_CHARDET:
        return "utf-8"
    with open(file_path, "rb") as f:
        raw = f.read(100000)
    result = chardet.detect(raw)
    return result.get("encoding") or "utf-8"


def csv_to_excel(
    input_path: Path,
    output_path: Path,
    encoding: str | None = None,
    delimiter: str | None = None,
) -> None:
    """
    Convert CSV to Excel. Handles encoding and delimiter for M-Pesa statements.
    """
    enc = encoding or _detect_encoding(input_path)
    try:
        df = pd.read_csv(input_path, encoding=enc, sep=delimiter or ",")
    except (UnicodeDecodeError, pd.errors.ParserError):
        # Fallback: try common encodings
        for fallback in ["utf-8", "latin-1", "iso-8859-1", "cp1252"]:
            try:
                df = pd.read_csv(input_path, encoding=fallback, sep=delimiter or ",")
                break
            except (UnicodeDecodeError, pd.errors.ParserError):
                continue
        else:
            raise ValueError("Could not decode CSV. Try specifying encoding in Advanced options.")

    df.to_excel(output_path, index=False, engine="openpyxl")
    # Adjust column widths for readability
    try:
        from openpyxl import load_workbook
        from openpyxl.utils import get_column_letter

        wb = load_workbook(output_path)
        ws = wb.active
        for i, col in enumerate(ws.columns, 1):
            max_len = min(max(len(str(c.value) or "") for c in col) + 2, 50)
            ws.column_dimensions[get_column_letter(i)].width = max_len
        wb.save(output_path)
    except Exception:
        pass  # Non-critical


def excel_to_csv(input_path: Path, output_path: Path) -> None:
    """Convert Excel to CSV. Supports .xlsx and .xls."""
    if input_path.suffix.lower() == ".xls":
        df = pd.read_excel(input_path, engine="xlrd")
    else:
        df = pd.read_excel(input_path, engine="openpyxl")
    df.to_csv(output_path, index=False, encoding="utf-8")


def pdf_to_excel(
    input_path: Path,
    output_path: Path,
    pages: list[int] | None = None,
    password: str | None = None,
) -> tuple[pd.DataFrame | None, str | None]:
    """
    Extract tables from PDF and save as Excel.
    Returns (DataFrame if tables found, optional warning message).
    Best for machine-generated PDFs (bank/M-Pesa statements).
    """
    import pdfplumber

    all_tables = []
    warning = None

    kwargs = {}
    if password:
        kwargs["password"] = password

    with pdfplumber.open(input_path, **kwargs) as pdf:
        page_range = pages if pages else range(len(pdf.pages))
        for i in page_range:
            if i < 0 or i >= len(pdf.pages):
                continue
            page = pdf.pages[i]
            tables = page.extract_tables()
            for tbl in tables:
                if tbl and any(any(cell for cell in row) for row in tbl):
                    all_tables.append(tbl)

        if not all_tables:
            text = pdf.pages[0].extract_text() if pdf.pages else ""
            if not text or not text.strip():
                warning = (
                    "No tables or text found. This PDF may be scanned. "
                    "Try an OCR tool for scanned documents."
                )
            else:
                # Fallback: try to parse text as lines/rows
                lines = [l.strip().split() for l in text.split("\n") if l.strip()]
                if lines:
                    all_tables.append(lines)

    if not all_tables:
        raise ValueError(
            "No extractable data found. "
            "This PDF might be scanned—try an OCR tool."
        )

    dfs = []
    for tbl in all_tables:
        df = pd.DataFrame(tbl[1:], columns=tbl[0] if tbl else None)
        if not df.empty:
            dfs.append(df)

    if not dfs:
        raise ValueError("No valid table data could be extracted from the PDF.")

    combined = pd.concat(dfs, ignore_index=True)
    combined.to_excel(output_path, index=False, engine="openpyxl")
    return combined, warning


def _to_latin1(s: str, max_len: int = 80) -> str:
    """Encode to latin-1 for fpdf2 compatibility. Truncate very long strings."""
    text = str(s)[:max_len]
    return text.encode("latin-1", "replace").decode("latin-1")


def excel_to_pdf(input_path: Path, output_path: Path) -> None:
    """
    Convert Excel to PDF using pandas + fpdf2. No LibreOffice required.
    Supports .xlsx and .xls. All sheets are rendered as tables.
    Uses landscape and smaller font for wide spreadsheets.
    """
    from fpdf import FPDF

    engine = "xlrd" if input_path.suffix.lower() == ".xls" else "openpyxl"
    xl = pd.ExcelFile(input_path, engine=engine)
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    sheet_count = 0
    for sheet_name in xl.sheet_names:
        df = pd.read_excel(xl, sheet_name=sheet_name)
        if df.empty or len(df.columns) == 0:
            continue
        sheet_count += 1

        col_count = len(df.columns)
        font_size = max(6, 10 - col_count // 5)
        orientation = "L" if col_count > 8 else "P"
        pdf.set_font("Helvetica", size=font_size)
        pdf.add_page(orientation=orientation)

        headers = [_to_latin1(str(c)) for c in df.columns]
        rows = [
            [_to_latin1(str(v) if pd.notna(v) else "") for v in row]
            for row in df.values.tolist()
        ]
        table_data = [headers] + rows
        with pdf.table(
            table_data,
            text_align="L",
            cell_fill_color=235,
            cell_fill_mode="ROWS",
        ):
            pass
    if sheet_count == 0:
        raise ValueError("Excel file has no data in any sheet.")
    pdf.output(str(output_path))
