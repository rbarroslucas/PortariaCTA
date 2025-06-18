from sqlalchemy import Column, String
from .access_base import AccessBase
from typing import Optional

class Uber(AccessBase):
    __tablename__ = "ubers"
    access_type = "uber"

    name = Column("name", String, nullable=False)
    license_plate = Column("license_plate", String, nullable=False)

    def __init__(self, name: str, address: str, user: str, dweller_id: int,
                 license_plate: str):
        super().__init__(address=address, user=user, dweller_id=dweller_id)
        self.name = name
        self.license_plate = license_plate


class UberBuilder:
    def __init__(self):
        self._address: Optional[str] = None
        self._user: Optional[str] = None
        self._dweller_id: Optional[int] = None
        self._name: Optional[str] = None
        self._license_plate: Optional[str] = None

    def with_address(self, address: str) -> 'UberBuilder':
        self._address = address
        return self

    def with_user(self, user: str) -> 'UberBuilder':
        self._user = user
        return self

    def with_dweller_id(self, dweller_id: int) -> 'UberBuilder':
        self._dweller_id = dweller_id
        return self

    def with_name(self, name: str) -> 'UberBuilder':
        self._name = name
        return self

    def with_license_plate(self, license_plate: str) -> 'UberBuilder':
        self._license_plate = license_plate
        return self

    def build(self) -> Uber:
        if None in [self._address, self._user, self._dweller_id, self._name, self._license_plate]:
            raise ValueError("Campos obrigatórios não preenchidos para transporte.")
        
        assert self._address is not None
        assert self._user is not None
        assert self._dweller_id is not None
        assert self._name is not None
        assert self._license_plate is not None

        return Uber(
            address=self._address,
            user=self._user,
            dweller_id=self._dweller_id,
            name = self._name,
            license_plate=self._license_plate
        )