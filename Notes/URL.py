# Типичный формат записи URL:

# dialect+driver://username:password@host:port/database




# SQLite

# Помним, что БД в SQLite - это просто обычный файл. Значит мы должны передавать в функцию  create_engine путь к этому файлу. Тут мы сталкиваемся с особенностями указания пути в различных ОС.

# При использовании относительных путей надо передавать 3 слэша: sqlite:///demo.db

# При использовании абсолютных путей надо передавать 4 слэша: sqlite:////src/databases/demo.db


# SQLAlchemy любезно предоставляет нам использовать собственный класс URL:

from sqlalchemy import URL, create_engine

url_object = URL.create(
    "mssql+pymssql",
    username="sa",
    password="YourStrong!Passw0rd",  # пароль текстом "как есть" - без экранирования
    host="localhost",
    database="master",
)

engine = create_engine(url_object)