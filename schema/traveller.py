from pydantic import BaseModel , EmailStr
from typing import Optional

class UserA(BaseModel):
    username:str
    firstname:str
    lastname:str
    email:EmailStr
    password:str

class Data_Update(BaseModel):
    email:Optional[str]=None
    password:Optional[str]=None