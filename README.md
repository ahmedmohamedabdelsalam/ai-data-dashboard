---
title: AI Data Dashboard
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
pinned: false
---

# AI Data Analysis Dashboard 

An advanced, full-stack platform for automated data analysis and visualization, powered by Artificial Intelligence. This project provides businesses and data scientists with instant insights, anomaly detection, correlation analysis, and data distributions from any customized CSV or Excel dataset.

##  Live Demos
- **Frontend (Web App)**: Hosted on [Vercel](https://frontend-nine-rust.vercel.app/) *(insert your actual vercel domain here if changed)*
- **Backend (API Server)**: Hosted on [Hugging Face Spaces](https://huggingface.co/spaces/Abdelsalam-1/ai-data-dashboard-api)

---

##  Core Features

1. **Automated Data Summarization**: Instantly calculates rows, columns, memory usage, and column data types.
2. **Correlation Analysis**: Generates an interactive Correlation Heatmap to identify strong positive/negative relationships between numeric variables.
3. **Data Distribution (Histograms)**: Dynamic, interactive charts allowing users to select any numeric column and visualize its distribution in real-time.
4. **Anomaly Detection**: Uses advanced Machine Learning (`IsolationForest` via `scikit-learn`) to detect and count outliers and anomalies within the dataset.
5. **AI-Powered Insights**: Integrates Large Language Models (LLMs) to read analysis results and generate a human-readable, executive-level narrative report.

---

##  Technology Stack

### Frontend (UI / Client)
- **Framework**: Next.js 14 (React)
- **Styling**: Tailwind CSS & Vanilla CSS (with responsive Glassmorphism design)
- **State Management**: Zustand (with local storage persistence)
- **Data Visualization**: Recharts (for dynamic histograms and charts)
- **API Client**: Axios

### Backend (Server / AI)
- **Framework**: FastAPI (Python 3.11)
- **Data Processing**: Pandas & NumPy
- **Machine Learning**: Scikit-Learn (Isolation Forest, KMeans)
- **LLM Integration**: OpenAI / OpenRouter APIs (for generating narrative insights)
- **Containerization**: Docker

---

##  Project Structure

```text
├── frontend/                 # Next.js Application
│   ├── app/                  # Pages and Layouts (Next.js App Router)
│   ├── components/           # Reusable UI Components (Cards, Charts, Buttons)
│   ├── hooks/                # Custom React Hooks (useAnalysisStore)
│   └── services/             # API connection logic
│
├── backend/                  # FastAPI Application
│   ├── app/                  # Main server logic
│   │   ├── api/              # API Routes (/upload_dataset, /full_analysis)
│   │   ├── services/         # Business logic (Distribution, Anomaly, AI Insights)
│   │   └── models/           # Pydantic schemas for data validation
│   ├── Dockerfile            # Hugging Face deployment container
│   └── requirements.txt      # Python dependencies
│
└── README.md                 # Project Documentation
```

---

##  Running Locally

### 1. Start the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
> The API will be available at `http://localhost:8000`

### 2. Start the Frontend
```bash
cd frontend
npm install
npm run dev
```
> The web app will be available at `http://localhost:3000`

### 3. Environment Variables
Create a `.env.local` file inside the `frontend` directory:
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```
For production, set it to your Hugging Face Space URL.

---

##  Contributing
Contributions, issues, and feature requests are welcome!

Made with ❤️ for Data Science & AI.
