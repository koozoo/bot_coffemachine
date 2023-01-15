from bot.database.main import Base
from sqlalchemy import Integer, Column


class Supervisor(Base):
    __tablename__ = "supervisors"

    supervisor_id = Column(Integer, primary_key=True)
    user_id = Column(Integer)

    def __init__(self, supervisor_id, user_id):
        self.user_id = user_id
        self.supervisor_id = supervisor_id
