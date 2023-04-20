from pydantic import BaseModel
from datetime import time
from typing import List


class User(BaseModel):
    tg_id: int
    name: str
    start_time: time
    end_time: time
    bus_stations: List[int]
    rating: float


class Driver(User):
    places: int

if __name__ == '__main__':
    dr = Driver(
        tg_id=1,
        name='asd',
        start_time=time(hour=1, minute=2),
        end_time=time(hour=1, minute=2),
        bus_stations=[1,2,3],
        rating=1.2,
        places=1
    )
    print(dr)