from sqlalchemy import Column, Integer, ForeignKey, Float, DateTime, String, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base
from app.schemas.order_status import OrderStatus

order_status_enum = Enum(
    OrderStatus,
    name="order_status",
    create_type=False  # 🚨 REQUIRED for Cloud SQL
)

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(String(30), unique=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), index=True)

    total_amount = Column(Float, nullable=False)

    status = Column(order_status_enum, default=OrderStatus.PAYMENT_PENDING, index=True)
    payment_method = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)

    address = relationship(
        "OrderAddress",
        uselist=False,                  # 🔥 SINGLE object
        back_populates="order",
        cascade="all, delete-orphan",
    )

    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan"
    )
