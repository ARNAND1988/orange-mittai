from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, List

from app.database import get_db
from app.utils.auth import get_current_user
from app.models.user import User
from app.models.address import UserAddress, OrderAddress

router = APIRouter(prefix="/addresses", tags=["Addresses"])

@router.get("/me", response_model=Dict[str, List[AddressRead]])
def get_my_addresses(
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Returns:
    - saved_addresses: editable
    - order_addresses: read-only (used in past orders)

    Frontend should deduplicate using:
    (house_number + postal_code)
    """

    saved_addresses = (
        db.query(UserAddress)
        .filter(UserAddress.user_id == current_user.id)
        .all()
    )

    order_addresses = (
        db.query(OrderAddress)
        .filter(OrderAddress.user_id == current_user.id)
        .all()
    )

    return {
        "saved_addresses": saved_addresses,
        "order_addresses": order_addresses,
    }

@router.patch("/me/{address_id}", response_model=AddressRead)
def update_saved_address(
        address_id: int,
        payload: UserAddressUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    """
    Update a user saved address.
    This NEVER affects old orders.
    """

    address = (
        db.query(UserAddress)
        .filter(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id,
            )
        .first()
    )

    if not address:
        raise HTTPException(
            status_code=404,
            detail="Saved address not found",
        )

    data = payload.dict(exclude_unset=True)

    for field, value in data.items():
        setattr(address, field, value)

    db.commit()
    db.refresh(address)

    return address

@router.patch("/orders/{address_id}")
def block_order_address_edit():
    raise HTTPException(
        status_code=403,
        detail="Order addresses are immutable and cannot be edited",
    )
