"""
Pydantic schemas for API request/response models.
"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BaseAnalysisResponse(BaseModel):
    """Base response model tracking status for partial analysis failure."""
    status: str = "success"
    reason: Optional[str] = None
    message: Optional[str] = None


class UploadResponse(BaseModel):
    """Response after successful dataset upload."""

    filename: str
    message: str = "Dataset uploaded successfully"
    dataset_id: Optional[str] = None


class ColumnInfo(BaseModel):
    """Information about a single column."""

    name: str
    dtype: str
    missing_count: int
    missing_pct: float
    unique_count: Optional[int] = None


class DatasetSummaryResponse(BaseAnalysisResponse):
    """Dataset summary including shape, columns, and missing values."""

    rows: int = Field(..., description="Number of rows")
    columns: int = Field(..., description="Number of columns")
    column_info: List[ColumnInfo] = Field(..., description="Per-column details")
    memory_usage_mb: Optional[float] = None
    dtypes_summary: Optional[Dict[str, int]] = None


class CorrelationResponse(BaseAnalysisResponse):
    """Correlation matrix and metadata."""

    correlation_matrix: Dict[str, Dict[str, float]] = Field(
        ..., description="Numeric columns correlation matrix"
    )
    numeric_columns: List[str] = Field(..., description="Columns included")
    message: Optional[str] = "Correlation analysis completed"


class AnomalyRecord(BaseModel):
    """Single anomaly record with score and label."""

    index: int
    score: float
    is_anomaly: bool
    values: Optional[Dict[str, Any]] = None


class AnomalyResponse(BaseAnalysisResponse):
    """Anomaly detection results using Isolation Forest."""

    n_anomalies: int = Field(..., description="Number of anomalies detected")
    n_total: int = Field(..., description="Total records analyzed")
    anomaly_indices: List[int] = Field(..., description="Row indices of anomalies")
    records: Optional[List[AnomalyRecord]] = None
    contamination: float = Field(..., description="Contamination parameter used")


class ClusteringResult(BaseModel):
    """Clustering analysis result (optional extra endpoint)."""

    n_clusters: int
    labels: List[int]
    cluster_sizes: Dict[int, int]
    inertia: Optional[float] = None


class FeatureImportanceResult(BaseModel):
    """Feature importance from Random Forest (optional)."""

    feature_importances: Dict[str, float]
    top_n: int


class AIInsightsResponse(BaseAnalysisResponse):
    """LLM-generated natural language insights."""

    summary: str = Field(..., description="Dataset summary")
    correlations_explained: Optional[str] = None
    report: str = Field(..., description="Full natural language report")
    generated_at: Optional[str] = None
    key_patterns: Optional[str] = None
    correlation_insights: Optional[str] = None
    anomaly_explanations: Optional[str] = None
    recommendations: Optional[str] = None

class HistogramBin(BaseModel):
    bin: str
    count: int

class FullAnalysisResponse(BaseAnalysisResponse):
    """Combined analysis response for the dashboard."""
    summary: DatasetSummaryResponse
    correlation: CorrelationResponse
    anomalies: AnomalyResponse
    insights: AIInsightsResponse
    distributions: Optional[Dict[str, List[HistogramBin]]] = None
    dataset_name: Optional[str] = None
