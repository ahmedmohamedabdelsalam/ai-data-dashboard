import pandas as pd
from app.core.logging import logger
from app.models.schemas import CorrelationResponse
from app.analysis.eda import get_correlation_matrix

def generate_correlation(df: pd.DataFrame) -> CorrelationResponse:
    """Generate correlation matrix safely."""
    try:
        logger.info("Generating correlation analysis.")
        numeric_df = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
        if numeric_df.empty or len(numeric_df.columns) == 0:
            return CorrelationResponse(
                status="disabled",
                reason="no_numeric_columns",
                message="No numeric columns available for correlation.",
                correlation_matrix={},
                numeric_columns=[]
            )
            
        matrix = get_correlation_matrix(numeric_df)
        return CorrelationResponse(
            correlation_matrix=matrix,
            numeric_columns=list(numeric_df.columns),
            message="Correlation analysis completed"
        )
    except Exception as e:
        logger.error(f"Error generating correlation: {e}")
        return CorrelationResponse(
            status="error",
            reason="correlation_failed",
            message=str(e),
            correlation_matrix={},
            numeric_columns=[]
        )
