from pydantic import BaseModel
from typing import Optional

class UberSchema(BaseModel):
    name : str
    license_plate :str
    address : str
    user : str