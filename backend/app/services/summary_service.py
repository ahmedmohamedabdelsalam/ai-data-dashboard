import pandas as pd
from app.core.logging import logger
from app.models.schemas import DatasetSummaryResponse
from app.analysis.eda import get_dataset_summary

def generate_summary(df: pd.DataFrame) -> DatasetSummaryResponse:
    """Generate a dataset summary safely."""
    try:
        logger.info("Generating dataset summary.")
        return get_dataset_summary(df)
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return DatasetSummaryResponse(
            status="error",
            reason="summary_failed",
            message=str(e),
            rows=0, columns=0, column_info=[]
        )
