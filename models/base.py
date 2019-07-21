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

    # TODO: turn this into a context manager https://docs.sqlalchemy.org/en/13/orm/session_basics.html#when-do-i-construct-a-session-when-do-i-commit-it-and-when-do-i-close-it
    def get_session(self):
        return self.Session()

    def delete(self):
        self.Session = None
        os.remove(f'{self.name}.db')
