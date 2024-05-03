from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


class Session:
    @staticmethod
    def create():
        DB_HOST = os.environ["DB_HOST"]
        DB_PORT = os.environ["DB_PORT"]
        DB_USERNAME = os.environ["DB_USERNAME"]
        DB_PASSWORD = os.environ["DB_PASSWORD"]
        DB_DATABASE = os.environ["DB_DATABASE"]

        DATABASE_URL = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
        engine = create_engine(DATABASE_URL)
        instance = sessionmaker(bind=engine)

        return instance()
