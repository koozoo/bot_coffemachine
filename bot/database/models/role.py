from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True)
    title = Column(Integer)

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"Роль: {self.title}"

    def __repr__(self):
        return f"роль: {self.title} id_object: {id(self)}"
