from httplib2 import Http
from googleapiclient.discovery import build
from oauth2client import file, client, tools

from models.models import Album, MediaItem

SCOPES = 'https://www.googleapis.com/auth/photoslibrary.readonly'

def authn_and_authz():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('photoslibrary', 'v1', http=creds.authorize(Http()))

def get_albums(photoslibrary):
    albums_response = photoslibrary.albums().list().execute()
    process_response = True
    albums = {}
    while process_response:
        albums_page = albums_response.get('albums', [])
        for album_raw in albums_page:
            album = Album(album_raw['id'], album_raw['title'], album_raw['productUrl'])
            albums[album.title] = album
            print("{0}".format(album))
        nextPageToken = albums_response.get('nextPageToken', None)
        if not nextPageToken is None:
            albums_response = photoslibrary.albums().list(pageToken=nextPageToken).execute()
        else:
            process_response = False
    return albums

def insert_media_items(photoslibrary, album):
    search_params = {'albumId': album.id}
    media_items_response = photoslibrary.mediaItems().search(body=search_params).execute()
    process_response = True
    media_items = {}
    print("{0}".format(album))
    while process_response:
        media_items_page = media_items_response.get('mediaItems', [])
        for media_item_raw in media_items_page:
            media_item = MediaItem(media_item_raw['id'], media_item_raw['filename'], media_item_raw['productUrl'])
            album.insert_media_item(media_item)
            print("  {0}".format(media_item))
        nextPageToken = media_items_response.get('nextPageToken', None)
        if not nextPageToken is None:
            search_params['pageToken'] = nextPageToken
            media_items_response = photoslibrary.mediaItems().search(body=search_params).execute()
        else:
            process_response = False

if __name__ == '__main__':
    photoslibrary = authn_and_authz()
    albums = get_albums(photoslibrary)
    for album_title in albums:
        insert_media_items(photoslibrary, albums[album_title])
