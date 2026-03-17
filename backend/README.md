# AI Data Analysis Agent

Production-style backend that lets users **upload a dataset (CSV or Excel)** and automatically run **intelligent data analysis** and **LLM-generated insights**.

---

## Architecture

```
backend/
├── app/
│   ├── main.py              # FastAPI app entry, CORS, lifespan
│   ├── config/
│   │   └── settings.py      # Env-based configuration
│   ├── api/
│   │   └── routes.py        # REST endpoints
│   ├── services/
│   │   └── dataset_service.py  # In-memory current dataset
│   ├── models/
│   │   └── schemas.py       # Pydantic request/response models
│   ├── utils/
│   │   └── file_utils.py    # Upload dir, file validation
│   ├── data_pipeline/
│   │   ├── loader.py        # CSV/Excel load
│   │   ├── cleaner.py       # Clean & numeric subset
│   │   └── pipeline.py      # Load → clean → expose
│   ├── analysis/
│   │   ├── eda.py           # Summary, correlation, missing, distributions
│   │   ├── plots.py         # Heatmaps, distribution plots (base64)
│   │   └── ml.py            # Isolation Forest, KMeans, feature importance
│   └── llm/
│       └── insights.py      # OpenAI / Gemini natural language report
├── requirements.txt
├── Dockerfile
└── README.md
```

**Flow:** Upload → pipeline loads and cleans data → all GET endpoints operate on the **current dataset** (single-dataset mode). EDA, ML, and LLM modules are modular and easy to extend.

---

## How to Run

### Local (no Docker)

1. **Create virtualenv and install deps**

   ```bash
   cd backend
   python -m venv .venv
   .venv\Scripts\activate   # Windows
   # source .venv/bin/activate  # Linux/macOS
   pip install -r requirements.txt
   ```

2. **Optional: set LLM and upload settings**

   ```bash
   set OPENAI_API_KEY=sk-...        # Windows
   set LLM_PROVIDER=openai
   set LLM_MODEL=gpt-4o-mini
   # Or for Gemini:
   set GEMINI_API_KEY=...
   set LLM_PROVIDER=gemini
   set LLM_MODEL=gemini-1.5-flash
   ```

3. **Run the API**

   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   - API: http://localhost:8000  
   - Swagger: http://localhost:8000/docs  
   - ReDoc: http://localhost:8000/redoc  

### Docker

```bash
cd backend
docker build -t ai-data-analysis-agent .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... ai-data-analysis-agent
```

Without `OPENAI_API_KEY` (or `GEMINI_API_KEY`), the rest of the API works; only `/api/ai_insights` will return a message asking for an API key.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| **POST** | `/api/upload_dataset` | Upload CSV or Excel file (form field: `file`) |
| **GET** | `/api/dataset_summary` | Rows, columns, column types, missing values |
| **GET** | `/api/correlation_analysis` | Correlation matrix (numeric columns) |
| **GET** | `/api/correlation_heatmap` | Correlation heatmap image (base64 PNG) |
| **GET** | `/api/anomaly_detection` | Anomalies via Isolation Forest (`?include_records=true` optional) |
| **GET** | `/api/clustering` | KMeans clustering (`?n_clusters=5` optional) |
| **GET** | `/api/feature_importance` | Random Forest feature importance (`?target=col&top_n=15`) |
| **GET** | `/api/ai_insights` | LLM-generated summary and report (OpenAI or Gemini) |
| **GET** | `/api/missing_report` | Missing values per column and overall |
| **GET** | `/api/distribution_plots` | Distribution histograms (base64 PNGs, `?max_cols=6`) |
| **GET** | `/api/missing_heatmap` | Missing values heatmap (base64 PNG) |
| **GET** | `/` | Service info and endpoint list |
| **GET** | `/health` | Health check |

All analysis endpoints require a dataset to be uploaded first via `POST /api/upload_dataset`.

---

## Example Requests

### 1. Upload dataset

```bash
curl -X POST "http://localhost:8000/api/upload_dataset" \
  -H "accept: application/json" \
  -F "file=@/path/to/your/data.csv"
```

Response:

```json
{
  "filename": "data.csv",
  "message": "Dataset uploaded successfully",
  "dataset_id": null
}
```

### 2. Dataset summary

```bash
curl "http://localhost:8000/api/dataset_summary"
```

Response (example):

```json
{
  "rows": 1000,
  "columns": 8,
  "column_info": [
    {
      "name": "age",
      "dtype": "int64",
      "missing_count": 0,
      "missing_pct": 0.0,
      "unique_count": 52
    }
  ],
  "memory_usage_mb": 0.12,
  "dtypes_summary": { "int64": 4, "float64": 2, "object": 2 }
}
```

### 3. Correlation analysis

```bash
curl "http://localhost:8000/api/correlation_analysis"
```

### 4. Anomaly detection

```bash
curl "http://localhost:8000/api/anomaly_detection?include_records=true"
```

### 5. AI insights (needs `OPENAI_API_KEY` or `GEMINI_API_KEY`)

```bash
curl "http://localhost:8000/api/ai_insights"
```

---

## Data Pipeline

1. **Load** – `loader.py`: CSV (utf-8/latin-1) or Excel (first sheet).
2. **Clean** – `cleaner.py`: Normalize column names, strip strings; optional numeric subset.
3. **Analyze** – EDA (summary, correlation, missing), plots (heatmap, distributions), ML (anomaly, clustering, feature importance).
4. **Insights** – `llm/insights.py`: Build context from shape, dtypes, sample, summary; call OpenAI or Gemini; return natural language report.

---

## Configuration (environment)

| Variable | Default | Description |
|----------|---------|-------------|
| `UPLOAD_DIR` | `uploads` | Directory for uploaded files |
| `MAX_UPLOAD_SIZE_MB` | `50` | Max file size (MB) |
| `LLM_PROVIDER` | `openai` | `openai` or `gemini` |
| `OPENAI_API_KEY` | - | Required for OpenAI insights |
| `GEMINI_API_KEY` | - | Required for Gemini insights |
| `LLM_MODEL` | `gpt-4o-mini` | Model name (e.g. `gemini-1.5-flash` for Gemini) |
| `KMEANS_N_CLUSTERS` | `5` | Default KMeans clusters |
| `ISOLATION_FOREST_CONTAMINATION` | `0.1` | Anomaly detection contamination |
| `DEBUG` | `false` | Enable debug mode |

---

## Code Quality

- **Modular**: Separate packages for `config`, `api`, `services`, `models`, `utils`, `data_pipeline`, `analysis`, `llm`.
- **Production-style**: Env-based config, CORS, lifespan, health check, Docker.
- **Documented**: Docstrings and README with architecture, run instructions, and examples.
- **Extensible**: Add new analysis in `analysis/`, new routes in `api/routes.py`, new pipeline steps in `data_pipeline/`.
