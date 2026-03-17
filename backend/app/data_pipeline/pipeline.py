"""
Data pipeline: load -> clean -> analyze -> insights.
Orchestrates the full flow for a single dataset.
"""
from pathlib import Path
from typing import Optional

import pandas as pd

from app.data_pipeline.loader import load_dataset
from app.data_pipeline.cleaner import clean_dataset, get_numeric_subset


class DataPipeline:
    """
    Production data pipeline: load, clean, and expose dataset for analysis.
    """

    def __init__(self, file_path: Optional[str | Path] = None):
        self._file_path: Optional[Path] = Path(file_path) if file_path else None
        self._raw_df: Optional[pd.DataFrame] = None
        self._df: Optional[pd.DataFrame] = None
        self._numeric_df: Optional[pd.DataFrame] = None

    def load(self, file_path: str | Path) -> pd.DataFrame:
        """Load dataset from file and store. Returns cleaned DataFrame."""
        self._file_path = Path(file_path)
        self._raw_df = load_dataset(self._file_path)
        self._df = clean_dataset(self._raw_df)
        self._numeric_df = get_numeric_subset(self._df)
        return self._df

    def set_dataframe(self, df: pd.DataFrame) -> None:
        """Set DataFrame directly (e.g. after upload in memory)."""
        self._raw_df = df.copy()
        self._df = clean_dataset(self._raw_df)
        self._numeric_df = get_numeric_subset(self._df)
        self._file_path = None

    @property
    def df(self) -> pd.DataFrame:
        """Cleaned full DataFrame."""
        if self._df is None:
            raise ValueError("No dataset loaded. Call load() or set_dataframe() first.")
        return self._df

    @property
    def numeric_df(self) -> pd.DataFrame:
        """Numeric-only subset for correlation and ML."""
        if self._numeric_df is None:
            raise ValueError("No dataset loaded.")
        return self._numeric_df

    @property
    def file_path(self) -> Optional[Path]:
        return self._file_path

    def has_numeric_columns(self) -> bool:
        """True if at least one numeric column exists."""
        return self._numeric_df is not None and len(self._numeric_df.columns) > 0
