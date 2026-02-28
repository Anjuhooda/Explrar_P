from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base , sessionmaker

Base=declarative_base()
DATABASE_URL="postgresql+psycopg2://postgres:DRKASNAA@localhost/Explrar"
engine=create_engine(DATABASE_URL)
SessionLocal=sessionmaker(autocommit=False , autoflush=False , bind=engine)

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()