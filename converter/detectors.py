"""Extension detection and format mapping for Convertex."""

from pathlib import Path

FORMAT_MAP = {
    # Documents
    ".pdf": [".docx", ".xlsx", ".txt"],
    ".docx": [".pdf", ".txt"],
    ".txt": [".pdf"],
    ".pptx": [".pdf"],
    ".html": [".pdf"],
    ".htm": [".pdf"],
    ".md": [".pdf", ".html"],
    ".rtf": [".pdf", ".txt"],
    ".odt": [".pdf", ".txt"],
    # Images
    ".jpg": [".png", ".webp", ".pdf"],
    ".jpeg": [".png", ".webp", ".pdf"],
    ".png": [".jpg", ".webp", ".pdf"],
    ".webp": [".png", ".jpg", ".pdf"],
    ".bmp": [".png", ".jpg"],
    ".tiff": [".png", ".jpg"],
    ".tif": [".png", ".jpg"],
    ".gif": [".png", ".jpg"],
    ".ico": [".png"],
    # Data
    ".csv": [".xlsx", ".pdf"],
    ".xlsx": [".csv", ".pdf"],
    ".xls": [".csv", ".pdf"],
    ".json": [".csv", ".xlsx", ".pdf", ".yaml"],
    ".xml": [".csv", ".xlsx", ".json"],
    ".yaml": [".json", ".csv", ".xlsx"],
    ".yml": [".json", ".csv", ".xlsx"],
}

# Human-readable format labels
FORMAT_LABELS = {
    ".docx": "Word (.docx)",
    ".pdf": "PDF (.pdf)",
    ".xlsx": "Excel (.xlsx)",
    ".csv": "CSV (.csv)",
    ".png": "PNG (.png)",
    ".jpg": "JPG (.jpg)",
    ".jpeg": "JPG (.jpeg)",
    ".webp": "WebP (.webp)",
    ".bmp": "BMP (.bmp)",
    ".tiff": "TIFF (.tiff)",
    ".tif": "TIFF (.tif)",
    ".gif": "GIF (.gif)",
    ".ico": "ICO (.ico)",
    ".txt": "Text (.txt)",
    ".html": "HTML (.html)",
    ".htm": "HTML (.htm)",
    ".md": "Markdown (.md)",
    ".rtf": "RTF (.rtf)",
    ".odt": "ODT (.odt)",
    ".pptx": "PowerPoint (.pptx)",
    ".json": "JSON (.json)",
    ".xml": "XML (.xml)",
    ".yaml": "YAML (.yaml)",
    ".yml": "YAML (.yml)",
}


def get_extension(filename: str) -> str:
    """Extract lowercase extension from filename."""
    return Path(filename).suffix.lower()


def get_output_formats(filename: str) -> list[tuple[str, str]]:
    """
    Return list of (extension, label) for supported output formats.
    Returns empty list if unsupported.
    """
    ext = get_extension(filename)
    if ext not in FORMAT_MAP:
        return []
    outputs = FORMAT_MAP[ext]
    return [(e, FORMAT_LABELS.get(e, e)) for e in outputs]


def is_supported(filename: str) -> bool:
    """Check if file type is supported for conversion."""
    return get_extension(filename) in FORMAT_MAP
