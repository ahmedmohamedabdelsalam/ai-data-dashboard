"""
Data cleaning: basic cleaning and normalization for analysis.
"""
from typing import Optional

import pandas as pd


def clean_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply basic cleaning: strip whitespace, normalize column names.

    Does not drop rows/columns by default to preserve data for analysis.
    Callers can optionally drop nulls or duplicates.

    Args:
        df: Raw DataFrame.

    Returns:
        Cleaned DataFrame (copy).
    """
    out = df.copy()

    # Normalize column names: strip whitespace, replace spaces with underscore
    out.columns = [
        str(c).strip().replace(" ", "_").replace("\n", "_")
        for c in out.columns
    ]

    # Strip string columns
    for col in out.select_dtypes(include=["object"]).columns:
        out[col] = out[col].astype(str).str.strip()

    return out


def get_numeric_subset(df: pd.DataFrame) -> pd.DataFrame:
    """Return DataFrame with only numeric columns (for correlation, ML)."""
    numeric = df.select_dtypes(include=["number"])
    return numeric.dropna(axis=1, how="all")
