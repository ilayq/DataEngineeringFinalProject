import uvicorn
import fastapi

from handlers import add_user_handler, get_user_data_handler
from shemas import Driver, Passenger
from typing import Union, List


app = fastapi.FastAPI()


@app.post('/user')
async def add_user(user: Union[Driver, Passenger]):
    response = await add_user_handler(user)
    if response:
        return {"msg": "success"}
    return {"msg": "failed"}


@app.patch('/user')
async def patch_user(user: Union[Driver, Passenger]):
    ...


@app.get('/user')
async def get_user_data(tg_id: int) -> Union[Driver, Passenger]:
    return await get_user_data_handler(tg_id=tg_id)


@app.get('/find_driver')
async def find_driver_for_passenger(passenger_tg_id: int) -> List[Driver]:
    ...


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
