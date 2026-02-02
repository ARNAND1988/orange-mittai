from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

from .order_item import OrderItemCreate, OrderItemRead
from .order_status import OrderStatus


# =========================
# CREATE ORDER
# =========================
class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    address_id: int                 # 🔥 REQUIRED for checkout
    payment_method: Optional[str] = "COD"


# =========================
# READ ORDER ADDRESS
# =========================
class OrderAddressRead(BaseModel):
    name: str
    phone: str
    house_number: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str

    class Config:
        from_attributes = True


# =========================
# READ ORDER
# =========================
class OrderRead(BaseModel):
    order_id: str
    total_amount: float
    status: OrderStatus
    created_at: datetime

    items: List[OrderItemRead]
    address: Optional[OrderAddressRead] = None  # 🔥 INCLUDED

    class Config:
        from_attributes = True
