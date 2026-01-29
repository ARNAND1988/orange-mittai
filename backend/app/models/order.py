from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(30), unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    total_amount = Column(Float, nullable=False)

    status = Column(String, default="PAYMENT_PENDING", index=True)
    payment_method = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
