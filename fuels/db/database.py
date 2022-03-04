from sqlalchemy import create_engine, Column, String, Boolean, \
    DateTime, ForeignKey, exists, func, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Integer, Enum

from geoalchemy2 import Geometry, func as geofunc
from geoalchemy2.shape import to_shape

import enum
from .settings import DB_URL

# Configure a Session class.
Session = sessionmaker()

# Create an engine which the Session will use for connections.
engine = create_engine(DB_URL)

# Create a configured Session class.
Session.configure(bind=engine)

# Create a Session
session = Session()

# Create a base for the models to build upon.
Base = declarative_base()


class FuelType(enum.Enum):
    DP = 1
    GAS = 2
    A95 = 3
    A92 = 4

class Station(Base):
    __tablename__ = "stations"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    company = Column(String, nullable=False)
    address = Column(String, nullable=True)
    telephone = Column(String, nullable=True)
    coordinates = Column(Geometry('POINT'), nullable=False)

    def get_human_coordinates(self):
        return to_shape(self.coordinates)

    def exists(self):
        return session.query(exists().where(
            Station.id == self.id)).scalar()

    def commit(self):
        session.add(self)
        session.commit()

    def __repr__(self):
        return "<Station (id='%i', name='%s', company='%s', company='%s', telephone='%s', coordinates='%s')>" % (
            self.id, self.name, self.company, self.address, self.telephone, to_shape(self.coordinates)
        )

class Status(Base):
    __tablename__ = "statuses"

    id = Column(Integer, primary_key=True)
    station_id = Column(Integer, ForeignKey("stations.id"))
    date = Column(DateTime, nullable=False)
    fuel_type = Column(Enum(FuelType), nullable=False)
    is_avail = Column(Boolean)

    def exists(self):
        return session.query(exists().where(
            Status.id == self.id)).scalar()


    def commit(self):
        session.add(self)
        session.commit()