from models.base import Base

class Album():
    def __init__(self, album_id, title, product_url):
        self.id = album_id
        self.title = title
        self.product_url = product_url
        self.media_items = {}

    def __repr__(self):
        return self.title

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.id == other.id

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

    def add_media_item(self, media_item):
        if not media_item.filename in self.media_items:
            self.media_items[media_item.filename] = media_item
        else:
            unique_filename = self._get_unique_filename(media_item.filename)
            media_item.filename = unique_filename
            self.media_items[unique_filename] = media_item

class MediaItem:
    def __init__(self, media_item_id, filename, product_url):
        self.id = media_item_id
        self.filename = filename
        self.product_url = product_url

    def __repr__(self):
        return "{}".format(self.filename)

    def __eq__(self, other):
        if not isinstance(other, Album):
            return NotImplemented

        return self.id == other.id
