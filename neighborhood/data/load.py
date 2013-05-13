import urllib
import urllib2
import json
import datetime
import pytz
import logging

from django.contrib.gis.geos import fromstr

from data.models import Fire, LandPermit, BuildingPermit, Violation, FoodViolation

log = logging.getLogger(__name__)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

FIRE_MAPPING = { # Maps city's fire codes to an aggregate code
    'Boat Taking on Water Major':'Rescue',
    'Tunnel Rescue':'Rescue',
    'WHAZMCI - Hazmat MCI':'Hazmat',
    'Tunnel Fire':'Fire',
    'WAFAH - Auto Fire Alarm Hazmat':'Hazmat',
    'Rescue Confined Space':'Rescue',
    'Rescue Water Major':'Rescue',
    'Aircraft Crash':'Plane Crash',
    'Tanker Fire':'Fire',
    'Rescue Heavy Major':'Rescue',
    'Explosion Minor':'Explosion',
    'HazMat MCI':'Hazmat',
    'Fire House Boat':'Fire',
    '"Spill':'Hazmat',
    '"Hazardous Mat':'Hazmat',
    'Explosion Major':'Explosion',
    'Pier Fire':'Fire',
    'Vault Fire (Electrical)':'Fire',
    'Train Derailment wFireHzmt':'Fire',
    'Dumpster Fire W/Exp.':'Explosion',
    'Natural Gas Leak Major':'Gas Leak',
    'Brush Fire W/Exp.':'Explosion',
    "Boat Under 50' Fire Water":'Fire',
    'Boat Fire In Marina':'Fire',
    "Boat Under 50' Fire Shore":'Fire',
    "Ship Fire 50'on Shore/Pier":'Fire',
    'Multiple Casualty Incident':'Multiple Casualty Incident',
    'Boat Taking Water Minr/Sho':'Rescue',
    'Shed Fire':'Fire',
    'Car Fire W/Exp.':'Explosion',
    'Assault w/Weapons 14':'Assault With Weapons',
    'HAZADV - Hazmat Advised':'Hazmat',
    'Rescue Rope':'Rescue',
    'Tranformer Fire':'Fire',
    '"Assault w/Weapons':'Assault With Weapons',
    'Garage Fire':'Fire',
    'Hazardous Mat- Spill-Leak':'Hazmat',
    'Fire Response Freeway':'Fire',
    'Chimney Fire':'Fire',
    'Rescue Automobile':'Rescue',
    'Rescue Water':'Rescue',
    'Dumpster Fire':'Fire',
    'Natural Gas Leak':'Gas Leak',
    'Car Fire Freeway':'Fire',
    'Bark Fire':'Fire',
    'Rescue Heavy':'Rescue',
    'Brush Fire':'Fire',
    'Fire in Single Family Res':'Fire',
    'Rubbish Fire':'Fire',
    'Assault w/Weap 7 per Rule':'Assault With Weapons',
    'Rescue Lock In/Out':'Rescue',
    'Fire in Building':'Fire',
    'Car Fire':'Fire',
    'Illegal Burn':'Fire',
    'Motor Vehicle Accident Freeway':'Car Accident',
    'Rescue Elevator':'Rescue',
    'Motor Vehicle Accident':'Car Accident',
}

VIOLATION_MAPPING = {
    'PREMISES':'Other',
    'PRESALE':'Other',
    'OTHER CONSTRUCTION':'Other',
    'NONCONSTRUCTION NOISE':'Noise',
    'CONSTRUCTION NOISE':'Noise',
    'MECHANICAL':'Permit Issue',
    'ELECTRICAL':'Permit Issue',
    'BUILDING AND PREMISES':'Vacant/Unfit Building',
    'SIGNS':'Sign Issue',
    'CONDO/COOP CONVERSION':'Condo Coming',
    'JUST CAUSE EVICTION':'Eviction',
    'SITE':'Illegal Construction or Clearing',
    '':'Other',
    'VACANT BUILDING':'Vacant/Unfit Building',
    'HOUSING':'Housing Code Violation',
    'BUILDING':'Illegal Construction or Clearing',
    'WEEDS AND VEGETATION':'Vegetation',
    'ZONING':'Zoning'
}

def get_fire_data():
    # Loads data of City of Seattle 911 Fire calls
    # 
    # JSON response should be of form:
    # {
    #   u'report_location': {u'latitude': u'47.701756', u'needs_recoding': False, u'longitude': u'-122.335022'},
    #   u'longitude': u'-122.335022',
    #   u'address': u'10049 College Way N',
    #   u'latitude': u'47.701756',
    #   u'incident_number': u'F110104009',
    #   u'type': u'Aid Response'
    # }
    
    base_url = "http://data.seattle.gov/resource/kzjm-xkqj.json"
    
    # Bootstrap with last 24 hours worth of data
    #
    # Need to include the timestamp parameter or data returned will not include a datetime field (SERIOUSLY)
    #
    # No timestamp: http://data.seattle.gov/resource/kzjm-xkqj.json
    # Timestamp: http://data.seattle.gov/resource/kzjm-xkqj.json?%24where=datetime%20%3E%20'2013-05-02%2013:00:00'
    #
    # Note that timestap version is equivalent to this code: ?$where=datetime > '2013-05-02 13:00:00'
    
    if Fire.objects.count() == 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
    else:
        latest = Fire.objects.latest('date')
        tz = pytz.timezone('US/Pacific')
        timestamp = latest.date.astimezone(tz).strftime("%F %H:%M:%S")
    
    query = "$where=datetime > '%s'" % timestamp
    # Use custom escaping as Socrata's API doesn't parse standard urllib.quote output properly
    url = base_url + "?" + query.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    try:
        response = urllib2.urlopen(url)
        
        if response.code == 200:
            all_data = json.load(response)
            
            tz = pytz.timezone("US/Pacific")
            for data in all_data:
                if 'incident_number' in data: # First response may be something like: {u'type': u' --T::00'}
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        if data['type'] in FIRE_MAPPING:
                            aggregate_type = FIRE_MAPPING[data['type']]
                        else:
                            aggregate_type = "Other"
                        
                        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
                        initial_date = datetime.datetime.fromtimestamp(float(data['datetime']))
                        
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        
                        date = updated_date
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        fire_obj, created = Fire.objects.get_or_create(
                                                            incident_number=data['incident_number'],
                                                            defaults={
                                                                'address':data['address'],
                                                                'incident_type':data['type'],
                                                                'aggregate_incident_type':aggregate_type,
                                                                'date':date,
                                                                'point':point
                                                            })
                        
                    # From experience, occasionally have missing latitude/longitude
                    except KeyError, e:
                        log.error("Missing key %s in fire data so skipping :: %s" % (e, data['incident_number']))
        
        else:
            log.error("Non-200 code on get_fire_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting fire data: %s" % e.getcode())
        


def get_land_use_data():
    # Loads data of City of Seattle land use permits
    # 
    # JSON response should be of form:
    # {
    #   "permit_type" : "PLAT LBA",
    #   "location" : {
    #     "needs_recoding" : false,
    #     "longitude" : "-122.367945",
    #     "latitude" : "47.54382"
    #   },
    #   "status" : "Application Accepted",
    #   "application_date" : "2013-05-09T00:00:00",
    #   "applicant_name" : "BERNARD, ANDREW",
    #   "application_permit_number" : "3015071",
    #   "edg_required" : "N",
    #   "category" : "MULTIFAMILY",
    #   "appealed_" : "N",
    #   "address" : "6560 HIGH POINT DR SW",
    #   "description" : "Land use application to adjust the boundary between 100 Unit Lots resulting in 53 Unit Lots, 3 tracts (B, C, 31B) for open space and one Tract A for easement. Parcel sizes vary from 1,097sf to 4,163sf",
    #   "value" : "0",
    #   "decision_type" : "I",
    #   "longitude" : "-122.367945",
    #   "latitude" : "47.543820",
    #   "permit_and_complaint_status_url" : {
    #     "url" : "http://web1.seattle.gov/dpd/PermitStatus/Project.aspx?id=3015071"
    #   }
    # }
    
    base_url = "http://data.seattle.gov/resource/uyyd-8gak.json"
    
    if LandPermit.objects.count() == 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
    else:
        latest = LandPermit.objects.latest('application_date')
        tz = pytz.timezone('US/Pacific')
        timestamp = latest.application_date.astimezone(tz).strftime("%F %H:%M:%S")
    
    query = "$where=application_date > '%s'" % timestamp
    url = base_url + "?" + query.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    try:
        response = urllib2.urlopen(url)
        
        if response.code == 200:
            all_data = json.load(response)
            
            tz = pytz.timezone("US/Pacific")
            for data in all_data:
                if 'permit_type' in data: # Test that it's a valid record before processing
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        
                        initial_date = datetime.datetime.strptime(data['application_date'], "%Y-%m-%dT%H:%M:%S")
                        
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        
                        date = updated_date
                        
                        appealed = True if data['appealed_'] == "Y" else False
                        edg_required = True if data['edg_required'] == "Y" else False
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        land_obj, created = LandPermit.objects.get_or_create(
                                                            permit_number=data['application_permit_number'],
                                                            defaults={
                                                                'permit_type':data['permit_type'],
                                                                'status':data['status'],
                                                                'application_date':date,
                                                                'applicant_name':data['applicant_name'],
                                                                'edg_required':edg_required,
                                                                'category':data['category'],
                                                                'appealed':appealed,
                                                                'address':data['address'],
                                                                'description':data['description'],
                                                                'value':int(data['value']),
                                                                'decision_type':data['decision_type'],
                                                                'url':data['permit_and_complaint_status_url']['url'],
                                                                'point':point
                                                            })
                        
                    # From experience, occasionally have missing latitude/longitude
                    except KeyError, e:
                        log.error("Missing key %s in land use data so skipping :: %s" % (e, data['application_permit_number']))
        
        else:
            log.error("Non-200 code on get_land_use_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting land use permit data: %s" % e.getcode())


def get_building_permits_data():
    # Loads data of City of Seattle building permits
    # 
    # JSON response should be of form:
    # {
    # "permit_type" : "Construction",
    #  "location" : {
    #    "needs_recoding" : false,
    #    "longitude" : "-122.369243",
    #    "latitude" : "47.54291191"
    #  },
    #  "status" : "Application Accepted",
    #  "application_date" : "2013-05-09T00:00:00",
    #  "work_type" : "Plan Review",
    #  "applicant_name" : "BERNARD, ANDREW",
    #  "application_permit_number" : "6358023",
    #  "category" : "SINGLE FAMILY / DUPLEX",
    #  "action_type" : "NEW",
    #  "address" : "6646 HIGH POINT DR SW",
    #  "description" : "Establish use as and construct new single family residence with attached garage, per plans.",
    #  "value" : "224630",
    #  "longitude" : "-122.369243",
    #  "latitude" : "47.54291191",
    #  "permit_and_complaint_status_url" : {
    #    "url" : "http://web1.seattle.gov/dpd/PermitStatus/Project.aspx?id=6358023"
    #  }
    # }
    
    base_url = "http://data.seattle.gov/resource/mags-97de.json"
    
    if BuildingPermit.objects.count() == 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
    else:
        latest = LandPermit.objects.latest('application_date')
        tz = pytz.timezone('US/Pacific')
        timestamp = latest.application_date.astimezone(tz).strftime("%F %H:%M:%S")
        
    query = "$where=application_date > '%s'" % timestamp
    url = base_url + "?" + query.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    try:
        response = urllib2.urlopen(url)
        
        if response.code == 200:
            all_data = json.load(response)
            
            tz = pytz.timezone("US/Pacific")
            for data in all_data:
                if 'permit_type' in data: # Test that it's a valid record before processing
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        
                        initial_date = datetime.datetime.strptime(data['application_date'], "%Y-%m-%dT%H:%M:%S")
                        
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        
                        date = updated_date
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        build_obj, created = BuildingPermit.objects.get_or_create(
                                                            permit_number=data['application_permit_number'],
                                                            defaults={
                                                                'permit_type':data['permit_type'],
                                                                'status':data['status'],
                                                                'application_date':date,
                                                                'applicant_name':data['applicant_name'],
                                                                'category':data['category'],
                                                                'action_type':data['action_type'],
                                                                'address':data['address'],
                                                                'description':data['description'],
                                                                'value':int(data['value']),
                                                                'url':data['permit_and_complaint_status_url']['url'],
                                                                'point':point
                                                            })
                                                            
                    # From experience, occasionally have missing latitude/longitude
                    except KeyError, e:
                        log.error("Missing key %s in building permit data so skipping :: %s" % (e, data['application_permit_number']))
                        
        else:
            log.error("Non-200 code on get_building_permits_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting building permit data: %s" % e.getcode())


def get_violations_data():
    # Loads data of City of Seattle code violation cases
    # 
    # JSON response should be of form:
    # {
    # "last_inspection_date" : "2013-05-09T00:00:00",
    #  "case_number" : "1029591",
    #  "status" : "OPEN",
    #  "location" : {
    #    "needs_recoding" : false,
    #    "longitude" : "-122.242624",
    #    "latitude" : "47.510702"
    #  },
    #  "date_case_created" : "2013-05-10T00:00:00",
    #  "case_group" : "ZONING",
    #  "last_inspection_result" : "FAILED",
    #  "address" : "7224 S TAFT ST",
    #  "description" : "The new driveway fence gate/door is over height.",
    #  "longitude" : "-122.242624",
    #  "case_type" : "CITATION",
    #  "latitude" : "47.510702",
    #  "permit_and_complaint_status_url" : {
    #    "url" : "http://web1.seattle.gov/dpd/PermitStatus/Project.aspx?id=1029591"
    #  }
    # }
    
    base_url = "http://data.seattle.gov/resource/dk8m-pdjf.json"
    
    if Violation.objects.count() == 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
    else:
        latest = Violation.objects.latest('date_case_created')
        tz = pytz.timezone('US/Pacific')
        timestamp = latest.date_case_created.astimezone(tz).strftime("%F %H:%M:%S")
    
    query = "$where=date_case_created > '%s'" % timestamp
    url = base_url + "?" + query.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    try:
        response = urllib2.urlopen(url)
        
        if response.code == 200:
            all_data = json.load(response)
            
            tz = pytz.timezone("US/Pacific")
            for data in all_data:
                if 'case_number' in data: # Test that it's a valid record before processing
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        
                        # Date case created
                        initial_date = datetime.datetime.strptime(data['date_case_created'], "%Y-%m-%dT%H:%M:%S")
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        date = updated_date
                        
                        # Date last inspection. Not included with every violation
                        if 'last_inspection_date' in data:
                            initial_date = datetime.datetime.strptime(data['last_inspection_date'], "%Y-%m-%dT%H:%M:%S")
                            updated_date = tz.localize(initial_date)
                            last_inspection_date = updated_date
                            inspection_result = data['last_inspection_result']
                        else:
                            last_inspection_date = None
                            inspection_result = ''
                        
                        
                        if 'case_group' in data: # For some reason, some records don't get a case_group
                            case_group = data['case_group']
                            
                            if data['case_group'] in VIOLATION_MAPPING:
                                category = VIOLATION_MAPPING[data['case_group']]
                            else:
                                category = 'Other'
                        else:
                            case_group = 'Other'
                            category = 'Other'
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        violation_obj, created = Violation.objects.get_or_create(
                                                            case_number=data['case_number'],
                                                            defaults={
                                                                'case_type':data['case_type'],
                                                                'address':data['address'],
                                                                'description':data['description'],
                                                                'case_group':case_group,
                                                                'category':category,
                                                                'date_case_created':date,
                                                                'date_last_inspection':last_inspection_date,
                                                                'last_inspection_result':inspection_result,
                                                                'status':data['status'],
                                                                'url':data['permit_and_complaint_status_url']['url'],
                                                                'point':point
                                                            })
                        
                    except KeyError, e:
                        log.error("Missing key %s in violation data so skipping :: %s" % (e, data['case_number']))
                    
        else:
            log.error("Non-200 code on get_violation_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting code violation data: %s" % e.getcode())


def get_food_violations_data():
    # Loads data of King Count food establishment inspection cases
    # 
    # JSON response should be of form:
    # {
    # "inspection_result" : "Unsatisfactory",
    #  "phone" : "(206) 947-1460",
    #  "inspection_business_name" : "@ The PEAK",
    #  "zip_code" : "98122",
    #  "inspection_score" : "25",
    #  "inspection_type" : "Routine Inspection/Field Review",
    #  "violation_description" : "3400 - Wiping cloths properly used, stored",
    #  "violation_record_id" : "IV6475303",
    #  "inspection_closed_business" : false,
    #  "city" : "SEATTLE",
    #  "violation_type" : "blue",
    #  "inspection_date" : "2013-01-25T00:00:00",
    #  "inspection_serial_num" : "DA2409066",
    #  "address" : "401 BROADWAY ",
    #  "description" : "Seating 13-50 - Risk Category III",
    #  "name" : "@ The PEAK",
    #  "business_id" : "PR0071429",
    #  "longitude" : "-122.3211984964",
    #  "latitude" : "47.6056239308",
    #  "program_identifier" : "@ The PEAK",
    #  "violation_points" : "5"
    # }
    
    base_url = "http://www.datakc.org/resource/f29f-zza5.json"
    
    if FoodViolation.objects.count() == 0:
        timestamp = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
    else:
        latest = FoodViolation.objects.latest('inspection_date')
        tz = pytz.timezone('US/Pacific')
        timestamp = latest.inspection_date.astimezone(tz).strftime("%F %H:%M:%S")
        
    query = "$where=inspection_date > '%s'" % timestamp
    url = base_url + "?" + query.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    try:
        response = urllib2.urlopen(url)
        
        if response.code == 200:
            all_data = json.load(response)
            
            tz = pytz.timezone("US/Pacific")
            for data in all_data:
                if 'inspection_result' in data: # Test that it's a valid record before processing
                    try:
                        # Only interested in failed inspections in Seattle
                        if data['inspection_result'] == 'Unsatisfactory' and data['city'].lower() == 'seattle':
                            point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                            
                            # Date case created
                            initial_date = datetime.datetime.strptime(data['inspection_date'], "%Y-%m-%dT%H:%M:%S")
                            updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                            date = updated_date
                            
                            violation_code = data['violation_description'][0:4]
                            violation_description = data['violation_description'][7:len(data['violation_description'])]
                            
                            # Use get_or_create so that we never risk creating the same incident twice
                            violation_obj, created = FoodViolation.objects.get_or_create(
                                                                violation_record_num=data['violation_record_id'],
                                                                defaults={
                                                                    'name':data['name'],
                                                                    'program_identifier':data['program_identifier'],
                                                                    'inspection_date':date,
                                                                    'place_description':data['description'],
                                                                    'address':data['address'],
                                                                    'business_name':data['inspection_business_name'],
                                                                    'inspection_type':data['inspection_type'],
                                                                    'violation_type':data['violation_type'], # Red or blue. Red must be fixed right away
                                                                    'violation_code':violation_code,
                                                                    'violation_description':violation_description,
                                                                    'inspection_serial_num':data['inspection_serial_num'],
                                                                    'point':point
                                                                })
                            
                    except KeyError, e:
                        log.error("Missing key %s in food violation data so skipping :: %s" % (e, data['violation_record_id']))
        
        else:
            log.error("Non-200 code on get_food_violations_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting food violation data: %s" % e.getcode())

