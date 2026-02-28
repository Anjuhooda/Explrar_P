from database import Base
from sqlalchemy import Column, Integer, String, DateTime,LargeBinary,ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

class User(Base):
    __tablename__ = "usertraveller"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
    profile=relationship("Profile",back_populates="traveller")
    bookings=relationship("Booking",back_populates="traveller")


class Profile(Base):
    __tablename__="profile_image"
    id = Column(Integer, primary_key=True, index=True)
    traveller_id = Column(Integer, nullable=False)
    bio = Column(String, nullable=True)
    description = Column(String, nullable=True)  
    phone = Column(String, nullable=True)
    file_name = Column(String, nullable=True)
    content_type = Column(String, nullable=True)
    image = Column(LargeBinary)
    
    traveller_id=Column(Integer,ForeignKey("usertraveller.id"))
    traveller=relationship("User",back_populates="profile")