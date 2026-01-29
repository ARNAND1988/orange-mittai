from sqlalchemy.orm import Session
from app.models.order import Order
from sqlalchemy.orm import joinedload
from app.models.order_item import OrderItem
from app.schemas.order_status import OrderStatus

def get_orders(db: Session):
    return (
        db.query(Order)
        .options(
            joinedload(Order.items).joinedload(OrderItem.product)
        )
        .order_by(Order.created_at.desc())
        .all()
    )


def update_order_status_service(
        db: Session,
        order_id: str,
        new_status: OrderStatus
):
   order =  (
        db.query(Order)
        .filter(Order.order_id == order_id)
        .first()
    )

   if not order:
       raise HTTPException(status_code=404, detail="Order not found")

   order.status = new_status
   db.commit()
   db.refresh(order)

   return {
       "order_id": order.order_id,
       "status": order.status,
       "message": "Order status updated successfully",
   }

