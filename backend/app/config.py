import os
from dotenv import load_dotenv

load_dotenv()

# -------------------------------------------------
# Environment
# -------------------------------------------------
APP_ENV = os.getenv("APP_ENV", "local")  # local | pi | gcp

IS_PROD = APP_ENV == "gcp"

# -------------------------------------------------
# Database
# -------------------------------------------------
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./local_shop.db"  # tests / fallback only
)

# -------------------------------------------------
# Storage (FILES)
# -------------------------------------------------
# local  -> Raspberry Pi filesystem
# gcs    -> Google Cloud Storage
STORAGE_BACKEND = os.getenv("STORAGE_BACKEND", "local")

# Local storage
LOCAL_UPLOAD_DIR = os.getenv("LOCAL_UPLOAD_DIR", "uploads")

# GCP Cloud Storage
GCP_PROJECT = os.getenv("GCP_PROJECT")
BUCKET_NAME = os.getenv("BUCKET_NAME")
CDN_BASE_URL = os.getenv("CDN_BASE_URL")  # optional (Cloud CDN)

# -------------------------------------------------
# Security
# -------------------------------------------------
JWT_SECRET = os.getenv("JWT_SECRET", "local-secret")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")  # override in prod
ALGORITHM = "HS256"

# -------------------------------------------------
# Features / Providers
# -------------------------------------------------
ANALYTICS_ENABLED = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"

PAYMENT_PROVIDER = os.getenv("PAYMENT_PROVIDER", "mock")
WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "mock")

# -------------------------------------------------
# App
# -------------------------------------------------
SHOP_NAME = os.getenv("SHOP_NAME", "Orange Mittai")
