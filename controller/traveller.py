from sqlalchemy.orm import Session
from fastapi import HTTPException,Depends,UploadFile,File,Form
from model.traveller import User,Profile
from schema.traveller import User1,Update_Date
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer


pwd_context = CryptContext(
    schemes=["argon2", "bcrypt", "pbkdf2_sha256"],
    default="argon2",
    deprecated="auto"
)
secu=OAuth2PasswordBearer(tokenUrl="/login")

def hash_password(password: str):
    return pwd_context.hash(password)
def veryfiy_password(password:str, plan_password:str):
    return pwd_context(password,plan_password)

def create_user(data: User1, db: Session):


    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")


    if len(data.password) < 8:
        raise HTTPException(status_code=400, detail="Password must be at least 8 characters")

    

    new_user = User(
        username=data.username,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=hash_password(data.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}



def get_all(db:Session):
    user=db.query(User).all()
    return user



def Update_register_user(user_id: int, user_data: Update_Date, db: Session):
    user_update = db.query(User).filter(User.id == user_id).first()
    if not user_update:
        raise HTTPException(status_code=404, detail="not valid user id")

    users_data = user_data.dict(exclude_unset=True)
    for key, value in users_data.items():
        setattr(user_update, key, value)

    db.commit()
    db.refresh(user_update)
    return user_update


def delete_register_user(user_id:int,db:Session):
    user_delete=db.query(User).filter(User.id==user_id).first()
    if not user_delete:
        raise HTTPException(status_code=404,detail="not valid user id")
    db.delete(user_delete) 
    db.commit()
    return user_delete


def auth(db:Session,email:str,password:str):
    users=db.query(User).filter(User.email==email).first()
    if not users:
        return False
    
    very=pwd_context.verify(password,users.password)
    if not very:
        return False
    return users




############ TOKEN ################


from typing import Optional
from datetime import timedelta,datetime
from jose import jwt , JWTError
from database import get_db

EXPIRY=24*60
SECRET_KEY="hello"
ALGORITHM="HS256"

def  Create_token(data:dict,expriy:Optional[timedelta]=None):
    user_data= data.copy()
    if expriy:
        expriy=datetime.utcnow()+expriy
    else:
        expriy=datetime.utcnow()+ timedelta(seconds=EXPIRY)
    user_data.update({"exp":expriy})
    token=jwt.encode(user_data,SECRET_KEY,algorithm=ALGORITHM)
    return token

def get_token(user_data:Update_Date,db:Session=Depends(get_db)):
    user=auth(db,user_data.email,user_data.password)
    if not user:
        raise HTTPException(status_code=404,detail="not valid user email,passowrd")
    users=Create_token(data={"sub":str(user.id)},expriy=timedelta(seconds=EXPIRY))
    return users
    
def valid_token(token:str=Depends(secu),db:Session=Depends(get_db)):
    cer=HTTPException(status_code=400,detail=" not valid details ")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        user_id=payload.get("sub")
        if user_id is None:
             return cer
    except JWTError:
        return cer
    user_check=db.query(User).filter(User.id==int(user_id)).first()
    if  user_check is None:
        raise HTTPException(status_code=404,detail="not valid user id ")
    return user_check


blacklisted_tokens = set()

def logout(token: str):
    blacklisted_tokens.add(token)
    print("//////////////////////////",blacklisted_tokens)
    
    return {"message": "Logout successful",
            "token":blacklisted_tokens}
    

MAX_IMAGE_SIZE = 4 * 1024 * 1024  
ALLOWED_CONTENT_TYPES = ["image/png", "image/jpeg", "image/jpg", "image/gif"]

async def create_profile_register(
    file: UploadFile = File(...),
    bio: str = Form(...),
    description: str = Form(...),
    traveller_id: int = Form(...),
    phone: str = Form(...),
    db: Session = Depends(get_db)
):
    
    register_profile = db.query(Profile).filter(Profile.traveller_id == traveller_id).first()
    if  register_profile:
        raise HTTPException(status_code=404, detail="Traveller ID not found")

    
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Invalid image type")


    if len(content) > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image size must be less than 4MB")

    profile = Profile(
        bio=bio,
        description=description,
        traveller_id=traveller_id,
        content_type=file.content_type,
        phone=phone,
        image=content,
        file_name=file.filename
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return {
        "message": "Image uploaded successfully",
        "filename": profile.file_name,
        "size": len(content),
        "content_type": profile.content_type
    }




    
from fastapi.responses import StreamingResponse
import io
def get_prfile_image(profile_id:int,db:Session):
    user=db.query(Profile).filter(Profile.id==profile_id).first()
    if not user :
        raise HTTPException(status_code=404,detail="not valid user profile_id")
    if not user.image:
        raise HTTPException(status_code=404,detail="not valid user")
    return  StreamingResponse(io.BytesIO(user.image),media_type=user.content_type)


def delete_profile(id:int,db:Session):
    userdelete=db.query(Profile).filter(Profile.id==id).first()
    if  userdelete:
        raise HTTPException(status_code=404,detail="not valid user image ")
    db.delete(userdelete)
    db.commit()
    return{
        "message":"your data delete"
    }