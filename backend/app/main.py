from fastapi import FastAPI
import os
import logging
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.config import SHOP_NAME
from app.logging import setup_logging

from app.api.v1.auth import router as auth_router
from app.api.v1.products import router as products_router
from app.api.v1.cart import router as cart_router
from app.api.v1.orders import router as orders_router
from app.api.v1.profile import router as profile_router

from app.api.v1.admin.product_admin import router as admin_product_router
from app.api.v1.admin.order_admin import router as admin_order_router
from app.api.v1.admin.tag_admin import router as admin_tag_router
from app.api.v1.tags import router as tag_router

from app.config import APP_ENV
# -------------------------------------------------
# Logging MUST be first
# -------------------------------------------------
setup_logging()

# -------------------------------------------------
# App
# -------------------------------------------------
app = FastAPI(title=SHOP_NAME)

# -------------------------------------------------
# Static files (local + Cloud Run safe)
# -------------------------------------------------
STATIC_DIR = "/tmp/products"

# 🔥 CRITICAL FIX: ensure directory exists BEFORE mounting
os.makedirs(STATIC_DIR, exist_ok=True)

logging.info("[STATIC] Mounting /products -> %s", STATIC_DIR)
logging.info("[STATIC] Exists? %s", os.path.exists(STATIC_DIR))

app.mount(
    "/products",
    StaticFiles(directory=STATIC_DIR),
    name="products"
)

# -------------------------------------------------
# CORS
# -------------------------------------------------



if APP_ENV == "pi":
    allow_origins = ["http://shop.localhost"]
elif APP_ENV == "gcp":
    allow_origins = ["https://shop.yourdomain.com"]
else:
    allow_origins = ["http://localhost:5173"]

logging.info("APP_ENV %s, [CORS] Allowed origins: %s", APP_ENV, allow_origins)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Routers
# -------------------------------------------------
app.include_router(auth_router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(products_router, prefix="/api/v1/products", tags=["products"])
app.include_router(cart_router, prefix="/api/v1/cart", tags=["cart"])
app.include_router(orders_router, prefix="/api/v1/orders", tags=["orders"])
app.include_router(profile_router, prefix="/api/v1/profile", tags=["profile"])

app.include_router(admin_product_router, prefix="/api/v1/admin/products", tags=["admin"])
app.include_router(admin_order_router, prefix="/api/v1/admin/orders", tags=["admin"])
app.include_router(admin_tag_router, prefix="/api/v1/admin/tags", tags=["admin"])

app.include_router(tag_router, prefix="/api/v1/tags", tags=["tags"])

# -------------------------------------------------
# Health check
# -------------------------------------------------
@app.get("/health")
def health():
    return {
        "status": "ok",
        "shop": SHOP_NAME
    }
