from sqlalchemy import create_engine
from sqlalchemy.orm import Session

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


try:
        engine = create_engine(DB_URL.get('postgresql'), echo=True)
        session = Session(engine)

        owner1 = Owners(
            owner_name='Иванов Иван Иванович',
            owner_email='ivanov@mail.ru',
            owner_phone='+71231231212'
            )

        owner2 = Owners(
            owner_name='Петров Пётр Петрович',
            owner_email='petrov@mail.ru',
            owner_phone='+71231231223'
            )

        owner3 = Owners(
            owner_name='Сидоров Сидор Сидорович',
            owner_email='sidorov@mail.ru',
            owner_phone='+71231231233'
            )

        session.add(owner1)
        session.add(owner2)
        session.add(owner3)

        session.commit()


except Exception as e:
    print('Error!', e)




