from bot.database.main import Base
from sqlalchemy import Integer, Column, String, Boolean


class Ltd(Base):
    __tablename__ = "ltds"

    id = Column(String, primary_key=True)
    title = Column(String)
    company_id = Column(String)
    is_active = Column(Boolean)

    def __init__(self, id, company_id, title="Noname", is_active=True):
        self.id = id
        self.title = title
        self.company_id = company_id
        self.is_active = is_active

    def __repr__(self):
        return f"ООО {self.title} id_object: {id(self)}"

    def __str__(self):
        return f"ООО {self.title}"
