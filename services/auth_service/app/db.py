from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import time
import os

MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "rootpassword")
MYSQL_NAME = os.getenv("MYSQL_DATABASE", "geodb")
MYSQL_HOST = os.getenv("MYSQL_HOST", "mysql")

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_NAME}"

retries = 10
for i in range(retries):
    try:
        engine = create_engine(SQLALCHEMY_DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        break
    except SQLAlchemyError as e:
        print(f"[auth_service] DB connection failed ({i+1}/{retries}), retrying in 5s...")
        time.sleep(5)
else:
    raise Exception("[auth_service] Could not connect to the database after multiple attempts.")


Base = declarative_base()
