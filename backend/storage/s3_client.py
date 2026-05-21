import os
from pathlib import Path

import boto3


def download_model_from_minio(local_path: str) -> None:
    """Télécharge le modèle depuis MinIO vers le filesystem local."""
    client = boto3.client(
        "s3",
        endpoint_url=os.getenv("MINIO_ENDPOINT", "http://localhost:9000"),
        aws_access_key_id=os.getenv("MINIO_ACCESS_KEY", "admin"),
        aws_secret_access_key=os.getenv("MINIO_SECRET_KEY", "password123"),
    )
    Path(local_path).parent.mkdir(parents=True, exist_ok=True)
    client.download_file(
        os.getenv("MINIO_BUCKET_MODELS", "ml-models"),
        os.getenv("MODEL_OBJECT_NAME", "model_latest.joblib"),
        local_path,
    )
    print(f"Modèle téléchargé → {local_path}")
