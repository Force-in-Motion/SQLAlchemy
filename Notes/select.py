# По аналогии с insert, всё начинается с импорта объекта:

from sqlalchemy import select, create_engine
from sqlalchemy.orm import Session

from src.config.url import DB_URL
from src.models import Owners

engine = create_engine(DB_URL.get('postgresql'), echo=True)
with Session(engine) as session:
    request = select(Owners.owner_id, Owners.owner_name)
    print('request:', request)

    for row in session.execute(request):

        print(row)