from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv()

Base = declarative_base()

class Conector:
    def __init__(self, user, password, dbname, host='localhost:5432'):
        self.DATABASE_URL = f"postgresql://{user}:{password}@{host}/{dbname}"
        self.engine = create_engine(self.DATABASE_URL)
        self.session_local = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.db = None

    def conect(self):
        self.db = self.session_local()
        return self.db

    def desconect(self):
        if self.db:
            self.db.close()