import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Database():
    def __init__(self, name):
        self.name = name
        _engine = create_engine(f'sqlite:///{self.name}.db')
        self.Session = sessionmaker(bind=_engine)
        Base.metadata.create_all(_engine)

    def get_session(self):
        return self.Session()

    def delete(self):
        self.Session = None
        os.remove(f'{self.name}.db')
