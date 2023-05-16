from sqlalchemy import create_engine
from .ORMModels import Base

#создаем подключение к базе данных
engine = create_engine('sqlite:///db.db', echo=True)

# импортируем класс Base и через него создаем таблицы
# Base хранит информацию о наследниках, и для этого мы наследовались от него
if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
