from pydantic import BaseModel
from typing import Optional
from datetime import date , time

class CarA(BaseModel):
    car_name:str
    seats:int
    p_p_km:int

class Update_car(BaseModel):
    seats:Optional[str]=None
    P_p_km:Optional[int]=None

class boookingA(BaseModel):
    traveller_id:int
    car_id:int
    pickup_date:date
    pickup_time:time
    status:int
    passenger:int