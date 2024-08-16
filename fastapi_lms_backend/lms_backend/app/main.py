import logging
from fastapi import FastAPI
from app.routers import book, general_api, student
from app.routers import register
from sqlalchemy.orm import Session
from app.database.session import Base, SessionLocal
from app.database.session import engine
from app.models.book import Book, User, BookRequest, UserRole
from app.utils import pwd_context

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


app = FastAPI(
)

app.include_router(register.router, prefix="/auth", tags=["Authentication"])
app.include_router(general_api.router, prefix="/general", tags=['General'])
app.include_router(book.router, prefix="/books", tags=["Librarian"])
app.include_router(student.router, prefix="/student", tags=['Student'])

# Base.metadata.drop_all(engine)
Base.metadata.create_all(bind=engine)


def sample_data(db: Session):
    user_1 = User(username='admin', role=UserRole.ADMIN,
                  password=pwd_context.hash('admin'))
    user_2 = User(username='guest', role=UserRole.GUEST,
                  password=pwd_context.hash('guest'))
    user_3 = User(username='student', role=UserRole.STUDENT,
                  password=pwd_context.hash('student'))

    book1 = Book(title='The Great Gatsby', genre='Fiction',
                 publication_year=1925, stock=5)
    book2 = Book(title='1984', genre='Dystopian',
                 publication_year=1949, stock=3)
    book3 = Book(title='To Kill a Mockingbird', genre='Fiction',
                 publication_year=1960, stock=4)

    db.add_all([user_1, user_2, user_3, book1, book2, book3])
    db.commit()

    request1 = BookRequest(user_id=user_2.id, book_id=book1.id)
    request2 = BookRequest(user_id=user_2.id, book_id=book2.id)
    request3 = BookRequest(user_id=user_3.id, book_id=book3.id)

    db.add_all([request1, request2, request3])
    db.commit()


if __name__ == "__main__":
    '''
    To run this script,
    python3 -m app.main
    '''
    db = SessionLocal()
    sample_data(db)
    db.close()
    logging.info("Sample data has been saved")
