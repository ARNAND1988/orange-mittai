from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.models.order import Order
from app.schemas.order import OrderCreate, OrderRead
from app.schemas.order_update import OrderStatusUpdate
from app.schemas.order_status import OrderStatus
from app.database import get_db
from app.utils.auth import get_current_user
from app.services.order_service import create_order
from app.services.order_history_service import (
    get_user_orders,
    get_user_order_by_id,
)

router = APIRouter()


# ✅ Place order
@router.post("", response_model=OrderRead)
def place_order(
        order_data: OrderCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return create_order(db, current_user.id, order_data)

# ✅ Order history (user)
@router.get("", response_model=List[OrderRead])
def order_history(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    print(current_user)
    return get_user_orders(db, current_user.id)


@router.get("/{order_id}", response_model=OrderRead)
def get_order_by_id(
        order_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    return get_user_order_by_id(db, current_user.id, order_id)

@router.patch("/{order_id}/cancel")
def cancel_order(
        order_id: str,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    order = (
        db.query(Order)
        .filter(
            Order.order_id == order_id,
            Order.user_id == current_user.id,
            )
        .first()
    )

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != OrderStatus.PAYMENT_PENDING.value:
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    order.status = OrderStatus.CANCELLED.value
    db.commit()

    return {
        "order_id": order.order_id,
        "status": order.status,
        "message": "Order cancelled successfully",
    }

