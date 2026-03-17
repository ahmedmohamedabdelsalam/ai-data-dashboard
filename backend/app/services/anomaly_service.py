import pandas as pd
from app.core.logging import logger
from app.models.schemas import AnomalyResponse
from app.analysis import run_anomaly_detection

def detect_anomalies(df: pd.DataFrame) -> AnomalyResponse:
    """Detect anomalies safely."""
    try:
        logger.info("Running anomaly detection.")
        return run_anomaly_detection(df, include_records=False)
    except Exception as e:
        logger.error(f"Error detecting anomalies: {e}")
        return AnomalyResponse(
            status="error",
            reason="anomaly_detection_failed",
            message=str(e),
            n_anomalies=0,
            n_total=len(df),
            anomaly_indices=[],
            contamination=0.0
        )
