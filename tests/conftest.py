import pytest

from models.base import Database


@pytest.fixture()
def db():
    db = Database('google-photos-sync-check-test')
    yield db
    db.delete()
