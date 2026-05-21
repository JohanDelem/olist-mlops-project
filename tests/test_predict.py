from unittest.mock import MagicMock, patch

from ml_olist.prediction.predict import predict

SAMPLE_FEATURES = {
    "price": 150.0,
    "freight_value": 15.0,
    "payment_installments": 3,
    "payment_value": 165.0,
    "order_item_id": 1,
    "order_purchase_timestamp": "2017-10-02T10:56:33",
    "seller_state": "SP",
    "customer_state": "RJ",
}


def test_predict_returns_float():
    mock_model = MagicMock()
    mock_model.predict.return_value = [12.5]
    with patch("ml_olist.prediction.predict.load_model", return_value=mock_model):
        result = predict(SAMPLE_FEATURES)
    assert isinstance(result, float)
    assert result == 12.5


def test_predict_calls_model():
    mock_model = MagicMock()
    mock_model.predict.return_value = [8.0]
    with patch("ml_olist.prediction.predict.load_model", return_value=mock_model):
        predict(SAMPLE_FEATURES)
    mock_model.predict.assert_called_once()
