from fastapi import HTTPException
from schema.car_schema import Car1,Update_car,Boooking1
from model.car_model import Car,Booking
from sqlalchemy.orm import Session

def create_car(data:Car1,db:Session):
    user= db.query(Car).filter(Car.car_name==data.car_name).first()
    if user:
        raise  HTTPException(status_code=404,detail="Not valid carname")
    traveller_car=Car(
        car_name=data.car_name,
        p_p_km=data.p_p_km,
        seats=data.seats,  
    )
    db.add(traveller_car)
    db.commit()
    db.refresh(traveller_car)
    return traveller_car

def delete_car_data(id:int,db:Session):
    car_traveller=db.query(Car).filter(Car.car_id==id).first()
    if not car_traveller:
        raise HTTPException(status_code=404,detail="not valid user carid ")
    db.delete(car_traveller)
    db.commit()
    return{
        "message":"Your Car data Delete"
    }
    
def get_all_cars(db:Session):
    cars=db.query(Car).all()
    if not cars:
        raise HTTPException(status_code=404,detail="not valid car data is available")
    return cars

def get_car_by_id(id:int,db:Session):
    carsGet=db.query(Car).filter(Car.car_id ==id).first()
    if not carsGet:
        raise HTTPException(status_code=404,detail="not valid car id ")
    return carsGet

def Uptade_car_data(id:int,data:Update_car,db:Session):
    update_car=db.query(Car).filter(Car.car_id==id).first()
    if not update_car:
        raise HTTPException(status_code=404,detail="not valid car id ")
    update_car= update_car.dict(exclude_unset=True)
    for key,value in update_car.items():
        setattr(update_car,key,value)
    db.commit()
    db.refresh(update_car)
    return update_car


from model.traveller import User
from datetime import datetime

def  booking_car(data:Booking1,db:Session):
    traveller_booking=db.query(User).filter(User.id==data.traveller_id).first()
    if not traveller_booking:
        raise HTTPException(status_code=404,detail="not valid user travller ")
    traveller_bookings=db.query(Car).filter(Car.car_id==data.car_id).first()
    if not traveller_bookings:
        raise HTTPException(status_code=404,detail="not valid car id ")
    # now=datetime.now()
    if not traveller_bookings.available:
        raise HTTPException(status_code=400,detail= "Car is already booked")
    if data.passenger < traveller_bookings.seats:
        raise HTTPException(status_code=404,detail="not valid passenger seats in this car")
    traveller_booking=Booking(
        traveller_id=data.traveller_id,
        car_id=data.car_id,
        status=data.status,
        pickup_date=data.pickup_date
        ,pickup_time=data.pickup_time,
        passenger=data.passenger
    )
    traveller_bookings.available =False
    db.add(traveller_booking)
    db.commit()
    db.refresh(traveller_booking)
    return traveller_booking

    

def booking_cancal(id:int,car_id:int,db:Session):
    delete_booking=db.query(Booking).filter(Booking.id==id).first()
    if not delete_booking:
        raise HTTPException(status_code=404,detail="not valid user booking id ")
    car = db.query(Car).filter(Car.car_id == car_id).first()

    if car:
        car.available = True  
    db.delete(delete_booking)
    db.commit()
    return {
        "message":"Not valid :"
    }