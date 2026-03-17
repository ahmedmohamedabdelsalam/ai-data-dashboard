"""
Plot generation for EDA: heatmaps, distributions, missing values.
Plots are generated as base64 or saved to bytes for API response.
"""
import base64
import io
from typing import List, Optional

import matplotlib
matplotlib.use("Agg")  # Non-interactive backend for server
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def _fig_to_base64(fig: plt.Figure) -> str:
    """Encode matplotlib figure to base64 PNG string."""
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=100, bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")


def generate_correlation_heatmap(
    df: pd.DataFrame,
    figsize: tuple = (10, 8),
    cmap: str = "RdBu_r",
    center: float = 0.0,
) -> str:
    """
    Generate correlation heatmap for numeric columns. Returns base64 PNG.
    """
    numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    if numeric.empty or len(numeric.columns) < 2:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "Not enough numeric columns for correlation heatmap", ha="center", va="center")
        out = _fig_to_base64(fig)
        plt.close(fig)
        return out

    corr = numeric.corr()
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(corr, annot=True, fmt=".2f", cmap=cmap, center=center, ax=ax, square=True)
    ax.set_title("Correlation Heatmap (Numeric Columns)")
    plt.tight_layout()
    out = _fig_to_base64(fig)
    plt.close(fig)
    return out


def generate_distribution_plots(
    df: pd.DataFrame,
    columns: Optional[List[str]] = None,
    max_cols: int = 6,
    figsize_per_plot: tuple = (4, 3),
) -> List[str]:
    """
    Generate distribution histograms for numeric columns. Returns list of base64 PNGs.
    """
    numeric = df.select_dtypes(include=["number"])
    if columns:
        numeric = numeric[[c for c in columns if c in numeric.columns]]
    if numeric.empty:
        return []

    cols = list(numeric.columns)[:max_cols]
    images = []
    for col in cols:
        fig, ax = plt.subplots(figsize=figsize_per_plot)
        numeric[col].dropna().hist(ax=ax, bins=min(30, max(10, len(numeric) // 20)), edgecolor="black", alpha=0.7)
        ax.set_title(f"Distribution: {col}")
        ax.set_xlabel(col)
        plt.tight_layout()
        images.append(_fig_to_base64(fig))
        plt.close(fig)
    return images


def generate_missing_heatmap(df: pd.DataFrame, figsize: tuple = (12, 6)) -> str:
    """Heatmap of missing values (rows x columns). Returns base64 PNG."""
    missing = df.isna().astype(int)
    if missing.sum().sum() == 0:
        fig, ax = plt.subplots(figsize=figsize)
        ax.text(0.5, 0.5, "No missing values", ha="center", va="center", fontsize=14)
        out = _fig_to_base64(fig)
        plt.close(fig)
        return out

    # Sample rows if too many for visualization
    max_rows = 500
    if len(missing) > max_rows:
        missing = missing.sample(n=max_rows, random_state=42)
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(missing, yticklabels=False, xticklabels=missing.columns, cbar_kws={"label": "Missing"}, ax=ax)
    ax.set_title("Missing Values (1 = missing)")
    plt.tight_layout()
    out = _fig_to_base64(fig)
    plt.close(fig)
    return out
