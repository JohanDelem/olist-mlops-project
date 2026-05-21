import joblib
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from ml_olist.training.data import load_olist_data, split_data


def evaluate(model_path: str = "artifacts/model_latest.joblib"):
    model = joblib.load(model_path)
    df = load_olist_data()
    _, X_test, _, y_test = split_data(df)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print(f"MAE  = {mae:.2f} jours")
    print(f"RMSE = {rmse:.2f} jours")
    print(f"R²   = {r2:.3f}")
    return {"mae": mae, "rmse": rmse, "r2": r2}


if __name__ == "__main__":
    evaluate()
