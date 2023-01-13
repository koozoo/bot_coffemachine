from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Access(Base):
    __tablename__ = "access"

    id = Column(Integer, primary_key=True)
    title = Column(String)

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return f"Уровень доступа: {self.title}"
