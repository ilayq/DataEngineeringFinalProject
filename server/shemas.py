from pydantic import BaseModel, validator
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
        validate_assignment = True

    @validator("end_time")
    def validate_time(cls, v, values):
        assert v > values["start_time"] 
        return v


class Driver(User):
    places: int

class Passenger(User):
    pass

if __name__ == '__main__':
    dr = Driver(
        tg_id=1,
        name='asd',
        start_time=time(hour=1, minute=2),
        end_time=time(hour=1, minute=3),
        bus_stations=[1,2,3],
        rating=1.2,
        places=1
    )
    print(dr)