from typing import Optional, Literal
from pydantic import BaseModel


class AccessRequestSchema(BaseModel):
    access_type: Literal["guest", "delivery", "uber"]

    # Comum
    name: Optional[str] = None
    address: Optional[str] = None
    user: Optional[str] = None

    # Campos específicos para guest
    is_driving: Optional[bool] = None

    # Campos específicos para delivery
    establishment: Optional[str] = None

    # Campos específicos para transport (Uber, taxi, etc.)
    license_plate: Optional[str] = None
