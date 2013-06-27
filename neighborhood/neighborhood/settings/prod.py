from base import *

import json

with open('/home/dotcloud/environment.json') as f:
  env = json.load(f)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'neighborhood',
        'USER': env['DB_POSTGIS_USER'],
        'PASSWORD': env['DB_POSTGIS_PASSWORD'],
        'HOST': env['DOTCLOUD_DB_SQL_HOST'],
        'PORT': int(env['DOTCLOUD_DB_SQL_PORT']),
    }
}

MEDIA_ROOT = '/home/dotcloud/data/media/'
MEDIA_URL = '/media/'

STATIC_ROOT = '/home/dotcloud/volatile/static/'

BROKER_URL = env['DOTCLOUD_DATA_REDIS_URL']

BROKER_HOST = env['DOTCLOUD_DATA_REDIS_HOST']
BROKER_PORT = int(env['DOTCLOUD_DATA_REDIS_PORT'])
BROKER_USER = env['DOTCLOUD_DATA_REDIS_LOGIN']
BROKER_PASSWORD = env['DOTCLOUD_DATA_REDIS_PASSWORD']
BROKER_VHOST = env['DOTCLOUD_DATA_REDIS_HOST']

CELERYBEAT_SCHEDULE = {
    'get-fire-data': {
        'task': 'tasks.get_fire',
        'schedule': crontab(minute=2, hour='*/2'), # Update 12x per day
    },
    'get-land-use-data': {
        'task': 'tasks.get_land_use',
        'schedule': crontab(minute=7, hour=0),
    },
    'get-building-permit-data': {
        'task': 'tasks.get_building_permits',
        'schedule': crontab(minute=12, hour=0),
    },
    'get-violations-data': {
        'task': 'tasks.get_violations',
        'schedule': crontab(minute=17, hour=0),
    },
    'get-food-violations-data' : {
        'task': 'tasks.get_food_violations',
        'schedule': crontab(minute=22, hour=0),
    },
    'get-police-call-data' : {
        'task': 'tasks.get_police_calls',
        'schedule': crontab(minute=27, hour='*/2'), # Update 12x per day
    },
    'get-police-incident-data' : {
        'task': 'tasks.get_police_incidents',
        'schedule': crontab(minute=32, hour='*/4'), # Update 6x per day
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'logfile': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/supervisor/neighborhood.log', # THIS IS ONLY DIFFERENCE WITH LOCAL SETTING
            'maxBytes': 50000,
            'backupCount': 2,
            'formatter': 'standard',
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers':['console'],
            'propagate': True,
            'level':'WARN',
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        '': { # Empty as want to make available to all apps
            'handlers': ['console', 'logfile'],
            'level': 'DEBUG',
        },
    }
}