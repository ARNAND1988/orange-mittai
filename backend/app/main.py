from fastapi import FastAPI
import os
from app.database import Base, engine
from app.config import SHOP_NAME

from app.api.v1.auth import router as auth_router
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.orders import router as orders_router

from app.api.v1.admin.product_admin import router as admin_product_router
from app.api.v1.admin.order_admin import router as admin_order_router
from app.api.v1.admin.tag_admin import router as admin_tag_router

from app.models.user import User
from app.models.product import Product
from app.models.cart import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title=SHOP_NAME)

# create tables
Base.metadata.create_all(bind=engine)

FRONTEND_ORIGINS = os.getenv(
    "FRONTEND_ORIGINS",
    "http://localhost:5173"
).split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routers
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["cart"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])

app.include_router(admin_product_router, prefix="/api/v1/admin/products", tags=["admin"])
app.include_router(admin_order_router, prefix="/api/v1/admin/orders", tags=["admin"])
app.include_router(admin_tag_router, prefix="/api/admin/tags", tags=["admin"])

@app.get("/health")
def health():
    return {"status": "ok", "shop": SHOP_NAME}
