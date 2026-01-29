from pydantic import BaseModel
from .order_status import OrderStatus

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
