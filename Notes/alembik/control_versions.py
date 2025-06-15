# 1. Каждая миграция в Alembic называется ревизией и хранится в отдельном Python-файле в папке versions/.
# Файл содержит:

# upgrade() — применяет изменения.
# downgrade() — откатывает изменения.
# Пример:

# def upgrade():
#     op.create_table("users", Column("id", Integer, primary_key=True))

# def downgrade():
#     op.drop_table("users")
# 2. Alembic создаёт в БД специальную таблицу alembic_version, где хранит хеш последней примененной ревизии:

# SELECT * FROM alembic_version;
# -- version_num
# -- '1234abc'
# 3. В Alembic используются указатели:

# head — последняя применённая ревизия в цепочке.
# base — начальное состояние (пустая БД).
# branches — его мы ещё не рассматривали (редкий случай) - если миграции ветвятся.
# Если несколько разработчиков создают миграции параллельно, Alembic может обнаружить ветвление (branching):

#            rev1 -> rev2
#           /
# rev_base
#           \
#            revA -> revB

# Как это исправить? - Создать слияние (merge):

# Для этого используется команда:

# alembic merge -m "Merge rev2 and revB" rev2 revB
# Далее необходимо вручную разрешить конфликты в новом файле миграции.

# Откат миграции

# Выполняется с помощью:

# alembic downgrade -1  # Откатывает одну миграцию
# alembic downgrade base  # Откатывает ВСЁ до пустой БД
# Просмотр истории миграций

# Используем команду:

# alembic history --verbose
# Пример лога:

# PS C:\SQLAlchemy_course\alembic\postgresql> alembic history --verbose
# Rev: 5ccc47b906cf (head)
# Parent: <base>
# Path: C:\SQLAlchemy_course\alembic\postgresql\versions\5ccc47b906cf_initial_migration.py
#     initial migration

#     Revision ID: 5ccc47b906cf
#     Revises:
#     Create Date: 2025-04-25 17:15:59.382395


# Управление зависимостями между миграциями
# В примере выше указана ревизия миграции и её предок:

# Rev: 5ccc47b906cf (head)
# Parent: <base>

# Каждая миграция может зависеть от других. Это указывается в параметре down_revision:

# revision = "5678def"
# down_revision = "1234abc" # Зависит от "1234abc"
# Теперь рассмотрим возможности, которые могут пригодиться в нашем проекте.

# Если Alembic создает функции upgrade() и downgrade() с кодом на Python, то мы можем использовать их для исполнения дополнительного кода:

# Запуск SQL-скриптов в миграциях

# def upgrade():
#     op.execute("CREATE INDEX idx_user_name ON users (name)")
# Таким образом мы можем прописать начальные значения в БД (например, конфигурационные параметры)


# Условные миграции (для разных СУБД)

# Добавив логическое выражение, можем выполнять специальные функции для каждой из СУБД(диалекта SQL):

# def upgrade():
#     if op.get_context().dialect.name == "postgresql":
#         op.create_index("idx_email", "users", ["email"])

# Откат с данными

# В этом случае дополняем функцию downgrade():

# def downgrade():
#     op.execute("DELETE FROM users WHERE email IS NULL")
#     op.drop_column("users", "email")


# Best Practices

# Всегда проверяйте сгенерированные миграции перед применением.
# Не редактируйте примененные миграции — это может сломать историю.
# Используйте --autogenerate с осторожностью — Alembic не всегда понимает сложные изменения.
# Храните миграции в системе контроля версий (Git).
# Тестируйте миграции на тестовой БД (перед продакшеном).


# Полезные команды

# alembic current - Текущая версия БД
# alembic heads - Все активные головные ревизии
# alembic upgrade --sql - Показать SQL без выполнения (к п.1. Best Practices)
# alembic stamp head - Проставить текущую версию без применения
# alembic history - История миграций


# ВАЖНО - нельзя удалять файлы миграций если они уже применены к базе данных командой alembic upgrade head,
# чтобы можно было удалить файл миграции нужно для начала откатить примененные к базе изменения командой alembic downgrade -1
# эта команда откатит применение последней миграции и тогда файл миграции можно удалять