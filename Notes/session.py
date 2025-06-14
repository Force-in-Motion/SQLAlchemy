# Session (сессии) в SQLAlchemy — это объект, который управляет взаимодействием с базой данных, обеспечивая удобный способ работы с транзакциями и объектами модели. Он является центральным элементом системы управления состоянием SQLAlchemy.
# Если говорить упрощенно, то Сессии отслеживают изменения, сделанные в рамках одной транзакции, а затем обрабатывают их: группируют повторяющиеся операции, выполняют топологическую сортировку по зависимостям и т.д. А затем выполняют их в базе.


from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.config.url import DB_URL
from src.models import Owners


try:
        engine = create_engine(DB_URL.get('postgresql'), echo=True)
        session = Session(engine)

        owner1 = Owners(
            owner_name='Иванов Иван Иванович',
            owner_email='ivanov@mail.ru',
            owner_phone='+71231231212'
            )

        owner2 = Owners(
            owner_name='Петров Пётр Петрович',
            owner_email='petrov@mail.ru',
            owner_phone='+71231231223'
            )

        owner3 = Owners(
            owner_name='Сидоров Сидор Сидорович',
            owner_email='sidorov@mail.ru',
            owner_phone='+71231231233'
            )

        session.add(owner1)
        session.add(owner2)
        session.add(owner3)

        session.commit()


except Exception as e:
    print('Error!', e)


# На предыдущем шаге для добавления записей мы использовали вариант с созданием экземпляров модели и "поштучного" их добавления:

#         engine = create_engine(DB_CONNECTION_URLS[subd], echo=True)
#         session = Session(engine)

#         owner1 = Owners( ... )
#         owner2 = Owners( ... )
#         owner3 = Owners( ... )

#         session.add(owner1)
#         session.add(owner2)
#         session.add(owner3)

#         session.commit()
# Мы можем немного сократить код, воспользовавшись методом сессии add_all():

#         engine = create_engine(DB_CONNECTION_URLS[subd], echo=True)
#         session = Session(engine)

#         owner1 = Owners( ... )
#         owner2 = Owners( ... )
#         owner3 = Owners( ... )

#         session.add_all([owner1, owner2, owner3]) # передаем массив объектов

#         session.commit()
# Раз сессии производят группировку объектов и выполняют предобработку для оптимизации выполнения запроса, то, наверное, мы можем работать одновременно с разными моделями в рамках одной сессии?

# Это, действительно, так:

#         owner4 = Owners(
#             owner_name='Смирнов Павел Федорович',
#             email='smirnov@mail.ru',
#             phone='+71231234233'
#             )

#         manip1 = Manipulations(manipulation_name='Первичный осмотр')


#         session.add_all([owner4, manip1])

#         print('session.new', session.new)

#         session.commit()
# Здесь мы создаем экземпляры двух моделей и выполняем операцию добавления записей.

# session.new содержит данные об объектах, которые находятся в очереди на обработку.

# В нашем примере это:

# IdentitySet([<Models.owners.Owners object at 0x0000025154E00D60>, <Models.manipulations.Manipulations object at 0x0000025154E00F10>])