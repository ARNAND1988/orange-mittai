from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.product import Product, Tag
from app.schemas.product_schema import ProductRead, ProductCreate, ProductUpdate
from app.utils.admin import require_admin
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ProductRead])
def get_products_admin(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return db.query(Product).all()

@router.post("/", response_model=ProductRead)
def create_product_admin(
        payload: ProductCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        image=payload.image,
        is_active=payload.is_active,
    )

    if payload.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(payload.tag_ids)).all()
        product.tags = tags

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

@router.patch("/{product_id}", response_model=ProductRead)
def update_product_admin(
        product_id: int,
        payload: ProductUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    data = payload.dict(exclude_unset=True)

    # Handle tag updates separately
    tag_ids = data.pop("tag_ids", None)
    if tag_ids is not None:
        product.tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()

    # Update remaining fields
    for field, value in data.items():
        setattr(product, field, value)

    db.commit()
    db.refresh(product)

    return product

@router.patch("/{product_id}/soft-delete")
def soft_delete_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404)

    product.is_active = False
    db.commit()

    return {"message": "Product deactivated"}

@router.patch("/{product_id}/restore")
def restore_product(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    product = db.query(Product).get(product_id)
    if not product:
        raise HTTPException(status_code=404)

    product.is_active = True
    db.commit()

    return {"message": "Product restored"}
