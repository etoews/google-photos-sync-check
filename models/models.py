from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from models.base import Base


class Album(Base):
    __tablename__ = 'albums'

    id = Column(String, primary_key=True)
    title = Column(String, unique=True, index=True)
    location = Column(String)

    media_items = relationship(
        'MediaItem', back_populates='album', collection_class=attribute_mapped_collection('filename'))

    def __init__(self, id, title, location):
        self.id = id
        self.title = self._normalise_title(title)
        self.location = location

    def add_media_item(self, media_item):
        if media_item.filename not in self.media_items:
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
            if unique_filename not in self.media_items:
                return unique_filename
            else:
                continue

    def _normalise_title(self, title):
        # normalise the title because of how Google Takeout mangles the title
        # TODO: warn on trailing space
        normalised_title = title.replace("_", "'")
        normalised_title = normalised_title[:50]
        return normalised_title

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.title == other.title

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.title)


class MediaItem(Base):
    __tablename__ = 'media_items'

    id = Column(String, primary_key=True)
    album_id = Column(String, ForeignKey('albums.id'), primary_key=True, nullable=True)
    filename = Column(String)
    location = Column(String)

    album = relationship('Album', back_populates='media_items')

    def __init__(self, id, filename, location):
        self.id = id
        self.filename = filename
        self.location = location
        self.album = None

    def __repr__(self):
        return self.filename

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.id == other.id
