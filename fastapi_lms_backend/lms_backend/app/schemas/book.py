from pydantic import BaseModel
from typing import List, Optional
from app.models.book import UserRole


class BookBase(BaseModel):
    id: int
    title: str
    publication_year: int
    genre: str
    stock: int


class ShowBook(BaseModel):
    title: str
    publication_year: int
    genre: str
    stock: int

    class Config:
        orm_mode = True


class User(BaseModel):
    username: str
    role: Optional[str] = UserRole.GUEST
    password: str


class UserDisplay(BaseModel):
    username: str
    role: str


class BookRequest(BaseModel):
    user_id: int
    book_id: int

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    user_id: int
    username: str


class BookResponse(BaseModel):
    book_id: int
    book_name: str
    status: str


class BookRequestResponse(BaseModel):
    id: int
    user: UserResponse
    book: BookResponse

    class Config:
        orm_mode = True


class BookResponseWithID(BookResponse):
    book_id: int
    book_name: str
    status: str


class RequestHistory(BaseModel):
    user: str
    requests: List[BookResponseWithID]

    class Config:
        orm_mode = True


class BookRequestHistory(BaseModel):
    requests: List[BookRequestResponse]
    total_reqs: int

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class UserLogin(BaseModel):
    username: str
    password: str


class TotalBooks(BaseModel):
    total_books: int


class UpdateBookPut(BaseModel):
    title: str
    publication_year: int
    genre: str
    stock: int

    class Config:
        orm_mode = True


class UpdateBookPatch(BaseModel):
    title: Optional[str] = None
    publication_year: Optional[int] = None
    genre: Optional[str] = None
    stock: Optional[int] = None

    class Config:
        orm_mode = True


class ActionUponBook(BaseModel):
    action: str


class BookData(BaseModel):
    title: str
    publication_year: int
    genre: str
    stock: int
