# Сортировка

# 1. Прямой порядок (ASC)

# По одному полю:
# users = session.query(User).order_by(User.name).all()
# Явное указание ASC:

# from sqlalchemy import asc
# users = session.query(User).order_by(asc(User.created_at)).all()



# 2. Обратный порядок (DESC)
# Используя функцию desc():

# from sqlalchemy import desc
# users = session.query(User).order_by(desc(User.created_at)).all()
# Используя метод .desc():

# users = session.query(User).order_by(User.created_at.desc()).all()



# 3. Сортировка по нескольким полям:
# users = session.query(User).order_by(
#     User.department,
#     User.salary.desc()
# ).all()
# Будет выполнена сортировка сначала по department (ASC), затем по salary (DESC)



# 4. Сортировка с условиями:
# from sqlalchemy import case
# priority_order = case(
#     [
#         (User.role == 'admin', 1),
#         (User.role == 'moderator', 2),
#         (User.role == 'user', 3)
#     ],
#     else_=4
# )

# users = session.query(User).order_by(priority_order, User.name).all()