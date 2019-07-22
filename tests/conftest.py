import pytest

from models.base import Database

@pytest.fixture(scope="session")
def db():
    db = Database('google-photos-sync-check-test')
    yield db
    db.delete()
