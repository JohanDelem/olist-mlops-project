from pydantic import BaseModel


class OrderFeatures(BaseModel):
    price: float
    freight_value: float
    payment_installments: int
    payment_value: float
    order_item_id: int
    order_purchase_timestamp: str
    seller_state: str
    customer_state: str


class PredictionResponse(BaseModel):
    delivery_time_days: float
    model_version: str = "latest"
