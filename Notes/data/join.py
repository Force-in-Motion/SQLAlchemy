# В таблице питомцев вид и владелец питомца заданы через числовые идентификаторы. Мы можем выполнить объединение этих таблиц с использованием функции join.

# join(left, right[, onclause, isouter, ...])


# Параметры:

# left – левая таблица для соединения
# right – правая таблица для соединения
# onclause – выражение, указывающее, по каким полям производить связывание. Если оставить None, FromClause.join() попытается объединить две таблицы на основе связи внешнего ключа.
# isouter – если True, отобразит LEFT OUTER JOIN вместо JOIN.
# full – если True, отобразит FULL OUTER JOIN вместо JOIN.


# Выведем вид животного вместо его id:
from sqlalchemy import select, join
from sqlalchemy.orm import session

from src.models import Pets, Species, Owners

stmt = select(Pets.name, Species.species_name, Pets.sex).select_from(join(Pets, Species, Pets.species==Species.species_id))

for row in session.execute(stmt):
    print(row)

('Мурзик', 'Кошка', 'M')
('Снежок', 'Собака', 'M')
('Мила', 'Кошка', 'F')
('Фиалка', 'Собака', 'F')
('Джек', 'Собака', 'M')
('Фиалка', 'Кошка', 'F')
('Белка', 'Кошка', 'F')
('Том', 'Кошка', 'M')

# Теперь выведем список владельцев и их животных:
stmt = select(Owners.owner_id, Owners.owner_name, Pets.name).select_from(join(Owners, Pets, Pets.owner_id==Owners.owner_id))

(1, 'Иванов Иван Иванович', 'Мурзик')
(1, 'Иванов Иван Иванович', 'Снежок')
(2, 'Петров Пётр Петрович', 'Мила')
(2, 'Петров Пётр Петрович', 'Фиалка')
(2, 'Петров Пётр Петрович', 'Джек')
(3, 'Сидоров Сидор Сидорович', 'Фиалка')
(3, 'Сидоров Сидор Сидорович', 'Белка')
# Из вывода видно, что был выполнен INNER JOIN (отсутствует владелец с owner_id=4)


# Для получения OUTER JOIN существует отдельная функция outerjoin():
from sqlalchemy import select, outerjoin

stmt = select(Owners.owner_id, Owners.owner_name, Pets.name).select_from(outerjoin(Owners, Pets, Pets.owner_id==Owners.owner_id))

(1, 'Иванов Иван Иванович', 'Мурзик')
(1, 'Иванов Иван Иванович', 'Снежок')
(2, 'Петров Пётр Петрович', 'Мила')
(2, 'Петров Пётр Петрович', 'Фиалка')
(2, 'Петров Пётр Петрович', 'Джек')
(3, 'Сидоров Сидор Сидорович', 'Фиалка')
(3, 'Сидоров Сидор Сидорович', 'Белка')
(4, 'Смирнов Павел Федорович', None)
# Нашелся владелец без питомца.

# А есть ли питомцы без владельцев?

# Можно поменять порядок следования соединяемых таблиц:
stmt = select(Owners.owner_id, Owners.owner_name, Pets.id, Pets.name).select_from(outerjoin(Pets, Owners, Pets.owner_id==Owners.owner_id))
# Или использовать join() с параметром isouter:

stmt = select(Owners.owner_id, Owners.owner_name, Pets.id, Pets.name).select_from(join(Pets, Owners, Pets.owner_id==Owners.owner_id, isouter=True))
# Результат:

(1, 'Иванов Иван Иванович', 1, 'Мурзик')
(1, 'Иванов Иван Иванович', 2, 'Снежок')
(2, 'Петров Пётр Петрович', 3, 'Мила')
(2, 'Петров Пётр Петрович', 4, 'Фиалка')
(2, 'Петров Пётр Петрович', 6, 'Джек')
(3, 'Сидоров Сидор Сидорович', 7, 'Фиалка')
(3, 'Сидоров Сидор Сидорович', 8, 'Белка')
(None, None, 5, 'Том')
# А вот и бесхозный питомец. Точнее, с неверно указанным id владельца.


# FULL JOIN мы получаем с использованием join() с параметром full:
stmt = select(Owners.owner_id, Owners.owner_name, Pets.id, Pets.name).select_from(join(Pets, Owners, Pets.owner_id==Owners.owner_id, full=True))

(1, 'Иванов Иван Иванович', 1, 'Мурзик')
(1, 'Иванов Иван Иванович', 2, 'Снежок')
(2, 'Петров Пётр Петрович', 3, 'Мила')
(2, 'Петров Пётр Петрович', 4, 'Фиалка')
(2, 'Петров Пётр Петрович', 6, 'Джек')
(3, 'Сидоров Сидор Сидорович', 7, 'Фиалка')
(3, 'Сидоров Сидор Сидорович', 8, 'Белка')
(None, None, 5, 'Том')
(4, 'Смирнов Павел Федорович', None, None)
# Обратите внимание, что для полного внешнего соединения (FULL OUTER JOIN) вам может понадобиться использовать комбинацию `LEFT JOIN` и `RIGHT JOIN` с `UNION`, так как не все базы данных поддерживают этот тип соединения напрямую.