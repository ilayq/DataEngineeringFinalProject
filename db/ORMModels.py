from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey, PrimaryKeyConstraint


Base = declarative_base()


class UserORM:
    tg_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False) 
    rating = Column(Float, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)


class PassengerORM(Base, UserORM):
    __tablename__ = 'passengers'


class DriverORM(Base, UserORM):
    __tablename__ = 'drivers'

    places = Column(Integer, nullable=False)


class BusStationORM(Base):
    __tablename__ = 'bus_stations'

    station_id = Column(Integer)
    person_tg_id = Column(Integer, ForeignKey('passengers.tg_id',
                                               ondelete='cascade',
                                               onupdate='cascade'),
                                    ForeignKey('drivers.tg_id',
                                               ondelete='cascade',
                                               onupdate='cascade'))
    PrimaryKeyConstraint(station_id, person_tg_id)
