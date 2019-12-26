# Google Photos Sync Check

Google Photos Sync Check is ...

https://developers.google.com/photos/library/guides/get-started#enable-the-api

save client_secret.json to this dir

## Clean

```bash
find . -name "*.DS_Store" -delete
find . -name "*.json" -delete
find . -name "*(*).HEIC" -delete
```

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
* Python 3.7
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
* decorators?
* types?
* ~memoize~

Database:
* SQLite
* SQLAlchemy
  * indexes
  * relationships
  * collection_class
  * sessions

Testing:
* PyTest
* PyTest-Cov
* PyLint
* TODO: Travis, ConcourseCI, CircleCI ???
* Memory profile?

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
