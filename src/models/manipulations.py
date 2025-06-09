from src.models.base import Base
from sqlalchemy import Column, String, Integer


class Manipulations(Base):
    """ Тип манипуляции с питомцем """

    __tablename__ = 'manipulations'

    manipulation_id = Column(Integer, primary_key=True)
    manipulation_name = Column(String, nullable=False)
