from pydantic import BaseModel
from typing import Optional

class AddressRead(BaseModel):
    id: int
    name: str
    phone: str
    house_number: str
    line1: str
    line2: Optional[str]
    city: str
    state: str
    postal_code: str
    country: str

    model_config = {
        "from_attributes": True
    }

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
