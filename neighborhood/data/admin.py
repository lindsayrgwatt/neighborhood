from django.contrib.gis import admin
from models import FireIncidentAggregateType, FireIncidentType, Fire
from models import PermitValue, BuildingPermit, LandPermit
from models import ViolationAggregateCategory, ViolationCategory, Violation, FoodViolation
from models import PoliceEventGroup, PoliceEventAggregateGroup, Police911Call, Police911Incident

admin.site.register(FireIncidentAggregateType, admin.GeoModelAdmin)
admin.site.register(FireIncidentType, admin.GeoModelAdmin)
admin.site.register(Fire, admin.GeoModelAdmin)

admin.site.register(PermitValue, admin.GeoModelAdmin)
admin.site.register(LandPermit, admin.GeoModelAdmin)
admin.site.register(BuildingPermit, admin.GeoModelAdmin)

admin.site.register(ViolationAggregateCategory, admin.GeoModelAdmin)
admin.site.register(ViolationCategory, admin.GeoModelAdmin)
admin.site.register(Violation, admin.GeoModelAdmin)
admin.site.register(FoodViolation, admin.GeoModelAdmin)

admin.site.register(PoliceEventGroup, admin.GeoModelAdmin)
admin.site.register(PoliceEventAggregateGroup, admin.GeoModelAdmin)
admin.site.register(Police911Call, admin.GeoModelAdmin)
admin.site.register(Police911Incident, admin.GeoModelAdmin)