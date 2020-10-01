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


@app.get("/user/{username}/")
def get_user(username, db: Session = Depends(get_db)):
    return crud.user_get(username, db)


@app.post("/user/login/", response_model=schemas.User)
def user_login(user: schemas.UserBasic, db: Session = Depends(get_db)):
    return crud.get_user_username(db, username=user.username, password=user.password)


@app.put("/user/{username}/")
def user_edit(username, user: schemas.UserInDB, db: Session = Depends(get_db)):
    return crud.edit_user(db, user, username)


@app.post("/author/{username}/")
def add_author(username, author: schemas.AuthorBase, db: Session = Depends(get_db)):
    return crud.new_author(db=db, author=author, username=username)


@app.put("/author/{author_id}/{username}/")
def author_edit(author: schemas.AuthorBase, author_id, username, db: Session = Depends(get_db)):
    return crud.author_edit(db, author_id, username, author)


@app.get("/author/{author_id}/{username}/")
def author_get_one(author_id, username, db: Session = Depends(get_db)):
    return crud.get_one_author(db, author_id, username)


@app.get("/author/{username}/")
def author_get(username, db: Session = Depends(get_db)):
    return crud.get_authors(db, username)


@app.delete("/author/{author_id}/{username}/")
def remove_author(author_id, username, db: Session = Depends(get_db)):
    return crud.delete_author(db, username, author_id)


@app.post("/publisher/{username}/")
def add_publisher(username, publisher: schemas.PublisherBase, db: Session = Depends(get_db)):
    return crud.new_publisher(db, username, publisher)


@app.put("/publisher/{pub_id}/{username}/")
def publisher_edit(pub_id, username, publisher: schemas.PublisherBase, db: Session = Depends(get_db)):
    return crud.edit_publisher(db, username, publisher, pub_id)


@app.get("/publisher/{username}/")
def publisher_get(username, db: Session = Depends(get_db)):
    return crud.get_publishers(username, db)


@app.get("/publisher/{pub_id}/{username}/")
def publisher_get_one(pub_id, username, db: Session = Depends(get_db)):
    return crud.get_one_publisher(username, pub_id, db)


@app.delete("/publisher/{pub_id}/{username}/")
def remove_publisher(pub_id, username, db: Session = Depends(get_db)):
    return crud.delete_publisher(pub_id, username, db)


@app.post("/shelf/{username}/")
def add_shelf(username, shelf: schemas.ShelfBase, db: Session = Depends(get_db)):
    return crud.new_shelf(username, shelf, db)


@app.get("/shelf/{username}/")
def shelf_get(username, db: Session = Depends(get_db)):
    return crud.get_shelf(username, db)


@app.get("/shelf/{shelf_id}/{username}/")
def shelf_get_one(shelf_id, username, db: Session = Depends(get_db)):
    return crud.get_one_shelf(shelf_id, username, db)


@app.put("/shelf/{shelf_id}/{username}/")
def shelf_edit(shelf_id, username, shelf: schemas.ShelfBase, db: Session = Depends(get_db)):
    return crud.edit_shelf(shelf_id, username, shelf, db)


@app.delete("/shelf/{shelf_id}/{username}/")
def shelf_remove(shelf_id, username, db: Session = Depends(get_db)):
    return crud.delete_shelf(shelf_id, username, db)


@app.post("/book/{username}/{pub_id}/")
def add_book_base(username, pub_id, book: schemas.BookBase, db: Session = Depends(get_db)):
    return crud.new_book_base(username, pub_id, book, db)


@app.post("/book_author/{book_id}/")
def add_book_author(book_id, author: List[int], db: Session = Depends(get_db)):
    return crud.add_book_author(book_id, author, db)


@app.post("/book_shelf/{book_id}/")
def add_book_shelf(book_id, shelf: List[int], db: Session = Depends(get_db)):
    return crud.add_book_shelf(book_id, shelf, db)


@app.delete("/book/{book_id}/")
def book_remove(book_id, db: Session = Depends(get_db)):
    return crud.remove_book(book_id, db)


@app.get("/books/{username}/")
def user_books(username, db: Session = Depends(get_db)):
    return crud.get_user_books(username, db)


@app.get("/book_author/{bid}/")
def get_book_authors(bid, db: Session = Depends(get_db)):
    return crud.get_book_author(bid, db)


@app.get("/publisher/{pub_id}/{username}/")
def get_book_publisher(pub_id, username, db: Session = Depends(get_db)):
    return crud.get_book_publisher(pub_id, username, db)


@app.post("/review/{username}/{bid}/")
def send_review(username, bid, review: schemas.ReviewBase, db: Session = Depends(get_db)):
    return crud.add_a_review(username, bid, review, db)


@app.get("/review/{username}/{bid}/")
def all_book_reviews(username, bid, db: Session = Depends(get_db)):
    return crud.get_review(username, bid, db)


@app.get("/book_rating/{bid}/")
def get_book_rating(bid, db: Session = Depends(get_db)):
    return crud.get_rating(bid, db)


@app.get("/books/")
def get_all_books(db: Session = Depends(get_db)):
    return crud.get_non_private_books(db)


@app.put("/book_lend/{bid}/{username}/")
def lend_a_book(bid, username, db: Session = Depends(get_db)):
    return crud.lend_a_book(bid, username, db)


@app.get("/all_lent_books/{username}/")
def get_lent_books(username, db: Session = Depends(get_db)):
    return crud.get_lent_books(username, db)


@app.put("/return_book/{bid}")
def return_a_book(bid, db:Session=Depends(get_db)):
    return crud.return_a_book(bid, db)


@app.get("/shelf_book/{username}/{sid}/")
def get_shelf_books(username, sid, db:Session=Depends(get_db)):
    return crud.get_shelf_books(username, sid, db)

app.mount("/static", StaticFiles(directory="./Bookshelf/static"))
