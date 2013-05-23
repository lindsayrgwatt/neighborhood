import datetime
import pytz

from django.http import HttpResponse

from hoods.models import Neighborhood
from data.models import Fire, FireIncidentAggregateType
from data.models import BuildingPermit, PermitValue, LandPermit
from data.models import Violation, ViolationAggregateCategory, FoodViolation
from data.models import Police911Incident, Police911Call, PoliceEventAggregateGroup

day_start = datetime.time(0,0,0)
day_end = datetime.time(23,59,59)
pacific = pytz.timezone('US/Pacific')

def calculate_neighborhood(neighborhood):
    # Return following: valid neighborhood, all Seattle (true or false), neighborhood object or None if all Seattle
    if neighborhood.lower() == 'seattle':
        return (True, True, None)
    
    try:
        hood = Neighborhood.objects.get(slug=neighborhood.lower())
        return (True, False, hood)
    except Neighborhood.DoesNotExist:
        return (False, False, None)
    


def calculate_date(date="yesterday"):
    # Return following: valid date, datetime date object, label
    if date == "yesterday":
        yesterday = datetime.datetime.now().date() - datetime.timedelta(1)
        return (True, yesterday, "Yesterday")
        
    try:
        date_obj = datetime.datetime.strptime(date, "%d%m%Y")
    except ValueError:
        return (False, None, "")
    
    now = datetime.datetime.now()
    
    if date_obj.date() > now.date():
        label = "In the future"
    
    elif now.date() == date_obj.date():
        label = "Today"
    
    elif now.date() - date_obj.date() == datetime.timedelta(1):
        label = "Yesterday"
    
    elif now.date() - date_obj.date() == datetime.timedelta(2):
        label = "Two days ago"
    
    elif now.date() - date_obj.date() < datetime.timedelta(7):
        label = "On " + date_obj.strftime("%A")
        
    else:
        label = "On " + date_obj.strftime("%A, %B %d, %Y")
        
    return(True, date_obj.date(), label)


def get_details(date, neighborhood=None):
    # Database stores a datetime object
    date_start = datetime.datetime.combine(date, day_start)
    date_end = datetime.datetime.combine(date, day_end)
    
    # Convert to UTC as timezone is enabled
    datetime_start = pacific.localize(date_start)
    datetime_end = pacific.localize(date_end)
    
    if neighborhood:
        fires = Fire.objects.filter(point__intersects=(neighborhood.mpoly), date__range=(datetime_start, datetime_end))
        building_permits = BuildingPermit.objects.filter(point__intersects=(neighborhood.mpoly), application_date__range=(datetime_start.date(), datetime_end.date()))
        land_permits = LandPermit.objects.filter(point__intersects=(neighborhood.mpoly), application_date__range=(datetime_start.date(), datetime_end.date()))
        code_violations = Violation.objects.filter(point__intersects=(neighborhood.mpoly), date_case_created__range=(datetime_start.date(), datetime_end.date()))
        food_violations = FoodViolation.objects.filter(point__intersects=(neighborhood.mpoly), inspection_date__range=(datetime_start.date(), datetime_end.date()))
        police_calls = Police911Call.objects.filter(point__intersects=(neighborhood.mpoly), date__range=(datetime_start, datetime_end))
        police_incidents = Police911Incident.objects.filter(point__intersects=(neighborhood.mpoly), date__range=(datetime_start, datetime_end))
    else:
        fires = Fire.objects.filter(date__range=(datetime_start, datetime_end))
        building_permits = BuildingPermit.objects.filter(application_date__range=(datetime_start.date(), datetime_end.date()))
        land_permits = LandPermit.objects.filter(application_date__range=(datetime_start.date(), datetime_end.date()))
        code_violations = Violation.objects.filter(date_case_created__range=(datetime_start.date(), datetime_end.date()))
        food_violations = FoodViolation.objects.filter(inspection_date__range=(datetime_start.date(), datetime_end.date()))
        police_calls = Police911Call.objects.filter(date__range=(datetime_start, datetime_end))
        police_incidents = Police911Incident.objects.filter(date__range=(datetime_start, datetime_end))
    
    fire_total = {}
    aggregates = FireIncidentAggregateType.objects.all()
    for aggregate in aggregates:
        fire_total[aggregate.description] = fires.filter(incident_category__aggregate=aggregate).count()
    
    building_permit_total = {}
    land_permit_total = {}
    ranges = PermitValue.objects.all()
    for value in ranges:
        building_permit_total[value.label] = building_permits.filter(value_range=value).count()
        land_permit_total[value.label] = land_permits.filter(value_range=value).count()
    
    code_violation_total = {}
    aggregates = ViolationAggregateCategory.objects.all()
    for aggregate in aggregates:
        if aggregate.category != 'Food Inspection':
            code_violation_total[aggregate.category] = code_violations.filter(group__aggregate=aggregate).count()
        else:
            code_violation_total[aggregate.category] = food_violations.filter(group__aggregate=aggregate).count()
    
    police_call_total = {}
    police_incident_total = {}
    aggregates = PoliceEventAggregateGroup.objects.all()
    for aggregate in aggregates:
        police_call_total[aggregate.category] = police_calls.filter(group__category=aggregate).count()
        police_incident_total[aggregate.category] = police_incidents.filter(group__category=aggregate).count()
    
    return (fires, fire_total, building_permits, building_permit_total, land_permits, land_permit_total, code_violations, code_violation_total, food_violations, police_calls, police_call_total, police_incidents, police_incident_total)


def detail(request, neighborhood, date):
    return HttpResponse("You're looking at neighborhood: %s for date: %s" % (neighborhood, date))
