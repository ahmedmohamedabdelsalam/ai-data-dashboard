"""
API route handlers for dataset upload and analysis.
"""
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.analysis import (
    get_correlation_matrix,
    get_dataset_summary,
    run_anomaly_detection,
    run_feature_importance,
    run_kmeans_clustering,
)
from app.analysis.plots import (
    generate_correlation_heatmap,
    generate_distribution_plots,
    generate_missing_heatmap,
)
from app.config.settings import settings
from app.models.schemas import (
    AIInsightsResponse,
    AnomalyResponse,
    CorrelationResponse,
    DatasetSummaryResponse,
    UploadResponse,
    FullAnalysisResponse,
)
from app.services.dataset_service import dataset_service
from app.services.summary_service import generate_summary
from app.services.correlation_service import generate_correlation
from app.services.anomaly_service import detect_anomalies
from app.services.distribution_service import generate_distributions
from app.services.ai_insights_service import generate_ai_insights
from app.core.logging import logger
from app.utils.file_utils import ensure_upload_dir, validate_file_extension

router = APIRouter(prefix="/api", tags=["analysis"])


def _require_dataset():
    """Raise 400 if no dataset is loaded."""
    if not dataset_service.has_dataset():
        raise HTTPException(
            status_code=400,
            detail="No dataset loaded. Upload a CSV or Excel file via POST /upload_dataset first.",
        )
    return dataset_service.get_pipeline()


@router.post("/upload_dataset", response_model=UploadResponse)
async def upload_dataset(file: UploadFile = File(...)):
    """
    Upload a CSV or Excel file. This dataset will be used for all analysis endpoints.
    """
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )

    upload_dir = ensure_upload_dir()
    safe_name = Path(file.filename).name
    file_path = upload_dir / safe_name

    contents = await file.read()
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    if len(contents) > max_bytes:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_UPLOAD_SIZE_MB} MB",
        )

    with open(file_path, "wb") as f:
        f.write(contents)

    dataset_service.set_from_upload(file_path, safe_name)
    return UploadResponse(filename=safe_name, message="Dataset uploaded successfully")


@router.get("/dataset_summary", response_model=DatasetSummaryResponse)
def dataset_summary():
    """
    Return dataset information: number of rows/columns, missing values, column types.
    """
    pipeline = _require_dataset()
    return get_dataset_summary(pipeline.df)


@router.get("/correlation_analysis", response_model=CorrelationResponse)
def correlation_analysis():
    """Return correlation matrix between numeric columns."""
    pipeline = _require_dataset()
    if not pipeline.has_numeric_columns():
        return CorrelationResponse(
            correlation_matrix={},
            numeric_columns=[],
            message="No numeric columns in dataset.",
        )
    matrix = get_correlation_matrix(pipeline.numeric_df)
    return CorrelationResponse(
        correlation_matrix=matrix,
        numeric_columns=list(pipeline.numeric_df.columns),
        message="Correlation analysis completed",
    )


@router.get("/correlation_heatmap")
def correlation_heatmap():
    """Return correlation heatmap as base64 PNG (for embedding in frontends)."""
    pipeline = _require_dataset()
    b64 = generate_correlation_heatmap(pipeline.df)
    return {"image_base64": b64, "format": "png"}


@router.get("/anomaly_detection", response_model=AnomalyResponse)
def anomaly_detection(include_records: bool = False):
    """Detect anomalies using Isolation Forest on numeric columns."""
    pipeline = _require_dataset()
    return run_anomaly_detection(pipeline.df, include_records=include_records)


@router.get("/clustering")
def clustering(n_clusters: int | None = None):
    """KMeans clustering on numeric columns. Optional n_clusters query param."""
    pipeline = _require_dataset()
    return run_kmeans_clustering(pipeline.df, n_clusters=n_clusters)


@router.get("/feature_importance")
def feature_importance(target: str | None = None, top_n: int = 15):
    """Feature importance from Random Forest. Optional target column."""
    pipeline = _require_dataset()
    return run_feature_importance(pipeline.df, target_column=target, top_n=top_n)


@router.get("/ai_insights", response_model=AIInsightsResponse)
def ai_insights():
    """Use LLM to generate human-readable insights about the dataset."""
    pipeline = _require_dataset()
    summary = get_dataset_summary(pipeline.df)
    correlation = get_correlation_matrix(pipeline.numeric_df) if pipeline.has_numeric_columns() else None
    return generate_ai_insights(
        summary=summary.model_dump(),
        correlation=correlation,
        anomalies=None
    )


@router.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}

@router.post("/full_analysis", response_model=FullAnalysisResponse)
def full_analysis():
    """Run all primary analysis steps and return a combined response."""
    pipeline = _require_dataset()
    dataset_name = dataset_service.get_filename()
    logger.info(f"Running full analysis for {dataset_name}")
    
    summary = generate_summary(pipeline.df)
    correlation = generate_correlation(pipeline.df)
    anomalies = detect_anomalies(pipeline.df)
    distributions = generate_distributions(pipeline.df)
    
    insights = generate_ai_insights(
        summary=summary.model_dump() if summary.status == "success" else {},
        correlation=correlation.correlation_matrix if correlation.status == "success" else None,
        anomalies=anomalies.model_dump() if anomalies.status == "success" else None,
    )
    
    has_errors = any(x.status != "success" for x in [summary, correlation, anomalies, insights])
    final_status = "partial_success" if has_errors else "success"
    final_message = "Completed with partial errors." if has_errors else "Full analysis completed successfully."
    
    if has_errors:
        logger.warning(f"Full analysis completed with partial issues for {dataset_name}.")
    else:
        logger.info(f"Full analysis completed successfully for {dataset_name}.")

    return FullAnalysisResponse(
        summary=summary,
        correlation=correlation,
        anomalies=anomalies,
        distributions=distributions,
        insights=insights,
        dataset_name=dataset_name,
        status=final_status,
        message=final_message
    )


@router.get("/missing_report")
def missing_report():
    """Missing values report (per column and overall)."""
    pipeline = _require_dataset()
    from app.analysis.eda import get_missing_report
    return get_missing_report(pipeline.df)


@router.get("/distribution_plots")
def distribution_plots(max_cols: int = 6):
    """Distribution plots for numeric columns as base64 PNGs."""
    pipeline = _require_dataset()
    images = generate_distribution_plots(pipeline.df, max_cols=max_cols)
    return {"images_base64": images, "format": "png"}


@router.get("/missing_heatmap")
def missing_heatmap():
    """Missing values heatmap as base64 PNG."""
    pipeline = _require_dataset()
    b64 = generate_missing_heatmap(pipeline.df)
    return {"image_base64": b64, "format": "png"}
