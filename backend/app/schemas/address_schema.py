from pydantic import BaseModel
from typing import Optional

class UserAddressBase(BaseModel):
    label: Optional[str] = "Home"
    name: str
    phone: str

    house_number: str
    line1: str
    line2: Optional[str] = None
    city: str
    state: str
    postal_code: str
    country: str

    is_default: Optional[bool] = False


class UserAddressCreate(UserAddressBase):
    pass


class UserAddressUpdate(BaseModel):
    label: Optional[str]
    name: Optional[str]
    phone: Optional[str]

    house_number: Optional[str]
    line1: Optional[str]
    line2: Optional[str]
    city: Optional[str]
    state: Optional[str]
    postal_code: Optional[str]
    country: Optional[str]

    is_default: Optional[bool]


class UserAddressRead(UserAddressBase):
    id: int

    class Config:
        from_attributes = True
