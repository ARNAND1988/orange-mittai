from pydantic import BaseModel, Field
from typing import Optional, List


class TagBase(BaseModel):
    name: str
    slug: str
    type: str  # CATEGORY | SUBCATEGORY | PROMOTION | LABEL
    parent_id: Optional[int] = None
    is_active: bool = True

class TagRead(TagBase):
    id: int

    class Config:
        orm_mode = True

# ========================
# Product schemas
# ========================

class ProductBase(BaseModel):
    name: str
    description: str = ""
    price: float
    stock: int = 0
    image: str
    is_active: bool = True


class ProductRead(ProductBase):
    id: int
    tags: List[TagRead] = Field(default_factory=list)

    class Config:
        orm_mode = True


class ProductCreate(ProductBase):
    tag_ids: List[int] = Field(default_factory=list)



# ========================
# Category schemas
# ========================

class ProductCategoryRead(BaseModel):
    id: int
    name: str
    image: str
    description: Optional[str] = None
    parent_id: Optional[int] = None

    products: List[ProductRead] = Field(default_factory=list)
    subcategories: List["ProductCategoryRead"] = Field(default_factory=list)

    class Config:
        orm_mode = True


ProductCategoryRead.update_forward_refs()

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    image: Optional[str] = None
    is_active: Optional[bool] = None

    # Replace categories with tags
    tag_ids: Optional[List[int]] = None
