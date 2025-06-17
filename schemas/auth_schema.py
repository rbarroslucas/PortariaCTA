from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    cpf: str
    password : str

    class Config:
        from_attributes = True