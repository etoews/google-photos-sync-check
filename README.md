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

## Notable

* Git
* Python 3.7
* Pyenv
* Pipenv
* Google API Python Client
* Generators
* SQLAlchemy
* SQLite
* Structured logging
* f strings
* PyTest
* Travis, ConcourseCI, CircleCI ???
* coverage?
* PyLint
* VS Code
* Python interpreter
* Comments
