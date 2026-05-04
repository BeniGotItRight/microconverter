"""Convertex converters."""

from .data_converter import (
    csv_to_excel,
    csv_to_pdf,
    excel_to_csv,
    excel_to_pdf,
    json_to_csv,
    json_to_excel,
    json_to_pdf,
    json_to_yaml,
    pdf_to_excel,
    xml_to_csv,
    xml_to_excel,
    xml_to_json,
    yaml_to_csv,
    yaml_to_excel,
    yaml_to_json,
)
from .document_converter import (
    html_to_pdf,
    markdown_to_html,
    markdown_to_pdf,
    odt_to_pdf,
    odt_to_text,
    pdf_to_text,
    pdf_to_word,
    pptx_to_pdf,
    rtf_to_pdf,
    rtf_to_text,
    text_to_pdf,
    word_to_pdf,
    word_to_text,
)
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
    """
    from pathlib import Path

    input_path = Path(input_path)
    output_path = Path(output_path)
    target_ext = target_ext.lower()
    if not target_ext.startswith("."):
        target_ext = "." + target_ext

    src_ext = input_path.suffix.lower()
    warning = None

    # --- PDF sources ---
    if src_ext == ".pdf":
        if target_ext == ".docx":
            pdf_to_word(input_path, output_path)
        elif target_ext == ".xlsx":
            _, warning = pdf_to_excel(input_path, output_path, pages=pages, password=password)
        elif target_ext == ".txt":
            pdf_to_text(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: PDF to {target_ext}")

    # --- Word ---
    elif src_ext == ".docx":
        if target_ext == ".pdf":
            word_to_pdf(input_path, output_path)
        elif target_ext == ".txt":
            word_to_text(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: DOCX to {target_ext}")

    # --- Text ---
    elif src_ext == ".txt":
        if target_ext == ".pdf":
            text_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: TXT to {target_ext}")

    # --- PowerPoint ---
    elif src_ext == ".pptx":
        if target_ext == ".pdf":
            pptx_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: PPTX to {target_ext}")

    # --- HTML ---
    elif src_ext in (".html", ".htm"):
        if target_ext == ".pdf":
            html_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: HTML to {target_ext}")

    # --- Markdown ---
    elif src_ext == ".md":
        if target_ext == ".pdf":
            markdown_to_pdf(input_path, output_path)
        elif target_ext == ".html":
            markdown_to_html(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: Markdown to {target_ext}")

    # --- RTF ---
    elif src_ext == ".rtf":
        if target_ext == ".pdf":
            rtf_to_pdf(input_path, output_path)
        elif target_ext == ".txt":
            rtf_to_text(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: RTF to {target_ext}")

    # --- ODT ---
    elif src_ext == ".odt":
        if target_ext == ".pdf":
            odt_to_pdf(input_path, output_path)
        elif target_ext == ".txt":
            odt_to_text(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: ODT to {target_ext}")

    # --- Images ---
    elif src_ext in (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif", ".gif", ".ico"):
        convert_image(input_path, output_path, target_ext)

    # --- CSV ---
    elif src_ext == ".csv":
        if target_ext == ".xlsx":
            csv_to_excel(input_path, output_path, encoding=encoding, delimiter=delimiter)
        elif target_ext == ".pdf":
            csv_to_pdf(input_path, output_path, encoding=encoding, delimiter=delimiter)
        else:
            raise ValueError(f"Unsupported conversion: CSV to {target_ext}")

    # --- Excel ---
    elif src_ext in (".xlsx", ".xls"):
        if target_ext == ".csv":
            excel_to_csv(input_path, output_path)
        elif target_ext == ".pdf":
            excel_to_pdf(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: Excel to {target_ext}")

    # --- JSON ---
    elif src_ext == ".json":
        if target_ext == ".csv":
            json_to_csv(input_path, output_path)
        elif target_ext == ".xlsx":
            json_to_excel(input_path, output_path)
        elif target_ext == ".pdf":
            json_to_pdf(input_path, output_path)
        elif target_ext in (".yaml", ".yml"):
            json_to_yaml(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: JSON to {target_ext}")

    # --- XML ---
    elif src_ext == ".xml":
        if target_ext == ".csv":
            xml_to_csv(input_path, output_path)
        elif target_ext == ".xlsx":
            xml_to_excel(input_path, output_path)
        elif target_ext == ".json":
            xml_to_json(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: XML to {target_ext}")

    # --- YAML ---
    elif src_ext in (".yaml", ".yml"):
        if target_ext == ".json":
            yaml_to_json(input_path, output_path)
        elif target_ext == ".csv":
            yaml_to_csv(input_path, output_path)
        elif target_ext == ".xlsx":
            yaml_to_excel(input_path, output_path)
        else:
            raise ValueError(f"Unsupported conversion: YAML to {target_ext}")

    else:
        raise ValueError(f"Unsupported source format: {src_ext}")

    return None, warning
