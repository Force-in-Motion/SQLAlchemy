from src.models.base import Base
from sqlalchemy import Column, Integer, Boolean, DateTime, Text


class ManipulationFacts(Base):
    """
    Тип манипуляции, производимой с питомцем
    """

    __tablename__ = 'manipulation_facts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    pet_id = Column(Integer, nullable=False)
    manipulation_id = Column(Integer, nullable=False)
    is_planned = Column(Boolean, default=True)
    begin_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    result = Column(Text, nullable=True)