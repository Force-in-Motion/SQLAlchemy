**alembic upgrade head**

Эта команда применяет все не примененные миграции к БД, доводя её до актуального состояния (до последней версии, обозначенной как **head**).

Что при этом происходит:

**1. Проверка истории:**

Alembic смотрит в таблицу **alembic\_version** в БД (если её нет — создает) и узнаёт последнюю применённую версию (например, 1234abcd).

**2. Поиск новых миграций:**

Сканирует папку `versions/` и находит все файлы миграций, которые ещё не были применены (их ревизии не записаны в таблицу alembic\_version)

**3. Применение миграций:**

Выполняет код из функций upgrade() **в каждом файле миграции по порядку**.

После каждой миграции обновляет таблицу alembic\_version, записывая новую ревизию.

```1c
           БД: пустая                     БД: есть таблица 'owners'
               |                                   |
alembic revision --autogenerate                    |
               |                                   |
               v                                   v
       создаётся миграция                  миграция обнаруживает,
      (create_table owners)                что таблица уже существует
               |                                   |
       alembic upgrade head                        |
               |                                   |
               v                                   v
       БД: таблица 'owners'              БД: остается без изменений
```

**4. Результат:**

Структура БД теперь соответствует моделям SQLAlchemy.

Лог выполнения команды alembic upgrade head для PostgreSQL:

```less
current_dir C:\SQLAlchemy_course
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 5ccc47b906cf, initial migration
```

***\* Псевдоним head в команде -  это указатель на последнюю миграцию в цепочке. Можно также указывать конкретную ревизию: alembic upgrade 1234abcd.***
