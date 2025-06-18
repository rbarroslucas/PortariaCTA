from sqlalchemy import Column, String, Integer, Boolean
from config.database import Base
from typing import Optional

class Dweller(Base):
    __tablename__ = "dwellers"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String)
    cpf = Column("cpf", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean, default=True)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, cpf, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.cpf = cpf
        self.password = password
        self.active = active
        self.admin = admin

class DwellerBuilder:
    def __init__(self):
        self._name: Optional[str] = None
        self._email: Optional[str] = None
        self._cpf: Optional[str] = None
        self._password: Optional[str] = None
        self._active: Optional[bool] = True
        self._admin: Optional[bool] = False

    def with_name(self, name: Optional[str]) -> 'DwellerBuilder':
        self._name = name
        return self

    def with_email(self, email: Optional[str]) -> 'DwellerBuilder':
        self._email = email
        return self

    def with_cpf(self, cpf: Optional[str]) -> 'DwellerBuilder':
        self._cpf = cpf
        return self

    def with_password(self, password: Optional[str]) -> 'DwellerBuilder':
        self._password = password
        return self

    def with_active_status(self, active: bool) -> 'DwellerBuilder':
        if self._active is not None:
            self._active = active
        return self

    def as_admin(self, admin: bool) -> 'DwellerBuilder':
        if self._admin is not None:
            self._admin = admin
        return self

    def build(self) -> Dweller:
        if None in [self._name, self._email, self._cpf, self._password]:
            raise ValueError("Campos obrigatórios não preenchidos para morador.")

        assert self._name is not None
        assert self._email is not None
        assert self._cpf is not None
        assert self._password is not None
        assert self._active is not None
        assert self._admin is not None

        return Dweller(
            name = self._name,
            email = self._email,
            cpf = self._cpf,
            password = self._password,   
            active = self._active,
            admin = self._admin               
        )
