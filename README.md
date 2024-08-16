# Python tools


```sh
poetry init
poetry install
poetry shell
poetry add Flask
```

## Test Flask

```sh
flask run --host=localhost --port=1337 --debug
```

## Test Celery

```sh
poetry add celery redis
celery -A make_celery.celery_app worker --loglevel=info --concurrency=2
# with beat
celery -A make_celery.celery_app worker -B --loglevel=info --concurrency=1
```

Visualize Monitoring

```sh
poetry add flower
celery -A make_celery.celery_app flower
```

```
gcloud builds submit "https://github.com/pybase-net/python-tools.git" --git-source-revision=main --config=cloudbuild.yaml
```