from src.models.base import Base
from sqlalchemy import Column, String, Integer


class Owners(Base):
    """ Владельцы питомцев """

    __tablename__ = 'owners'

    owner_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_name = Column(String, nullable=False)
    owner_phone = Column(String, nullable=True)
    owner_email = Column(String, nullable=True)


