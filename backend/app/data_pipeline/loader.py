"""
Dataset loader: load CSV or Excel files into pandas DataFrame.
"""
from pathlib import Path
from typing import Optional

import pandas as pd

from app.utils.file_utils import get_file_extension


def load_dataset(file_path: str | Path) -> pd.DataFrame:
    """
    Load dataset from CSV or Excel file.

    Args:
        file_path: Path to the file (CSV or Excel).

    Returns:
        Loaded DataFrame.

    Raises:
        ValueError: If file format is not supported or load fails.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = get_file_extension(path.name)
    if ext == ".csv":
        return _load_csv(path)
    if ext in (".xlsx", ".xls"):
        return _load_excel(path)
    raise ValueError(f"Unsupported file format: {ext}. Use .csv, .xlsx, or .xls")


def _load_csv(path: Path) -> pd.DataFrame:
    """Load CSV with common encodings and separators."""
    try:
        return pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        return pd.read_csv(path, encoding="latin-1")
    except Exception as e:
        raise ValueError(f"Failed to load CSV: {e}") from e


def _load_excel(path: Path) -> pd.DataFrame:
    """Load first sheet of Excel file."""
    try:
        return pd.read_excel(path, sheet_name=0, engine="openpyxl")
    except Exception as e:
        raise ValueError(f"Failed to load Excel: {e}") from e
