**Транзакция** — это последовательность операций с БД, которая выполняется как единое целое. Она должна быть:

* **Атомарной (Atomic)** — либо все операции выполняются, либо ни одна.
* **Согласованной (Consistent)** — БД переходит из одного валидного состояния в другое.
* Изолированной (Isolated) **— параллельные транзакции не мешают друг другу.
* **Долговечной (Durable)** — после фиксации изменения сохраняются даже при сбое.

Эти требования, их ещё называют (по аббревиатуре) **ACID **— набор требований к транзакционной системе, обеспечивающий наиболее надёжную и предсказуемую её работу.

SQLAlchemy поддерживает транзакции через Session (ORM) и Connection (Core).

Пример через Session (мы уже использовали этот вариант):

```python
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()  # Начинается неявная транзакция

try:
    user = User(name="Alice")
    session.add(user)
    session.commit()  # Фиксация изменений
except:
    session.rollback()  # Откат при ошибке
    raise
finally:
    session.close()  # Закрытие сессии
```

Пример через Core:

```applescript
with engine.connect() as connection:
    transaction = connection.begin()  # Явное начало транзакции
    try:
        connection.execute(text("INSERT INTO users (name) VALUES ('Bob')"))
        transaction.commit()  # Фиксация изменений
    except:
        transaction.rollback()  # Откат
        raise
```

Рассмотрим подробно каждое свойство ACID на примере базы данных для учета животных (Pets) и манипуляций (ManipulationFacts).

Модели:

```sql
pets = Table(
    'pets', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('species', String(30)),
    Column('arrival_date', DateTime, default=datetime.utcnow)
)

manipulation_facts = Table(
    'manipulation_facts', metadata,
    Column('id', Integer, primary_key=True),
    Column('pet_id', Integer, ForeignKey('pets.id')),
    Column('procedure', String(100)),
    Column('executed_at', DateTime, default=datetime.utcnow)
)
```

**Атомарность (Atomicity)** — либо все операции выполняются, либо ни одна.

Пример для бизнес-процесса, отталкивающегося от карточки манипуляций: открывается форма для манипуляции, а затем в неё вносятся необходимые данные (питомец, дата, срочность и т.д.)

Что это значит Атомарность в этом случае? - Добавление нового питомца и процедуры должно выполняться как единое целое.

```python
def add_pet_with_procedure(conn, pet_name, species, procedure):
    trans = conn.begin()  # Начинаем транзакцию
    try:
        # Вставляем питомца
        pet_result = conn.execute(
            pets.insert().values(name=pet_name, species=species)
        pet_id = pet_result.inserted_primary_key[0]
        
        # Вставляем процедуру
        conn.execute(
            manipulation_facts.insert().values(
                pet_id=pet_id,
                procedure=procedure
            ))
        
        trans.commit()  # Фиксируем оба изменения
        print("Операция успешно завершена")
    except Exception as e:
        trans.rollback()  # Откатываем при ошибке
        print(f"Ошибка: {e}. Все изменения отменены.")

# Использование
with engine.connect() as conn:
    add_pet_with_procedure(conn, "Барсик", "Кошка", "Вакцинация")
```

Что произойдет при ошибке:

Если вставка в manipulation\_facts провалится, запись в pets тоже не сохранится.

**Согласованность (Consistency)** — БД переходит из одного валидного состояния в другое.

Другими словами: каждая успешная транзакция по определению фиксирует только допустимые результаты.

Например: Проверим ограничения перед выполнением операции.

```python
def add_manipulation(conn, pet_id, procedure):
    # Проверяем существование питомца
    check = conn.execute(
        pets.select().where(pets.c.id == pet_id)
    ).fetchone()
    
    if not check:
        raise ValueError("Питомец с таким ID не существует")
    
    # Проверяем валидность процедуры
    if not procedure or len(procedure) > 100:
        raise ValueError("Некорректное описание процедуры")
    
    # Если проверки пройдены, выполняем вставку
    conn.execute(
        manipulation_facts.insert().values(
            pet_id=pet_id,
            procedure=procedure
        ))
    print("Процедура успешно добавлена")

# Использование
with engine.begin() as conn:  # Автоматическое управление транзакцией
    try:
        add_manipulation(conn, 1, "Стрижка когтей")
    except ValueError as e:
        print(f"Ошибка согласованности: {e}")
```

Выполненные проверки гарантируют:

* В manipulation\_facts не может быть ссылок на несуществующих питомцев
* Все строковые ограничения соблюдаются

**Изолированность (Isolated) **— во время выполнения транзакции параллельные транзакции не должны оказывать влияния на её результат. Изолированность — требование дорогое, поэтому в реальных базах данных существуют режимы, не полностью изолирующие транзакцию (уровни изолированности, допускающие фантомное чтение).

Выбор уровня изоляции - это всегда компромисс между:

1. Согласованностью данных
2. Производительностью
3. Параллелизмом операций

При параллельном выполнении транзакций возможны следующие аномалии (проблемы):

* потерянное обновление (англ. **lost update**) — при одновременном изменении одного блока данных разными транзакциями теряются все изменения, кроме последнего;
* «грязное» чтение (англ. **dirty read**) — чтение данных, добавленных или изменённых транзакцией, которая впоследствии не подтвердится (откатится);
* неповторяющееся чтение (англ. **non-repeatable read**) — при повторном чтении в рамках одной транзакции ранее прочитанные данные оказываются изменёнными;
* фантомное чтение (англ. **phantom reads**) — одна транзакция в ходе своего выполнения несколько раз выбирает множество строк по одним и тем же критериям. Другая транзакция в интервалах между этими выборками добавляет строки или изменяет столбцы некоторых строк, используемых в критериях выборки первой транзакции, и успешно заканчивается. В результате получится, что одни и те же выборки в первой транзакции дают разные множества строк.

В SQLAlchemy для решения этих проблем используются следующие уровни изоляции:

#### Read Uncommitted (Грязное чтение)

Это самый низкий уровень изоляции. Он позволяет читать незафиксированные изменения ("грязные данные").

Для него характерна высокая производительность, но и значителен риск несогласованных данных.

```scss
# Транзакция 1 (изменяет данные)
with engine.connect() as conn1:
    conn1.execution_options(isolation_level="READ UNCOMMITTED")
    conn1.execute(text("BEGIN"))
    conn1.execute(text("UPDATE pets SET name = 'Новое имя' WHERE id = 1"))
    # Не фиксируем!

# Транзакция 2 (читает незафиксированные данные)
with engine.connect() as conn2:
    conn2.execution_options(isolation_level="READ UNCOMMITTED")
    result = conn2.execute(text("SELECT name FROM pets WHERE id = 1")).fetchone()
    print(result)  # Увидит 'Новое имя', хотя первая транзакция не закоммитила
```

Проблемы:

* Если первая транзакция откатится, вторая будет работать с некорректными данными
* Не поддерживается в PostgreSQL (автоматически повышается до READ COMMITTED)

#### Read Committed (Чтение зафиксированных данных)

Это уровень по умолчанию в PostgreSQL и многих других СУБД. Он гарантирует чтение только зафиксированных данных.

Возможно "неповторяемое чтение" (non-repeatable read).

```scss
# Транзакция 1
with engine.connect() as conn1:
    conn1.execution_options(isolation_level="READ COMMITTED")
    with conn1.begin():
        conn1.execute(text("UPDATE pets SET species = 'Кот' WHERE id = 1"))

# Транзакция 2
with engine.connect() as conn2:
    conn2.execution_options(isolation_level="READ COMMITTED")
    
    # Первое чтение
    result1 = conn2.execute(text("SELECT species FROM pets WHERE id = 1")).fetchone()
    print("До изменения:", result1[0])
    
    # После изменения в другой транзакции
    result2 = conn2.execute(text("SELECT species FROM pets WHERE id = 1")).fetchone()
    print("После изменения:", result2[0])  # Может измениться!
```

Типичные проблемы:

* Non-repeatable read: повторное чтение тех же данных может дать различный результат
* Phantom reads: появление новых строк при повторном выполнении запроса

#### Repeatable Read (Повторяемое чтение)

Этот уровень гарантирует, что данные, прочитанные в транзакции, не изменятся.

Блокирует изменяемые строки до конца транзакции, но не защищает от фантомных чтений (новые строки могут появляться).

```applescript
# Транзакция 1 (долгая)
with engine.connect() as conn1:
    conn1.execution_options(isolation_level="REPEATABLE READ")
    with conn1.begin():
        # Первое чтение
        count = conn1.execute(text("SELECT COUNT(*) FROM pets")).scalar()
        print("Начальное количество:", count)
        
        # Имитируем долгую обработку
        time.sleep(5)
        
        # Повторное чтение
        count = conn1.execute(text("SELECT COUNT(*) FROM pets")).scalar()
        print("Конечное количество:", count)  # Будет таким же

# Параллельно в другой транзакции
with engine.connect() as conn2:
    with conn2.begin():
        conn2.execute(text("INSERT INTO pets (name, species) VALUES ('Новый', 'Пёс')"))
```

Особенности:

* В PostgreSQL фактически предотвращает и фантомные чтения (расширение стандарта)
* В MySQL/MariaDB фантомные чтения возможны

#### Serializable (Сериализуемый)

Это самый строгий уровень изоляции. Он эмулирует последовательное выполнение транзакций.

Полностью предотвращает:

* Грязные чтения
* Неповторяемые чтения
* Фантомные чтения

```python
def transfer_procedure(conn, from_pet, to_pet, procedure):
    try:
        with conn.begin():
            # Проверяем существование процедуры
            exists = conn.execute(
                text("SELECT 1 FROM manipulation_facts WHERE pet_id = :pid AND procedure = :proc"),
                {"pid": from_pet, "proc": procedure}
            ).scalar()
            
            if not exists:
                raise ValueError("Процедура не найдена")
            
            # Перемещаем процедуру
            conn.execute(
                text("""
                    UPDATE manipulation_facts 
                    SET pet_id = :to_pet 
                    WHERE pet_id = :from_pet AND procedure = :proc
                """),
                {"to_pet": to_pet, "from_pet": from_pet, "proc": procedure}
            )
    except Exception as e:
        print(f"Ошибка: {e}")
        raise

# Параллельные вызовы
with engine.connect() as conn:
    conn.execution_options(isolation_level="SERIALIZABLE")
    
    # Эти вызовы будут выполняться последовательно
    Thread(target=transfer_procedure, args=(conn, 1, 2, "Вакцинация")).start()
    Thread(target=transfer_procedure, args=(conn, 2, 1, "Стрижка")).start()
```

Особенности реализации:

* В PostgreSQL использует предикатные блокировки
* В MySQL использует блокировки диапазонов индексов
* Может вызывать ошибки сериализации (Error 40001 в PostgreSQL)

### Рекомендации по выбору уровня изоляции:

1. Для отчетов и аналитики: READ COMMITTED

* Высокая производительность
* Незначительные расхождения допустимы

2. Для финансовых операций: REPEATABLE READ или SERIALIZABLE

* Гарантированная согласованность
* В PostgreSQL часто достаточно REPEATABLE READ

3. Для высоконагруженных систем:

* READ COMMITTED + оптимистичная блокировка
* ORM-уровневая проверка версий

4. Для сложных бизнес-процессов: SERIALIZABLE

* Когда важна абсолютная согласованность
* С обработкой ошибок сериализации

Пример обработки ошибок сериализации:

```python
from sqlalchemy.exc import OperationalError
from psycopg2.errors import SerializationFailure

def safe_serializable_operation():
    max_retries = 3
    for attempt in range(max_retries):
        with engine.connect() as conn:
            conn.execution_options(isolation_level="SERIALIZABLE")
            try:
                with conn.begin():
                    # Критическая операция
                    conn.execute(text("..."))
                    return True
            except OperationalError as e:
                if isinstance(e.orig, SerializationFailure):
                    print(f"Попытка {attempt + 1}: конфликт сериализации, повторяем")
                    continue
                raise
    return False
```

**Долговечность (Durability)** — после фиксации, изменения сохраняются даже при сбое.
Пример:

```scss
def critical_operation(conn):
    # Включаем WAL (Write-Ahead Logging) для PostgreSQL
    conn.execute(text("SET synchronous_commit = ON"))
    
    trans = conn.begin()
    try:
        # Важная операция - например, хирургическое вмешательство
        conn.execute(
            manipulation_facts.insert().values(
                pet_id=1,
                procedure="Сложная операция",
                executed_at=datetime.utcnow()
            ))
        
        # Фиксация с гарантией записи на диск
        trans.commit()
        print("Данные о процедуре гарантированно сохранены")
    except Exception as e:
        trans.rollback()
        print(f"Ошибка: {e}")

# Использование
with engine.connect() as conn:
    critical_operation(conn)
```

**После commit данные записаны в постоянное хранилище.**

Выживет даже при перезагрузке сервера БД!

Ключевое различие: Durability vs Atomicity:

**Durability (Долговечность) - **Гарантирует, что уже зафиксированные (committed) изменения сохранятся даже при сбое оборудования (отключение электричества, крах сервера БД).
Пример: После COMMIT данные записываются в постоянное хранилище (журнал транзакций/WAL).

**Atomicity (Атомарность) - **Гарантирует, что либо все операции транзакции выполнятся, либо ни одна из них.
Пример: Если ошибка происходит до COMMIT, все изменения откатываются.

**Сценарий 1**: Успешное выполнение (COMMIT).

1. Данные вставлены в таблицу manipulation\_facts.
2. trans.commit():

* PostgreSQL: Синхронно записывает изменения в WAL (Write-Ahead Log) на диск.
* Только после успешной записи в WAL транзакция считается завершённой.

3. Даже если сервер упадёт сразу после COMMIT, данные будут восстановлены из WAL при перезапуске.

**Сценарий 2**: Ошибка и откат (ROLLBACK)

1. Если возникнет ошибка (например, нарушение UNIQUE-ограничения):

* Выполнится trans.rollback().
* Изменения не будут записаны в WAL.

2. Durability не нарушается, потому что:

* Незафиксированные данные никогда не попадают в постоянное хранилище.
* Некорректные данные отбрасываются на этапе Atomicity.

**Как обеспечивается Durability?**
***WAL (Write-Ahead Logging)***

* Все изменения сначала записываются в журнал (WAL), потом в саму БД.
* Даже при сбое система может восстановить данные из WAL.

***Синхронная запись (synchronous\_commit = ON)***

* PostgreSQL ждёт подтверждения записи WAL на диск перед возвратом COMMIT.
* Альтернатива: synchronous\_commit = OFF (риск потери данных при сбое).

***Журналирование на файловых системах***

* ОС гарантирует, что данные, переданные в write(), действительно записаны на диск.
