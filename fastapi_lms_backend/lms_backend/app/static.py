from dotenv import load_dotenv
import os

load_dotenv()

# test db credentials
TEST_DB_USER = os.getenv('TEST_DB_USER')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD')
TEST_DB_HOST = os.getenv('TEST_DB_HOST')
TEST_DB_NAME = os.getenv('TEST_DB_NAME')

# development db credentials
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')

# jwt credentials
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))
