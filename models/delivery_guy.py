from sqlalchemy import Column, String, Integer, ForeignKey
from config.database import Base

class DeliveryGuy(Base):
    __tablename__ = "delivery_guys"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    establishment = Column("establishment", String, nullable=False)
    address = Column("address", String, nullable=False)

    user = Column("user", String, nullable=False)
    dweller_id = Column(Integer, ForeignKey("dwellers.id"), nullable=False)

    def __init__(self, name, establishment, address, user, dweller_id):
        self.name = name
        self.establishment = establishment
        self.address = address
        self.user = user
        self.dweller_id = dweller_id