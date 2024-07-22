from flask import Flask
from .celery import celery_init_app


def create_app(config_class=None):
    app = Flask(__name__)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_mapping(
            CELERY=dict(
                broker_url="redis://localhost:6379",
                result_backend="redis://localhost:6379",
                task_ignore_result=True,
            ),
        )

    with app.app_context():
        from . import routes  # Import routes

        # Initialize Celery within the app context
        celery_init_app(app)

    return app
