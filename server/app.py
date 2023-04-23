import uvicorn
import fastapi

from handlers import add_user_handler, get_user_data_handler, patch_user_handler
from shemas import Driver, Passenger
from typing import Union, List


app = fastapi.FastAPI()


def make_response(response: bool) -> dict:
    if response:
        return {"msg": "success"}
    return {"msg": "failed"}


@app.post('/user')
async def add_user(user: Union[Driver, Passenger]) -> bool:
    response = await add_user_handler(user)
    return make_response(response)


@app.patch('/user')
async def patch_user(user: Union[Driver, Passenger]) -> bool:
    response = await patch_user_handler(user)
    return make_response(response)


@app.get('/user')
async def get_user_data(tg_id: int) -> Union[Driver, Passenger]:
    return await get_user_data_handler(tg_id=tg_id)


@app.get('/find_driver')
async def find_driver_for_passenger(passenger_tg_id: int) -> List[Driver]:
    ...


if __name__ == '__main__':
    uvicorn.run('app:app', reload=True)
