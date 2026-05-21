from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path("artifacts/model_latest.joblib")

_model = None


def load_model(model_path: Path = MODEL_PATH):
    global _model
    if _model is None:
        _model = joblib.load(model_path)
    return _model


def predict(features: dict) -> float:
    """
    Reçoit un dict avec les features brutes d'une commande,
    retourne le temps de livraison prédit en jours.
    """
    model = load_model()
    df = pd.DataFrame([features])
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    prediction = model.predict(df)
    return float(prediction[0])
