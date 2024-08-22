from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.book import Book
from app.database.session import get_db
from app.schemas.book import TotalBooks, BookData


router = APIRouter()


@router.get('/total-books', response_model=TotalBooks)
def get_total_books(db: Session = Depends(get_db)):
    total = db.query(Book).count()
    if total == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='No books found')
    return TotalBooks(total_books=total)


@router.get('/{book_id}', response_model=BookData)
def get_book(book_id: int, db: Session = Depends(get_db)):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Book with id {book_id} not found')
    return book
