from pydantic import BaseModel , EmailStr
from typing import Optional

class User1(BaseModel):
    username:str
    firstname:str
    lastname:str
    email:EmailStr
    password:str

class Data_Update(BaseModel):
    email:Optional[str]=None
    password:Optional[str]=None