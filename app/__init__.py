from flask import Flask
from .celery import celery_init_app
import os

redis_host = os.environ.get("REDISHOST", "localhost")
redis_port = int(os.environ.get("REDISPORT", 6379))
redis_url = f"redis://{redis_host}:{redis_port}"

print(f"[DEBUG]{redis_url}")
def create_app(config_class=None):
    app = Flask(__name__)


    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_mapping(
            CELERY=dict(
                broker_url=f"{redis_url}/0",
                result_backend=f"{redis_url}/1",
                task_ignore_result=True,
                timezone="Asia/Ho_Chi_Minh",
                enable_utc=True,
            ),
            CELERY_QUEUES={
                'default': {
                    'exchange': 'default',
                    'binding_key': 'default',
                },
                'priority_high': {
                    'exchange': 'priority_high',
                    'binding_key': 'priority_high',
                },
            },
            CELERY_ROUTES={
                'app.tasks.add': {'queue': 'priority_high'},
                'app.tasks.subtract': {'queue': 'default'},
                'app.tasks.scheduler': {'queue': 'default'},
            },
        )

    with app.app_context():
        from . import routes  # Import routes

        # Initialize Celery within the app context
        celery_init_app(app)

    return app
