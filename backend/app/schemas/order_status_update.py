from pydantic import BaseModel
from app.schemas.order_status import OrderStatus

class OrderStatusUpdate(BaseModel):
    status: OrderStatus
