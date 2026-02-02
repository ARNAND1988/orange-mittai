from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.utils.admin import require_admin
from app.database import get_db
from app.models.product import Product, Tag
from app.schemas.product_schema import ProductRead, ProductCreate, ProductUpdate
from app.utils.admin import require_admin
from app.models.user import User
from app.utils.auth import get_current_user
from app.services.uplaod_admin_service import upload_product_image
from app.services.product_admin_service import create_product, attach_tags_to_product
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("", response_model=List[ProductRead])
def get_products_admin(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="Admin access required")

    return db.query(Product).all()


@router.post("/add")
async def add_product(
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),

        image: UploadFile = File(...),
        name: str = Form(...),
        description: str = Form(""),
        price: float = Form(...),
        stock: int = Form(...),
        is_active: bool = Form(True),
        tag_ids: Optional[str] = Form(None)
):

    parsed_tag_ids = (
        [int(x) for x in tag_ids.split(",")]
        if tag_ids else []
    )

    logger.info("Parsed tag IDs: %s", parsed_tag_ids)

    # 1️⃣ Upload image
    image_url = upload_product_image(image)

    # 2️⃣ Build payload
    payload = ProductCreate(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image=image_url,
        is_active=is_active,
        tag_ids=parsed_tag_ids
    )

    # 3️⃣ Create product
    product_id = create_product(db, payload)

    # 4️⃣ Attach tags (if any)
    if parsed_tag_ids:
        attach_tags_to_product(
            db,
            product_id=product_id,
            tag_ids=parsed_tag_ids
        )

    return {
        "id": product_id,
        "image": image_url,
        "tag_ids": parsed_tag_ids,
        "status": "created"
    }

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

@router.get("/{product_id}", response_model=ProductRead)
def get_product_admin(
        product_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    if not current_user.is_admin:
        raise HTTPException(status_code=403)

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
