import uvicorn
import fastapi

from typing import Union, List
import datetime

from handlers import add_user_handler, get_user_data_handler, patch_user_handler, find_driver_handler
from shemas import Driver, Passenger


app = fastapi.FastAPI()


active_drivers: List[Driver]
active_drivers = []


def check_driver_list(func):

    def check_drivers(*args, **kwargs):
        cur_time = datetime.datetime.now()
        cur_timedelta = datetime.timedelta(hours=cur_time.hour, minutes=cur_time.minute)
        pop_shift = 0
        for idx in range(len(active_drivers)):
            driver = active_drivers[idx - pop_shift]
            driver_time = driver.start_time
            driver_timedelta = datetime.timedelta(hours=driver_time.hour, minutes=driver_time.minute)
            if cur_timedelta + datetime.timedelta(minutes=10) >= driver_timedelta:
                active_drivers.pop(idx - pop_shift)
                pop_shift += 1
        print(active_drivers)
        func(*args, **kwargs)
    
    return check_drivers


def make_response(response: bool) -> dict:
    if response:
        return {"msg": "success"}
    return {"msg": "failed"}


@check_driver_list
@app.post('/user')
async def add_user(user: Union[Driver, Passenger]):
    response = await add_user_handler(user)
    return make_response(response)


@check_driver_list
@app.patch('/user')
async def patch_user(user: Union[Driver, Passenger]):
    response = await patch_user_handler(user)
    return make_response(response)


@check_driver_list
@app.get('/user')
async def get_user_data(tg_id: int) -> Union[Driver, Passenger]:
    r = await get_user_data_handler(tg_id=tg_id)
    if not r:
        return {"msg": "fail"}
    return r


@check_driver_list
@app.get('/find_driver')
async def find_driver_for_passenger(passenger_tg_id: int) -> Driver:
    driver = await find_driver_handler(passenger_tg_id, active_drivers)
    if driver:
        return driver
    else:
        return {"msg": "unable to find driver", "status": "fail"}


@check_driver_list
@app.get('/add_driver_to_query')
async def add_driver_to_active(driver_tg_id: int):
    driver = await get_user_data_handler(tg_id=driver_tg_id)
    active_drivers.append(driver)
    return make_response(driver)


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
