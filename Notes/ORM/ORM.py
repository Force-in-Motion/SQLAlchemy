from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Определяем базовый класс для моделей
Base = declarative_base()


# Определяем модель Owners
class Owner(Base):
    __tablename__ = 'owners'

    id = Column(Integer, primary_key=True)
    name = Column(String)


# Создаем соединение с базой данных
engine = create_engine('sqlite:///example.db')  # Замените на вашу БД
Session = sessionmaker(bind=engine)
session = Session()

# 1. Запрос: select * from owners
owners = session.query(Owner).all()
for owner in owners:
    print(owner.id, owner.name)

# 2. Запрос: select count(*) from owners
count = session.query(Owner).count()
print("Total owners:", count)

# Закрываем сессию
session.close()


# Лучшая практика:

# Использовать ORM для бизнес-логики.
# Использовать Core для аналитики и оптимизации.
# ✅ Выбирайте Core, если:

# Нужен полный контроль над SQL.
# Работаете с сложными запросами (оконные функции, CTE).
# Производительность критична (ETL, аналитика).
# ✅ Выбирайте ORM, если:

# Разрабатываете веб-приложение (Django-like).
# Хотите меньше кода для операций CRUD.
# Нужны автоматические связи (например, owner.pets).