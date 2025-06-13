# По аналогии с insert, всё начинается с импорта объекта:

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from src.config.url import DB_URL
from src.models import Owners

engine = create_engine(DB_URL.get('postgresql'), echo=True)

with Session(engine) as session: # При помощи контекстного менеджера открываем сессию
    request = select(Owners.owner_id, Owners.owner_name) # Формируем запрос используя метод select, указываем какие данные хотим получить и откуда
    print('request:', request)

    response = session.execute(request) # Отправляем запрос и записываем ответ в response

    for row in response:

        print(row)