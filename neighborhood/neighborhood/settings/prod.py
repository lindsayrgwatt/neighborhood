from base import *

import json

with open('/home/dotcloud/environment.json') as f:
  env = json.load(f)

DEBUG = True
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