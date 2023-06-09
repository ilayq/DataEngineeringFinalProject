'''Главный файл, откуда запускается сервер'''


import os, sys

#добавляем папку проекта в поле видимости
sys.path.append(rf"C:\Users\{os.getlogin()}\de_project")

import uvicorn # библиотека которая запускает сервер
import fastapi # сам сервер

from typing import Union
import datetime

# это обработчики запросов на сервер
from server.handlers import add_user_handler, get_user_data_handler, patch_user_handler, find_driver_handler
from server.shemas import Driver, Passenger

# создаем экземпляр класса сервера
app = fastapi.FastAPI()

# список активных водителей
active_drivers: dict[Driver]
active_drivers = dict()

#функция которая проверяет список и удаляет водителей, для которых прошел срок ожидания
def check_driver_list():
    cur_time = datetime.datetime.now()
    cur_timedelta = datetime.timedelta(hours=cur_time.hour, minutes=cur_time.minute)
    keys = active_drivers.keys()
    to_del = []
    for driver in keys:
        driver_time = driver.start_time
        driver_timedelta = datetime.timedelta(hours=driver_time.hour, minutes=driver_time.minute)
        if not (driver_timedelta - datetime.timedelta(minutes=10) <= cur_timedelta  <= driver_timedelta + datetime.timedelta(minutes=10)):
            to_del.append(driver)
        elif active_drivers[driver] == 0:
            to_del.append(driver)
    for key in to_del:
        print(f'delete driver from queue:{key}')
        del active_drivers[key]
    print(active_drivers)    


#фукнция которая возвращает ответ сервера
def make_response(response: bool) -> dict:
    if response:
        return {"msg": "success"}
    return {"msg": "failed"}

#обработчик для добавления юзера
@app.post('/user')
async def add_user(user: Union[Driver, Passenger]):
    response = await add_user_handler(user)
    return make_response(response)

#обновление данных юзера
@app.patch('/user')
async def patch_user(user: Union[Driver, Passenger]):
    response = await patch_user_handler(user)
    return make_response(response)

# получение данных юзера
@app.get('/user')
async def get_user_data(tg_id: int):
    r = await get_user_data_handler(tg_id=tg_id)
    if not r:
        return {"msg": "fail"}
    return r


#находим водителя и возвращаем его данные
@app.get('/find_driver')
async def find_driver_for_passenger(passenger_tg_id: int):
    check_driver_list()
    driver = await find_driver_handler(passenger_tg_id, active_drivers)
    print(f'\n\nDriver found: {driver}\n\n')
    if driver:
        return driver
    else:
        return {"msg": "unable to find driver", "status": "fail"}


#добавляем водителя в очередь 
@app.get('/add_driver_to_query')
async def add_driver_to_active(driver_tg_id: int):
    check_driver_list()
    driver = await get_user_data_handler(tg_id=driver_tg_id)
    active_drivers[driver] = driver.places
    print(f'\n\nadd driver to queue:{driver}')
    return make_response(driver)


#запуск сервера
if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
