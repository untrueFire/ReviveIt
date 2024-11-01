# reviveit_backend

This is the backend of ReviveIt.

## Project Setup

We recommend to [install `uv`](https://docs.astral.sh/uv/getting-started/installation/) for project management.
```sh
uv sync && \
source .venv/bin/activate && \
./manage.py makemigrations api && \
./manage.py migrate && \
./manage.py createsuperuser
```
If you don't want to use `uv`, you can still use your own tools for local running and testing, just change the first line to `pip install -r requirements.in	`

## Hot-Reload for Development
```sh
./manage.py runserver
```

## Run for production
Refer to the dockerfile.

---

> [!NOTE]
> You may need to install the development dependencies by `pip install -r requirements-dev.in` to run the following
### Run Unit Tests with [Coverage.py](https://coverage.readthedocs.io/en/latest/)

```sh
coverage run --include=api/*.py ./manage.py test
```

### Lint with [PyLint](https://www.pylint.org/)

```sh
uv run pylint --rcfile=.pylintrc api reviveit_backend
```
