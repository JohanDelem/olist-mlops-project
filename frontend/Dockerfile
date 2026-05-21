FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir streamlit httpx

COPY frontend/app.py .

ENV PYTHONPATH=/app

EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0", "--server.port", "8501"]
