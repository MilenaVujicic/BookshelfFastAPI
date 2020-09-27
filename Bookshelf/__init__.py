from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles

from sqlalchemy.orm import Session

from .db import crud, models, schemas
from .db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.creat_user(db=db, user=user)


app.mount("/static", StaticFiles(directory="./Bookshelf/static"))