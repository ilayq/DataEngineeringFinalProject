'''Файл который содержит форматы ответов и запросов сервера'''

# импортируем специальный класс, в котором описана валидация данных и приведение к формату Json
# импортируем валидатор - фукнцию, в которой можно описать специальные проверки для данных 
from pydantic import BaseModel, validator
from datetime import time, datetime
from typing import List


# Описываем те же поля, что и в бд
class User(BaseModel):
    tg_id: int
    name: str
    start_time: time
    bus_station: int

    # подкласс для настройки
    # orm_mode - режим совместимости с классами для баз данных
    # validate_assignment - проверка данных не только при создании, но и при изменении класса
    class Config:  
        orm_mode = True
        validate_assignment = True

    # специальный метод, вычисляющий хеш объекта, нужен чтобы добавлять класс в словари и множества
    def __hash__(self) -> int:
        return hash((type(self),) + tuple(self.__dict__.values()))


class Driver(User):
    places: int
    car: str

    def __hash__(self) -> int:
        return super().__hash__()

class Passenger(User):
    pass

    def __hash__(self) -> int:
        return super().__hash__()

if __name__ == '__main__':
    #тесты
    dr = Driver(
        tg_id=1,
        name='asd',
        start_time=time(hour=1, minute=2),
        end_time=time(hour=1, minute=3),
        bus_station=1,
        places=1,
        car="asd 123"
    )
    a = dict()
    a[dr] = 1
    print(a[dr])
