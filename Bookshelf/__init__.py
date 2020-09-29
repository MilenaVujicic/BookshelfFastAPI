from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from typing import List

from .db import crud, models, schemas
from .db.database import SessionLocal, engine
from .db.schemas import User

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserInDB, db: Session = Depends(get_db)):
    return crud.creat_user(db=db, user=user)


@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return crud.get_all_users(db=db)


@app.post("/user/login/", response_model=schemas.User)
def user_login(user: schemas.UserBasic, db: Session = Depends(get_db)):
    return crud.get_user_username(db, username=user.username, password=user.password)


@app.post("/author/{username}/")
def add_author(username, author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.new_author(db=db, author=author, username=username)


@app.put("/author/{author_id}/{username}/")
def author_edit(author: schemas.AuthorBase, author_id, username, db: Session = Depends(get_db)):
    return crud.author_edit(db, author_id, username, author)


@app.get("/author/{author_id}/{username}/")
def author_get_one(author_id, username, db: Session= Depends(get_db)):
    return crud.get_one_author(db, author_id, username)


@app.get("/author/{username}/")
def author_get(username, db: Session = Depends(get_db)):
    return crud.get_authors(db, username)


@app.delete("/author/{author_id}/{username}/")
def remove_author(username, author_id, db:Session= Depends(get_db)):
    return crud.delete_author(db, username, author_id)


@app.post("/publisher/{username}/")
def add_publisher(username,publisher:schemas.PublisherBase, db:Session= Depends(get_db)):
    return crud.new_publisher(db, username, publisher)


@app.put("/publisher/{pub_id}/{username}/")
def publisher_edit(pub_id, username, publisher:schemas.PublisherBase, db:Session=Depends(get_db)):
    return crud.edit_publisher(db, username, publisher, pub_id)


@app.get("/publisher/{username}/")
def publisher_get(username, db:Session=Depends(get_db)):
    return crud.get_publishers(username, db)


@app.get("/publisher/{pub_id}/{username}/")
def publisher_get_one(pub_id, username, db:Session=Depends(get_db)):
    return crud.get_one_publisher(username, pub_id, db)


@app.delete("/publisher/{pub_id}/{username}/")
def remove_publisher(pub_id, username, db:Session=Depends(get_db)):
    return crud.delete_publisher(pub_id, username, db)


app.mount("/static", StaticFiles(directory="./Bookshelf/static"))
