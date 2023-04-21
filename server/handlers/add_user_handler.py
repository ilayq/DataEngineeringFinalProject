import os, sys

sys.path.append(fr'C:\Users\{os.getlogin()}\de_project')

from sqlalchemy.orm import Session

from db import BusStationORM, engine, DriverORM, PassengerORM
from server.shemas import Driver, Passenger
from typing import Union


async def add_user_handler(user: Union[Driver, Passenger]) -> bool:
    bus_stations = user.bus_stations
    dicted_user = user.dict()
    del dicted_user['bus_stations']
    print(f'\n\n\{isinstance(user, Driver)}\n\n {user.__class__}\n\n')
    with Session(engine) as db:
        if "places" in dicted_user:     
            db.add(DriverORM(**dicted_user))
        else:
            db.add(PassengerORM(**dicted_user))
        db.commit()
        db.close()
    user_tg_id = user.tg_id
    with Session(engine) as db:
        for station_id in bus_stations:
            db.add(BusStationORM(station_id=station_id,
                                 person_tg_id=user_tg_id))
        db.commit()
        db.close()
    return True
