import os, sys

sys.path.append(fr'C:\Users\{os.getlogin()}\de_project')

from sqlalchemy.orm import Session

from db import engine, DriverORM, PassengerORM
from server.shemas import Driver, Passenger
from typing import Union


async def add_user_handler(user: Union[Driver, Passenger]) -> bool:
    dicted_user = user.dict()
    #переводим данные о пользователе в словарь, чтобы потом создать класс для бд
    print(f"dicted user: {dicted_user}")
    with Session(engine) as db: #подключение к бд
        if "places" in dicted_user:     
            db.add(DriverORM(**dicted_user))
        else:
            db.add(PassengerORM(**dicted_user))
        db.commit() # подтверждаем изменения и закрываем соединение
        db.close()
    return True
