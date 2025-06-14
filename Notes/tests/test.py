# SQLAlchemy представляет для тестирования несколько вариантов:
import pytest
# In-memory SQLite: Быстро, но несовместимо со сложными SQL-функциями.
# Тестовая БД на каждый тест: pytest + фикстуры для создания и удаления. Подробнее в 5.2
# Транзакционные тесты: Откат после каждого теста (rollback). Подробнее в 8.3
# Главные правила тестирования:

# Никогда не тестируйте против продакшен-БД.
# Каждый тест должен стартовать с чистого состояния.
# Используйте фикстуры для подготовки данных (например, Factory Boy).
# Для CI/CD подойдет комбинация: SQLite (быстро) + Docker (для сложных кейсов).

# In-memory SQLite - это база данных SQLite, которая хранится в оперативной памяти, а не на диске.

# Она идеально подходит для юнит-тестов и быстрых экспериментов.

# После завершения работы программы БД SQLite исчезает.

# Пример подключения:

from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")  # URL подключения

# Преимущества:

# Молниеносная скорость - нет затрат на запись/чтение с диска. Тесты работают в 10-100 раз быстрее, чем при работе с PostgreSQL или MySQL.
# Полная изоляция тестов - каждый тест стартует с чистой БД. Нет риска повредить данные продакшена.
# Простота настройки - не требует установки СУБД или Docker.

# Недостатки:

# Не поддерживает сложные SQL-функции - некоторые операции из PostgreSQL/MySQL не работают (например, JSONB, специфичные индексы).
# Нет персистентности (персистентность - это возможность хранить объекты постоянно, даже между выполнениями программы) -  данные исчезают после закрытия соединения.
# Один поток на БД - по умолчанию нельзя делить одно соединение между потоками.


# Пример функции, которая проверит возможность создания таблицы:

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.models import Base


def db_session():
    engine = create_engine("sqlite:///:memory:")  # БД в RAM
    Base.metadata.create_all(engine)
    yield sessionmaker(bind=engine)()
    Base.metadata.drop_all(engine)


# Существует специализированный фреймворк для тестирования программного обеспечения на языке Python - Pytest.
# Он позволяет разработчикам создавать и запускать тесты для проверки корректности работы своих программ.

# Основные преимущества pytest:

# Простота использования: Тесты пишутся как обычные функции с понятными assert-утверждениями
# Автоматическое обнаружение тестов: pytest находит тесты по соглашениям (файлы test_*.py и функции test_*)
# Фикстуры (fixtures): Мощный механизм для подготовки тестового окружения
# Параметризация: Легко запускать один тест с разными входными данными
# Плагины: Богатая экосистема расширений
# Подробные отчеты: Четкие сообщения об ошибках
# Подробнее по п.2. Pytest может автоматически находить тестовые файлы и директории, для этого должны соблюдаться следующие условности:

# Имя файла должно начинаться с ”test” или заканчиваться “test.py”.
# Имена функций и переменных должны быть написаны в нижнем регистре, а слова должны быть разделены подчеркиванием. При этом имя тестовой функции должно начинаться с “test_” (например “test_sql_injections”).
# Установка пакета:

# pip install pytest

# Можно использовать параметры (запускать один тест с разными наборами данных):
def add(a, b):
    return a + b

@pytest.mark.parametrize("a,b,expected", [
     (1, 2, 3),
     (5, -1, 4),
     (0, 0, 0),
     (100, 200, 300)
 ])
def test_add(a, b, expected):
     assert add(a, b) == expected


# 4. Фикстуры - это функции, которые подготавливают данные или состояние для тестов. Похоже на работу parametrize:

@pytest.fixture
def sample_data():
     return [1, 2, 3, 4, 5]

def test_sum(sample_data):
    assert sum(sample_data) == 15

def test_length(sample_data):
    assert len(sample_data) == 5


# В документации к Pytest рекомендуют вынести все тесты в отдельный каталог и использовать conftest.py для хранения общих фикстур. Благодаря этому, они будут доступны во всех тестах:

# Структура проекта:
#
# project/
# ├── src/
# │   └── myapp/
# │       ├── __init__.py
# │       └── module.py
# └── tests/
#     ├── __init__.py
#     ├── test_module.py
#     └── conftest.py


# 4.2 Существует расширенная версия фикстур -  с параметрами:
#
# @pytest.fixture(params=['sqlite', 'postgresql'])
# def database(request):
#     if request.param == 'sqlite':
#         engine = create_engine('sqlite:///:memory:')
#     elif request.param == 'postgresql':
#         engine = create_engine('postgresql://user:pass@localhost/test')
#     return engine
#
# def test_db_connection(database):
#     assert database.connect() is not None



# Тесты, написанные с использованием pytest, можно запустить несколькими способами:

# 1. Запуск всех тестов в проекте:
# pytest


# 2. Запуск конкретного тестового файла:
# pytest test_owners.py


# 3. Запуск конкретного теста:
# pytest test_owners.py::test_create_owner


# 4. Запуск с подробным выводом (-v) и выводом print-ов (-s):
# pytest -v -s


# 5. Запуск с генерацией отчета о покрытии:
# pytest --cov=your_module




# Логирование в файл

# Можно перенаправить вывод в файл:
# pytest -v > test.log 2>&1


# Или с помощью встроенного механизма pytest:
# pytest --log-file=test.log --log-file-level=DEBUG


# 5. Для просмотра SQL-запросов
# Добавьте echo в фикстуру db_engine для логирование SQL:

@pytest.fixture(scope="session")
def db_engine(postgres_container):
    engine = create_engine(
        f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost:{PORT}/{POSTGRES_DB}",
        echo=True  # Включаем логирование SQL
    )
    yield engine
    engine.dispose()


# 6. Просмотр логов после падения теста
# pytest --show-capture=all


# 7. Генерация HTML-отчета
# * требуется установка плагина:
# pip install pytest-html

# Создание HTML-отчета:
# pytest --html=report.html


# 8. Логирование через logging
# Если в коде используется модуль logging, добавьте конфигурацию:
# import logging
# logging.basicConfig(level=logging.DEBUG)

# И запустите тесты с захватом логов:
# pytest --log-cli-level=DEBUG


# Для наиболее полного лога рекомендуется использовать комбинацию:
# pytest -v -s --log-cli-level=DEBUG --show-capture=all