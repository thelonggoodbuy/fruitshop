from config.celery import app
from celery import shared_task
import logging


@shared_task
def task_one():
    print("This is task one")


@shared_task
def task_two():
    print("This is task two")
