### Назначение

* **Что это?**: Шаблон Mako (`.mako` — формат шаблонов) для генерации файлов миграций (например, `<revision_id>_create_product_table.py`).
* **Зачем нужен?**: Определяет структуру и содержимое новых файлов миграций, создаваемых командами `alembic revision` или `alembic revision --autogenerate`.
* **Где находится?**: В папке `alembic/` (обычно `alembic/script.py.mako`).

### Структура и разбор строк

Стандартный шаблон `script.py.mako`:

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa
${imports if imports else ""}

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```

#### Разбор строк

1. **Комментарий с метаданными**:

   ```mako
   """${message}

   Revision ID: ${up_revision}
   Revises: ${down_revision | comma,n}
   Create Date: ${create_date}
   """
   ```

   * `${message}`: Описание миграции, заданное в `-m` (например, `create Product table`).
   * `${up_revision}`: Уникальный ID новой ревизии (например, `f0ac56cb8e72`).
   * `${down_revision | comma,n}`: ID предыдущей ревизии, от которой зависит текущая (или `None`).
   * `${create_date}`: Дата создания миграции (например, `2025-07-17 14:29:00`).
2. **Импорты**:

   ```mako
   from alembic import op
   import sqlalchemy as sa
   ${imports if imports else ""}
   ```

   * `from alembic import op`: Импортирует объект `op` для операций миграций (например, `op.create_table`).
   * `import sqlalchemy as sa`: Импортирует SQLAlchemy для определения типов колонок (например, `sa.String`).
   * `${imports if imports else ""}`: Добавляет дополнительные импорты, если они нужны (например, для специфичных типов).
3. **Идентификаторы ревизии**:

   ```mako
   revision = ${repr(up_revision)}
   down_revision = ${repr(down_revision)}
   branch_labels = ${repr(branch_labels)}
   depends_on = ${repr(depends_on)}
   ```

   * `revision`: ID текущей ревизии.
   * `down_revision`: ID предыдущей ревизии (для цепочки миграций).
   * `branch_labels`: Метки веток (используются для ветвления миграций, обычно `None`).
   * `depends_on`: Зависимости от других ревизий (для сложных миграций, обычно `None`).
4. **Функции миграции**:

   ```mako
   def upgrade() -> None:
       ${upgrades if upgrades else "pass"}

   def downgrade() -> None:
       ${downgrades if downgrades else "pass"}
   ```

   * `upgrade()`: Код для применения миграции (например, создание таблицы `Product`).
   * `downgrade()`: Код для отката миграции (например, удаление таблицы `Product`).
   * `${upgrades if upgrades else "pass"}`: Если миграция создана с `--autogenerate`, содержит команды (например, `op.create_table`), иначе `pass`.

### Пример сгенерированного файла

Для команды `alembic revision --autogenerate -m "create Product table"`:

```python
# alembic/versions/f0ac56cb8e72_create_product_table.py
"""create Product table

Revision ID: f0ac56cb8e72
Revises: None
Create Date: 2025-07-17 14:29:00

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'f0ac56cb8e72'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'Product',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('description', sa.String, nullable=False),
        sa.Column('price', sa.Integer, nullable=False)
    )

def downgrade() -> None:
    op.drop_table('Product')
```

### Как работать?

* **Создание**: Создаётся автоматически при `alembic init alembic`.
* **Редактирование**:
  * Обычно редактировать `script.py.mako` не нужно, так как стандартный шаблон подходит для большинства случаев.
  * Если хочешь изменить структуру файлов миграций, отредактируй шаблон. Например, добавь комментарий:
    ```mako
    """${message}

    Revision ID: ${up_revision}
    Revises: ${down_revision | comma,n}
    Create Date: ${create_date}
    Author: Your Name
    """
    ```
* **Проверка**:
  * Создай миграцию:
    ```bash
    alembic revision --autogenerate -m "test"
    ```
  * Проверь сгенерированный файл:
    ```bash
    cat alembic/versions/*.py
    ```

### Как настраивать?

* **Добавить импорты**:
  * Если используешь специфичные типы (например, `JSON`), добавь в шаблон:
    ```mako
    import sqlalchemy as sa
    from sqlalchemy.dialects.postgresql import JSON
    ${imports if imports else ""}
    ```
* **Добавить аннотации**:
  * Для строгой типизации добавь аннотации в `upgrade` и `downgrade`:
    ```mako
    def upgrade() -> None:
        ${upgrades if upgrades else "pass"}

    def downgrade() -> None:
        ${downgrades if downgrades else "pass"}
    ```
* **Кастомные метаданные**:
  * Добавь дополнительные поля, например, автора:

    ```mako
    """${message}

    Revision ID: ${up_revision}
    Revises: ${down_revision | comma,n}
    Create Date: ${create_date}
    Author: ${author | 'Unknown'}
    """
    ```

    * Задай автора при создании миграции:
      ```bash
      alembic revision --autogenerate -m "test" --author="Your Name"
      ```

### Пример для твоего проекта

Оставь стандартный `script.py.mako`, так как он подходит для твоих миграций (`Product` модель):

```mako
"""${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = ${repr(up_revision)}
down_revision = ${repr(down_revision)}
branch_labels = ${repr(branch_labels)}
depends_on = ${repr(depends_on)}

def upgrade() -> None:
    ${upgrades if upgrades else "pass"}

def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
```

---

## Связь с твоим контекстом (`Ecomerce`)

### Твой проект

* Ты используешь Alembic для управления таблицами, например, `Product`:
  ```python
  # models/product.py
  from sqlalchemy.orm import Mapped, mapped_column
  from sqlalchemy import String, Integer
  from models.base import Base

  class Product(Base):
      __tablename__ = 'Product'
      id: Mapped[int] = mapped_column(primary_key=True)
      name: Mapped[str] = mapped_column(String, nullable=False)
      description: Mapped[str] = mapped_column(String, nullable=False)
      price: Mapped[int] = mapped_column(Integer, nullable=False)
  ```
* Ты упомянул проблему с созданием таблиц, которая решилась с `alembic revision --autogenerate` благодаря правильной настройке `env.py`.

### Как файлы связаны с проектом

* **`alembic.ini`**:
  * Убедись, что `sqlalchemy.url` соответствует твоему `DBConnector`:
    ```ini
    sqlalchemy.url = postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL
    ```
  * Если запускаешь Alembic на хосте:
    ```ini
    sqlalchemy.url = postgresql+asyncpg://gsa:0502@localhost:8080/PostgreSQL
    ```
* **`env.py`**:
  * Проверь, что импортирована модель `Product`:
    ```python
    import models.product
    target_metadata = Base.metadata
    ```
  * Используй `create_async_engine` для асинхронного PostgreSQL.
* **`script.py.mako`**:
  * Стандартный шаблон подходит для твоих миграций, так как ты создаёшь простые таблицы (`Product`).
  * Пример миграции:
    ```bash
    alembic revision --autogenerate -m "create Product table"
    alembic upgrade head
    ```

### Проверка

1. **Проверь конфигурацию**:
   ```bash
   alembic current
   psql -h localhost -p 8080 -U gsa -d PostgreSQL -c "\dt"
   ```
2. **Создай миграцию**:
   ```bash
   alembic revision --autogenerate -m "test"
   cat alembic/versions/*.py
   ```
3. **Применяй миграции**:
   ```bash
   alembic upgrade head --verbose
   ```
4. **Тестируй API**:
   ```bash
   docker-compose up --build -d
   curl -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"name":"Laptop","description":"Cool laptop","price":999}'
   curl http://localhost:8000/products
   ```

### Рекомендации

1. **`alembic.ini`**:
   * Храни пароль в переменных окружения:

     ```bash
     export DB_URL=postgresql+asyncpg://gsa:0502@db:5432/PostgreSQL
     ```

     ```ini
     sqlalchemy.url = %(DB_URL)s
     ```
2. **`env.py`**:
   * Импортируй все модели:
     ```python
     import models.product
     import models.order  # Если добавишь модель Order
     ```
   * Добавь логи:
     ```python
     import logging
     logging.basicConfig()
     logging.getLogger('alembic').setLevel(logging.INFO)
     ```
3. **`script.py.mako`**:
   * Оставь стандартный шаблон, если не нужны кастомные метаданные.
4. **Избегай ошибок**:
   * Если таблицы не создаются, проверь `env.py` (импорт моделей, `target_metadata`).
   * Если ошибка подключения, проверь `sqlalchemy.url` и `docker-compose.yml`.
