from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True)
    full_address = Column(String)
    phone = Column(String)
    ltd_id = Column(Integer)
    is_active = Column(Boolean)

    def __init__(self, id, address, ltd_id, phone="0", is_active=True):
        self.id = id
        self.full_address = address
        self.ltd_id = ltd_id
        self.phone = phone
        self.is_active = is_active

    def __repr__(self):
        return f"Адресс: {self.full_address} id_object: {id(self)}"

    def __str__(self):
        return f"Адрес: {self.full_address}"
