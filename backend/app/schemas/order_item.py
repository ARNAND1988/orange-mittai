from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderItemRead(BaseModel):
    product_id: int
    product_name: str
    price: float
    quantity: int

    class Config:
        from_attributes = True