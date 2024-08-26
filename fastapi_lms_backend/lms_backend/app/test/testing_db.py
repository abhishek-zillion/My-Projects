from app.main import app
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.session import get_db, Base
from app.static import (
    TEST_DB_HOST,
    TEST_DB_NAME,
    TEST_DB_PASSWORD,
    TEST_DB_USER
)
from app.models.book import User, Book, BookRequest, UserRole
from app.main import app, pwd_context



create_engine_ = create_engine(
    f"mysql+pymysql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}")

test_engine = create_engine(
    f"mysql+pymysql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{TEST_DB_HOST}/{TEST_DB_NAME}")

TestSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=test_engine)

TestBase = Base


def override_get_db():
    try:
        db = TestSessionLocal()
        yield db
    finally:
        db.close()


def override_dependencies():
    app.dependency_overrides[get_db] = override_get_db


def factory_objects():
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
        request1 = BookRequest(user_id=user_2.id, book_id=book1.id)
        request2 = BookRequest(user_id=user_2.id, book_id=book2.id)
        request3 = BookRequest(user_id=user_3.id, book_id=book3.id)
        return user_1, user_2, user_3, book1, book2, book3, request1, request2, request3