# Python tools


```sh
poetry init
poetry install
poetry shell
poetry add Flask
```

## Test Celery

```sh
poetry add celery redis
celery -A make_celery.celery_app worker --loglevel=info
```