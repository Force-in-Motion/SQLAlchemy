# Логика использования логических операторов осталась прежней:

# .filter(Model.column == value) - WHERE условия

# .filter_by(column=value) - упрощенный фильтр

# .filter(Model.column.in_(subquery)) - IN условие

# .filter(Model.name.like('%John%')).all() - Like условие


# 1. AND (и) - несколько условий через filter() или &:

# Вариант 1 - последовательные filter():

# users = session.query(User).filter(
#     User.age >= 18,
#     User.is_active == True
# ).all()


# Вариант 2 - с использованием and_():

# from sqlalchemy import and_
# users = session.query(User).filter(
#     and_(
#         User.age >= 18,
#         User.is_active == True
#     )
# ).all()


# 2. OR (или):

# from sqlalchemy import or_
# users = session.query(User).filter(
#     or_(
#         User.role == 'admin',
#         User.role == 'moderator'
#     )
# ).all()


# Или с использованием символа | (пайп):

# users = session.query(User).filter(
#     (User.role == 'admin') | (User.role == 'moderator')
# ).all()

# 3. NOT (отрицание):

# from sqlalchemy import not_
# inactive_users = session.query(User).filter(
#     not_(User.is_active)
# ).all()

# Также можно использовать оператор Python != :

# inactive_users = session.query(User).filter(
#     User.is_active != True
# ).all()



# Комбинировать условия:

# users = session.query(User).filter(
#     or_(
#         and_(User.age >= 18, User.age <= 30),
#         and_(User.is_vip == True, User.age > 30)
#     )
# ).all()