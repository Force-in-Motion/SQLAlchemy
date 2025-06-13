# Импортируем этот модуль:

from sqlalchemy import delete
from sqlalchemy.orm import session

from src.models import Pets

# Удаление одной записи:
stmt = delete(Pets).where(Pets.id == 5)

res = session.execute(stmt)

print('res:', res.rowcount)

session.commit() # res: 1


# Удаление нескольких записей мало чем отличается:
stmt = delete(Pets).where(Pets.name.like('М%'))

res = session.execute(stmt)

print('res:', res.rowcount)

session.commit() # res: 2