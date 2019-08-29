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
python google-photos-sync-check.py rebuild_db
python google-photos-sync-check.py sync_check ~/Pictures
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
* TODO: logging

Database:
* SQLite
* SQLAlchemy
  * indexes
  * relationships
  * collection_class

Testing:
* PyTest
* PyTest-Cov
* PyLint
* TODO: Travis, ConcourseCI, CircleCI ???

Library:
* Google API Python Client
* Jinja

Websites:
* [realpython.com](https://realpython.com/)
* sqlachemy
* stackoverflow
* gp api site

Related work:
...
