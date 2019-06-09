import pytest

from models.models import Album, MediaItem

def test_add_media_item():
    album = Album("AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk")
    media_item_filename = "IMG_3673.JPG"
    media_item = MediaItem("AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg", media_item_filename, "https://photos.google.com/lr/photo/AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg")
    album.add_media_item(media_item)

    assert len(album.media_items) == 1
    assert album.media_items[media_item_filename] == media_item

def test_insert_non_unique_media_item():
    album = Album("AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk")
    media_item_filename = "GPTempDownload.jpg"
    media_item = MediaItem("AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg", media_item_filename, "https://photos.google.com/lr/photo/AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg")
    album.add_media_item(media_item)
    album.add_media_item(media_item)

    assert len(album.media_items) == 2
    assert "GPTempDownload.jpg" in album.media_items
    assert "GPTempDownload(1).jpg" in album.media_items

def test_get_unique_filename():
    album = Album("AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk", "2019-03-26 - Dive - Mermaid's Kitchen East", "https://photos.google.com/lr/album/AEinCCD8UTwCuzv8jfpBqa_uZ1tr9jXVhTeUkt5TgwQvpywfAnn1Ohk")
    media_item_filename = "GPTempDownload.jpg"
    media_item = MediaItem("AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg", media_item_filename, "https://photos.google.com/lr/photo/AEinCCCffWPTI1kYP24kHbV7iJrQp60Ne35bJWa7gYjUoj7lX5VatigBJvyO8_TTeQEot1Mx3I4hGggR7p6RY0froLcuz1IGwg")
    album.add_media_item(media_item)

    unique_filename = album._get_unique_filename(media_item_filename)

    assert unique_filename == "GPTempDownload(1).jpg"
