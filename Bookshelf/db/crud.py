from sqlalchemy.orm import Session
from . import models, schemas
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt

from typing import Optional

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


def new_author(db:Session, author: schemas.AuthorBase, username:str):
    owner = db.query(models.User).filter(models.User.username==username).first()
    db_author = models.Author(name=author.name, surname=author.surname, owner_id=owner.id)
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def author_edit(db:Session, author_id:int, username:str, author:schemas.AuthorBase):
    db_author = db.query(models.Author).filter(models.Author.id == author_id).first()
    db_author.surname = author.surname
    db_author.name = author.name
    db.commit()
    return db_author


def get_one_author(db:Session, author_id:int, username:str):
    db_author = db.query(models.Author).filter(models.Author.id==author_id).first()
    return db_author


def get_authors(db:Session, username:str):
    owner = db.query(models.User).filter(models.User.username==username).first()
    db_authors = db.query(models.Author).filter(models.Author.owner_id==owner.id).all()
    return db_authors


def delete_author(db:Session, username:str, author_id:int):
    db_author = db.query(models.Author).filter(author_id==author_id).delete()
    db.commit()


def new_publisher(db:Session, username:str, publisher:schemas.PublisherBase):
    owner = db.query(models.User).filter(models.User.username==username).first()
    db_publisher = models.Publisher(name=publisher.name, owner_id=owner.id)
    db.add(db_publisher)
    db.commit()
    db.refresh(db_publisher)
    return db_publisher


def edit_publisher(db:Session, username:str, publisher:schemas.PublisherBase, pub_id:int):
    db_pub = db.query(models.Publisher).filter(models.Publisher.id==pub_id).first()
    db_pub.name = publisher.name
    db.commit()
    return db_pub


def get_publishers(username:str, db:Session):
        owner = db.query(models.User).filter(models.User.username==username).first()
        db_publishers = db.query(models.Publisher).filter(models.Publisher.owner_id==owner.id).all()

        return db_publishers


def get_one_publisher(username:str, pub_id:int, db:Session):
    db_publisher = db.query(models.Publisher).filter(models.Publisher.id==pub_id).first()
    return db_publisher


def delete_publisher(pub_id:int, username:str, db:Session):
    db_publisher = db.query(models.Publisher).filter(models.Publisher.id==pub_id).delete()
    db.commit()