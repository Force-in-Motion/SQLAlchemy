# Важно:

# Порядок вызова методов важен: limit() и offset() должны идти после order_by()
# Для больших offset используйте ключевой набор (keyset pagination) вместо offset (об этом на следующем шаге)
# В сочетании с offset() всегда используйте order_by() для стабильных результатов
# limit(0) вернет пустой результат (полезно для тестирования)


# Теперь к примерам использования.

# 1. Получить первые 5 пользователей
# users = session.query(User).limit(5).all()


#  2. Последние 3 зарегистрировавшихся пользователя:
# new_users = session.query(User).order_by(
#     User.created_at.desc()
# ).limit(3).all()


# 3. Топ-5 самых активных пользователей:
# top_active = session.query(User).join(Post).group_by(
#     User.id
# ).order_by(
#     func.count(Post.id).desc()
# ).limit(5).all()


# 4. Пропуск первых 10 записей:
# users = session.query(User).offset(10).all()


# 5. Пагинация (limit + offset) - используется в web:
# Выводим список пользователей постранично, разбив по 10 пользователей.
# Первая страница (элементы 1-10):

# page1 = session.query(User).order_by(
#     User.id
# ).limit(10).offset(0).all()
# Вторая страница (элементы 11-20):

# page2 = session.query(User).order_by(
#     User.id
# ).limit(10).offset(10).all()
# Можно сделать параметрически:

# def get_page(page_num, page_size=10):
#     return session.query(User).order_by(
#         User.id
#     ).limit(page_size).offset((page_num - 1) * page_size).all()page3 = get_page(3)  # Элементы 21-30


# 6. Limit с подзапросом:
# # Сначала выбираем ID, затем полные объекты
# user_ids = session.query(User.id).order_by(
#     User.registration_date
# ).limit(100).all()

# users = session.query(User).filter(
#     User.id.in_([u.id for u in user_ids])
# ).all()


# 7. Проверка наличия данных (без загрузки всех данных):
# # Проверить, есть ли хотя бы один активный пользователь
# has_active = session.query(User).filter(
#     User.is_active == True
# ).limit(1).first() is not None


# 8. Получение только количества для пагинации:
# total_users = session.query(func.count(User.id)).scalar()
# pages = (total_users + page_size - 1) // page_size