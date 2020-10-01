from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
import base64
from fastapi import File, UploadFile
from typing import Optional, List

SECRET_KEY = "4f3eafb12616c4b12ef8678600edc59f60049eba7afc9deb566b9bd7790007d3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_all_users(db: Session):
    return db.query(models.User)


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_username(db: Session, username: str, password: str):
    user_db = db.query(models.User).filter(models.User.username == username).first()
    if verify_password(password, user_db.password):
        return user_db


def creat_user(db: Session, user: schemas.UserInDB):
    pw = get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, password=pw, first_name=user.first_name,
                          last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def edit_user(db: Session, user: schemas.UserInDB, username: str):
    user_db = db.query(models.User).filter(models.User.username == username).first()
    user_db.username = user.username
    user_db.email = user.email
    user_db.first_name = user.first_name
    user_db.last_name = user.last_name
    db.commit()
    return user_db


def user_get(username: str, db: Session):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    return db_user


def new_author(db: Session, author: schemas.AuthorBase, username: str):
    owner = db.query(models.User).filter(models.User.username == username).first()
    db_author = models.Author(name=author.name, surname=author.surname, owner_id=owner.id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def author_edit(db: Session, author_id: int, username: str, author: schemas.AuthorBase):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    db_author.surname = author.surname
    db_author.name = author.name
    db.commit()
    return db_author


def get_one_author(db: Session, author_id: int, username: str):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    return db_author


def get_authors(db: Session, username: str):
    owner = db.query(models.User).filter(models.User.username == username).first()
    db_authors = db.query(models.Author).filter(models.Author.owner_id == owner.id).all()
    return db_authors


def delete_author(db: Session, username: str, author_id: int):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    db_author.author_books = []
    db.commit()
    db.refresh(db_author)
    db.delete(db_author)
    db.commit()


def new_publisher(db: Session, username: str, publisher: schemas.PublisherBase):
    owner = db.query(models.User).filter(models.User.username == username).first()
    db_publisher = models.Publisher(name=publisher.name, owner_id=owner.id)
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


def edit_publisher(db: Session, username: str, publisher: schemas.PublisherBase, pub_id: int):
    db_pub = db.query(models.Publisher).filter(models.Publisher.id == pub_id).first()
    db_pub.name = publisher.name
    db.commit()
    return db_pub


def get_publishers(username: str, db: Session):
    owner = db.query(models.User).filter(models.User.username == username).first()
    db_publishers = db.query(models.Publisher).filter(models.Publisher.owner_id == owner.id).all()

    return db_publishers


def get_one_publisher(username: str, pub_id: int, db: Session):
    db_publisher = db.query(models.Publisher).filter(models.Publisher.id == pub_id).first()
    return db_publisher


def delete_publisher(pub_id: int, username: str, db: Session):
    db_publisher = db.query(models.Publisher).filter(models.Publisher.id == pub_id).first()
    db_publisher.publisher_books = []
    db.commit()
    db.refresh(db_publisher)
    db.delete(db_publisher)
    db.commit()


def new_shelf(username: str, shelf: schemas.ShelfBase, db: Session):
    owner = db.query(models.User).filter(models.User.username == username).first()
    db_shelf = models.Shelf(name=shelf.name, description=shelf.description, owner_id=owner.id)
    db.add(db_shelf)
    db.commit()
    db.refresh(db_shelf)
    return db_shelf


def get_shelf(username: str, db: Session):
    owner = db.query(models.User).filter(models.User.username == username).first()
    shelves = db.query(models.Shelf).filter(models.Shelf.owner_id == owner.id).all()
    return shelves


def get_one_shelf(shelf_id: int, username: str, db: Session):
    db_shelf = db.query(models.Shelf).filter(models.Shelf.id == shelf_id).first()
    return db_shelf


def edit_shelf(shelf_id: int, username: str, shelf: schemas.ShelfBase, db: Session):
    db_shelf = db.query(models.Shelf).filter(models.Shelf.id == shelf_id)
    db_shelf.name = shelf.name
    db_shelf.description = shelf.description
    db.commit()
    return db_shelf


def delete_shelf(shelf_id: int, username: str, db: Session):
    db_shelf = db.query(models.Shelf).filter(models.Shelf.id == shelf_id).first()
    db_shelf.shelf_books = []
    db.commit()
    db.refresh(db_shelf)
    db.delete(db_shelf)
    db.commit()


def new_book_base(username: str, pub_id: int, book: schemas.BookBase, db: Session):
    book_owner = db.query(models.User).filter(models.User.username == username).first()
    book_publisher = db.query(models.Publisher).filter(models.Publisher.id == pub_id).first()

    db_book = models.Book(title=book.title, pages=book.pages, description=book.description,
                          isbn=book.isbn, read=book.read, lent=book.lent, private=book.private,
                          owner=book_owner.id, publisher=book_publisher.id)
    db.add(db_book)

    db.commit()
    db.refresh(db_book)
    format, imgstr = book.cover.split(';base64,')
    ext = format.split('/')[-1]
    name = username + str(db_book.id) + '.' + ext
    path = "./Bookshelf/static/" + name
    with open(path, 'wb') as f:
        f.write(base64.b64decode(imgstr))
        f.close()

    db_book.cover = path[12:]
    db.commit()
    db.refresh(db_book)
    return db_book


def add_book_author(book_id: int, author: List[int], db: Session):
    book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
    for id in author:
        author_db = db.query(models.Author).filter(models.Author.id==id).first()
        book_db.book_authors.append(author_db)

    db.commit()
    db.refresh(book_db)
    return book_db


def add_book_shelf(book_id: int, shelf: List[int], db: Session):
    book_db = db.query(models.Book).filter(models.Book.id==book_id).first()
    for id in shelf:
        shelf_db = db.query(models.Shelf).filter(models.Shelf.id==id).first()
        book_db.book_shelves.append(shelf_db)

    db.commit()
    db.refresh(book_db)
    return book_db


def remove_book(book_id: int, db: Session):
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    book.book_authors = []
    book.book_shelves = []
    db.commit()
    db.refresh(book)
    db.delete(book)
    db.commit()


def get_user_books(username:str, db:Session):
    owner = db.query(models.User).filter(models.User.username==username).first()

    db_books = db.query(models.Book).filter(models.Book.owner==owner.id).all()

    return db_books


def get_book_author(book_id:int, db:Session):
    db_book = db.query(models.Book).filter(models.Book.id==book_id).first()
    authors = []
    for a in db_book.book_authors:
        authors.append(a)

    return authors


def get_book_publisher(pub_id:int, username:str, db:Session):
    db_publisher = db.query(models.Publisher).filter(models.Publisher.id==pub_id).first()

    return db_publisher


def add_a_review(username:str, bid:int, review:schemas.ReviewBase, db:Session):
    owner = db.query(models.User).filter(models.User.username==username).first()
    book = db.query(models.Book).filter(models.Book.id==bid).first()

    db_review = models.Review(rating=review.rating, content=review.content, reviewer_id=owner.id,
                              book_id=book.id)

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


def get_review(username:str, bid:int, db:Session):
    reviews = db.query(models.Review).filter(models.Review.book_id==bid).all()

    return reviews


def get_rating(bid:int, db:Session):
    book = db.query(models.Book).filter(models.Book.id==bid).first()
    reviews = book.book_reviews

    avg_val = 0

    for r in reviews:
        avg_val += r.rating

    if len(reviews) > 0:
        avg_val = avg_val/len(reviews)

    return avg_val


def get_non_private_books(db:Session):
    books = db.query(models.Book).filter(models.Book.private==False, models.Book.lent==False).all()
    return books


def lend_a_book(bid:int, username:str, db:Session):
    book = db.query(models.Book).filter(models.Book.id==bid).first()
    user = db.query(models.User).filter(models.User.username==username).first()

    book.lent_to_id = user.id
    book.lent = True

    db.commit()
    db.refresh(book)
    return book


def get_lent_books(username:str, db:Session):
    user = db.query(models.User).filter(models.User.username==username).first()
    books = db.query(models.Book).filter(models.Book.lent_to_id==user.id).all()

    return books


def return_a_book(bid:int, db:Session):
    book = db.query(models.Book).filter(models.Book.id==bid).first()

    book.lent = False
    book.lent_to_id = None

    db.commit()
    db.refresh(book)
    return book


def get_shelf_books(username:str, sid:int, db:Session):
    shelf = db.query(models.Shelf).filter(models.Shelf.id==sid).first()

    books = shelf.shelf_books

    return books