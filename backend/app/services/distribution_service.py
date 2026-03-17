import numpy as np
import pandas as pd
from typing import Dict, List
from app.core.logging import logger
from app.models.schemas import HistogramBin

def generate_distributions(df: pd.DataFrame, bins: int = 20) -> Dict[str, List[HistogramBin]]:
    """Compute histogram bins for numeric columns."""
    try:
        logger.info("Generating distribution bins.")
        numeric_cols = df.select_dtypes(include=["number"]).columns
        result = {}
        for col in numeric_cols:
            series = df[col].dropna()
            if series.empty:
                continue
            counts, bin_edges = np.histogram(series, bins=bins)
            histogram = []
            for i in range(len(counts)):
                start = bin_edges[i]
                end = bin_edges[i+1]
                histogram.append(HistogramBin(bin=f"{start:.2f}-{end:.2f}", count=int(counts[i])))
            result[col] = histogram
        return result
    except Exception as e:
        logger.error(f"Error generating distributions: {e}")
        return {}
