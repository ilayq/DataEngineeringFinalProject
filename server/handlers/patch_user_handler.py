import os, sys

sys.path.append(fr'C:\Users\{os.getlogin()}\de_project')

from sqlalchemy.orm import Session
from sqlalchemy import update, delete, and_

from db import BusStationORM, engine, DriverORM, PassengerORM
from server.shemas import Driver, Passenger
from typing import Union
from .get_user_data_handler import get_stations_by_user_tg_id


async def patch_user_handler(user: Union[Driver, Passenger]) -> bool:
    user_tg_id = user.tg_id
    # old_user_data = get_user_data_handler(user_tg_id)
    # new
    new_params = user.dict()
    new_bus_stations = set(new_params["bus_stations"])
    del new_params["bus_stations"]
    if "places" in user.dict():
        # class Driver detected
        q = update(DriverORM).where(DriverORM.tg_id == user_tg_id).values(new_params)
    else:
        # class Passenger detected
        q = update(PassengerORM).where(PassengerORM.tg_id == user_tg_id).values(new_params)

    # updating all user data except bus_stations
    with engine.connect() as db:
        db.execute(q)
        db.commit()
        db.close()
    
    current_bus_stations = set(await get_stations_by_user_tg_id(user_tg_id))

    stations_to_add = new_bus_stations - current_bus_stations
    stations_to_delete = current_bus_stations - new_bus_stations

    with engine.connect() as db:
        for station in stations_to_delete:
            delete_q = delete(BusStationORM).where(and_(BusStationORM.station_id == station,
                                                        BusStationORM.person_tg_id == user_tg_id))
            db.execute(delete_q)
        db.commit()
        db.close()

    with Session(engine) as db:
        for station in stations_to_add:
            db.add(BusStationORM(station_id=station,
                                 person_tg_id=user_tg_id))
        db.commit()
        db.close()
    return True
