# В SQLAlchemy мы должны вызвать метод where к исходной таблице:
from sqlalchemy.orm import session
from sqlalchemy import select
from src.models import Owners, Pets

stmt = select(Owners).where(Owners.owner_id == 1)
print(list(session.execute(stmt)))

# Результат: [(Owners(owner_id=1, owner_name='Иванов Иван Иванович', phone='+71231231212', email='ivanov@mail.ru'),)]
# Операнды в where используются питоновские:

# == - Равно
# != - Не равно
# < - Меньше
# <= - Меньше или равно
# > - Больше
# >= - Больше или равно
# Способов использования логических операндов в where несколько.

# Например для AND:

# 1. Последовательное применение
stmt = select(Pets).where(Pets.owner_id == 2).where(Pets.sex == 'F')
for row in session.execute(stmt):
    print(row)


# 2. Использование операнда '&':
stmt = select(Pets).where((Pets.owner_id == 2) & (Pets.sex == 'F'))


# 3. Использование функции and_:
from sqlalchemy import and_, select

stmt = select(Pets).where(and_(Pets.owner_id == 2, Pets.sex == 'F'))


# Результат во всех трех вариантах идентичен:
(Pets(id=3, species=2, owner_id=2, name='Мила', sex='F', weight=2.37, birthdate='2022-12-04 19:09:13.964935'),)
(Pets(id=4, species=1, owner_id=2, name='Фиалка', sex='F', weight=7.84, birthdate='2023-07-22 19:09:13.972309'),)

# * в модель Pets добавлена функция __repr__, аналогичная __repr__ в модели Owners.

# Список функций логических операторов:

# and_ - Логическое И
# or_ - Логическое ИЛИ
# not_ - Логическое НЕ


# Если мы хотим использовать фильтрацию аналогичную SQL "LIKE", то мы тоже вызываем like, но это будет метод, применяемый к значению поля:

# В этом примере мы выбираем всех питомцев с именем, начинающимся на "М".
stmt = select(Pets).where(Pets.name.like('М%'))

(Pets(id=1, species=2, owner_id=1, name='Мурзик', sex='M', weight=6.93, birthdate='2016-12-02 19:09:13.585252'),)
(Pets(id=3, species=2, owner_id=2, name='Мила', sex='F', weight=2.37, birthdate='2022-12-04 19:09:13.964935'),)


# По этому же принципу работает и BETWEEN:
stmt = select(Pets).where(Pets.birthdate.between('2020-04-04', '2020-12-31'))

(Pets(id=6, species=1, owner_id=2, name='Джек', sex='M', weight=2.68, birthdate='2020-06-27 19:09:13.974897'),)
(Pets(id=8, species=2, owner_id=3, name='Белка', sex='F', weight=8.43, birthdate='2020-04-13 19:09:13.976747'),)