from sqlalchemy.orm import Session
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.schemas.order import OrderCreate
from app.utils.order_id import generate_order_id

def create_order(db: Session, user_id: int, order_data: OrderCreate):
    if not order_data.items:
        raise ValueError("Order must contain items")

    total_amount = 0
    order_items = []

    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()

        if not product:
            raise ValueError(f"Product {item.product_id} not found")

        if product.stock < item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")

        total_amount += product.price * item.quantity

        order_items.append(
            OrderItem(
                product_id=product.id,
                price=product.price,
                quantity=item.quantity
            )
        )

    order = Order(
        user_id=user_id,
        total_amount=total_amount,
        payment_method=order_data.payment_method,
        status="PAYMENT_PENDING"
    )

    db.add(order)
    db.flush()  # gives order.id

    order.order_id = generate_order_id(order.id)
    order.items = order_items

    db.commit()
    db.refresh(order)

    return order
