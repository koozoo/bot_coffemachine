from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Device(Base):
    __tablename__ = "divices"

    id = Column(String, primary_key=True)
    model = Column(String)
    device_type = Column(String)
    sn = Column(String)
    company_id = Column(String)
    address_id = Column(String)
    is_activ = Column(Boolean)

    def __init__(self, id, model, device_type, sn, company_id, address_id, is_activ=True):
        self.id = id
        self.model = model
        self.device_type = device_type
        self.sn = sn
        self.company_id = company_id
        self.address_id = address_id
        self.is_activ = is_activ

    def __str__(self):
        return f"MODEL: {self.model}\n" \
               f"S/N: {self.sn}"
