from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Company(Base):
    __tablename__ = "companys"

    id = Column(String, primary_key=True)
    title = Column(String)
    is_active = Column(Boolean)

    def __init__(self, id, title="Noname", is_active=True):
        self.id = id
        self.title = title
        self.is_active = is_active

    def __repr__(self):
        return f"Компания {self.title} id_object: {id(self)}"

    def __str__(self):
        return f"Компания {self.title}"

