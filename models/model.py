
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
db = SQLAlchemy()
Base = declarative_base()

# Classes for tables. Here you define the structure for the database, the datatypes etc

class City(Base):

    __tablename__ = 'cities'

    city_id = Column(Integer, primary_key=True)
    city = Column(String)


class Coordinate(Base):

    __tablename__ = 'coordinates'
    coordinate_id = Column(Integer, primary_key=True, autoincrement=True)
     
    datetime = Column(DateTime, default=datetime.utcnow)
    latitude = Column(Float)
    longitude = Column(Float)
    weight = Column(Float)
    city_id = Column(Integer, ForeignKey('cities.city_id'))