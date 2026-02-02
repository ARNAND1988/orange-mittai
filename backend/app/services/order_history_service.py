from sqlalchemy.orm import Session, joinedload
from app.models.order import Order
from app.models.order_item import OrderItem


def get_user_orders(db: Session, user_id: int):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.address),   # 🔥 LOAD ADDRESS
        )
        .filter(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
        .all()
    )


def get_user_order_by_id(
        db: Session,
        user_id: int,
        order_id: str,
):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product),
            joinedload(Order.address),   # 🔥 LOAD ADDRESS
        )
        .filter(
            Order.user_id == user_id,
            Order.order_id == order_id,
            )
        .first()
    )
