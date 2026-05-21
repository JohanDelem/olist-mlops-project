import pandas as pd
import pytest
from ml_olist.training.data import FEATURE_COLS, TARGET_COL, validate_schema


def make_valid_df():
    data = {col: [1.0] for col in FEATURE_COLS}
    data["order_purchase_timestamp"] = pd.to_datetime(["2017-10-02"])
    data[TARGET_COL] = [10.0]
    return pd.DataFrame(data)


def test_validate_schema_ok():
    df = make_valid_df()
    validate_schema(df)


def test_validate_schema_missing_column():
    df = make_valid_df().drop(columns=["price"])
    with pytest.raises(ValueError, match="Colonnes manquantes"):
        validate_schema(df)


def test_validate_schema_negative_target():
    df = make_valid_df()
    df[TARGET_COL] = [-1.0]
    with pytest.raises(ValueError, match="négatives ou nulles"):
        validate_schema(df)
