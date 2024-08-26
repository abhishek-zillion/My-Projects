from sqlalchemy import text
import unittest
import logging
import json
from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy.orm import Session, close_all_sessions
from app.models.book import User, Book, BookRequest, UserRole
from app.utils import create_access_token
from app.celery_settings.tasks import *
from app.static import TEST_DB_NAME

from app.test.testing_db import (
    create_engine_,
    test_engine,
    TestSessionLocal,
    TestBase,
    override_get_db,
    override_dependencies,
    factory_objects
)
from unittest.mock import Mock, patch

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

# Override dependencies
# override_get_db()
override_dependencies()


def teardown_database():
    '''
    This function either cleans up the database
    or remove tables from the database
    '''
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
        cls.db = TestSessionLocal()
        cls.create_sample_data(cls.db)
        cls.access_token = cls.get_access_token(cls.db)
        cls.load_data_from_json_files()

    @classmethod
    def load_data_from_json_files(cls):
        """
        Load data from JSON files and populate the database.
        """
        try:
            with open('../dump_data/book.json', 'r') as file:
                books = json.load(file)
            with open('../dump_data/user.json', 'r') as file:
                users = json.load(file)
            with open('../dump_data/book_request.json', 'r') as file:
                book_requests = json.load(file)

            db = TestSessionLocal()
            try:
                for book in books:
                    db.add(Book(**book))
                for user in users:
                    db.add(User(**user))
                for book_request in book_requests:
                    db.add(BookRequest(**book_request))
                db.commit()
                logging.debug("Data loaded successfully from JSON files")
            except Exception as e:
                db.rollback()
                logging.error(f"Error loading data into database: {str(e)}")
            finally:
                db.close()
        except Exception as e:
            logging.error(f"Error reading JSON files: {str(e)}")

    @classmethod
    def tearDownClass(cls):
        '''
        Can either drop the database
        or truncate the database
        '''
        logging.debug("Starting tearDownClass")
        try:
            logging.debug("Closing all sessions")
            close_all_sessions()

            logging.debug("Disposing test engine")
            test_engine.dispose()

            logging.debug("In-memory cleanup completed")
        except Exception as e:
            logging.error(f"Error during in-memory cleanup: {str(e)}")
        finally:
            TestBase.metadata.drop_all(bind=test_engine)
            logging.debug("Finished tearDownClass")

    @classmethod
    def get_access_token(cls, db: Session):
        user = db.query(User).filter(User.username == 'admin').first()
        if user:
            return create_access_token(data={"sub": user.username})
        return ""

    @classmethod
    def create_sample_data(cls, db: Session):
        db.add_all([data for data in factory_objects()])
        db.commit()

    def test_get_book(self):
        response = self.client.get("/general/1")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json(), dict)

    def test_signup(self):
        data = {
            "username": "test_1",
            "role": UserRole.GUEST,
            "password": 'password'
        }

        response = self.client.post("auth/signup", json=data)
        data = response.json()
        self.assertEqual(data['username'], "test_1")
        self.assertIsNotNone(data['role'])
        self.assertIsNone(data.get('password'))
        self.assertEqual(response.status_code, 200)

    @patch('app.routers.book.check_stock_status')
    def test_get_all_books(self,
                           mock_check_stock_status):

        mock_check_stock_status.apply_async.return_value = 'OK'

        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        response = self.client.get("/books/all-books", headers=headers)
        # print('checking mock status', check_stock_status())
        # print(response.json(), sep=' ')
        self.assertEqual(response.status_code, 200)
        mock_check_stock_status.apply_async.assert_called_once()
        self.assertIsInstance(response.json(), list)


if __name__ == '__main__':
    unittest.main()
