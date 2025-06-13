# В SQLAlchemy используется два подхода работы с базами данных: Core и ORM.

# Сейчас мы будем использовать Core-подход. Про ORM-подход мы будем говорить в 6-м модуле.

# Для использования функций SQL в запросах (при Core-подходе), мы должны импортировать модуль func:

from sqlalchemy import func, select, create_engine
from sqlalchemy.orm import Session

from src.config.url import DB_URL
from src.models import Owners

# Наиболее часто используемые функции из func:

func.count()        # Подсчет количества строк.
func.sum()          # Сумма значений.
func.avg()          # Среднее значение.
func.min()          # Минимальное значение.
func.max()          # Максимальное значение.
func.concat()       # Конкатенация строк.
func.lower()        # Приведение строки к нижнему регистру.
func.upper()        # Приведение строки к верхнему регистру.
func.now()          # Текущая дата и время.
func.date()         # Извлечение даты.
func.substring()    # Извлечение подстроки.

# Как видите: название функций совпадает с названием их SQL аналога.

# Рекомендую использовать вызов функций, так как указано в примере выше - с использованием имени библиотеки. Иначе высока вероятность переопределения функции из одного модуля функцией с аналогичным именем из другого модуля.

# Пример запроса:
engine = create_engine(DB_URL.get('postgresql'), echo=True)
session = Session(engine)

stmt = select(
            func.count(),                       # количество записей в таблице
            func.sum(Owners.owner_id),          # сумма значений в поле owner_id
            func.max(Owners.owner_phone)        # максимальное значение в поле phone
            ).select_from(Owners)               # явное указание основной таблицы в запросе

print('stmt:', stmt)

for row in session.execute(stmt):
    print(row)

# Вывод:

# SELECT count(*) AS count_1, sum(owners.owner_id) AS sum_1, max(owners.phone) AS max_1
# FROM owners

# (4, 10, '+71231234233')


# Можно не указывать select_from, если для всех функций явно прописан источник:

stmt = select(
            func.count(Owners.owner_id),        # количество записей в таблице по owner_id
            func.sum(Owners.owner_id),          # сумма значений в поле owner_id
            func.max(Owners.owner_phone)        # максимальное значение в поле phone
            )


# Для присвоения алиасов используется метод label:

stmt = select(
            func.count(Owners.owner_id).label('total_count'),   # количество записей в таблице
            func.sum(Owners.owner_id).label('total_id'),        # сумма значений в поле owner_id
            func.max(Owners.owner_phone).label('max_phone')     # максимальное значение в поле phone
            )

# Теперь к элементам результата можно обращаться по имени алиаса:

for row in session.execute(stmt):
    print(row.total_count, row.total_id, row.max_phone)

# # Печатает: 4 10 +71231234233