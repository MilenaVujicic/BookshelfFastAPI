from typing import List, Optional

from pydantic import BaseModel


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


class UserBase(BaseModel):
    email: str
    username: str
    first_name: str
    last_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    first_name: str
    last_name: str
    authors: List[Author] = []

    class Config:
        orm_mode = True

