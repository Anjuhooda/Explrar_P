from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from schema.traveller import UserA,Update_Date
from database import get_db
from controller.traveller import create_user,get_all,Update_register_user,delete_register_user,get_token,valid_token,logout,create_profile_register,get_prfile_image

router = APIRouter()

@router.post("/create")
def user_create(data: UserA, db: Session = Depends(get_db)):
    return create_user(data, db)

@router.get("/get")
def get_all_traveller(db:Session=Depends(get_db)):
    return get_all(db)


@router.put("/update")
def Update_register(user_id: int, user_date: Update_Date, db: Session = Depends(get_db)):
    return Update_register_user(user_id, user_date, db)

@router.delete("/deleteregister")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    return  delete_register_user(user_id,db)


@router.post("/login")
def login_with_token(login_in:Update_Date,db:Session=Depends(get_db)):
    token=get_token(login_in,db)
    return {
        "token" :token
    }



@router.post("/logout")
def logout_Register(token:str=Depends(valid_token)):
    return logout(token)




from fastapi import File,UploadFile,Form
@router.post("/creatprofile")
async def Profile_create(file:UploadFile=File(...),
                   bio:str=Form(...),
                   discription:str=Form(...),
                    register_id:int=Form(...),
                    phone:str=Form(...),
                    db:Session=Depends(get_db)):
    return  await  create_profile_register(file,bio,discription,register_id,phone,db)


@router.get("/get image")
def get_register_image(profile_id:int,db:Session=Depends(get_db)):
    return get_prfile_image (profile_id,db)

@router.delete("/delete profile")
def delete_profile(id:int,db:Session=Depends(get_db)):
    return (id,db)