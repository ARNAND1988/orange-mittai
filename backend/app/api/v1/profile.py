from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.models.address import UserAddress
from app.utils.auth import get_current_user
from app.schemas.user_schema import UserUpdate
from app.schemas.address_schema import (
    UserAddressCreate,
    UserAddressRead,
    UserAddressUpdate,
)
from app.utils.security import verify_password, hash_password

router = APIRouter()


@router.get("")
def get_profile(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    user = (
        db.query(User)
        .filter(User.id == current_user.id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return {
        "id": user.id,
        "email": user.email,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone": user.phone,
        "is_admin": user.is_admin,
    }

@router.get("/addresses", response_model=list[UserAddressRead])
def list_addresses(
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    return (
        db.query(UserAddress)
        .filter(UserAddress.user_id == user.id)
        .order_by(UserAddress.is_default.desc())
        .all()
    )


@router.post("/addresses", response_model=UserAddressRead)
def add_address(
        payload: UserAddressCreate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    if payload.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == user.id
        ).update({"is_default": False})

    address = UserAddress(
        user_id=user.id,
        **payload.dict(),
    )

    db.add(address)
    db.commit()
    db.refresh(address)
    return address


@router.put("/addresses/{address_id}", response_model=UserAddressRead)
def update_address(
        address_id: int,
        payload: UserAddressUpdate,
        db: Session = Depends(get_db),
        user=Depends(get_current_user),
):
    address = (
        db.query(UserAddress)
        .filter(
            UserAddress.id == address_id,
            UserAddress.user_id == user.id,
            )
        .first()
    )

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    for field, value in payload.dict(exclude_unset=True).items():
        setattr(address, field, value)

    if payload.is_default:
        db.query(UserAddress).filter(
            UserAddress.user_id == user.id,
            UserAddress.id != address.id,
            ).update({"is_default": False})

    db.commit()
    db.refresh(address)
    return address

@router.put("")
def update_profile(
        payload: UserUpdate,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # --------------------
    # Profile fields
    # --------------------
    if payload.first_name is not None:
        user.first_name = payload.first_name

    if payload.last_name is not None:
        user.last_name = payload.last_name

    if payload.phone is not None:
        user.phone = payload.phone

    # --------------------
    # Password change
    # --------------------
    if payload.new_password:
        if not payload.current_password:
            raise HTTPException(
                status_code=400,
                detail="Current password is required to change password",
            )

        if not verify_password(payload.current_password, user.hashed_password):
            raise HTTPException(
                status_code=400,
                detail="Current password is incorrect",
            )

        user.hashed_password = hash_password(payload.new_password)

    db.commit()
    db.refresh(user)

    return {
        "message": "Profile updated successfully",
    }

@router.delete("/addresses/{address_id}")
def delete_address(
        address_id: int,
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user),
):
    address = (
        db.query(UserAddress)
        .filter(
            UserAddress.id == address_id,
            UserAddress.user_id == current_user.id,
            )
        .first()
    )

    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    was_default = address.is_default

    db.delete(address)
    db.commit()

    # Optional safety: ensure at least one default address
    if was_default:
        next_address = (
            db.query(UserAddress)
            .filter(UserAddress.user_id == current_user.id)
            .first()
        )
        if next_address:
            next_address.is_default = True
            db.commit()

    return {"message": "Address deleted successfully"}