import pytest

from models.models import Album, MediaItem
from models.base import Database

def test_add_media_item():
    media_item_filename = "IMG_3673.JPG"
    media_item = MediaItem("mediaitem123", media_item_filename, "https://photos.google.com/lr/photo/mediaitem123")

    album = Album("album123", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/album123")
    album.add_media_item(media_item)

    assert len(album.media_items) == 1

    assert media_item_filename in album.media_items
    assert album.media_items[media_item_filename] == media_item
    assert media_item.album == album

def test_add_non_unique_media_item():
    media_item_filename = "GPTempDownload.jpg"
    media_item_unique_filename = "GPTempDownload(1).jpg"
    media_item_123 = MediaItem("mediaitem123", media_item_filename, "https://photos.google.com/lr/photo/mediaitem123")
    media_item_456 = MediaItem("mediaitem456", media_item_filename, "https://photos.google.com/lr/photo/mediaitem456")

    album = Album("album123", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/album123")
    album.add_media_item(media_item_123)
    album.add_media_item(media_item_456)

    assert len(album.media_items) == 2

    assert media_item_filename in album.media_items
    assert album.media_items[media_item_filename] == media_item_123
    assert media_item_123.album == album

    assert media_item_unique_filename in album.media_items
    assert album.media_items[media_item_unique_filename] == media_item_456
    assert media_item_456.album == album

def test_persist_album(session):
    album = Album("album123", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/album123")

    session.add(album)
    session.commit()

    albums = session.query(Album).all()

    assert len(albums) == 1
    assert albums[0].id == album.id

    session.close()

def test_persist_media_item(session):
    media_item = MediaItem("mediaitem123", "IMG_3673.JPG", "https://photos.google.com/lr/photo/mediaitem123")

    session.add(media_item)
    session.commit()

    media_items = session.query(MediaItem).all()

    assert len(media_items) == 1
    assert media_items[0].id == media_item.id

    session.close()

def test_persist_album_with_media_item(session):
    media_item = MediaItem("mediaitem001", "IMG_3673.JPG", "https://photos.google.com/lr/photo/mediaitem001")

    album = Album("album001", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/album001")
    album.add_media_item(media_item)

    session.add(album)
    session.add(media_item)
    session.commit()

    # albums = session.query(Album).all()

    # assert len(albums) == 1
    # assert albums[0].id == album.id

    session.close()
