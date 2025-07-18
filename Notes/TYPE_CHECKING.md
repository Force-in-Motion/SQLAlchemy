## 3. Что такое **if TYPE\_CHECKING** и как работает **from service.database.models import Post**?

### Назначение **if TYPE\_CHECKING**

* Конструкция **if TYPE\_CHECKING** используется для **условного импорта** типов во время проверки типов (type checking) инструментами, такими как **mypy** или IDE (например, PyCharm, VS Code).
* Это помогает избежать **циклических импортов** на этапе выполнения кода, сохраняя при этом корректные аннотации типов для статической проверки.

### Почему нужен **if TYPE\_CHECKING**?

* В твоём коде модели **User** и **Post** ссылаются друг на друга:

  * **Post** использует **User** в **relationship(user: Mapped["User"])**.
  * **User** использует **Post** в **relationship(posts: Mapped[list["Post"]])**.
* Если ты напрямую импортируешь **User** в **Post** и **Post** в **User**, возникает **циклический импорт**:

  ```python
  # models/post.py
  from service.database.models import User
  class Post(Base):
      user: Mapped["User"] = relationship(back_populates="posts")

  # models/user.py
  from service.database.models import Post
  class User(Base):
      posts: Mapped[list["Post"]] = relationship(back_populates="user")
  ```

  * Это вызовет ошибку **ImportError**, так как Python пытается загрузить один модуль до завершения загрузки другого.
* **if TYPE\_CHECKING** решает проблему, позволяя импортировать типы только для проверки типов, а не во время выполнения.

### Как работает?

* **from typing import TYPE\_CHECKING** импортирует флаг **TYPE\_CHECKING**, который равен **True** только во время статической проверки типов (например, **mypy**) и **False** во время выполнения программы.
* Ты помещаешь импорт внутрь блока **if TYPE\_CHECKING**:

  ```python
  from typing import TYPE_CHECKING

  if TYPE_CHECKING:
      from service.database.models import User
  ```
* **Во время выполнения кода** (**python app.py**):

  * **TYPE\_CHECKING = False**, поэтому импорт **from service.database.models import User****не выполняется**.
  * Это предотвращает циклический импорт.
* **Во время проверки типов** (**mypy** или IDE):

  * **TYPE\_CHECKING = True**, поэтому импорт выполняется, и **mypy** знает, что **User** — это класс из **service.database.models**.
* Вместо прямого использования импортированного класса **User** ты используешь **строковые аннотации** (**"User"** или **list["Post"]**) в **Mapped**:

  ```python
  user: Mapped["User"] = relationship(back_populates="posts")
  posts: Mapped[list["Post"]] = relationship(back_populates="user")
  ```

  * Строковые аннотации позволяют SQLAlchemy и **mypy** понять типы без необходимости импортировать классы во время выполнения.

### Пример работы

1. **Код**:

   ```python
   # models/post.py
   from typing import TYPE_CHECKING
   from sqlalchemy.orm import Mapped, relationship
   from service.database.models.base import Base

   if TYPE_CHECKING:
       from service.database.models import User

   class Post(Base):
       __tablename__ = "Post"
       user_id: Mapped[int] = mapped_column(ForeignKey("User.id"))
       user: Mapped["User"] = relationship(back_populates="posts")
   ```

   ```python
   # models/user.py
   from typing import TYPE_CHECKING
   from sqlalchemy.orm import Mapped, relationship
   from service.database.models.base import Base

   if TYPE_CHECKING:
       from service.database.models import Post

   class User(Base):
       __tablename__ = "User"
       posts: Mapped[list["Post"]] = relationship(back_populates="user")
   ```
2. **Во время выполнения**:

   * Python игнорирует **if TYPE\_CHECKING**, поэтому **User** не импортируется в **post.py**, а **Post** — в **user.py**.
   * SQLAlchemy использует строковые аннотации (**"User"**, **list["Post"]**) для определения связей.
3. **Во время проверки типов**:

   * **mypy** видит импорты и знает, что **User** и **Post** — это классы из **service.database.models**.
   * Это позволяет **mypy** проверять корректность типов, например, что **user.posts** возвращает список объектов **Post**.

### Альтернативы

* Если не использовать **if TYPE\_CHECKING**, можно полностью отказаться от импортов и использовать только строковые аннотации:
  ```python
  class Post(Base):
      user: Mapped["User"] = relationship(back_populates="posts")
  ```
  * SQLAlchemy поддерживает строковые имена классов, но **mypy** может не знать типы без **if TYPE\_CHECKING**, что ухудшит автодополнение в IDE.
* Другой вариант — реорганизовать код, чтобы избежать циклических импортов (например, вынести модели в один файл), но это менее удобно.
