from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

from models.base import Database
from models.models import Album, MediaItem

SCOPES = 'https://www.googleapis.com/auth/photoslibrary.readonly'

def authn_and_authz():
    store = file.Storage('client_token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('photoslibrary', 'v1', http=creds.authorize(Http()))

def get_album_pages(photoslibrary):
    albums_response = photoslibrary.albums().list().execute()

    while True:
        yield albums_response.get('albums', [])

        nextPageToken = albums_response.get('nextPageToken', None)
        if not nextPageToken is None:
            albums_response = photoslibrary.albums().list(pageToken=nextPageToken).execute()
        else:
            break

def process_album_page(album_page):
    albums = []
    for album_raw in album_page:
        album = Album(album_raw['id'], album_raw['title'], album_raw['productUrl'])
        albums.append(album)
    return albums

def get_media_items_pages(photoslibrary, album):
    search_params = {'albumId': album.id}
    media_items_response = photoslibrary.mediaItems().search(body=search_params).execute()

    while True:
        yield media_items_response.get('mediaItems', [])

        nextPageToken = media_items_response.get('nextPageToken', None)
        if not nextPageToken is None:
            search_params['pageToken'] = nextPageToken
            media_items_response = photoslibrary.mediaItems().search(body=search_params).execute()
        else:
            break

def process_media_items_page(media_items_page):
    media_items = []
    for media_item_raw in media_items_page:
        media_item = MediaItem(media_item_raw['id'], media_item_raw['filename'], media_item_raw['productUrl'])
        media_items.append(media_item)
    return media_items

if __name__ == '__main__':
    photoslibrary = authn_and_authz()

    db = Database('google-photos-sync-check')
    session = db.get_session()

    # in this algorithm, the unit of work is the page rather than the individual album or media item

    album_pages = get_album_pages(photoslibrary)
    for album_page in album_pages:
        albums = process_album_page(album_page)
        session.add_all(albums)

        for album in albums:
            media_items_pages = get_media_items_pages(photoslibrary, album)
            print(album.title)

            for media_items_page in media_items_pages:
                media_items = process_media_items_page(media_items_page)
                session.add_all(media_items)

                for media_item in media_items:
                    album.add_media_item(media_item)
                    print(media_item.filename)

        session.commit()

    session.close()
