from sqlalchemy import Column, String, Integer, Boolean
from config.database import Base

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
