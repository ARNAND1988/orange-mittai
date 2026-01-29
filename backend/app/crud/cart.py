from sqlalchemy.orm import Session
from app.models.cart import CartItem

def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int):
    item = db.query(CartItem).filter_by(
        user_id=user_id, product_id=product_id
    ).first()

    if item:
        item.quantity += quantity
    else:
        item = CartItem(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(item)

    db.commit()
    return item
