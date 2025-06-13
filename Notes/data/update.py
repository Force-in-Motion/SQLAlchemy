# Импортируем этот модуль и можем приступать к правкам:

from sqlalchemy import update
from sqlalchemy.orm import session

from src.models import Pets

# Для питомца с id=5 неверно установлено значение owner_id. Его надо заменить на 4:

stmt = update(Pets).where(Pets.id == 5).values(owner_id=4)
res = session.execute(stmt)
print('res:', res, res.rowcount)
session.commit()

# Тут всё просто:

# что сделать? - изменить таблицу Pets,
# где? - фильтр по условию в where
# какие изменения? - установить значение поля owner_id

# Дополнительно мы получили и напечатали результат выполнения команды (res) и количество затронутых командой строк (res.rowcount):
#
# res: <sqlalchemy.engine.cursor.CursorResult object at 0x000001B5E439D0C0> 1