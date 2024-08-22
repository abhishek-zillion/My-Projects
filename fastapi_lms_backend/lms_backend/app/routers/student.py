from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.schemas.book import (RequestHistory, BookRequestResponse,
                              BookResponseWithID,
                              UserResponse, BookResponse,
                              )
from app.database.session import get_db
from app.models.book import (Book, User, BookRequest as BookRequestModel,
                             UserRole, RequestStatus)
from app.utils import get_current_user
from app.celery_settings.tasks import check_stock_status

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get('/request-details', response_model=RequestHistory)
def your_requests(db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request can only made by students")
    user_id = current_user.id
    requests = db.query(BookRequestModel).filter(
        BookRequestModel.user_id == user_id)

    request_items = [BookResponseWithID(
        book_id=req.book_id, book_name=req.book.title, status=req.status)
        for req in requests]
    return RequestHistory(user=current_user.username, requests=request_items)


@router.post('/request-book', response_model=BookRequestResponse,
             status_code=status.HTTP_201_CREATED)
def create_book_request(book_id: int, db: Session = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request can only made by students")
    book = db.query(Book).filter(Book.id == book_id).first()

    if not current_user.id or not book:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail='User or Book not found')

    existing_request = db.query(BookRequestModel).filter(
        BookRequestModel.user_id == current_user.id,
        BookRequestModel.book_id == book_id,
        BookRequestModel.status == RequestStatus.REQUESTED).first()
    if existing_request:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='You already have requested for this book')
    if book.stock != 0:
        new_request = BookRequestModel(
            user_id=current_user.id, book_id=book_id)
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='Book is out of stock')
    check_stock_status.apply_async()
    db.add(new_request)
    db.commit()
    db.refresh(new_request)

    return BookRequestResponse(id=new_request.id,
                               user=UserResponse(
                                   user_id=current_user.id,
                                   username=current_user.username),
                               book=BookResponse(book_id=book.id,
                                                 book_name=book.title,
                                                 status=new_request.status))


@router.delete('/request-delete', status_code=status.HTTP_204_NO_CONTENT)
def delete_request(book_id: int, db: Session = Depends(get_db),
                   current_user: User = Depends(get_current_user)):
    if current_user.role != UserRole.STUDENT:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Request can only made by students")
    request = db.query(BookRequestModel).filter(
        BookRequestModel.user_id == current_user.id,
        BookRequestModel.book_id == book_id).first()

    if not request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Request not found')

    db.delete(request)
    db.commit()
    return {"message": "Request deleted successfully"}
