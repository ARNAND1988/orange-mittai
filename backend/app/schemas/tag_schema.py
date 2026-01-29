from pydantic import BaseModel
from typing import Optional


class TagBase(BaseModel):
    name: str
    slug: str
    type: str  # CATEGORY | SUBCATEGORY | PROMOTION | LABEL
    parent_id: Optional[int] = None
    is_active: bool = True


class TagCreate(TagBase):
    pass


class TagUpdate(TagBase):
    pass


class TagRead(TagBase):
    id: int

    model_config = {
        "from_attributes": True
    }
