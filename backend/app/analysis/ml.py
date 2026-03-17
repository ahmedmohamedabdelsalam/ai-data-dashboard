"""
Machine Learning: anomaly detection (Isolation Forest), clustering (KMeans), feature importance (RandomForest).
"""
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest, RandomForestClassifier, RandomForestRegressor
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

from app.config.settings import settings
from app.models.schemas import AnomalyRecord, AnomalyResponse


def _prepare_numeric(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[str], Optional[SimpleImputer], Optional[StandardScaler]]:
    """Get numeric subset, impute and scale. Returns (X, columns, imputer, scaler)."""
    numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    if numeric.empty:
        return df, [], None, None
    cols = list(numeric.columns)
    imputer = SimpleImputer(strategy="median")
    X = imputer.fit_transform(numeric)
    scaler = StandardScaler()
    X = scaler.fit_transform(X)
    return pd.DataFrame(X, columns=cols, index=df.index), cols, imputer, scaler


def run_anomaly_detection(
    df: pd.DataFrame,
    contamination: Optional[float] = None,
    include_records: bool = False,
    max_records: int = 100,
) -> AnomalyResponse:
    """
    Run Isolation Forest on numeric columns. Returns anomaly indices and scores.
    """
    X_df, cols, _, _ = _prepare_numeric(df)
    if X_df.empty or len(cols) == 0:
        return AnomalyResponse(
            n_anomalies=0,
            n_total=len(df),
            anomaly_indices=[],
            contamination=contamination or settings.ISOLATION_FOREST_CONTAMINATION,
        )

    cont = contamination if contamination is not None else settings.ISOLATION_FOREST_CONTAMINATION
    iso = IsolationForest(contamination=cont, random_state=42)
    pred = iso.fit_predict(X_df)
    scores = -iso.score_samples(X_df)  # higher = more anomalous

    anomaly_mask = pred == -1
    anomaly_indices = list(np.where(anomaly_mask)[0])
    n_anomalies = len(anomaly_indices)
    n_total = len(df)

    records = None
    if include_records and n_anomalies > 0:
        subset = anomaly_indices[:max_records]
        records = []
        for i in subset:
            row = df.iloc[i]
            records.append(
                AnomalyRecord(
                    index=int(i),
                    score=float(scores[i]),
                    is_anomaly=True,
                    values=row.to_dict() if hasattr(row, "to_dict") else None,
                )
            )

    return AnomalyResponse(
        n_anomalies=n_anomalies,
        n_total=n_total,
        anomaly_indices=anomaly_indices,
        records=records,
        contamination=cont,
    )


def run_kmeans_clustering(
    df: pd.DataFrame,
    n_clusters: Optional[int] = None,
) -> Dict[str, Any]:
    """
    Run KMeans on numeric columns. Returns labels and cluster sizes.
    """
    X_df, cols, _, _ = _prepare_numeric(df)
    if X_df.empty or len(cols) == 0:
        return {"n_clusters": 0, "labels": [], "cluster_sizes": {}, "inertia": None}

    n = n_clusters or min(settings.KMEANS_N_CLUSTERS, len(X_df) - 1, 10)
    n = max(2, n)
    km = KMeans(n_clusters=n, random_state=42)
    labels = km.fit_predict(X_df)
    sizes = {int(k): int(v) for k, v in enumerate(np.bincount(labels))}
    return {
        "n_clusters": n,
        "labels": labels.tolist(),
        "cluster_sizes": sizes,
        "inertia": float(km.inertia_),
    }


def run_feature_importance(
    df: pd.DataFrame,
    target_column: Optional[str] = None,
    top_n: int = 15,
    task: str = "regression",
) -> Dict[str, float]:
    """
    Compute feature importance using Random Forest.
    If target_column is None, uses last numeric column as target (for demo).
    task: 'regression' or 'classification'.
    """
    numeric = df.select_dtypes(include=["number"]).dropna(axis=1, how="all")
    if numeric.empty or len(numeric.columns) < 2:
        return {}

    if target_column and target_column in numeric.columns:
        target = target_column
    else:
        target = numeric.columns[-1]

    X = numeric.drop(columns=[target])
    y = numeric[target]
    X = SimpleImputer(strategy="median").fit_transform(X)
    feature_names = list(numeric.drop(columns=[target]).columns)

    if task == "classification":
        try:
            y = pd.Categorical(y).codes
            if len(np.unique(y)) < 2:
                return {}
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        except Exception:
            return {}
    else:
        model = RandomForestRegressor(n_estimators=100, random_state=42)

    model.fit(X, y)
    imp = dict(zip(feature_names, model.feature_importances_.tolist()))
    sorted_imp = dict(sorted(imp.items(), key=lambda x: -x[1])[:top_n])
    return sorted_imp
