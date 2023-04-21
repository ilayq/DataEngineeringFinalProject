from pydantic import BaseModel
from datetime import time, datetime
from typing import List


def string_to_time_encoder(date: str) -> time:
    print(datetime.strptime(date, "%H:%M").time())
    return datetime.strptime(date, "%H:%M").time()


class User(BaseModel):
    tg_id: int
    name: str
    start_time: time
    end_time: time
    bus_stations: List[int]
    rating: float

    class Config:
        # json_encoders = {
        #     time: string_to_time_encoder
        # }
        orm_mode = True


class Driver(User):
    places: int

class Passenger(User):
    pass