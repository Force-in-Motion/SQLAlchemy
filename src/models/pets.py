from src.models.base import Base
from sqlalchemy import Column, Integer, String, Float, DateTime


class Pets(Base):
    """
    Класс для описания питомцев
    """

    __tablename__ = 'pets'

    id = Column(Integer, primary_key=True, autoincrement=True)
    species = Column(Integer, nullable=True)
    owner_id = Column(Integer, nullable=True)
    name = Column(String, nullable=False)
    sex = Column(String, default='Male')
    weight = Column(Float, nullable=True)
    birthdate = Column(DateTime, nullable=True)