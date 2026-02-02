from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Product, Tag
from app.schemas.product_schema import (
    ProductRead,
    ProductCreate,
    ProductUpdate,
)
from app.utils.auth import get_current_user
from app.models.user import User

router = APIRouter()


@router.get("", response_model=List[ProductRead])
def list_products(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .filter(Product.is_active == True)
        .all()
    )

