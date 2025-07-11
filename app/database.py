from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
import psycopg2
import psycopg2.extras
import time
from .config import settings
import urllib.parse

password = urllib.parse.quote_plus(settings.database_password)

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.database_username}:{password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="localhost",
#             database="fastapi",
#             user="cipher",
#             password="ahmad@2003",
#             port=5433,
#             cursor_factory=psycopg2.extras.RealDictCursor
#             )
#         cursor = conn.cursor()
#         print("Database connection successful")
#         break
#     except Exception as e:
#         print("Database connection failed")
#         print(f"Error: {e}") 