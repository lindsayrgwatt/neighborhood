from celery import task
from data.load import get_fire_data

@task(name="tasks.get_fire")
def fire_data():
    get_fire_data()
    return "get_fire_data() called"

@task(name="tasks.add")
def add(x, y):
    return x + y
