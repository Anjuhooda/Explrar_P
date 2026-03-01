from database import Base
from sqlalchemy import Column , Integer , String , DateTime , ForeignKey , Boolean , Time , Date
from sqlalchemy.orm import relationship,mapped_column,Mapped
from datetime import datetime,date,time


class Car(Base):
    __tablename__="car"
    car_id=Column(Integer,primary_key=True)
    car_name=Column(String,nullable=False)
    seats=Column(Integer,nullable=False)
    price_per_km=Column(Integer,nullable=False)
    available=Column(Boolean,nullable=False)
    bookings=relationship("Booking",back_populates="cars")
    
    
class Booking (Base):
    __tablename__="booking"
    id=Column(Integer,primary_key=True,index=True)
    traveller_id=Column(Integer,ForeignKey("usertraveller.id"))
    car_id=Column(Integer,ForeignKey("car.car_id"))
    # pickup_date=Column(date)
    # pickup_time=Column(time)
    pickup_date: Mapped[date] = mapped_column(Date, nullable=False)
    pickup_time: Mapped[time] = mapped_column(Time, nullable=False)

    status=Column(Integer)
    passenger=Column(Integer)
    created_at=Column(DateTime,default=datetime.now)
     
     
    traveller=relationship("User",back_populates="bookings")
    cars=relationship("Car",back_populates="bookings")