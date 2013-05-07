from base import *

import json

with open('/home/dotcloud/environment.json') as f:
  env = json.load(f)

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'hood',
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