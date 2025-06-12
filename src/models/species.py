from src.models.base import Base
from sqlalchemy import Column, Integer, String


class Species(Base):
    """ Вид питомца """

    __tablename__ = 'species'

    species_id = Column(Integer, primary_key=True, autoincrement=True)
    species_name = Column(String, nullable=False)

