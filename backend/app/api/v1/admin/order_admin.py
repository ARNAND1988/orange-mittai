from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.order_status_update import OrderStatusUpdate
from app.database import get_db
from app.models.order import Order
from app.schemas.order_status import OrderStatus
from app.utils.admin import require_admin
from app.models.user import User
from app.services.order_admin_service import get_orders, update_order_status_service


router = APIRouter()

@router.get("/")
def list_all_orders(
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    return get_orders(db)

@router.patch("/{order_id}/status")
def update_order_status(
        order_id: str,
        payload: OrderStatusUpdate,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),
):
    return update_order_status_service(
        db,
        order_id,
        payload.status,   # ✅ ONLY the enum
    )
