from flask import Flask
from flask_cors import CORS
from .celery import celery_init_app
from .firebase import FirebaseConnector


def create_app(config_class=None):
    app = Flask(__name__)

    cors = CORS(app, resources={r"/*": {"origins": "*"}})

    # ready
    firebase_instance = FirebaseConnector()
    # create connection
    firebase_instance.connect()
    # create collection
    firebase_instance.check_and_create_collection()
    # init firebase data
    user_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    firebase_instance.add_new_users(user_ids=user_ids)

    firebase_instance.add_user_if_not_exists(user_id=11)
    firebase_instance.update_user_notifications(user_id=11, number_of_unnotified_messages=10)

    if config_class:
        app.config.from_object(config_class)
    else:
        app.config.from_mapping(
            CELERY=dict(
                broker_url="redis://localhost:6379/0",
                result_backend="redis://localhost:6379/1",
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
