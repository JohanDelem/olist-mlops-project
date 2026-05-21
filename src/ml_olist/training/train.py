from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline

from ml_olist.training.data import load_olist_data, split_data, validate_schema
from ml_olist.training.features import build_preprocessing_pipeline

ARTIFACTS_DIR = Path("artifacts")


def train(n_estimators: int = 100, max_depth: int = 10, random_state: int = 42):
    # Chargement
    print("Chargement des données...")
    df = load_olist_data()
    validate_schema(df)
    X_train, X_test, y_train, y_test = split_data(df)
    print(f"Train : {len(X_train)} lignes | Test : {len(X_test)} lignes")

    # Pipeline complet : preprocessing + modèle
    preprocessing = build_preprocessing_pipeline()
    model = Pipeline(
        [
            ("preprocessing", preprocessing),
            (
                "regressor",
                RandomForestRegressor(
                    n_estimators=n_estimators,
                    max_depth=max_depth,
                    random_state=random_state,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    # MLflow tracking
    mlflow.set_experiment("olist-delivery-time")
    with mlflow.start_run():
        mlflow.log_params(
            {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "random_state": random_state,
            }
        )

        print("Entraînement...")
        model.fit(X_train, y_train)

        # Évaluation
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        mlflow.log_metrics({"mae": mae, "rmse": rmse, "r2": r2})
        print(f"MAE={mae:.2f}  RMSE={rmse:.2f}  R²={r2:.3f}")

        # Sauvegarde locale
        ARTIFACTS_DIR.mkdir(exist_ok=True)
        model_path = ARTIFACTS_DIR / "model_latest.joblib"
        joblib.dump(model, model_path)
        print(f"Modèle sauvegardé → {model_path}")

        mlflow.sklearn.log_model(model, "model")

    return model


if __name__ == "__main__":
    train()
