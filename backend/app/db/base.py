from sqlalchemy.orm import declarative_base

Base = declarative_base()

# 🔥 THIS LINE IS CRITICAL
from app.models import *  # noqa