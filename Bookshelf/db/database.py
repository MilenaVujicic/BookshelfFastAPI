from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@projectServer/book_DB_2"
SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@0.0.0.0:5432/book_DB_2'
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

