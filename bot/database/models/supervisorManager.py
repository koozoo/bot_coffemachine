from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class SupervisorManager(Base):
    __tablename__ = "supervisorManager"

    id = Column(Integer, primary_key=True)
    supervisor_id = Column(Integer)
    manager_id = Column(Integer)

    def __init__(self, super, manager):
        self.supervisor_id = super
        self.manager_id = manager
