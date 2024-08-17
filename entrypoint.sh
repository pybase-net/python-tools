#!/bin/bash

## Start Redis in the background
#redis-server &
#
## Wait a few seconds to ensure Redis is up
#sleep 5

# Start Celery worker and beat
# flask run --host=0.0.0.0 --port=8080 &
celery -A make_celery.celery_app worker -B --loglevel=info --concurrency=1
