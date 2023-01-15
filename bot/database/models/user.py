from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    phone = Column(String(26))
    email = Column(String)
    company_id = Column(Integer)
    unit_id = Column(Integer)
    access = Column(Integer)
    role = Column(Integer)
    is_activ = Column(Boolean)

    def __init__(self, user_id, name="Noname", phone="0", email="null", access=0,
                 role=4, activ=True, company_id=0, unit_id=0):
        self.user_id = user_id
        self.name = name
        self.phone = phone
        self.email = email
        self.access = access
        self.role = role
        self.company_id = company_id
        self.unit_id = unit_id
        self.is_activ = activ

    def __repr__(self):
        return f"{self.user_id} {self.name}"