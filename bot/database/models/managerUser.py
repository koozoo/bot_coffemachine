from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class ManagerUser(Base):
    __tablename__ = "managerUser"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    manager_id = Column(Integer)

    def __init__(self, user, manager):
        self.user_id = user
        self.manager_id = manager
