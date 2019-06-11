from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from models.base import Base

class Album(Base):
    __tablename__ = 'albums'

    id = Column(String, primary_key=True)
    title = Column(String)
    product_url = Column(String)

    media_items = relationship('MediaItem', back_populates='album', collection_class=attribute_mapped_collection('filename'))

    def __init__(self, id, title, product_url):
        self.id = id
        self.title = title
        self.product_url = product_url

    def add_media_item(self, media_item):
        if not media_item.filename in self.media_items:
            self.media_items[media_item.filename] = media_item
        else:
            unique_filename = self._get_unique_filename(media_item.filename)
            media_item.filename = unique_filename
            self.media_items[unique_filename] = media_item

    def _get_unique_filename(self, filename):
        index_of_last_dot = filename.rfind('.')
        filename_without_extension = filename[:index_of_last_dot]
        extension = filename[index_of_last_dot+1:]

        for n in range(1, 1000):
            # the "{filename_without_extension}({n}).{extension}" format is how Google Takeout does unique filenames
            unique_filename = f"{filename_without_extension}({n}).{extension}"
            if not unique_filename in self.media_items:
                return unique_filename
            else:
                continue

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.id == other.id

class MediaItem(Base):
    __tablename__ = 'media_items'

    id = Column(String, primary_key=True)
    filename = Column(String)
    product_url = Column(String)
    album_id = Column(String, ForeignKey('albums.id'))

    album = relationship('Album', back_populates='media_items')

    def __init__(self, id, filename, product_url):
        self.id = id
        self.filename = filename
        self.product_url = product_url
        self.album = None

    def _get_unique_filename(self, filename, album):
        if album is None:
            return filename
        elif not filename in album.media_items:
            return filename
        else:
            index_of_last_dot = filename.rfind('.')
            filename_without_extension = filename[:index_of_last_dot]
            extension = filename[index_of_last_dot+1:]

            for n in range(1, 1000):
                # the "{filename_without_extension}({n}).{extension}" format is how Google Takeout does unique filenames
                unique_filename = f"{filename_without_extension}({n}).{extension}"

                if not unique_filename in album.media_items:
                    return unique_filename
                else:
                    continue

    def __repr__(self):
        return "{}".format(self.filename)

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.id == other.id
