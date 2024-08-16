from celery import shared_task
import time


@shared_task(ignore_result=False)
def add(x, y):
    time.sleep(5)
    return x + y


@shared_task(ignore_result=False)
def subtract(x, y):
    time.sleep(10)
    return x - y


@shared_task(ignore_result=False)
def hello():
    print("Scheduler ...")
    return True
