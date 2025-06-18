**Alembic** — это инструмент для управления миграциями базы данных, разработанный автором SQLAlchemy Майклом Байером. Он используется для синхронизации структуры базы данных (схемы) с изменениями в моделях SQLAlchemy, таких как добавление таблиц, столбцов, индексов или ограничений. В контексте твоего проекта `Ecomerce` (FastAPI, SQLAlchemy, PostgreSQL в Docker, модели `Owners`, `Pets`, `Species`, `ManipulationFacts`), Alembic идеально подходит для управления изменениями схемы, особенно с учётом твоих вопросов о транзакциях, индексах, кэше, JOIN-ах и `relationship`. Я подробно объясню, что такое Alembic, как его установить, настроить, использовать, какие команды доступны, как работает контроль версий, и всё остальное, связанное с его применением в твоём проекте.

### Что такое Alembic?

- **Определение**: Alembic — это библиотека для Python, которая управляет миграциями базы данных, позволяя применять изменения схемы (например, создание таблиц, добавление столбцов) и откатывать их при необходимости.
- **Зачем нужен**:
  - **Синхронизация моделей и базы**: Когда ты добавляешь новый столбец в модель `Pet` (например, `age`), Alembic создаёт миграцию для добавления этого столбца в таблицу `pets` в PostgreSQL.
  - **Контроль версий**: Хранит историю изменений схемы, позволяя откатить базу к предыдущему состоянию.
  - **Командная разработка**: Упрощает работу нескольких разработчиков, синхронизируя изменения базы.
  - **Поддержка транзакций**: Миграции выполняются в транзакциях, что обеспечивает целостность данных.
- **Особенности**:
  - Интеграция с SQLAlchemy: Использует `Base.metadata` для сравнения моделей с текущей схемой базы.
  - Поддержка большинства СУБД: PostgreSQL, MySQL, SQLite, Oracle.
  - Гибкость: Позволяет писать миграции вручную или генерировать автоматически.
  - Контроль версий: Использует систему, похожую на Git, с уникальными идентификаторами миграций.

### Установка Alembic

1. **Установка через pip**:
   Убедись, что ты активировал виртуальное окружение твоего проекта `Ecomerce`:

   ```bash
   source /home/gsa/Code/Python/Practice/SQLALchemy/.venv/bin/activate
   pip install alembic
   ```

   Проверь установку:

   ```bash
   alembic --version
   ```
2. **Зависимости**:

   - SQLAlchemy (уже установлен в твоём проекте).
   - Драйвер базы данных (`psycopg2-binary` для PostgreSQL):
     ```bash
     pip install psycopg2-binary
     ```
3. **Инициализация Alembic в проекте**:
   Перейди в корень проекта:

   ```bash
   cd /home/gsa/Code/Python/Practice/SQLALchemy
   ```

   Инициализируй Alembic:

   ```bash
   alembic init alembic
   ```

   Это создаёт:

   - Папку `alembic/` с файлами миграций.
   - Файл `alembic.ini` для конфигурации.

### Структура Alembic

После инициализации структура выглядит так:

```
/home/gsa/Code/Python/Practice/SQLALchemy/
├── alembic/
│   ├── env.py          # Скрипт для выполнения миграций
│   ├── script.py.mako  # Шаблон для новых миграций
│   ├── versions/       # Папка с файлами миграций
└── alembic.ini         # Конфигурационный файл
```

- **`alembic.ini`**: Содержит настройки, такие как строка подключения к базе.
- **`env.py`**: Определяет, как Alembic взаимодействует с твоими моделями SQLAlchemy и базой.
- **`versions/`**: Хранит Python-файлы миграций (например, `abc123_add_column.py`).
- **`script.py.mako`**: Шаблон для генерации новых миграций.

### Настройка Alembic

#### 1. Настройка `alembic.ini`

Открой `alembic.ini` и укажи строку подключения к твоей базе PostgreSQL:

```ini
[alembic]
script_location = alembic
sqlalchemy.url = postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL
```

- **`sqlalchemy.url`**: Соответствует твоему `engine` в `main.py`. Если используешь `sqlalchemy_course`, укажи:
  ```ini
  sqlalchemy.url = postgresql+psycopg2://gsa:0502@localhost:8080/sqlalchemy_course
  ```
- Другие параметры (опционально):
  ```ini
  file_template = %%(rev)s_%%(slug)s  # Формат имени файлов миграций
  timezone = UTC                      # Временная зона для меток времени
  ```

#### 2. Настройка `env.py`

Файл `alembic/env.py` нужно отредактировать, чтобы Alembic знал о твоих моделях (`Base` из `models.base`). Пример:

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Импортируем Base и модели
from models.base import Base
from models.owners import Owner
from models.pets import Pet
from models.species import Species
from models.manipulations import Manipulation
from models.manipulation_facts import ManipulationFact

config = context.config
fileConfig(config.config_file_name)

# Указываем metadata для автогенерации миграций
target_metadata = Base.metadata

def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

- **Изменения**:
  - Импортируй `Base` и все модели (`Owner`, `Pet`, etc.).
  - Укажи `target_metadata = Base.metadata` для связи с твоими моделями.
- **Зачем**: Это позволяет Alembic сравнивать текущую схему базы с `Base.metadata` для автогенерации миграций.

#### 3. Создание таблицы для отслеживания версий

Alembic создаёт таблицу `alembic_version` в базе для хранения текущей версии миграции. Инициализируй её:

```bash
alembic stamp head
```

Проверь в PostgreSQL:

```bash
psql -h localhost -p 8080 -U gsa -d PostgreSQL -c "SELECT * FROM alembic_version;"
```

### Основные команды Alembic

Alembic предоставляет CLI-команды для управления миграциями. Выполняй их из корня проекта:

1. **`alembic init <directory>`**:

   - Инициализирует Alembic, создаёт папку (например, `alembic`).
   - Пример: `alembic init alembic`
2. **`alembic revision -m "message"`**:

   - Создаёт новый файл миграции в `alembic/versions/` с указанным описанием.
   - Пример:
     ```bash
     alembic revision -m "add age column to pets"
     ```

     Создаёт файл, например, `abc123_add_age_column_to_pets.py`.
3. **`alembic revision --autogenerate -m "message"`**:

   - Автоматически генерирует миграцию, сравнивая `Base.metadata` с текущей схемой базы.
   - Пример:
     ```bash
     alembic revision --autogenerate -m "add age to pets"
     ```
   - **Важно**: Убедись, что все модели импортированы в `env.py`, иначе автогенерация не увидит изменения.
4. **`alembic upgrade <revision>`**:

   - Применяет миграции до указанной версии (или `head` для последней).
   - Пример:
     ```bash
     alembic upgrade head
     ```

     Применяет все миграции.
   - Или конкретная версия:
     ```bash
     alembic upgrade abc123
     ```
5. **`alembic downgrade <revision>`**:

   - Откатывает миграции до указанной версии (или `base` для начального состояния).
   - Пример:
     ```bash
     alembic downgrade -1
     ```

     Откатывает последнюю миграцию.
   - Или:
     ```bash
     alembic downgrade base
     ```

     Удаляет все миграции.
6. **`alembic current`**:

   - Показывает текущую версию миграции в базе.
   - Пример:
     ```bash
     alembic current
     ```

     Вывод: `abc123 (head)`
7. **`alembic history`**:

   - Показывает историю миграций.
   - Пример:

     ```bash
     alembic history
     ```

     Вывод:
     ```
     abc123 -> def456 (head), add index to pets
     base -> abc123, add age column to pets
     ```
8. **`alembic stamp <revision>`**:

   - Устанавливает текущую версию миграции в `alembic_version` без выполнения миграций.
   - Пример:
     ```bash
     alembic stamp head
     ```
9. **`alembic merge <revision1> <revision2>`**:

   - Объединяет две ветки миграций в одну (используется при конфликтах в команде).
   - Пример:
     ```bash
     alembic merge abc123 def456
     ```
10. **`alembic heads`**:

    - Показывает все "головы" (head) миграций, если есть несколько веток.
    - Пример:
      ```bash
      alembic heads
      ```

### Как работает контроль версий

- **Миграции как версии**: Каждая миграция — это Python-файл в `alembic/versions/` с уникальным идентификатором (например, `abc123`). Файл содержит функции:
  - `upgrade()`: Применяет изменения (например, `op.create_table`).
  - `downgrade()`: Откатывает изменения (например, `op.drop_table`).
- **Таблица `alembic_version`**: Хранит текущий идентификатор миграции (например, `abc123`), чтобы Alembic знал, какие миграции уже применены.
- **Даг миграций**: Миграции образуют направленный ациклический граф (DAG), где каждая миграция ссылается на предыдущую через атрибут `down_revision`.
- **Ветвление**: Если два разработчика создают миграции одновременно, возникают ветки. Их можно объединить с `alembic merge`.

**Пример файла миграции**:

```python
# alembic/versions/abc123_add_age_column_to_pets.py
from alembic import op
import sqlalchemy as sa

revision = 'abc123'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.add_column('pets', sa.Column('age', sa.Integer, nullable=True))

def downgrade():
    op.drop_column('pets', 'age')
```

- `revision`: Уникальный ID миграции.
- `down_revision`: ID предыдущей миграции.
- `upgrade()`: Добавляет столбец `age` в таблицу `pets`.
- `downgrade()`: Удаляет столбец `age`.

### Пример использования в `Ecomerce`

#### Шаг 1: Инициализация

```bash
cd /home/gsa/Code/Python/Practice/SQLALchemy
alembic init alembic
```

#### Шаг 2: Настройка

- В `alembic.ini`:
  ```ini
  sqlalchemy.url = postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL
  ```
- В `alembic/env.py` добавь:
  ```python
  from models.base import Base
  from models.owners import Owner
  from models.pets import Pet
  from models.species import Species
  from models.manipulations import Manipulation
  from models.manipulation_facts import ManipulationFact
  target_metadata = Base.metadata
  ```

#### Шаг 3: Создание начальной миграции

Если твои таблицы (`owners`, `pets`, etc.) уже созданы через `Base.metadata.create_all()`, синхронизируй Alembic:

```bash
alembic revision --autogenerate -m "initial schema"
```

Отредактируй сгенерированный файл (например, `alembic/versions/abc123_initial_schema.py`), если нужно. Пример:

```python
from alembic import op
import sqlalchemy as sa

revision = 'abc123'
down_revision = None

def upgrade():
    op.create_table(
        'owners',
        sa.Column('owner_id', sa.Integer, primary_key=True),
        sa.Column('owner_name', sa.String, nullable=False),
        sa.Column('owner_email', sa.String)
    )
    op.create_table(
        'pets',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('owner_id', sa.Integer, sa.ForeignKey('owners.owner_id')),
        sa.Column('name', sa.String, nullable=False)
    )
    # Другие таблицы...

def downgrade():
    op.drop_table('pets')
    op.drop_table('owners')
    # Другие таблицы...
```

Применяй миграцию:

```bash
alembic upgrade head
```

#### Шаг 4: Добавление нового столбца

Добавь столбец `age` в модель `Pet`:

```python
# models/pets.py
class Pet(Base):
    __tablename__ = 'pets'
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('owners.owner_id'))
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=True)  # Новый столбец
```

Создай миграцию:

```bash
alembic revision --autogenerate -m "add age to pets"
```

Проверь `alembic/versions/def456_add_age_to_pets.py`:

```python
def upgrade():
    op.add_column('pets', sa.Column('age', sa.Integer, nullable=True))

def downgrade():
    op.drop_column('pets', 'age')
```

Применяй:

```bash
alembic upgrade head
```

#### Шаг 5: Добавление индекса

Ты спрашивал про индексы. Создай индекс на `Pet.owner_id`:

```bash
alembic revision --autogenerate -m "add index on pet owner_id"
```

Редактируй миграцию:

```python
def upgrade():
    op.create_index('ix_pet_owner_id', 'pets', ['owner_id'], unique=False)

def downgrade():
    op.drop_index('ix_pet_owner_id', table_name='pets')
```

Применяй:

```bash
alembic upgrade head
```

### Интеграция с FastAPI

В `Ecomerce` ты используешь FastAPI. Для применения миграций при старте приложения:

```python
# src/main.py
from sqlalchemy import create_engine
from alembic.config import Config
from alembic import command

engine = create_engine('postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL')

def apply_migrations():
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")

if __name__ == "__main__":
    apply_migrations()
    # Запуск FastAPI
```

Или используй команду перед запуском:

```bash
alembic upgrade head
uvicorn src.main:app --reload
```

### Лучшие практики

1. **Автогенерация с осторожностью**:
   - Проверяй сгенерированные миграции, так как автогенерация может пропустить сложные изменения (например, переименование столбцов).
2. **Ясные описания**:
   - Используй понятные `-m "message"` (например, `"add age to pets"`).
3. **Резервные копии**:
   - Перед миграциями делай бэкап базы:
     ```bash
     pg_dump -h localhost -p 8080 -U gsa PostgreSQL > backup.sql
     ```
4. **Тестируй миграции**:
   - Создай тестовую базу в Docker:

     ```bash
     docker run -d --name test_postgres -e POSTGRES_USER=gsa -e POSTGRES_PASSWORD=0502 -e POSTGRES_DB=test_db -p 8081:5432 postgres:16.4
     ```

     Применяй миграции:
     ```bash
     alembic -x sqlalchemy.url=postgresql+psycopg2://gsa:0502@localhost:8081/test_db upgrade head
     ```
5. **Контроль версий в Git**:
   - Добавь `alembic/versions/` и `alembic.ini` в Git:
     ```bash
     git add alembic/
     git commit -m "Add Alembic migrations"
     ```
6. **Избегай ручного редактирования базы**:
   - Все изменения вносите через миграции, а не через `psql`.

### Связь с твоим контекстом

- **Проект `Ecomerce`**: Ты используешь SQLAlchemy с PostgreSQL, `sessionmaker`, JOIN-ы, `relationship`, транзакции, индексы и кэш. Alembic поможет:
  - Управлять изменениями таблиц (`Owners`, `Pets`, etc.).
  - Добавлять индексы (например, на `Pets.owner_id`).
  - Синхронизировать схему с моделями, особенно при добавлении новых столбцов или таблиц.
- **Пример**: Если ты добавишь `relationship` в `Pet` для связи с `Species`, Alembic создаст миграцию для нового `ForeignKey`.
- **Docker**: Убедись, что PostgreSQL доступен:
  ```bash
  docker ps | grep PostgreSQL
  psql -h localhost -p 8080 -U gsa -d PostgreSQL
  ```

### Распространённые проблемы и решения

1. **Ошибка "Table not found"**:
   - Убедись, что все модели импортированы в `env.py`.
   - Проверь строку подключения в `alembic.ini`.
2. **Конфликты миграций**:
   - Если два разработчика создали миграции, используй:
     ```bash
     alembic merge abc123 def456 -m "merge branches"
     ```
3. **Автогенерация не видит изменений**:
   - Проверь, что `Base.metadata` включает все модели.
   - Убедись, что база синхронизирована:
     ```bash
     alembic current
     ```
4. **Ошибки PostgreSQL**:
   - Проверь логи:
     ```bash
     docker logs PostgreSQL
     ```
   - Убедись, что пользователь `gsa` имеет права:
     ```sql
     GRANT ALL PRIVILEGES ON DATABASE PostgreSQL TO gsa;
     ```

### Дополнительные возможности

1. **Кастомные операции**:
   - Используй `op.execute()` для произвольных SQL:
     ```python
     def upgrade():
         op.execute("CREATE INDEX custom_idx ON pets USING GIN (name)")
     ```
2. **Миграции данных**:
   - Для изменения данных в таблице:
     ```python
     def upgrade():
         op.execute("UPDATE pets SET age = 0 WHERE age IS NULL")
     ```
3. **Множественные базы**:
   - Для поддержки нескольких баз используй `-x`:
     ```bash
     alembic -x sqlalchemy.url=postgresql+psycopg2://gsa:0502@localhost:8080/other_db upgrade head
     ```
4. **CI/CD интеграция**:
   - Добавь миграции в GitHub Actions:
     ```yaml
     jobs:
       migrate:
         runs-on: ubuntu-latest
         steps:
         - uses: actions/checkout@v4
         - run: pip install alembic psycopg2-binary
         - run: alembic upgrade head
           env:
             SQLALCHEMY_URL: postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL
     ```

### Если что-то не работает

- **Ошибка миграции**:
  - Покажи вывод команды (например, `alembic upgrade head`).
  - Проверь `alembic_version`:
    ```sql
    SELECT * FROM alembic_version;
    ```
- **Конфликт импортов**:
  - Убедись, что `env.py` импортирует все модели без циклических зависимостей.
- **Docker проблемы**:
  - Проверь, что контейнер работает:
    ```bash
    docker ps
    ```
  - Логи:
    ```bash
    docker logs PostgreSQL
    ```

### Быстрое решение

1. Установи и инициализируй:
   ```bash
   pip install alembic
   alembic init alembic
   ```
2. Настрой `alembic.ini`:
   ```ini
   sqlalchemy.url = postgresql+psycopg2://gsa:0502@localhost:8080/PostgreSQL
   ```
3. Настрой `env.py`:
   ```python
   from models.base import Base
   target_metadata = Base.metadata
   ```
4. Создай начальную миграцию:
   ```bash
   alembic revision --autogenerate -m "initial schema"
   alembic upgrade head
   ```
5. Проверь:
   ```bash
   psql -h localhost -p 8080 -U gsa -d PostgreSQL -c "\dt"
   ```

Удачи с Alembic в твоём проекте `Ecomerce`! 😎
