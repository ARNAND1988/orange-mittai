# app/schemas/order_item.py
from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemRead(BaseModel):
    product_id: int
    price: float
    quantity: int

    class Config:
        from_attributes = True

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: str | None = None

class OrderRead(BaseModel):
    order_id: str
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes = True