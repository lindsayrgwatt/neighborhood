from celery import task
from data.load import get_fire_data, get_land_use_data, get_building_permits_data, get_violations_data

@task(name="tasks.get_fire", ignore_result=True)
def fire_data():
    return get_fire_data()

@task(name="tasks.get_land_use", ignore_result=True)
def land_use_data():
    return get_land_use_data()


@task(name="tasks.get_building_permits", ignore_result=True)
def building_permit_data():
    return get_building_permits_data()


@task(name="tasks.get_violations", ignore_results=True)
def violations_data():
    return get_violations_data()
