"""Extension detection and format mapping for Convertex."""

from pathlib import Path

FORMAT_MAP = {
    ".pdf": [".docx", ".xlsx"],
    ".docx": [".pdf"],
    ".txt": [".pdf"],
    ".jpg": [".png", ".pdf"],
    ".jpeg": [".png", ".pdf"],
    ".png": [".jpg", ".jpeg", ".pdf"],
    ".csv": [".xlsx"],
    ".xlsx": [".csv", ".pdf"],
    ".xls": [".csv", ".pdf"],
}

# Human-readable format labels for dropdown
FORMAT_LABELS = {
    ".docx": "Word (.docx)",
    ".pdf": "PDF (.pdf)",
    ".xlsx": "Excel (.xlsx)",
    ".csv": "CSV (.csv)",
    ".png": "PNG (.png)",
    ".jpg": "JPG (.jpg)",
    ".jpeg": "JPG (.jpeg)",
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
