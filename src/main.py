from config.url import DB_URL

from models.base import Base
from models.manipulations import Manipulations
from models.manipulation_facts import ManipulationFacts
from models.owners import Owners
from models.pets import Pets
from models.species import Species

from sqlalchemy import create_engine

try:
    engine = create_engine(DB_URL.get('postgresql'), echo=True)
    Base.metadata.create_all(engine)
except Exception as e:
    print('Error!', e)




