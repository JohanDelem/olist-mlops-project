FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copier le package source + la config
COPY src/ ./src/
COPY backend/ ./backend/
COPY pyproject.toml .

RUN pip install --no-cache-dir -e .

ENV PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "backend.app:app", "--host", "0.0.0.0", "--port", "8000"]
