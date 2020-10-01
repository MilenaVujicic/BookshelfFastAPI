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


class AuthorId(BaseModel):
    id:int

class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class PublisherBase(BaseModel):
    name: str


class PublisherCreate(PublisherBase):
    pass


class Publisher(PublisherBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class ShelfBase(BaseModel):
    name: str
    description: str


class ShelfCreate(BaseModel):
    pass


class ShelfId(ShelfBase):
    id: int


class Shelf(ShelfBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class BookBase(BaseModel):
    id: int
    title: str
    pages: int
    description: str
    isbn: str
    read: bool
    lent: bool
    private: bool
    cover: str


class BookCreate(BookBase):
    pass


class Book(BookBase):
    owner_id: int

    class Config:
        orm_mode = True


class AuthorBookBase(BaseModel):
    authorId: int
    bookId: int


class AuthorBookCreate(AuthorBookBase):
    pass


class AuthorBook(BaseModel):
    id: int


class ShelfBookBase(BaseModel):
    bookId: int
    shelfId: int


class ShelfBookCreate(ShelfBookBase):
    pass


class ShelfBook(ShelfBookBase):
    id: int

    class Config:
        orm_mode = True


class ReviewBase(BaseModel):
    rating:int
    content:str


class ReviewCreate(ReviewBase):
    pass


class Review(ReviewBase):
    id: int
    reviewer_id:int
    book_id:int

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
    user_authors: List[Author] = []
    user_publishers: List[Publisher] = []
    user_books: List[Book] = []
    user_shelves: List[Shelf] = []
    user_reviews: List[Review] = []

    class Config:
        orm_mode = True
