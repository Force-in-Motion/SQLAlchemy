from sqlalchemy import create_engine

from src.config.url import DB_URL

from src.models.base import Base
from src.models.manipulations import Manipulations
from src.models.manipulation_facts import ManipulationFacts
from src.models.owners import Owners
from src.models.pets import Pets
from src.models.species import Species


try:
    engine = create_engine(DB_URL.get('postgresql'), echo=True)
    Base.metadata.create_all(engine)
except Exception as e:
    print('Error!', e)




