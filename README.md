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

```sh
gcloud builds submit "https://github.com/pybase-net/python-tools.git" --git-source-revision=main  --config=cloudbuild.yaml
```

## Local

```sh
docker build -t my-celery-app .
docker run -d -p 8080:8080 --name my-celery-container my-celery-app
docker logs my-celery-container --follow
```

## Create redis

```sh
gcloud redis instances create pybaseredis \
    --size=1 \
    --region=us-central1 \
    --redis-version=redis_6_x \
    --tier=standard \
    --labels=env=dev

gcloud auth login
gcloud config set project playground-s-11-4b04a4c2

gcloud builds submit "https://github.com/pybase-net/python-tools.git" --git-source-revision=main  --config=cloudbuild.yaml
```

redis://10.234.41.148:6379/0
redis://10.234.41.148:6379/1