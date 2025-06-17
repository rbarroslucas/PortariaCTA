from pydantic import BaseModel
from typing import Optional

class DeliverySchema(BaseModel):
    name : str
    establishment : str
    address : str
    user : str
