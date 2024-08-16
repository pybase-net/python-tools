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
gcloud config set project playground-s-11-362b4d45

gcloud builds submit "https://github.com/pybase-net/python-tools.git" --git-source-revision=main  --config=cloudbuild.yaml
```

REDIS_BROKER_URL=redis://10.241.102.155:6379/0
REDIS_RESULT_BACKEND=redis://10.241.102.155:6379/1

gcloud compute networks vpc-access connectors create my-vpc-connector \
    --network default \
    --region us-central1 \
    --range 10.8.0.0/28

```sh
gcloud compute networks create my-vpc-network \
    --subnet-mode=custom
gcloud compute networks subnets create my-vpc-subnet \
    --network=my-vpc-network \
    --region=us-central1 \
    --range=10.8.0.0/24
gcloud redis instances create my-redis-instance \
    --size=1 \
    --region=us-central1 \
    --network=my-vpc-network \
    --redis-version=redis_6_x
gcloud compute networks vpc-access connectors create my-vpc-connector \
    --network my-vpc-network \
    --region us-central1 \
    --range 10.8.0.0/28
gcloud run deploy my-cloud-run-service \
    --image gcr.io/my-project/my-image \
    --vpc-connector my-vpc-connector \
    --set-env-vars REDIS_HOST=10.8.0.2,REDIS_PORT=6379 \
    --region us-central1 \
    --allow-unauthenticated

```

```sh
gcloud redis instances create pybase-redis-instance \
    --size=1 \
    --region=us-central1 \
    --network=default \
    --redis-version=redis_6_x

gcloud compute networks vpc-access connectors delete my-vpc-connector \
    --region us-central1

gcloud compute networks vpc-access connectors create my-vpc-connector \
    --network default \
    --region us-central1 \
    --range 10.8.0.0/28 \
    --min-instances 2 \
    --max-instances 3 \
    --machine-type e2-micro

```
