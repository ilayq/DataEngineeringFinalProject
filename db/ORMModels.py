from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Time


Base = declarative_base()

#Создаем Класс Юзера с общеми полями для водителей и пассажиров
# Каждое поле - это колонка в базе данных
# primary_key - специальная пометка, что данные в столбце уникальные и по ним будет осуществляться поиск в бд
# nullable - означает, что столбец может быть пустым (если тру)
class UserORM:
    tg_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False) 
    start_time = Column(Time, nullable=False)
    bus_station = Column(Integer, nullable=False)

# Наследуемся от класса юзер и класса Base
# указываем __tablename__ - название таблицы в бд
class PassengerORM(Base, UserORM):
    __tablename__ = 'passengers'


class DriverORM(Base, UserORM):
    __tablename__ = 'drivers'

    places = Column(Integer, nullable=False)
    car = Column(String, nullable=False)
