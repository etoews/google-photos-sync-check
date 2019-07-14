# Google Photos Sync Check

Python 3

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
python google-photos-sync-check.py path_and_db ~/Pictures
```

## Test

```bash
pipenv shell
python -m pytest
```

## Things

Development things:
* Git
* VS Code
* Python interpreter
* Comments

Python things:
* Python 3.7
* Pyenv
* Pipenv

Python lang things:
* f strings
* list comprehensions
* generators
* argparse
* logging?

Database things:
* SQLite
* SQLAlchemy
  * indexes
  * relationships
  * collection_class

Testing things:
* PyTest
* Travis, ConcourseCI, CircleCI ???
* coverage?
* PyLint

Library things:
* Google API Python Client
