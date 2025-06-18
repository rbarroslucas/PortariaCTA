from sqlalchemy import Column, String
from .access_base import AccessBase
from typing import Optional

class DeliveryGuy(AccessBase):
    __tablename__ = "delivery_guys"
    access_type = "delivery"

    name = Column("name", String, nullable=True)
    establishment = Column("establishment", String, nullable=False)

    def __init__(self, address: str, user: str, dweller_id: int,
                 establishment: str, name: Optional[str] = None):
        super().__init__(address=address, user=user, dweller_id=dweller_id)
        self.name = name
        self.establishment = establishment

class DeliveryGuyBuilder:
    def __init__(self):
        self._address: Optional[str] = None
        self._user: Optional[str] = None
        self._dweller_id: Optional[int] = None
        self._name: Optional[str] = None
        self._establishment: Optional[str] = None

    def with_address(self, address: Optional[str] = None) -> 'DeliveryGuyBuilder':
        self._address = address
        return self

    def with_user(self, user: Optional[str] = None) -> 'DeliveryGuyBuilder':
        self._user = user
        return self

    def with_dweller_id(self, dweller_id: int) -> 'DeliveryGuyBuilder':
        self._dweller_id = dweller_id
        return self

    def with_name(self, name: Optional[str] = None) -> 'DeliveryGuyBuilder':
        self._name = name
        return self
    
    def with_establishment(self, establishment: Optional[str] = None) -> 'DeliveryGuyBuilder':
        self._establishment = establishment
        return self
    
    
    def build(self) -> DeliveryGuy:
        if None in [self._address, self._user, self._dweller_id, self._establishment]:
            raise ValueError("Campos obrigatórios não preenchidos para delivery.")
        
        assert self._address is not None
        assert self._user is not None
        assert self._dweller_id is not None
        assert self._establishment is not None

        return DeliveryGuy(
            address=self._address,
            user=self._user,
            dweller_id=self._dweller_id,
            name = self._name,
            establishment = self._establishment,
        )