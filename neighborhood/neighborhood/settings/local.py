from base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'neighborhood',
        'USER': 'lindsayrgwatt',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

BROKER_URL = 'redis://localhost:6379/0'
CELERYBEAT_SCHEDULE = { # Store locally so can change values to test queue without futzing prod settings
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
            'filename': PROJECT_ROOT + "/logfile",
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