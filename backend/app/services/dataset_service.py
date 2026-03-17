"""
Dataset service: in-memory store for uploaded dataset and pipeline.
API endpoints use this to access the current dataset after upload.
"""
from pathlib import Path
from typing import Optional

from app.data_pipeline.pipeline import DataPipeline


class DatasetService:
    """
    Holds the active dataset pipeline. Single-dataset mode:
    upload replaces the current dataset.
    """

    def __init__(self) -> None:
        self._pipeline: Optional[DataPipeline] = None
        self._current_filename: Optional[str] = None

    def set_from_upload(self, file_path: Path, filename: str) -> None:
        """Load dataset from uploaded file and set as current."""
        pipeline = DataPipeline()
        pipeline.load(file_path)
        self._pipeline = pipeline
        self._current_filename = filename

    def get_pipeline(self) -> Optional[DataPipeline]:
        """Return current pipeline or None if no dataset loaded."""
        return self._pipeline

    def get_filename(self) -> Optional[str]:
        return self._current_filename

    def has_dataset(self) -> bool:
        return self._pipeline is not None

    def clear(self) -> None:
        """Clear current dataset."""
        self._pipeline = None
        self._current_filename = None


# Singleton used by API
dataset_service = DatasetService()
