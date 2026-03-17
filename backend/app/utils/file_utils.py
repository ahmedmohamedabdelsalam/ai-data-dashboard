"""
File handling utilities for uploads and validation.
"""
import os
from pathlib import Path
from typing import Optional

from app.config.settings import settings


def ensure_upload_dir() -> Path:
    """Create upload directory if it does not exist. Return path."""
    path = Path(settings.UPLOAD_DIR)
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_file_extension(filename: str) -> Optional[str]:
    """Extract file extension in lowercase (e.g. .csv)."""
    if not filename or "." not in filename:
        return None
    return "." + filename.rsplit(".", 1)[-1].lower()


def validate_file_extension(filename: str) -> bool:
    """Check if file extension is allowed for upload."""
    ext = get_file_extension(filename)
    return ext in settings.ALLOWED_EXTENSIONS if ext else False
