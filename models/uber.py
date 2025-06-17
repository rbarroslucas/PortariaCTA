from sqlalchemy import Column, String, Integer, ForeignKey
from config.database import Base

class Uber(Base):
    __tablename__ = "ubers"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String, nullable=False)
    license_plate = Column("license_plate", String, nullable=False)
    address = Column("address", String, nullable=False)

    user = Column("name_user", String)
    dweller_id = Column("dweller", ForeignKey("dwellers.id"), nullable=False)

    def __init__(self, name, license_plate, address, user, dweller_id):
        self.name = name
        self.license_plate = license_plate
        self.address = address
        self.user = user
        self.dweller_id = dweller_id