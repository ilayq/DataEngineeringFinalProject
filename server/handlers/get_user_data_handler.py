import os, sys

sys.path.append(fr'C:\Users\{os.getlogin()}\de_project')

from sqlalchemy.orm import Session
from sqlalchemy import select

from db import BusStationORM, engine, DriverORM, PassengerORM
from server.shemas import Driver, Passenger
from typing import Union


async def get_stations_by_user_tg_id(tg_id: int) -> list[int]:
    q = select(BusStationORM.station_id).where(BusStationORM.person_tg_id == tg_id)
    with engine.connect() as db:
        for row in db.execute(q):
            yield row[0]


async def get_user_data_handler(tg_id: int) -> Union[Driver, Passenger]:
    with Session(engine) as db:
        q = select(DriverORM).where(DriverORM.tg_id == tg_id)
        driver_response = db.execute(q).fetchone()
    bus_stations = [_ async for _ in get_stations_by_user_tg_id(tg_id)]
    
    if driver_response:
        driver_response[0].bus_stations = bus_stations
        return Driver.from_orm(driver_response[0])
    
    with Session(engine) as db:
        q = select(PassengerORM).where(PassengerORM.tg_id == tg_id)
        passenger_response = db.execute(q).fetchone()
    passenger_response[0].bus_stations = bus_stations
    return Passenger.from_orm(passenger_response[0])
