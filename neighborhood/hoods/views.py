import datetime
import pytz

from django.http import HttpResponse
from django.shortcuts import render_to_response

from hoods.models import Neighborhood
from data.models import Fire, FireIncidentAggregateType
from data.models import BuildingPermit, PermitValue, LandPermit
from data.models import Violation, ViolationAggregateCategory, FoodViolation
from data.models import Police911Incident, Police911Call, PoliceEventAggregateGroup

day_start = datetime.time(0,0,0)
day_end = datetime.time(23,59,59)
pacific = pytz.timezone('US/Pacific')

################# Helper methods #####################
def calculate_neighborhood(neighborhood):
    """
    Takes a string and returns the following: valid neighborhood, all Seattle (true or false), neighborhood object or None if all Seattle
    """
    if neighborhood.lower() == 'seattle':
        return (True, True, None)
    
    try:
        hood = Neighborhood.objects.get(slug=neighborhood.lower())
        return (True, False, hood)
    except Neighborhood.DoesNotExist:
        return (False, False, None)
    


def calculate_date(date="yesterday"):
    # Return following: valid date, datetime date object, label
    if date.lower() == "yesterday":
        yesterday = datetime.datetime.now().date() - datetime.timedelta(1)
        return (True, yesterday, "Yesterday")
    
    if date.lower() == "today":
        today = datetime.datetime.now().date()
        return (True, today, "Today")
    
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
    
    print "label is:"
    print label
    
    return(True, date_obj.date(), label)


def is_weekend(date):
    if date.weekday() < 5:
        return False
    else:
        return True


def get_details(date, neighborhood=None):
    """
    Date is a datetime object. neighborhood is a Neighborhood object.
    """
    
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


################# Actual views #######################
def detail(request, neighborhood, date):
    # Date
    validated_date = calculate_date(date)
    
    weekend = is_weekend(validated_date[1])
    
    if not validated_date[0]:
        return HttpResponse("That's an invalide date. I expect date values of DDMMYYYY or 'yesterday' or 'today'")
    
    # Check neighborhood & get details
    prospective_neighborhood = calculate_neighborhood(neighborhood)
    
    if not prospective_neighborhood[0]:
        return HttpResponse("I've no idea what that neighborhood is")
    
    if prospective_neighborhood[1]:
        neighborhood_name = 'Seattle'
        details = get_details(validated_date[1])
    else:
        neighborhood_name = prospective_neighborhood[2].name
        details = get_details(validated_date[1], prospective_neighborhood[2])
    
    
    # Aggregate permits
    keys = [permit.label for permit in PermitValue.objects.all().order_by('value')]
    #keys = details[3].keys()
    permits = []
    for key in keys:
        permits.append({
            'label':key,
            'land':details[5][key],
            'building':details[3][key]
        })
    
    context = {
        'neighborhood_name': neighborhood_name,
        'date_label': validated_date[2],
        'police_call_count': details[9].count(),
        'police_incident_count': details[11].count(),
        'police_call_detail': details[10],
        'police_incident_detail': details[12],
        'fire_count': details[0].count(),
        'fire_detail': details[1],
        'land_permit_count':details[4].count(),
        'building_permit_count': details[2].count(),
        'permit_detail': permits,
        'weekend': weekend,
        'code_violations_count': details[6].count(),
        'food_violations_count': details[8].count(),
        'code_violations_details': details[7],
    }
    
    return render_to_response('hoods/summary.html', context)
