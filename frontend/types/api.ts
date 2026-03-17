export interface UploadResponse {
  filename: string;
  message: string;
  dataset_id?: string | null;
}

export interface ColumnInfo {
  name: string;
  dtype: string;
  missing_count: number;
  missing_pct: number;
  unique_count?: number | null;
}

export interface DatasetSummary {
  rows: number;
  columns: number;
  column_info: ColumnInfo[];
  memory_usage_mb?: number | null;
  dtypes_summary?: Record<string, number> | null;
}

export interface CorrelationResponse {
  correlation_matrix: Record<string, Record<string, number>>;
  numeric_columns: string[];
  message: string;
}

export interface AnomalyRecord {
  index: number;
  score: number;
  is_anomaly: boolean;
  values?: Record<string, unknown>;
}

export interface AnomalyResponse {
  n_anomalies: number;
  n_total: number;
  anomaly_indices: number[];
  records?: AnomalyRecord[];
  contamination: number;
}

export interface AIInsightsResponse {
  summary: string;
  correlations_explained?: string | null;
  report: string;
  generated_at?: string | null;
}

export interface HistogramBin {
  bin: string;
  count: number;
}

export interface FullAnalysisResponse {
  summary: DatasetSummary;
  correlation: CorrelationResponse;
  anomalies: AnomalyResponse;
  insights: AIInsightsResponse;
  distributions?: Record<string, HistogramBin[]>;
  dataset_name?: string;
}

