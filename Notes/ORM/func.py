# 1. .all()  - получить все результаты запроса в виде списка.

# Особенности:
# Всегда возвращает список (даже если 0 или 1 результат)
# Выполняет запрос к базе данных
# owners = session.query(Owners).all()
# # Возвращает: [<Owners 1>, <Owners 2>, ...] или []
# Эквивалент SQL:  SELECT * FROM owners;

# 2. .first() - получить первую запись из результата.

# Особенности:
# Возвращает None, если нет результатов
# Добавляет LIMIT 1 к SQL-запросу
# Не вызывает исключений при отсутствии результатов
# owners = session.query(Owners).filter(Owners.id == 1).first()
# # Возвращает: <Owners 1> или None
# Эквивалент SQL:  SELECT * FROM owners WHERE id = 1 LIMIT 1;
#
# 3. .one() - получить ровно одну запись.

# Особенности:
# Вызывает sqlalchemy.orm.exc.NoResultFound, если нет результатов
# Вызывает sqlalchemy.orm.exc.MultipleResultsFound, если результатов несколько
# Гарантирует, что результат единственный
# Полезен для запросов по уникальным ключам
# owners = session.query(Owners).filter(Owners.email == 'unique@example.com').one()
# except NoResultFound:
#     print("Владелец не найден")
# except MultipleResultsFound:
#     print("Найдено несколько владельцев")
# Эквивалент SQL:   SELECT * FROM owners WHERE email = 'unique@example.com';

# 4. .scalar() - получить первый элемент первого результата.

# Особенности:
# Возвращает одно значение (не объект модели)
# Полезен для агрегатных функций и запросов одного столбца
# Возвращает None, если нет результатов
# Эквивалентен вызову .one()[0], но безопаснее
# count = session.query(func.count(Owners.id)).scalar()
# # Возвращает: 42 (число) или None

# email = session.query(Owners.email).filter(Owners.id == 1).scalar()
# # Возвращает: 'user@example.com' или None
# Эквивалент SQL:   SELECT count(id) FROM owners;
# и
# SELECT email FROM owners WHERE id = 1;


# SQLAlchemy также предоставляет комбинированные методы:

# .one_or_none() - как .one(), но возвращает None вместо исключения при отсутствии результатов
# .scalar_one() - комбинация .one() и .scalar()
# .scalar_one_or_none() - комбинация .one_or_none() и .scalar()