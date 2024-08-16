#!/bin/bash

# Start Redis in the background
redis-server &

# Start Celery worker and beat
celery -A make_celery.celery_app worker -B --loglevel=info --concurrency=1
