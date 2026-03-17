# AI Data Analysis Agent - Root Dockerfile for HF Spaces
FROM python:3.11-slim

WORKDIR /app

# System deps for matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Copy backend content to /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Ensure uploads dir exists
RUN mkdir -p uploads && chmod 777 uploads

ENV PYTHONPATH=/app
ENV UPLOAD_DIR=/app/uploads

# Hugging Face Spaces expects port 7860
EXPOSE 7860

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
