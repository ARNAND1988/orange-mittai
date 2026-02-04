from sqlalchemy.orm import Session
from sqlalchemy import select
from app.schemas.product_schema import ProductCreate
from app.models.product import Product, Tag
import logging

logger = logging.getLogger(__name__)

def create_product(
        db: Session,
        payload: ProductCreate
) -> int:
    product = Product(
        name=payload.name,
        description=payload.description,
        price=payload.price,
        stock=payload.stock,
        image=payload.image,
        is_active=payload.is_active
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product.id

def attach_tags_to_product(
        db: Session,
        *,
        product_id: int,
        tag_ids: list[int],
) -> None:
    """
    Attach tags to a product using SQLAlchemy relationships.
    """

    if not tag_ids:
        return

    logger.info(
        "Attaching tags %s to product %s",
        tag_ids,
        product_id
    )

    # 1️⃣ Load product
    product = db.execute(
        select(Product).where(Product.id == product_id)
    ).scalar_one()

    # 2️⃣ Load tags (only active ones, optional)
    tags = db.execute(
        select(Tag).where(
            Tag.id.in_(tag_ids),
            Tag.is_active == True
        )
    ).scalars().all()

    if not tags:
        logger.warning("No valid tags found for ids=%s", tag_ids)
        return

    # 3️⃣ Attach (SQLAlchemy handles product_tags table)
    product.tags.extend(tags)

    db.commit()
