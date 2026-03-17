"""
Exploratory Data Analysis: summary, correlation, missing values, distributions.
"""
from typing import Any, Dict, List

import numpy as np
import pandas as pd

from app.models.schemas import ColumnInfo, DatasetSummaryResponse


def get_dataset_summary(df: pd.DataFrame) -> DatasetSummaryResponse:
    """
    Build dataset summary: rows, columns, dtypes, missing values, memory.
    """
    rows, cols = df.shape
    memory_mb = df.memory_usage(deep=True).sum() / (1024 * 1024)
    dtypes_summary = df.dtypes.astype(str).value_counts().to_dict()
    dtypes_summary = {k: int(v) for k, v in dtypes_summary.items()}

    column_info: List[ColumnInfo] = []
    for c in df.columns:
        s = df[c]
        missing = s.isna().sum()
        missing_pct = (missing / len(df) * 100) if len(df) > 0 else 0.0
        unique = s.nunique() if s.dtype == "object" or s.dtype.name.startswith("int") else None
        column_info.append(
            ColumnInfo(
                name=str(c),
                dtype=str(s.dtype),
                missing_count=int(missing),
                missing_pct=round(missing_pct, 2),
                unique_count=int(unique) if unique is not None else None,
            )
        )

    return DatasetSummaryResponse(
        rows=rows,
        columns=cols,
        column_info=column_info,
        memory_usage_mb=round(memory_mb, 2),
        dtypes_summary=dtypes_summary,
    )


def get_correlation_matrix(df: pd.DataFrame) -> Dict[str, Dict[str, float]]:
    """
    Compute Pearson correlation matrix for numeric columns only.
    Returns nested dict: {col: {col2: correlation}}.
    """
    numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    if numeric.empty or len(numeric.columns) == 0:
        return {}
    corr = numeric.corr()
    return corr.round(4).to_dict()


def get_missing_report(df: pd.DataFrame) -> Dict[str, Any]:
    """Report of missing values per column and overall."""
    missing = df.isna().sum()
    total = len(df) * len(df.columns)
    total_missing = df.isna().sum().sum()
    return {
        "per_column": missing[missing > 0].to_dict(),
        "total_missing_values": int(total_missing),
        "total_cells": total,
        "missing_pct": round(total_missing / total * 100, 2) if total > 0 else 0,
    }


def get_distribution_stats(df: pd.DataFrame) -> Dict[str, Dict[str, Any]]:
    """Basic distribution stats (count, mean, std, min, quartiles, max) per numeric column."""
    numeric = df.select_dtypes(include=["number"])
    if numeric.empty:
        return {}
    return numeric.describe().round(4).to_dict()
