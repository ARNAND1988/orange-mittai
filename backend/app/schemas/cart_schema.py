from pydantic import BaseModel

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int

class CartItemRead(BaseModel):
    id: int
    product_id: int
    user_id: int
    quantity: int

    class Config:
        orm_mode = True
