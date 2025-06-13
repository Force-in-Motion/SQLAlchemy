# Для сортировки выдачи в SQLAlchemy используется метод order_by:
from src.models import Pets
from sqlalchemy import select
# по возрастанию:
stmt = select(Pets).order_by(Pets.birthdate)


#по убыванию:
from sqlalchemy import desc, select

stmt = select(Pets).order_by(desc(Pets.birthdate))


# Как видите, для сортировки по убыванию мы используем дополнительную функцию desc.

# В качестве параметра метода order_by передавать последовательно несколько полей.

# Это пример сортировки по двум полям sex и birthday:

stmt = select(Pets).order_by(Pets.sex, Pets.birthdate)


# Для ограничения вывода [TOP() в MS SQL, LIMIT - в некоторых других СУБД] используется метод limit:

stmt = select(Pets).order_by(Pets.sex, Pets.birthdate).limit(2)
# Аргумент метода задает сколько записей максимально будет содержаться в выводе.

