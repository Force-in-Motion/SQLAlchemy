Создание всех таблиц сразу:

```
from sqlalchemy import create_engine

from src.config.url import DB_URL
from src.models import Base



try:
    engine = create_engine(DB_URL.get('postgresql'), echo=True)
    Base.metadata.create_all(engine)
except Exception as e:
    print('Error!', e)
```
