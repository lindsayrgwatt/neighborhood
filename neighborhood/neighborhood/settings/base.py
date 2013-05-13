import os
import djcelery

from datetime import timedelta
from celery.schedules import crontab

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(settings_dir)))

# Django settings for neighborhood project.
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

TIME_ZONE = 'US/Pacific'
# Note that if you change time zone, need to update celery scheduler:
# http://docs.celeryproject.org/en/latest/userguide/periodic-tasks.html

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '9p^(10!s%fhhh2@do)^()cxvvu%cgayxkm!ye9i6v(6xz_t4u1'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'neighborhood.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'neighborhood.wsgi.application'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'neighborhood/templates/'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.gis',
    'south',
    'djcelery',
    'hoods',
    'data',
)

djcelery.setup_loader()

CELERY_IMPORTS = ("data.tasks", )
CELERY_DISABLE_RATE_LIMITS = True
CELERYBEAT_SCHEDULE = { # The 1 minute crontab is for local testing to make sure queue working
    'get-fire-data': {
        'task': 'tasks.get_fire',
        #'schedule': crontab(minute="*/1"),
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'get-land-use-data': {
        'task': 'tasks.get_land_use',
        #'schedule': crontab(minute='*/1'),
        'schedule': crontab(minute='0', hour='*/6'),
    },
    'get-building-permit-data': {
        'task': 'tasks.get_building_permits',
        #'schedule': crontab(minute='*/1'),
        'schedule': crontab(minute='0', hour='*/12'),
    },
    'get-violations-data': {
        'task': 'tasks.get_violations',
        #'schedule': crontab(minute='*/1'),
        'schedule': crontab(minute='0', hour='*/12'),
    },
    'get-food-violations-data' : {
        'task': 'tasks.get_food_violations',
        #'schedule':crontab(minute='*/1'),
        'schedule': crontab(minute='0', hour='*/12'),
    }
}