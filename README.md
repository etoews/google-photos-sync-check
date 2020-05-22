# Google Photos Sync Check

[![CircleCI](https://circleci.com/gh/etoews/google-photos-sync-check/tree/circleci-project-setup.svg?style=svg)](https://circleci.com/gh/etoews/google-photos-sync-check/tree/circleci-project-setup)


Google Photos Sync Check is a utility to check that the albums you have in [Google Photos](https://photos.google.com/) (GP) are in sync with the albums you have locally on disk.

This utility is part of my personal workflow for how I use GP. GP is my primary storage for all of my photos/videos whereas my home server is my backup storage.

Absolutely all of my photos/videos go into albums. Periodically I download all new albums I've uploaded to GP from my phone and other devices using [Google Takeout](https://photos.google.com/). I use this utility to make sure I haven't missed anything and that it's all in sync.

## Enable the API

In order to use this utility, follow the instructions in [Enable the Google Photos Library API](https://developers.google.com/photos/library/guides/get-started#enable-the-api).

As part of that process you'll download a client_secret.json file. Save it to this dir.

## Run

```bash
pipenv install --ignore-pipfile
pipenv shell
python google-photos-sync-check.py --verbose rebuild_db
python google-photos-sync-check.py --verbose sync_check ~/Pictures
```

## Test

```bash
pipenv shell
python -m pytest --cov=.
```

## Notable

Development:
* Git
* VS Code
* Python interpreter
* Docs: [etoews.github.io/google-photos-sync-check/](https://etoews.github.io/google-photos-sync-check/)
* TODO: method and module docs

Python:
* Python 3
* Pyenv
* Pipenv

Python lang features:
* f strings
* list comprehensions
* generators
* argparse
* sets
* context manager
* glob
* lambda
* logging
* signal handler
* TODO: global exception handler
* TODO: types
* ~memoize~

Database:
* SQLite
* [SQLiteOnline](https://sqliteonline.com/)
* SQLAlchemy
  * indexes
  * relationships
  * collection_class
  * sessions

Testing:
* PyTest
* PyTest-Cov
* PyLint
* CircleCI
* TODO: Memory profile

Library:
* [Pipfile](Pipfile)
* Google API Python Client
* Jinja

Websites:
* [Google Photos APIs](https://developers.google.com/photos)
* [realpython.com](https://realpython.com/)
* [SQLAlchemy](https://docs.sqlalchemy.org/en/13/orm/tutorial.html)
* [StackOverflow](https://stackoverflow.com)

Related work:
* [Timeliner](https://github.com/mholt/timeliner)
* [Perkeep](https://perkeep.org)

## Clean

Post Google Takeout cleanup.

```bash
find . -name "*.DS_Store" -delete
find . -name "*.json" -delete
find . -name "*(*).HEIC" -delete
find . -name "*_original" -delete
```
