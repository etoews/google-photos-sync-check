import os

from contextlib import contextmanager

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

    @contextmanager
    def session_context(self):
        """Provide a transactional scope around a series of operations."""
        session = self.Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    def delete(self):
        self.Session = None
        os.remove(f'{self.name}.db')
