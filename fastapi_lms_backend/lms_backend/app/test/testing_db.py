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
