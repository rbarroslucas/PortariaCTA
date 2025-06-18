from sqlalchemy import Column, String, Boolean
from .access_base import AccessBase
from typing import Optional
from fastapi import HTTPException

class Guest(AccessBase):
    __tablename__ = "guests"
    access_type = "guest"

    name = Column("name", String, nullable=False)
    is_driving = Column("is_driving", Boolean, nullable=True)

    def __init__(self, name: str, address: str, user: str, dweller_id: int,
                 is_driving: Optional[bool] = None):
        super().__init__(address=address, user=user, dweller_id=dweller_id)
        self.name = name
        self.is_driving = is_driving


class GuestBuilder:
    def __init__(self):
        self._address: Optional[str] = None
        self._user: Optional[str] = None
        self._dweller_id: Optional[int] = None
        self._name: Optional[str] = None
        self._is_driving: Optional[bool] = None

    def with_address(self, address: Optional[str] = None) -> 'GuestBuilder':
        self._address = address
        return self

    def with_user(self, user: Optional[str] = None) -> 'GuestBuilder':
        self._user = user
        return self

    def with_dweller_id(self, dweller_id: int) -> 'GuestBuilder':
        self._dweller_id = dweller_id
        return self

    def with_name(self, name: Optional[str] = None) -> 'GuestBuilder':
        self._name = name
        return self

    def with_is_driving(self, is_driving: Optional[bool] = None) -> 'GuestBuilder':
        self._is_driving = is_driving
        return self

    def build(self) -> Guest:
        if None in [self._address, self._user, self._dweller_id, self._name] or "" in [self._address, self._user, self._name]:
            raise HTTPException(status_code=400, detail='Campos obrigatórios não preenchidos para convidado.')
        
        assert self._address is not None
        assert self._user is not None
        assert self._dweller_id is not None
        assert self._name is not None

        return Guest(
            address=self._address,
            user=self._user,
            dweller_id=self._dweller_id,
            name=self._name,
            is_driving=self._is_driving
        )
    
