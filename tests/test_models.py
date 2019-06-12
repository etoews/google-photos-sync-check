import pytest

from models.models import Album, MediaItem
from models import base

def test_init_db():
    base.init()

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
