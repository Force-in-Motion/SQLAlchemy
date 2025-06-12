from sqlalchemy import create_engine, insert
from sqlalchemy.orm import Session

from src.config.url import DB_URL

from src.models.base import Base
from src.models.manipulations import Manipulations
from src.models.manipulation_facts import ManipulationFacts
from src.models.owners import Owners
from src.models.pets import Pets
from src.models.species import Species



# Добавление данных через ORM
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




# Другой вариант создания записей в таблице - это использование конструктора SQL-выражений.
try:
    engine = create_engine(DB_URL.get('postgresql'), echo=True)
    session = Session(engine)
    stmt_species= insert(Species).values(
        [
            {'species_id': 1, 'species_name': 'Собака'},
            {'species_id': 2, 'species_name': 'Кошка'},
        ]
    )



    session.execute(stmt_species)

    stmt_pets = insert(Pets).values(
        [
            {'id': 1,  'species': 2,  'owner_id': 1,  'name': 'Мурзик',  'sex': 'M',  'weight': 6.93,  'birthdate': '2016-12-02 19:09:13.585252'},
            {'id': 2,  'species': 1,  'owner_id': 1,  'name': 'Снежок',  'sex': 'M',  'weight': 7.32,  'birthdate': '2019-05-07 19:09:13.587283'},
            {'id': 3,  'species': 2,  'owner_id': 2,  'name': 'Мила',  'sex': 'F',  'weight': 2.37,  'birthdate': '2022-12-04 19:09:13.964935'},
            {'id': 4,  'species': 1,  'owner_id': 2,  'name': 'Фиалка',  'sex': 'F',  'weight': 7.84,  'birthdate': '2023-07-22 19:09:13.972309'},
            {'id': 5,  'species': 2,  'owner_id': 5,  'name': 'Том',  'sex': 'M',  'weight': 4.12,  'birthdate': '2015-05-05 19:09:13.974340'},
            {'id': 6,  'species': 1,  'owner_id': 2,  'name': 'Джек',  'sex': 'M',  'weight': 2.68,  'birthdate': '2020-06-27 19:09:13.974897'},
            {'id': 7,  'species': 2,  'owner_id': 3,  'name': 'Фиалка',  'sex': 'F',  'weight': 5.53,  'birthdate': '2021-02-18 19:09:13.976747'},
            {'id': 8,  'species': 2,  'owner_id': 3,  'name': 'Белка',  'sex': 'F',  'weight': 8.43,  'birthdate': '2020-04-13 19:09:13.976747'}
        ]
    )

    session.execute(stmt_pets)

    session.commit()

except Exception as e:
    print('Error!', e)




