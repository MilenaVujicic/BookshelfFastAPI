from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id==user_id).first()


def creat_user(db: Session, user: schemas.UserCreate):
    pw = user.password
    db_user = models.User(email=user.email, hashed_password=pw, first_name=user.first_name, last_name=user.last_name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

