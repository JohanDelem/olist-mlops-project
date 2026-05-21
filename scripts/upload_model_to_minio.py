"""
Script de publication du modèle vers MinIO.
À lancer après chaque entraînement réussi.
"""

import os
from pathlib import Path

import boto3
from dotenv import load_dotenv

load_dotenv()

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "admin")
SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "password123")
BUCKET = os.getenv("MINIO_BUCKET_MODELS", "ml-models")
OBJECT_NAME = os.getenv("MODEL_OBJECT_NAME", "model_latest.joblib")
LOCAL_MODEL_PATH = Path("artifacts/model_latest.joblib")


def upload_model():
    client = boto3.client(
        "s3",
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )

    # Créer le bucket s'il n'existe pas
    existing = [b["Name"] for b in client.list_buckets()["Buckets"]]
    if BUCKET not in existing:
        client.create_bucket(Bucket=BUCKET)
        print(f"Bucket '{BUCKET}' créé.")

    client.upload_file(str(LOCAL_MODEL_PATH), BUCKET, OBJECT_NAME)
    print(f"Modèle uploadé → s3://{BUCKET}/{OBJECT_NAME}")


if __name__ == "__main__":
    upload_model()
