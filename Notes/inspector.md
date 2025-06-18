Inspect в SQLAlchemy используется для получения информации о различных объектах, таких как таблицы, модели, соединения и т.д. Он возвращает объект инспектора, который предоставляет методы для извлечения информации о структуре базы данных и связанных объектах.

Импортируем:

```javascript
from sqlalchemy import inspect
```

```
try:
    engine = create_engine(DB_URL.get('postgresql'))
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    if tables:
        print('\tТаблицы: ', ','.join(tables))
    else:
        print('\tТаблицы отсутствуют')

except Exception as e:
    print('Error!', e)
```

**Получение информации о колонках в таблице**

```sql
columns = inspector.get_columns('имя_таблицы')
   for column in columns:
       print(column)
```

**Проверка существования таблицы**

```perl
exists = inspector.has_table('имя_таблицы')
print(exists)
```

**Получение информации о внешних ключах**

```bash
foreign_keys = inspector.get_foreign_keys('имя_таблицы')
print(foreign_keys)
```

**Получение информации об индексах**

```bash
indexes = inspector.get_indexes('имя_таблицы')
print(indexes)
```

**Сводная информация по модели**

```python
from your_model import 'имя_модели'

model_inspect = inspect('имя_модели') #inspect на уровне модели

relationships = model_inspect.relationships #связи с другими таблицами
for relation in relationships:
    print(relation)

# список столбцов с указанием типа данных
for column in model_inspect.columns:
    print(column.key, column.type)
```
