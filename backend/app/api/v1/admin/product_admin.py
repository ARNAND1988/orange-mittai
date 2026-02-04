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
from app.services.uplaod_admin_service import upload_product_image, delete_product_image
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

@router.patch("/{product_id}")
async def update_product_admin(
        product_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(require_admin),

        # Optional fields
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: Optional[float] = Form(None),
        stock: Optional[int] = Form(None),
        is_active: Optional[bool] = Form(None),
        tag_ids: Optional[str] = Form(None),
        image: Optional[UploadFile] = File(None),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # 1️⃣ Update image if provided
    if image:
        old_image_url = product.image

        new_image_url = upload_product_image(image)
        product.image = new_image_url

        if old_image_url:
            delete_product_image(old_image_url)

    # 2️⃣ Update scalar fields
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    if is_active is not None:
        product.is_active = is_active

    # 3️⃣ Update tags (replace all)
    if tag_ids is not None:
        parsed_tag_ids = (
            [int(x) for x in tag_ids.split(",")]
            if tag_ids else []
        )

        product.tags = (
            db.query(Tag)
            .filter(Tag.id.in_(parsed_tag_ids))
            .all()
        )

    db.commit()
    db.refresh(product)

    return {
        "id": product.id,
        "image": product.image,
        "tag_ids": [t.id for t in product.tags],
        "status": "updated"
    }