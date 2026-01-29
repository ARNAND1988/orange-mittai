from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.crud.order import place_order
from app.dependencies import get_current_user
from app.schemas.order_schema import OrderRead

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/")
def create_order(
        db: Session = Depends(get_db),
        user=Depends(get_current_user)
):
    order = place_order(db, user.id)
    if not order:
        raise HTTPException(status_code=400, detail="Cart is empty")
    return order
