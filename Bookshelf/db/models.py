from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, SmallInteger, Table
from sqlalchemy.orm import relationship
from .database import Base

AuthorBook = Table('AuthorBook',
                   Base.metadata,
                   Column('id', Integer, primary_key=True),
                   Column('author_id', Integer, ForeignKey('authors.id')),
                   Column('book_id', Integer, ForeignKey('books.id')))

ShelfBook = Table('ShelfBook',
                  Base.metadata,
                  Column('id', Integer, primary_key=True),
                  Column('shelf_id', Integer, ForeignKey("shelves.id")),
                  Column('book_id', Integer, ForeignKey("books.id")))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)

    user_authors = relationship("Author", back_populates="author_owner")
    user_publishers = relationship("Publisher", back_populates="publisher_owner")
    user_books = relationship("Book", back_populates="book_owner", foreign_keys='Book.owner')
    user_lent_books = relationship("Book", back_populates="book_lent_to", foreign_keys='Book.lent_to_id')
    user_shelves = relationship("Shelf", back_populates="shelf_owner")
    user_reviews = relationship("Review", back_populates="review_owner")


class Author(Base):
    __tablename__ = "authors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    author_owner = relationship("User", back_populates="user_authors", lazy='joined')
    author_books = relationship("Book", secondary=AuthorBook, backref='authors_books')


class Publisher(Base):
    __tablename__ = "publishers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    publisher_owner = relationship("User", back_populates="user_publishers")
    publisher_books = relationship("Book", back_populates="book_publisher")


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    pages = Column(SmallInteger, index=True)
    description = Column(String, index=True)
    isbn = Column(String, index=True)
    read = Column(Boolean, default=False, index=True)
    lent = Column(Boolean, default=False, index=True)
    private = Column(Boolean, default=False, index=True)
    cover = Column(String, index=True)
    owner = Column(Integer, ForeignKey("users.id"))
    publisher = Column(Integer, ForeignKey("publishers.id"))
    lent_to_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    book_owner = relationship("User", back_populates="user_books", foreign_keys=[owner])
    book_lent_to = relationship("User", back_populates="user_lent_books", foreign_keys=[lent_to_id])
    book_publisher = relationship("Publisher", back_populates="publisher_books")
    book_authors = relationship('Author', secondary=AuthorBook, backref='authors_books', lazy='dynamic')
    book_shelves = relationship('Shelf', secondary=ShelfBook, backref='shelves_books', lazy='dynamic')
    book_reviews = relationship("Review", back_populates='book_review')


class Shelf(Base):
    __tablename__ = "shelves"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    shelf_owner = relationship('User', back_populates="user_shelves")
    shelf_books = relationship('Book', secondary=ShelfBook, backref='shelves_books',lazy='joined')


class Review(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer, index=True)
    content = Column(String, index=True)
    reviewer_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))

    review_owner = relationship('User', back_populates='user_reviews')
    book_review = relationship('Book', back_populates='book_reviews')
