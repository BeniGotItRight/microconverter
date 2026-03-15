"""Utilities: temp files, cleanup."""

import atexit
import os
import tempfile
from pathlib import Path

_TEMP_FILES: set[str] = set()
_cleanup_registered = False


def create_temp_file(suffix: str, delete_on_exit: bool = True) -> Path:
    """Create a temp file. Optionally register for cleanup on exit."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)
    if delete_on_exit:
        _TEMP_FILES.add(path)
        _ensure_cleanup_registered()
    return Path(path)


def cleanup_temp(path: str | Path) -> None:
    """Remove temp file if it exists."""
    path = str(path)
    try:
        if os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass
    _TEMP_FILES.discard(path)


def _cleanup_all() -> None:
    for p in list(_TEMP_FILES):
        cleanup_temp(p)


def _ensure_cleanup_registered() -> None:
    global _cleanup_registered
    if not _cleanup_registered:
        atexit.register(_cleanup_all)
        _cleanup_registered = True
