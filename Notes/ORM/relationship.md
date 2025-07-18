```markdown
### Назначение
- `relationship` в SQLAlchemy — это инструмент ORM (Object-Relational Mapping), который позволяет **связывать объекты моделей** в Python, чтобы упростить работу с отношениями между таблицами (например, один-ко-многим, многие-ко-многим).
- Оно создаёт **атрибут** в классе модели, через который ты можешь:
  - Получать связанные объекты (например, список постов пользователя через `user.posts`).
  - Автоматически загружать связанные данные из базы данных при обращении к атрибуту.

### Как работает?
- `relationship` указывает SQLAlchemy, как связать два класса моделей (например, `User` и `Post`), чтобы ты мог работать с объектами, а не писать SQL-запросы вручную.
- В твоём коде:

  ```python
  # В модели User
  posts: Mapped[list["Post"]] = relationship(back_populates="user")
```

* Это говорит SQLAlchemy, что у объекта **User** есть атрибут **posts**, который возвращает список объектов **Post**, связанных с этим пользователем.
* **back\_populates="user"** указывает обратную связь: в модели **Post** есть атрибут **user**, который ссылается на объект **User**.

```python
# В модели Post
user: Mapped["User"] = relationship(back_populates="posts")
```

* Это указывает, что у объекта **Post** есть атрибут **user**, который возвращает объект **User**, связанный с этим постом.

### Пример использования

Предположим, у тебя есть пользователь и посты в базе:

```python
from sqlalchemy.ext.asyncio import AsyncSession
from service.database.models import User, Post

async def get_user_with_posts(session: AsyncSession, user_id: int):
    user = await session.get(User, user_id)
    if user:
        print(f"User: {user.name}")
        for post in user.posts:  # Используем relationship
            print(f"Post: {post.title}, Body: {post.body}")
    return user
```

* **Что происходит**:
  * **user.posts** автоматически загружает все посты, у которых **user\_id** соответствует **id** пользователя.
  * SQLAlchemy выполняет запрос вида:
    ```sql
    SELECT * FROM Post WHERE user_id = :user_id;
    ```
  * **post.user** возвращает объект **User**, связанный с постом.

### Параметры **relationship**

* **back\_populates**: Указывает обратную связь (например, **user.posts** ↔ **post.user**).
* **lazy**: Определяет, когда загружать связанные данные:

  * **select** (по умолчанию): Загружает данные при первом обращении.
  * **joined**: Загружает данные сразу с помощью JOIN.
  * **subquery**: Использует подзапрос.
  * В твоём коде используется **lazy="select"** по умолчанию.
* Пример с **joined**:

  ```python
  posts: Mapped[list["Post"]] = relationship(back_populates="user", lazy="joined")
  ```

  * Это заставит SQLAlchemy загружать посты сразу при загрузке пользователя:
    ```sql
    SELECT User.*, Post.* FROM User LEFT JOIN Post ON User.id = Post.user_id WHERE User.id = :user_id;
    ```

---

## 2. Чем **relationship** отличается от **ForeignKey**?

### ForeignKey

* **Назначение**: Определяет **внешний ключ** на уровне базы данных. Это ограничение (constraint) в таблице, которое указывает, что значение в столбце (например, **user\_id** в **Post**) должно соответствовать значению первичного ключа в другой таблице (например, **id** в **User**).
* **Где используется**: В определении столбцов модели с помощью **mapped\_column**.
* **Работа**:

  * Создаёт связь на уровне базы данных (в PostgreSQL это **FOREIGN KEY** constraint).
  * Обеспечивает целостность данных: ты не можешь вставить **Post** с **user\_id**, которого нет в таблице **User**.
* **Пример**:

  ```python
  user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
  ```

  * В таблице **Post** создаётся столбец **user\_id**, который ссылается на **id** в таблице **User**.
  * SQL:
    ```sql
    CREATE TABLE Post (
        id INTEGER PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        body TEXT NOT NULL DEFAULT '',
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES User(id)
    );
    ```

### relationship

* **Назначение**: Создаёт **связь на уровне объектов** в Python, чтобы ты мог обращаться к связанным данным через атрибуты (например, **user.posts** или **post.user**).
* **Где используется**: В определении атрибутов модели с помощью **relationship**.
* **Работа**:

  * Не влияет на структуру базы данных (не создаёт столбцы или ограничения).
  * Использует информацию о **ForeignKey** для построения запросов и загрузки связанных данных.
* **Пример**:

  ```python
  posts: Mapped[list["Post"]] = relationship(back_populates="user")
  ```

  * Позволяет получить список постов пользователя через **user.posts**.

### Основные отличия


| **Аспект**               | **ForeignKey**                                                      | **relationship**                                                             |
| ------------------------------ | ------------------------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Уровень**             | База данных (SQL)                                         | Python (ORM)                                                                 |
| **Назначение**       | Определяет внешний ключ в таблице      | Создаёт связь между объектами моделей       |
| **Влияние на БД**   | Создаёт столбец и ограничение FOREIGN KEY | Не влияет на структуру БД                               |
| **Пример**               | **user\_id: Mapped[int] = mapped\_column(ForeignKey("User.id"))**   | **posts: Mapped[list["Post"]] = relationship(back\_populates="user")**       |
| **Зависимость**     | Требуется для**relationship**                           | Использует**ForeignKey**для связи                          |
| **Использование** | Указывает, как таблицы связаны в БД    | Упрощает доступ к связанным данным в коде |

### Как они работают вместе?

* **ForeignKey** задаёт связь на уровне базы данных (например, **Post.user\_id** → **User.id**).
* **relationship** использует эту связь для работы с объектами в Python:
  * **user.posts** загружает все посты с **user\_id**, равным **user.id**.
  * **post.user** загружает пользователя с **id**, равным **post.user\_id**.

### Пример в твоём проекте

* В модели **Post**:
  ```python
  user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
  user: Mapped["User"] = relationship(back_populates="posts")
  ```

  * **ForeignKey("User.id")**: Создаёт столбец **user\_id** в таблице **Post**, который ссылается на **id** в таблице **User**.
  * **relationship(back\_populates="posts")**: Позволяет обращаться к объекту **User** через **post.user**.
* В модели **User**:
  ```python
  posts: Mapped[list["Post"]] = relationship(back_populates="user")
  ```

  * Позволяет получить список постов через **user.posts**.
