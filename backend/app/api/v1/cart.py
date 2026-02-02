from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.cart import CartItem
from app.models.product import Product
from app.schemas.cart_schema import CartItemCreate, CartItemRead
from app.utils.auth import get_current_user

router = APIRouter()

# ------------------------------
# Add item to cart
# ------------------------------
@router.post("", response_model=CartItemRead)
def add_to_cart(item: CartItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # Check product exists
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Check if already in cart
    cart_item = db.query(CartItem).filter(
        CartItem.user_id == user.id,
        CartItem.product_id == item.product_id
    ).first()

    if cart_item:
        cart_item.quantity += item.quantity
    else:
        cart_item = CartItem(user_id=user.id, product_id=item.product_id, quantity=item.quantity)
        db.add(cart_item)

    db.commit()
    db.refresh(cart_item)
    return cart_item

# ------------------------------
# Get all cart items for user
# ------------------------------
@router.get("", response_model=List[CartItemRead])
def get_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    items = db.query(CartItem).filter(CartItem.user_id == user.id).all()
    return items

# ------------------------------
# Update quantity of a cart item
# ------------------------------
@router.put("/{cart_item_id}", response_model=CartItemRead)
def update_cart_item(cart_item_id: int, quantity: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    cart_item.quantity = quantity
    db.commit()
    db.refresh(cart_item)
    return cart_item

# ------------------------------
# Remove cart item
# ------------------------------
@router.delete("/{cart_item_id}")
def remove_cart_item(cart_item_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.user_id == user.id
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    return {"detail": "Cart item removed"}
