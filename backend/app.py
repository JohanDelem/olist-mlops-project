import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

from ml_olist.prediction.predict import load_model, predict  # noqa: E402
from ml_olist.prediction.schemas import OrderFeatures, PredictionResponse  # noqa: E402

from backend.storage.s3_client import download_model_from_minio  # noqa: E402

LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH", "artifacts/model_latest.joblib")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Télécharge le modèle depuis MinIO au démarrage."""
    try:
        download_model_from_minio(LOCAL_MODEL_PATH)
        load_model(LOCAL_MODEL_PATH)
        print("Modèle chargé avec succès.")
    except Exception as e:
        print(f"Attention : impossible de charger le modèle depuis MinIO : {e}")
        print("Tentative de chargement local...")
        try:
            load_model(LOCAL_MODEL_PATH)
        except Exception:
            print("Aucun modèle disponible.")
    yield


app = FastAPI(
    title="Olist Delivery Time API",
    description="Prédit le temps de livraison en jours pour une commande Olist.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict_delivery(features: OrderFeatures):
    try:
        result = predict(features.model_dump())
        return PredictionResponse(delivery_time_days=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e
