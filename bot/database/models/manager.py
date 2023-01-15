from bot.database.main import Base
from sqlalchemy import Integer, Column


class Manager(Base):
    __tablename__ = "managers"

    manager_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    def __init__(self, manager_id, user_id):
        self.user_id = user_id
        self.manager_id = manager_id
