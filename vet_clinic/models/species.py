from vet_clinic.models.base import Base
from sqlalchemy import Column, Integer, String


class Species(Base):
    """ Вид питомца """
    __tablename__ = 'species'

    species_id = Column(Integer, primary_key=True)
    species_name = Column(String(30), nullable=False)

