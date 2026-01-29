from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import relationship, Session
from app.db.base import Base


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    label = Column(String, default="Home")  # Home / Office / Other
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    house_number = Column(String, nullable=False)
    line1 = Column(String, nullable=False)
    line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", backref="addresses")

    def __repr__(self):
        return f"<UserAddress({self.house_number}, {self.postal_code})>"

class OrderAddress(Base):
    __tablename__ = "order_addresses"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    house_number = Column(String, nullable=False)
    line1 = Column(String, nullable=False)
    line2 = Column(String, nullable=True)
    city = Column(String, nullable=False)
    state = Column(String, nullable=False)
    postal_code = Column(String, nullable=False)
    country = Column(String, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", backref="address")
    user = relationship("User")

    def __repr__(self):
        return f"<OrderAddress(order={self.order_id}, {self.house_number}, {self.postal_code})>"

def get_all_known_addresses_for_user(db: Session, user_id: int):
    """
    Returns all addresses known to the user:
    - Saved user addresses (editable)
    - Order addresses (read-only snapshots)

    Frontend should deduplicate using:
    (house_number + postal_code)
    """

    saved_addresses = (
        db.query(UserAddress)
        .filter(UserAddress.user_id == user_id)
        .all()
    )

    order_addresses = (
        db.query(OrderAddress)
        .filter(OrderAddress.user_id == user_id)
        .all()
    )

    return {
        "saved_addresses": saved_addresses,
        "order_addresses": order_addresses,
    }

def update_user_address(
        db: Session,
        *,
        address_id: int,
        user_id: int,
        data: dict,
):
    """
    Edit a user's saved address.

    - Only affects UserAddress
    - Does NOT affect any past orders
    """

    address = (
        db.query(UserAddress)
        .filter(
            UserAddress.id == address_id,
            UserAddress.user_id == user_id,
            )
        .first()
    )

    if not address:
        raise ValueError("Address not found or access denied")

    # Prevent accidental changes to ownership
    data.pop("user_id", None)
    data.pop("id", None)

    for field, value in data.items():
        if hasattr(address, field):
            setattr(address, field, value)

    db.commit()
    db.refresh(address)

    return address
