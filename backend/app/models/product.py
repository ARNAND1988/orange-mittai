from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import relationship
from app.db.base import Base

product_tags = Table(
    "product_tags",
    Base.metadata,
    Column("product_id", ForeignKey("products.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
)


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, index=True, nullable=False)

    # CATEGORY | SUBCATEGORY | PROMOTION | LABEL
    type = Column(String, nullable=False)

    parent_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    parent = relationship(
        "Tag",
        remote_side=[id],
        backref="children"
    )

    is_active = Column(Boolean, default=True, nullable=False)

    products = relationship(
        "Product",
        secondary=product_tags,
        back_populates="tags",
    )

    def __repr__(self):
        return f"<Tag(name={self.name}, type={self.type})>"


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String)
    image = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    is_active = Column(Boolean, default=True, nullable=False)

    tags = relationship(
        "Tag",
        secondary=product_tags,
        back_populates="products",
    )

    def __repr__(self):
        tag_names = [tag.name for tag in self.tags]
        return f"<Product(name={self.name}, tags={tag_names})>"
