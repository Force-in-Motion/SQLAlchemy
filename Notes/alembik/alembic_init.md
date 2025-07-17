### Назначение

* **Что это?**: Конфигурационный файл Alembic, содержащий настройки для управления миграциями.
* **Зачем нужен?**: Определяет параметры подключения к базе данных, путь к миграциям и другие глобальные настройки. Это первый файл, который читает Alembic при выполнении команд (например, `alembic revision` или `alembic upgrade`).
* **Где находится?**: В корне проекта, рядом с папкой `alembic/`.

### Структура и разбор строк

Пример `alembic.ini`, адаптированный для твоего проекта:

```ini
[alembic]
# Путь к папке с миграциями
script_location = alembic

# Шаблон имени файлов миграций
file_template = %%(rev)s_%%(slug)s

# URL базы данных
sqlalchemy.url = postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL

# Логирование
[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```

#### Разбор строк

1. **[alembic]**:
   * Секция с основными настройками Alembic.
2. `script_location = alembic`:
   * Указывает путь к папке с миграциями (обычно `alembic/`). Здесь хранятся файлы миграций (например, `<revision_id>_create_product_table.py`) и `env.py`.
   * Если папка называется иначе, укажи путь, например, `migrations/`.
3. `file_template = %%(rev)s_%%(slug)s`:
   * Шаблон имени файлов миграций.
   * `%s(rev)s`: Идентификатор ревизии (например, `f0ac56cb8e72`).
   * `%s(slug)s`: Короткое описание миграции, основанное на `-m` (например, `create_product_table`).
   * Пример: Для команды `alembic revision -m "create Product table"` создастся файл `f0ac56cb8e72_create_product_table.py`.
4. `sqlalchemy.url = postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL`:
   * URL подключения к базе данных.
   * Формат: `dialect+driver://username:password@host:port/database`.
   * В твоём проекте: `postgresql+asyncpg` (асинхронный драйвер для PostgreSQL), пользователь `gsa`, пароль `0502`, хост `db` (имя сервиса в `docker-compose.yml`), порт `5432`, база `PostgreSQL`.
   * Если запускаешь Alembic на хосте (не в Docker), замени `db:5432` на `localhost:8080` (согласно твоему `docker-compose.yml`).
5. **[loggers], [handlers], [formatters], [logger\_\*], [handler\_\*], [formatter\_\*]**:
   * Настройки логирования для Alembic и SQLAlchemy.
   * `logger_alembic.level = INFO`: Логи Alembic выводятся с уровнем `INFO` (например, SQL-запросы при `alembic upgrade --verbose`).
   * `handler_console`: Вывод логов в консоль (`sys.stderr`).
   * `formatter_generic`: Формат логов (например, `%(levelname)s [%(name)s] %(message)s`).

### Как работать?

* **Создание**: Создаётся автоматически при выполнении команды `alembic init alembic`.
* **Редактирование**:

  * Открой файл в текстовом редакторе (например, VS Code).
  * Измени `sqlalchemy.url` для соответствия базе данных:
    ```ini
    sqlalchemy.url = postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL
    ```
  * Если миграции хранятся в другой папке, обнови `script_location`:
    ```ini
    script_location = migrations
    ```
* **Проверка**:

  ```bash
  alembic current
  ```

  * Если возникает ошибка подключения, проверь `sqlalchemy.url`.

### Как настраивать?

* **Подключение к базе**:
  * Убедись, что `sqlalchemy.url` совпадает с URL в твоём `DBConnector`:
    ```python
    self.__engine = create_async_engine(url="postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL", echo=True)
    ```
* **Логирование**:
  * Для подробных логов установи `logger_alembic.level = DEBUG`.
* **Шаблон файлов**:
  * Измени формат имён миграций:

    ```ini
    file_template = %%(year)d_%%(rev)s_%%(slug)s
    ```

    * Добавляет год в имя файла (например, `2025_f0ac56cb8e72_create_product_table.py`).
* **Хранение пароля**:
  * Не храни пароль в `sqlalchemy.url` в продакшене. Используй переменные окружения:

    ```ini
    sqlalchemy.url = postgresql+asyncpg://%(DB_USER)s:%(DB_PASS)s@%(DB_HOST)s:%(DB_PORT)s/%(DB_NAME)s
    ```

    * Задай переменные в `.env` или `docker-compose.yml`:
      ```bash
      export DB_URL=postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL
      ```

### Пример для твоего проекта

```ini
[alembic]
script_location = alembic
file_template = %%(rev)s_%%(slug)s
sqlalchemy.url = postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers = console
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
```
