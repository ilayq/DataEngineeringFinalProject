import uvicorn
import fastapi
from shemas import Driver, Passenger
from typing import Union, List


app = fastapi.FastAPI()


@app.post('/user')
async def add_user(user: Union[Driver, Passenger]):
    if isinstance(user, Driver):
        return {"msg": "driver"}
    else:
        return {"msg": "passenger"}
    ...


@app.patch('/user')
async def patch_user(user: Union[Driver, Passenger]):
    ...


@app.get('/user')
async def get_user_data(tg_id: int) -> Union[Driver, Passenger]:
    ...


@app.get('/find_driver')
async def find_driver_for_passenger(passenger_tg_id: int) -> List[Driver]:
    ...


if __name__ == '__main__':
    uvicorn.run('server:app', reload=True)
