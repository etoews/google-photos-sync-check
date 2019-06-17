import pytest

from models.base import Database

@pytest.fixture(scope="session")
def session():
    db = Database('google-photos-sync-check-test')
    session = db.get_session()
    yield session
    db.delete()
