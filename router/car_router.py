from fastapi import APIRouter,Depends
router=APIRouter()
from sqlalchemy.orm import Session
from schema.car_schema import CarA,Update_car,bookingA
from database import get_db

from controller.car_controller import create_car,delete_car_data,get_all_cars,get_car_by_id,Uptade_car_data,booking_car,booking_cencle
@router.post("/carcreate")
def car_add_create(car_data:CarA,
    db:Session=Depends(get_db)):
    return create_car(car_data,db)

@router.delete("/cardelet")
def remove_car_data(id:int,db:Session=Depends(get_db)):
    return delete_car_data (id,db)

@router.get("/getcar")
def car_getting(db:Session=Depends(get_db)):
    return get_all_cars(db)

@router.get("/getbyid")
def getById(id:int,db:Session=Depends(get_db)):
    return get_car_by_id(id,db)

@router.put("/update")
def update_car_date(id:int,data:Update_car,db:Session=Depends(get_db)):
    return   Uptade_car_data(id,db,data)


@router.post("/booking")
def booking_cars(data:bookingA,db:Session=Depends(get_db)):
    return booking_car(data,db)

@router.delete("/removebooking")
def cancle_booking(id:int,car_id:int,db:Session=Depends(get_db)):
    return  booking_cencle(id,car_id,db)