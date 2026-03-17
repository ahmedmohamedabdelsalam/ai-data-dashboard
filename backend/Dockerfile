# AI Data Analysis Agent - Production Dockerfile
FROM python:3.11-slim

WORKDIR /app

# System deps for matplotlib (optional, for non-headless if needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libfreetype6-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
# Create uploads dir
RUN mkdir -p uploads

ENV PYTHONPATH=/app
ENV UPLOAD_DIR=/app/uploads

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
