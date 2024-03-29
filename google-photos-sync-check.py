import argparse, glob, logging, os, signal, sys  # noqa E401

from pathlib import Path
from os import path, getcwd

from httplib2 import Http
from jinja2 import Environment, PackageLoader
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from sqlalchemy import or_, exists

from models.base import Database
from models.models import Album, MediaItem

SCOPES = 'https://www.googleapis.com/auth/photoslibrary.readonly'

logger = logging.getLogger(__name__)


def authn_and_authz():
    store = file.Storage('client_token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
        flags = tools.argparser.parse_args(args=[])
        creds = tools.run_flow(flow, store, flags)

    return build('photoslibrary', 'v1', http=creds.authorize(Http()), static_discovery=False)


def get_album_pages(photoslibrary):
    albums_response = photoslibrary.albums().list().execute()

    while True:
        albums_page = albums_response.get('albums', [])
        logger.debug("Got albums page. Total albums in page: %s", len(albums_page))

        yield albums_page

        nextPageToken = albums_response.get('nextPageToken', None)

        if nextPageToken:
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
        media_items_page = media_items_response.get('mediaItems', [])
        logger.debug("Got media items page for album: %s. Total media items in page: %s",
                     album.title, len(media_items_page))

        yield media_items_page

        nextPageToken = media_items_response.get('nextPageToken', None)

        if nextPageToken:
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


def get_local_albums(local_albums_path):
    if not path.exists(local_albums_path):
        raise FileNotFoundError(local_albums_path)

    logger.debug("Getting local albums from path: %s", local_albums_path)

    albums = set()
    album_paths = glob.glob(f"{local_albums_path}/**/[0-9][0-9][0-9][0-9][ -]*/", recursive=True)

    for album_path in album_paths:
        album = Album(None, Path(album_path).name, album_path)
        albums.add(album)

    return albums


def get_db_albums(db):
    logger.debug("Getting DB albums from DB: %s", db.name)

    with db.session_context() as session:
        albums = session.query(Album).filter(or_(Album.title.like("____ -%"), Album.title.like("____-__-__%")))

    return set(albums)


def sync_check(args):
    path = args.path
    local_albums = get_local_albums(path)
    logger.info("Total number of local albums: %s", len(local_albums))

    db = Database('google-photos-sync-check')
    db_albums = get_db_albums(db)
    logger.info("Total number of DB albums: %s", len(db_albums))

    local_albums_diff = local_albums.difference(db_albums)
    local_albums_diff = sorted(local_albums_diff, key=lambda x: getattr(x, 'title'))

    db_albums_diff = db_albums.difference(local_albums)
    db_albums_diff = sorted(db_albums_diff, key=lambda x: getattr(x, 'title'))

    report(local_albums_diff, db_albums_diff)


def report(local_albums_diff, db_albums_diff):
    env = Environment(loader=PackageLoader('google-photos-sync-check', 'templates'))
    template = env.get_template('report.html')

    report = template.render(local_albums_diff=local_albums_diff, db_albums_diff=db_albums_diff)

    os.makedirs("reports", exist_ok=True)
    with open("reports/report.html", "w") as report_file:
        report_file.write(report)

    logger.info("Report generated at: file://%s/reports/report.html", getcwd())


def refresh_db(args):
    photoslibrary = authn_and_authz()

    db = Database('google-photos-sync-check')

    album_pages = get_album_pages(photoslibrary)

    with db.session_context() as session:
        for album_page in album_pages:
            albums = process_album_page(album_page)

            for album in albums:
                album_exists = session.query(exists().where(Album.title == album.title)).scalar()

                if album_exists:
                    logger.debug("Album already exists: %s", album.title)
                else:
                    media_items_pages = get_media_items_pages(photoslibrary, album)

                    for media_items_page in media_items_pages:
                        media_items = process_media_items_page(media_items_page)

                        for media_item in media_items:
                            album.add_media_item(media_item)

                    session.add(album)
                    session.commit()

                    logger.info("Album added: %s", album.title)


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help="Print debugging messages")

    subparsers = parser.add_subparsers()

    parser_path_and_db = subparsers.add_parser(
        'sync_check', help='Sync check between a local file path and the database of all albums and media items')
    parser_path_and_db.add_argument('path', type=str, help='Local file path to photo albums')
    parser_path_and_db.set_defaults(func=sync_check)

    parser_refresh_db = subparsers.add_parser(
        'refresh_db', help='Refresh the database of all albums and media items from the Google Photos API')
    parser_refresh_db.set_defaults(func=refresh_db)

    return parser.parse_args()


def configure_logging(verbose):
    if verbose:
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO

    logging.basicConfig(format='%(asctime)s.%(msecs)03d, %(levelname)s, %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S', level=logging_level)

    logging.getLogger('oauth2client').setLevel(logging.ERROR)
    logging.getLogger('googleapiclient').setLevel(logging.ERROR)


def signal_handler(signum, frame):
    logger.info("Received signal %s. Exiting.", signal.Signals(signum).name)
    sys.exit(0)


if __name__ == '__main__':
    args = get_args()

    configure_logging(args.verbose)

    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    args.func(args)
