import argparse

from os import listdir
from os.path import isdir, isfile, join

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

def get_local_albums(path):
    albums = []
    years = [year for year in listdir(path) if isdir(join(path, year))]

    for year in years:
        year_path = join(path, year)

        for title in listdir(year_path):
            album_path = join(year_path, title)

            if isdir(album_path):
                album = Album(None, title, album_path)
                albums.append(album)

    return frozenset(albums)

def get_db_albums(db):
    session = db.get_session()

    albums = session.query(Album)

    session.close()

    return frozenset(albums)

def sync_check(args):
    path = args.path
    local_albums = get_local_albums(path)

    db = Database('google-photos-sync-check')
    db_albums = get_db_albums(db)

    print(f"diff:")
    diff = local_albums.difference(db_albums)
    for album in diff:
        print(f"  {album}\t\t\t{album.__hash__()}")

    print("\n")

    print(f"local albums:")
    for album in local_albums:
        print(f"  {album}\t\t\t{album.__hash__()}")

    print("\n")

    print(f"db albums:")
    for album in db_albums:
        print(f"  {album}\t\t\t{album.__hash__()}")

def rebuild_db(args):
    photoslibrary = authn_and_authz()

    db = Database('google-photos-sync-check')
    session = db.get_session()

    # in this algorithm, the unit of work is the page rather than the individual album or media item

    album_pages = get_album_pages(photoslibrary)

    for album_page in album_pages:
        albums = process_album_page(album_page)
        session.add_all(albums)

        for album in albums:
            print(album.title)
            media_items_pages = get_media_items_pages(photoslibrary, album)

            for media_items_page in media_items_pages:
                media_items = process_media_items_page(media_items_page)
                session.add_all(media_items)

                for media_item in media_items:
                    print(media_item.filename)
                    album.add_media_item(media_item)

        session.commit()

    session.close()

def get_args():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_path_and_db = subparsers.add_parser('sync_check', help='Sync check between a local file path and the database of all albums and media items')
    parser_path_and_db.add_argument('path', type=str, help='Local file path to photo albums')
    parser_path_and_db.set_defaults(func=sync_check)

    parser_rebuild_db = subparsers.add_parser('rebuild_db', help='Rebuild the database of all albums and media items from the Google Photos API')
    parser_rebuild_db.set_defaults(func=rebuild_db)

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    args.func(args)
