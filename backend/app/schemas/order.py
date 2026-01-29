from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from .order_item import OrderItemCreate, OrderItemRead
from .order_status import OrderStatus

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    payment_method: Optional[str] = None

class OrderRead(BaseModel):
    order_id: str
    total_amount: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemRead]

    class Config:
        from_attributes = True
