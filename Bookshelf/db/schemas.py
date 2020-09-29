from typing import List, Optional

from datetime import datetime, timedelta

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class AuthorBase(BaseModel):
    name: Optional[str] = None
    surname: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class PublisherBase(BaseModel):
    name:str


class PublisherCreate(PublisherBase):
    pass


class Publisher(PublisherBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserInDB(UserBase):
    password: str


class UserTime(UserInDB):
    time_claim: datetime


class UserBasic(BaseModel):
    username: str
    password: str


class User(UserInDB):
    id: int
    is_active: bool
    username: str
    first_name: str
    last_name: str
    authors: List[Author] = []

    class Config:
        orm_mode = True
