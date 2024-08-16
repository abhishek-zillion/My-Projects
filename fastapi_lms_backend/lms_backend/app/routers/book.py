from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.schemas.book import (ShowBook, UpdateBookPatch, BookRequestResponse,
                              UserResponse, BookResponse,
                              BookRequestHistory,
                              ActionUponBook,
                              UpdateBookPut)
from app.database.session import get_db
from app.models.book import (Book, User, BookRequest as BookRequestModel,
                             UserRole, RequestStatus)
from typing import List
from app.utils import get_current_user

router = APIRouter()


@router.get('/all-books', response_model=List[ShowBook])
def get_books(db: Session = Depends(get_db),
              current_user: User = Depends(get_current_user)):

    books = db.query(Book).all()
    if not books:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='Books not found')
    return books


@router.post('/add', response_model=ShowBook,
             status_code=status.HTTP_201_CREATED)
def add_book(book: ShowBook, db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can add books')
    existing_book = db.query(Book).filter(
        and_(Book.title == book.title,
             Book.publication_year == book.publication_year,
             Book.genre == book.genre)
    ).first()

    if existing_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f'Book with title "{book.title}"\
                                already exists.')
    new_book = Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get('/request-history', response_model=BookRequestHistory)
def get_request_history(current_user: User = Depends(get_current_user),
                        db: Session = Depends(get_db)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can view request history')
    requests = db.query(BookRequestModel).all()

    book_reqs = []
    for req in requests:
        book = db.query(Book).filter(Book.id == req.book_id).first()
        book_reqs.append(
            BookRequestResponse(id=book.id,
                                user=UserResponse(
                                    user_id=req.user_id,
                                    username=req.user.username),
                                book=BookResponse(
                                    book_id=book.id, book_name=book.title,
                                    status=req.status)
                                )
        )
    total_book_requests = db.query(BookRequestModel).all()
    return BookRequestHistory(requests=book_reqs,
                              total_reqs=len(total_book_requests))


@router.post('/request-action', status_code=status.HTTP_200_OK)
def act(req_id: int, action: ActionUponBook, db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can execute actions')
    book_request = db.query(BookRequestModel).filter(
        BookRequestModel.id == req_id).first()
    if not book_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Book request with id {req_id} not found')
    if book_request.book.stock != 0:
        book_request.status = action.action
        if action.action == RequestStatus.ACCEPTED:
            book_request.book.stock -= 1
        if action.action == RequestStatus.RETURNED:
            book_request.book.stock += 1
        db.commit()
        db.refresh(book_request)
        return {'message':
                f'Action {action.action} upon book request with id {req_id}\
                executed successfully'}
    return {'message': 'Book is out of stock'}


@router.put('/update-book/{book_id}', status_code=status.HTTP_200_OK)
def update_book_put(book_id: int, book: UpdateBookPut,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can update books')
    book_record = db.query(Book).filter(Book.id == book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Book with id {book_id} not found')

    for key, value in book.dict(exclude_unset=True).items():
        setattr(book_record, key, value)

    db.commit()
    db.refresh(book_record)
    return book_record


@router.patch('/update-book/{book_id}',
              status_code=status.HTTP_200_OK)
def update_book_patch(book_id: int, book: UpdateBookPatch,
                      db: Session = Depends(get_db),
                      current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can update books')
    book_record = db.query(Book).filter(Book.id == book_id).first()
    if not book_record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Book with id {book_id} not found')

    for key, value in book.dict(exclude_unset=True).items():
        setattr(book_record, key, value)

    db.commit()
    db.refresh(book_record)
    return book_record


@router.delete('/delete-book', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(name: str = None, book_id: int = None,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Only librarian can delete books')
    if not name and not book_id:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={
            'Enter either a title or book id'
        })

    if book_id:
        book = db.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Book with id {book_id} not found')
    elif name:
        books = db.query(Book).filter(Book.title == name).all()
        if len(books) > 1:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f'Multiple book with title {name}')
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f'Book with title {name} not found')

    db.delete(book)
    db.commit()
    return {"message": "Book delted successfully"}
