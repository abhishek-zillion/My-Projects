from sqlalchemy import text
import unittest
import logging
from fastapi.testclient import TestClient
from app.main import app, pwd_context
from sqlalchemy.orm import Session
from app.models.book import User, Book, BookRequest, UserRole
from app.utils import create_access_token
from app.static import (
    TEST_DB_NAME,
)

from app.test.testing_db import (
    create_engine_,
    test_engine,
    TestSessionLocal,
    TestBase,
    override_get_db,
    override_dependencies
)

override_get_db()
override_dependencies()

logging.basicConfig(level=logging.DEBUG)


def teardown_database():
    logging.debug("Starting database teardown")
    try:
        with create_engine_.connect() as connection:
            logging.debug(f"Dropping database {TEST_DB_NAME}")
            connection.execute(text(f"DROP DATABASE IF EXISTS {TEST_DB_NAME}"))
            connection.commit()
        logging.debug('Database dropped successfully')
    except Exception as e:
        logging.error(f"Error during database teardown: {str(e)}")
    finally:
        logging.debug("Finished database teardown")


class TestGeneralEndpoint(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with create_engine_.connect() as connection:
            connection.execute(
                text(f"CREATE DATABASE IF NOT EXISTS {TEST_DB_NAME}"))
        TestBase.metadata.create_all(bind=test_engine)
        cls.client = TestClient(app)
        db = TestSessionLocal()
        cls.create_sample_data(db)
        cls.access_token = cls.get_access_token(db)

    @classmethod
    def tearDownClass(cls):
        logging.debug("Starting tearDownClass")
        try:
            logging.debug("Closing all sessions")
            TestSessionLocal.close_all()

            logging.debug("Disposing test engine")
            test_engine.dispose()

            logging.debug("In-memory cleanup completed")
        except Exception as e:
            logging.error(f"Error during in-memory cleanup: {str(e)}")
        finally:
            teardown_database()

            logging.debug("Finished tearDownClass")

    @classmethod
    def get_access_token(cls, db: Session):
        user = db.query(User).filter(User.username == 'admin').first()
        if user:
            return create_access_token(data={"sub": user.username})
        return ""

    @classmethod
    def create_sample_data(cls, db: Session):
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

    def test_get_book(self):
        print("Test get_book")
        response = self.client.get("/general/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)


if __name__ == '__main__':
    unittest.main()
