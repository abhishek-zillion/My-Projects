from app.celery_settings.celery import celery_app
from app.database.session import SessionLocal
from app.models.book import Book, BookRequest, RequestStatus
from app.utils import send_email


@celery_app.task
def check_stock_status():
    db = SessionLocal()
    try:
        books = db.query(Book).all()
        for book in books:
            if book.stock <= 0:
                print(f'Alert: Low stock for book {book.title}')
        return f'Count of total books:{len(books)}'
    finally:
        db.close()


@celery_app.task
def check_pending_request():
    db = SessionLocal()
    try:
        requests = db.query(BookRequest).filter(
            BookRequest.status == RequestStatus.REQUESTED).all()
        if len(requests) > 0:
            send_email(subject='Pending Book Request',
                       body='Take Immediate Action',
                       to_email='abhishek.zillioninfotech@gmail.com')
            print(f'Count of pending requests: {len(requests)}')
        print('No pending requests')
    finally:
        db.close()
