from django.contrib.gis import admin
from models import Fire

admin.site.register(Fire, admin.GeoModelAdmin)