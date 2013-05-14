from django.contrib.gis import admin
from models import Fire, LandPermit, BuildingPermit, Violation, FoodViolation, Police

admin.site.register(Fire, admin.GeoModelAdmin)
admin.site.register(LandPermit, admin.GeoModelAdmin)
admin.site.register(BuildingPermit, admin.GeoModelAdmin)
admin.site.register(Violation, admin.GeoModelAdmin)
admin.site.register(FoodViolation, admin.GeoModelAdmin)
admin.site.register(Police, admin.GeoModelAdmin)