from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.address import UserAddress, OrderAddress
from app.schemas.order import OrderCreate
from app.schemas.order_status import OrderStatus
from app.utils.order_id import generate_order_id


def create_order(db: Session, user_id: int, order_data: OrderCreate):
    if not order_data.items:
        raise HTTPException(status_code=400, detail="Order must contain items")

    # =========================
    # 1️⃣ Validate address
    # =========================
    address = (
        db.query(UserAddress)
        .filter(
            UserAddress.id == order_data.address_id,
            UserAddress.user_id == user_id,
            )
        .first()
    )

    if not address:
        raise HTTPException(status_code=400, detail="Invalid address")

    total_amount = 0
    order_items = []

    # =========================
    # 2️⃣ Validate products + stock
    # =========================
    for item in order_data.items:
        product = (
            db.query(Product)
            .filter(Product.id == item.product_id)
            .first()
        )

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )

        total_amount += product.price * item.quantity

        order_items.append(
            OrderItem(
                product_id=product.id,
                price=product.price,
                quantity=item.quantity,
            )
        )

    # =========================
    # 3️⃣ Create order
    # =========================
    order = Order(
        user_id=user_id,
        total_amount=round(total_amount, 2),
        payment_method=order_data.payment_method,
        status=OrderStatus.PAYMENT_PENDING.value,
    )

    db.add(order)
    db.flush()  # gives order.id

    order.order_id = generate_order_id(order.id)
    order.items = order_items

    # =========================
    # 4️⃣ 🔥 SNAPSHOT ADDRESS
    # =========================
    order_address = OrderAddress(
        order_id=order.id,
        user_id=user_id,
        name=address.name,
        phone=address.phone,
        house_number=address.house_number,
        line1=address.line1,
        line2=address.line2,
        city=address.city,
        state=address.state,
        postal_code=address.postal_code,
        country=address.country,
    )

    db.add(order_address)

    # =========================
    # 5️⃣ Commit
    # =========================
    db.commit()
    db.refresh(order)

    return order
