from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base
from config.database import Base

class AccessBase(Base):
    __abstract__ = True

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    address = Column("address", String, nullable=False)
    user = Column("user", String, nullable=False)
    dweller_id = Column("dweller", ForeignKey("dwellers.id"), nullable=False)

    def __init__(self, address: str, user: str, dweller_id: int):
        self.address = address
        self.user = user
        self.dweller_id = dweller_id