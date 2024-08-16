from app.database.session import Base
from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship


class UserRole(str, PyEnum):
    ADMIN = 'librarian'
    STUDENT = 'student'
    GUEST = 'guest'


class RequestStatus(str, PyEnum):
    REQUESTED = 'requested'
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'
    RETURNED = 'returned'


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    role = Column(Enum(UserRole))
    password = Column(String(255), nullable=False)

    book_requests = relationship("BookRequest", back_populates='user')


class Book(Base):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    genre = Column(String(255), nullable=False)
    publication_year = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False)

    book_requests = relationship("BookRequest", back_populates='book')


class BookRequest(Base):
    __tablename__ = 'book_request'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    book_id = Column(Integer, ForeignKey('book.id'))
    status = Column(Enum(RequestStatus), default=RequestStatus.REQUESTED)

    user = relationship('User', back_populates='book_requests')
    book = relationship('Book', back_populates='book_requests')
