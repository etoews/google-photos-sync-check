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

def sync_check_path_and_db(args):
    path = args.path
    albums = {}

    years = [name for name in listdir(path) if isdir(join(path, name))]
    print(years)

    for year in years:
        print(year)

        year_path = join(path, year)
        album_names = [name for name in listdir(year_path) if isdir(join(year_path, name))]

        for album_name in album_names:
            print(f"  {album_name}")

            album_path = join(year_path, album_name)
            media_item_names = [name for name in listdir(album_path) if isfile(join(album_path, name))]
            albums[album_name] = media_item_names

            for media_item_name in media_item_names:
                print(f"    {media_item_name}")

def rebuild_db():
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

    parser_path_and_db = subparsers.add_parser('path_and_db', help='Sync check between a local file path and the database')
    parser_path_and_db.set_defaults(func=sync_check_path_and_db)
    parser_path_and_db.add_argument('path', type=str, help='Local file path to photo albums')

    parser_rebuild_db = subparsers.add_parser('rebuild_db', help='Rebuild the database')
    parser_rebuild_db.set_defaults(func=rebuild_db)

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    args.func(args)
