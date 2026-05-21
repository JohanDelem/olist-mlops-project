import pandas as pd
from ml_olist.common.features import add_olist_features


def make_df():
    return pd.DataFrame(
        {
            "price": [100.0, 200.0],
            "freight_value": [10.0, 20.0],
            "order_item_id": [1, 2],
            "order_purchase_timestamp": pd.to_datetime(
                [
                    "2017-10-02T10:56:33",
                    "2017-11-15T08:00:00",
                ]
            ),
        }
    )


def test_add_olist_features_columns():
    df = add_olist_features(make_df())
    assert "freight_ratio" in df.columns
    assert "log_price" in df.columns
    assert "is_multi_item" in df.columns
    assert "purchase_dow" in df.columns
    assert "purchase_month" in df.columns


def test_is_multi_item():
    df = add_olist_features(make_df())
    assert df["is_multi_item"].iloc[0] == 0  # order_item_id=1
    assert df["is_multi_item"].iloc[1] == 1  # order_item_id=2


def test_log_price_positive():
    df = add_olist_features(make_df())
    assert (df["log_price"] > 0).all()


def test_no_mutation():
    original = make_df()
    add_olist_features(original)
    assert "freight_ratio" not in original.columns  # df.copy() dans la fonction
