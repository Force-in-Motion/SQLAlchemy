# Другой вариант создания записей в таблице - это использование конструктора SQL-выражений.

# Для начала нам надо импортировать соответствующий объект:

from sqlalchemy import insert, create_engine
from sqlalchemy.orm import  Session

from src.config.url import DB_URL
from src.models import Owners, Species, Pets, Base

engine = create_engine(DB_URL.get('postgresql'), echo=True)
Base.metadata.create_all(engine)
session = Session(engine)

# Далее, формируем выражение:

stmt = insert(Owners).values(
                owner_name='Смирнов Павел Федорович',
                email='smirnov@mail.ru',
                phone='+71231234233'
                )

print('stmt:', stmt)

# вывод: stmt: INSERT INTO owners (owner_name, phone, email) VALUES (:owner_name, :phone, :email)



# Мы можем посмотреть как будут выглядеть отдельно скомпилированное выражение и передаваемые параметры:

compiled = stmt.compile()
print('compiled:', compiled)
print('compiled.params:', compiled.params)


# Выполняем выражение и коммитим:

session.execute(stmt)

session.commit()

# =========================================================================================


# Было бы странно, если бы в SQLAlchemy отсутствовала возможность массового добавления информации (Bulk insert).

# Основа запроса - знакомый нам Insert, только в качестве аргумента он принимает массив словарей:

stmt = insert(Owners).values(
        [
            {'owner_name': 'Иванов Иван Иванович', 'email': 'ivanov@mail.ru', 'phone': '+71231231212'},
            {'owner_name': 'Петров Пётр Петрович', 'email': 'petrov@mail.ru', 'phone': '+71231231223'},
            {'owner_name': 'Сидоров Сидор Сидорович', 'email': 'sidorov@mail.ru', 'phone': '+71231234233'},
            {'owner_name': 'Смирнов Павел Федорович', 'email': 'smirnov@mail.ru', 'phone': '+71231231233'},
        ]
    )

session.execute(stmt)

session.commit()


# Для того, чтобы передать NULL-значение в таблицу БД, необходимо передавать None в качестве значения поля:

# {'owner_name': 'Петров Пётр Петрович', 'email': None, 'phone': '+71231231223'},



# Воспользуемся этим способом и зададим начальные значения для таблиц: species и pets:

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