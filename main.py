from fastapi import FastAPI
from database import Base , engine
from router.car_router import router as car_router
from router.traveller import router as traveller_router
from router.car_router import router as bookingcar

app=FastAPI
Base.metabase.create_all(bind=engine)

app.include_router(car_router)
app.include_router(traveller_router)
app.include_router(bookingcar)