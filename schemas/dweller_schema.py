from pydantic import BaseModel
from typing import Optional

class DwellerSchema(BaseModel):
    name : str
    email : str
    cpf : str
    password : str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    class Config:
        from_attributes = True 