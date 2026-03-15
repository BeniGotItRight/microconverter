"""Convertex converters."""

from .data_converter import (
    csv_to_excel,
    excel_to_csv,
    excel_to_pdf,
    pdf_to_excel,
)
from .document_converter import pdf_to_word, text_to_pdf, word_to_pdf
from .image_converter import convert_image


def convert(
    input_path,
    output_path,
    target_ext: str,
    *,
    encoding: str | None = None,
    delimiter: str | None = None,
    pages: list[int] | None = None,
    password: str | None = None,
) -> tuple[object | None, str | None]:
    """
    Route to appropriate converter. Returns (preview_data, warning_message).
    preview_data is DataFrame for PDF→Excel when preview requested; else None.
    """
    from pathlib import Path

    input_path = Path(input_path)
    output_path = Path(output_path)
    target_ext = target_ext.lower()
    if not target_ext.startswith("."):
        target_ext = "." + target_ext

    src_ext = input_path.suffix.lower()
    warning = None

    # PDF sources
    if src_ext == ".pdf":
        if target_ext == ".docx":
            pdf_to_word(input_path, output_path)
        elif target_ext == ".xlsx":
            _, warning = pdf_to_excel(input_path, output_path, pages=pages, password=password)
        else:
            raise ValueError(f"Unsupported conversion: PDF to {target_ext}")

    # Word
    elif src_ext == ".docx":
        if target_ext == ".pdf":
            word_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: DOCX to {target_ext}")

    # Text
    elif src_ext == ".txt":
        if target_ext == ".pdf":
            text_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: TXT to {target_ext}")

    # Images
    elif src_ext in (".jpg", ".jpeg", ".png"):
        convert_image(input_path, output_path, target_ext)

    # CSV
    elif src_ext == ".csv":
        if target_ext == ".xlsx":
            csv_to_excel(input_path, output_path, encoding=encoding, delimiter=delimiter)
        else:
            raise ValueError(f"Unsupported conversion: CSV to {target_ext}")

    # Excel
    elif src_ext in (".xlsx", ".xls"):
        if target_ext == ".csv":
            excel_to_csv(input_path, output_path)
        elif target_ext == ".pdf":
            excel_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: Excel to {target_ext}")

    else:
        raise ValueError(f"Unsupported source format: {src_ext}")

    return None, warning
