import os
from dotenv import load_dotenv

load_dotenv()  # load from .env file

APP_ENV = os.getenv("APP_ENV", "local")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./local_shop.db")
JWT_SECRET = os.getenv("JWT_SECRET", "local-secret")
ANALYTICS_ENABLED = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"

PAYMENT_PROVIDER = os.getenv("PAYMENT_PROVIDER", "mock")
WHATSAPP_PROVIDER = os.getenv("WHATSAPP_PROVIDER", "mock")
SHOP_NAME = os.getenv("SHOP_NAME", "Orange Mittai")

SECRET_KEY = "supersecretkey"  # change for production
ALGORITHM = "HS256"
