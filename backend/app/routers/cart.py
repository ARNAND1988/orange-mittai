from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.cart import CartItemCreate
from app.crud.cart import add_to_cart
from app.dependencies import get_current_user
from app.schemas.cart_schema import CartItemCreate

router = APIRouter(prefix="/cart", tags=["Cart"])

@router.post("/")
def add_item(
        data: CartItemCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    return add_to_cart(db, user.id, data.product_id, data.quantity)
