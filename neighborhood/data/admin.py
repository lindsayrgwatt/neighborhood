from django.contrib.gis import admin
from models import Fire, LandPermit, BuildingPermit

admin.site.register(Fire, admin.GeoModelAdmin)
admin.site.register(LandPermit, admin.GeoModelAdmin)
admin.site.register(BuildingPermit, admin.GeoModelAdmin)