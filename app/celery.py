from celery import Celery, Task
from flask import Flask
from celery.schedules import crontab
# from .tasks import subtract,add,hello

def celery_init_app(app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(
        app.name,
        task_cls=FlaskTask,
    )
    celery_app.config_from_object(app.config["CELERY"])
    celery_app.conf.beat_schedule = {
        # Execute every 1 minute.
        'scheduler-every-minute': {
            'task': 'app.tasks.hello',
            'schedule': crontab('*/1'),
            # 'args': ( "Scheduler started" ),
        },
    }
    celery_app.autodiscover_tasks(['app'])

    celery_app.set_default()
    app.extensions["celery"] = celery_app
    return celery_app

