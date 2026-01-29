from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart import CartItem

def place_order(db: Session, user_id: int):
    cart_items = db.query(CartItem).filter_by(user_id=user_id).all()
    if not cart_items:
        return None

    total = sum(i.quantity * i.product.price for i in cart_items)

    order = Order(user_id=user_id, total_amount=total)
    db.add(order)
    db.flush()

    for item in cart_items:
        db.add(OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            price=item.product.price,
            quantity=item.quantity
        ))

    db.query(CartItem).filter_by(user_id=user_id).delete()
    db.commit()
    return order
