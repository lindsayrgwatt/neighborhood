import urllib
import urllib2
import json
import datetime
import pytz
import logging
import os
import csv

from django.contrib.gis.geos import fromstr
from django.contrib.gis.geos.error import GEOSException

from data.models import FireIncidentAggregateType, FireIncidentType, Fire
from data.models import PermitValue, LandPermit, BuildingPermit
from data.models import ViolationAggregateCategory, ViolationCategory, Violation, FoodViolation
from data.models import HundredBlockSection, ZoneBeat, DistrictSector, CensusTract, ClearanceCode, PoliceEventDetail, PoliceEventAggregateGroup, PoliceEventGroup, PoliceOffenseCode, PoliceOffenseCodeExtension, PoliceSummaryOffenseCode, Police

log = logging.getLogger(__name__)

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

utc = pytz.utc

CUTOFF_DATE = datetime.datetime(2011, 1, 1, 0, 0, 0)
tz = pytz.timezone("US/Pacific")
CUTOFF_DATE = tz.localize(CUTOFF_DATE)

#################################
#
# Fire
#
def create_fire_incident_objects():
    false_alarm = FireIncidentAggregateType.objects.create(description='False Alarm')
    medic_aid = FireIncidentAggregateType.objects.create(description='Medical or Aid Response')
    hazmat = FireIncidentAggregateType.objects.create(description='Hazmat, Gas Leak or Explosion')
    fire = FireIncidentAggregateType.objects.create(description='Fire')
    rescue = FireIncidentAggregateType.objects.create(description='Rescue')
    car = FireIncidentAggregateType.objects.create(description='Car Accident')
    assault = FireIncidentAggregateType.objects.create(description='Weapon Assault/Multiple Casulaties')
    other = FireIncidentAggregateType.objects.create(description='Other')
    
    temp1 = FireIncidentType(description="LINK - Link Control Center", aggregate=other).save()
    temp2 = FireIncidentType(description="Mutual Aid- Strike Team Lad", aggregate=other).save()
    temp3 = FireIncidentType(description="Tunnel Rescue", aggregate=rescue).save()
    temp4 = FireIncidentType(description="Tunnel Medic", aggregate=medic_aid).save()
    temp5 = FireIncidentType(description="Mutual Aid- Hazmat", aggregate=hazmat).save()
    temp6 = FireIncidentType(description="Mutual Aid- Adv. Life", aggregate=medic_aid).save()
    temp7 = FireIncidentType(description="Tank Farm", aggregate=other).save()
    temp8 = FireIncidentType(description="Mutual Aid- Tech Res", aggregate=medic_aid).save()
    tmep9 = FireIncidentType(description="Tanker Fire", aggregate=fire).save()
    temp10 = FireIncidentType(description="ANTIB - Antibiotic Delivery", aggregate=other).save()
    temp11 = FireIncidentType(description="Automatic Aid Dist 11", aggregate=other).save()
    temp12 = FireIncidentType(description="Aircraft Standby", aggregate=other).save()
    temp13 = FireIncidentType(description="Rescue Confined Space", aggregate=other).save()
    temp14 = FireIncidentType(description="QAID- Quick Dispatch Aid Call", aggregate=medic_aid).save()
    temp15 = FireIncidentType(description="Automatic Fire Dist 11", aggregate=other).save()
    temp16 = FireIncidentType(description="MCI Major", aggregate=other).save()
    temp17 = FireIncidentType(description="Explosion Major", aggregate=hazmat).save()
    temp18 = FireIncidentType(description="Help the Fire Fighter", aggregate=other).save()
    temp19 = FireIncidentType(description="Mutual Aid- Strike Eng.", aggregate=other).save()
    temp20 = FireIncidentType(description="Rescue Water Major", aggregate=rescue).save()
    temp21 = FireIncidentType(description="COMED Poss Patient", aggregate=other).save()
    temp22 = FireIncidentType(description="W1RED - 1  Unit", aggregate=other).save()
    temp23 = FireIncidentType(description="Train Derailment wFireHzmt", aggregate=hazmat).save()
    temp24 = FireIncidentType(description="Tunnel Aid", aggregate=medic_aid).save()
    temp25 = FireIncidentType(description="Hazardous Material w/Fire", aggregate=hazmat).save()
    temp26 = FireIncidentType(description="Quick Aid Response", aggregate=medic_aid).save()
    temp27 = FireIncidentType(description="Explosion Minor", aggregate=hazmat).save()
    temp28 = FireIncidentType(description="Fire House Boat", aggregate=fire).save()
    temp29 = FireIncidentType(description="Mutual Aid- Task Force", aggregate=medic_aid).save()
    temp30 = FireIncidentType(description="MUK9 - FIU CAPTAIN K9", aggregate=other).save()
    temp31 = FireIncidentType(description="Rescue Heavy Major", aggregate=rescue).save()
    temp31 = FireIncidentType(description="HazMat MCI", aggregate=hazmat).save()
    temp32 = FireIncidentType(description="AFA4 - Auto Alarm 2 + 1 + 1", aggregate=false_alarm).save()
    temp33 = FireIncidentType(description="Dumpster Fire W/Exp.", aggregate=fire).save()
    temp34 = FireIncidentType(description="Pier Fire", aggregate=fire).save()
    temp35 = FireIncidentType(description="Hazardous Decon", aggregate=hazmat).save()
    temp36 = FireIncidentType(description="Natural Gas Leak Major", aggregate=hazmat).save()
    temp37 = FireIncidentType(description="Reduce Resp Opposite Tunnel", aggregate=other).save()
    temp38 = FireIncidentType(description="Mutual Aid- Ladder", aggregate=medic_aid).save()
    temp39 = FireIncidentType(description="Vault Fire (Electrical)", aggregate=fire).save()
    temp40 = FireIncidentType(description="Boat Taking Water Minr/Sho", aggregate=rescue).save()
    temp41 = FireIncidentType(description="Boat Fire In Marina", aggregate=fire).save()
    temp42 = FireIncidentType(description="Water Job Major", aggregate=other).save()
    temp43 = FireIncidentType(description="Boat Under 50' Unknown", aggregate=other).save()
    temp44 = FireIncidentType(description="Boat Under 50' Fire Shore", aggregate=fire).save()
    temp45 = FireIncidentType(description="Ship Fire 50'on Shore/Pier", aggregate=fire).save()
    temp46 = FireIncidentType(description="Multiple Casualty Incident", aggregate=assault).save()
    temp47 = FireIncidentType(description="Mutual Aid- Aid", aggregate=medic_aid).save()
    temp48 = FireIncidentType(description="Boat Under 50' Fire Water", aggregate=fire).save()
    temp49 = FireIncidentType(description="RMC Chief", aggregate=other).save()
    temp50 = FireIncidentType(description="Drill", aggregate=other).save()
    temp51 = FireIncidentType(description="Multiple Medic Resp 14 Per", aggregate=medic_aid).save()
    temp52 = FireIncidentType(description="Brush Fire W/Exp.", aggregate=fire).save()
    temp53 = FireIncidentType(description="temp Car Fire W/Exp.", aggregate=fire).save()
    temp54 = FireIncidentType(description="Shed Fire", aggregate=fire).save()
    temp55 = FireIncidentType(description="Assault w/Weapons 14", aggregate=fire).save()
    temp56 = FireIncidentType(description="HAZADV - Hazmat Advised", aggregate=hazmat).save()
    temp57 = FireIncidentType(description="Spill- Non-Hazmat", aggregate=other).save()
    temp58 = FireIncidentType(description="Rescue Rope", aggregate=rescue).save()
    temp59 = FireIncidentType(description="Garage Fire", aggregate=fire).save()
    temp60 = FireIncidentType(description="Mutual Aid- Engine", aggregate=medic_aid).save()
    temp61 = FireIncidentType(description="Hazardous Mat- Spill-Leak", aggregate=hazmat).save()
    temp62 = FireIncidentType(description="Furnace Problem", aggregate=false_alarm).save()
    temp63 = FireIncidentType(description="Tranformer Fire", aggregate=fire).save()
    temp64 = FireIncidentType(description="Fire Response Freeway", aggregate=fire).save()
    temp65 = FireIncidentType(description="HazMat Reduced", aggregate=hazmat).save()
    temp66 = FireIncidentType(description="Hang-Up- Fire", aggregate=fire).save()
    temp67 = FireIncidentType(description="Mutual Aid- Medic", aggregate=medic_aid).save()
    temp68 = FireIncidentType(description="Chempack Engine", aggregate=other).save()
    temp69 = FireIncidentType(description="Aid Service", aggregate=medic_aid).save()
    temp70 = FireIncidentType(description="Quick Dispatch Medic 7", aggregate=medic_aid).save()
    temp71 = FireIncidentType(description="TEST - MIS TEST", aggregate=other).save()
    temp72 = FireIncidentType(description="Food On The Stove Out", aggregate=false_alarm).save()
    temp73 = FireIncidentType(description="Rescue Automobile", aggregate=rescue).save()
    temp74 = FireIncidentType(description="Chimney Fire", aggregate=fire).save()
    temp75 = FireIncidentType(description="Quick Dispatch Medic", aggregate=medic_aid).save()
    temp76 = FireIncidentType(description="Medic Response Freeway", aggregate=medic_aid).save()
    temp77 = FireIncidentType(description="Rescue Water", aggregate=rescue).save()
    temp78 = FireIncidentType(description="Food On The Stove", aggregate=fire).save()
    temp79 = FireIncidentType(description="Natural Gas Leak", aggregate=hazmat).save()
    temp80 = FireIncidentType(description="3RED - 1 +1 + 1", aggregate=fire).save()
    temp81 = FireIncidentType(description="Dumpster Fire", aggregate=fire).save()
    temp82 = FireIncidentType(description="Assault w/Weapons- Aid", aggregate=assault).save()
    temp83 = FireIncidentType(description="Investigate In Service", aggregate=other).save()
    temp84 = FireIncidentType(description="Car Fire Freeway", aggregate=fire).save()
    temp85 = FireIncidentType(description="Single Medic Unit", aggregate=medic_aid).save()
    temp86 = FireIncidentType(description="Fuel Spill", aggregate=hazmat).save()
    temp87 = FireIncidentType(description="Wires Down", aggregate=other).save()
    temp88 = FireIncidentType(description="Aid Response Freeway", aggregate=medic_aid).save()
    temp89 = FireIncidentType(description="Bark Fire", aggregate=fire).save()
    temp90 = FireIncidentType(description="Rescue Heavy", aggregate=rescue).save()
    temp91 = FireIncidentType(description="Brush Fire", aggregate=fire).save()
    temp92 = FireIncidentType(description="Electrical Problem", aggregate=false_alarm).save()
    temp93 = FireIncidentType(description="Rubbish Fire", aggregate=fire).save()
    temp94 = FireIncidentType(description="Fire in Single Family Res", aggregate=fire).save()
    temp95 = FireIncidentType(description="Assault w/Weap 7 per Rule", aggregate=assault).save()
    temp96 = FireIncidentType(description="Rescue Lock In/Out", aggregate=rescue).save()
    temp97 = FireIncidentType(description="Activated CO Detector", aggregate=false_alarm).save()
    temp98 = FireIncidentType(description="Fire in Building", aggregate=fire).save()
    temp99 = FireIncidentType(description="4RED - 2 + 1 + 1", aggregate=fire).save()
    temp100 = FireIncidentType(description="Unk Odor", aggregate=false_alarm).save()
    temp101 = FireIncidentType(description="EVENT - Special Event", aggregate=other).save()
    temp102 = FireIncidentType(description="Water Job Minor", aggregate=other).save()
    temp103 = FireIncidentType(description="Natural Gas Odor", aggregate=false_alarm).save()
    temp104 = FireIncidentType(description="Car Fire", aggregate=fire).save()
    temp105 = FireIncidentType(description="Automatic Fire Alarm False", aggregate=false_alarm).save()
    temp106 = FireIncidentType(description="Alarm Bell", aggregate=false_alarm).save()
    temp107 = FireIncidentType(description="Illegal Burn", aggregate=fire).save()
    temp108 = FireIncidentType(description="Hang-Up- Aid", aggregate=medic_aid).save()
    temp109 = FireIncidentType(description="Investigate Out Of Service", aggregate=other).save()
    temp110 = FireIncidentType(description="Medic Response- 6 per Rule", aggregate=medic_aid).save()
    temp111 = FireIncidentType(description="Motor Vehicle Accident Freeway", aggregate=car).save()
    temp112 = FireIncidentType(description="Rescue Elevator", aggregate=rescue).save()
    temp113 = FireIncidentType(description="1RED 1 Unit", aggregate=fire).save()
    temp114 = FireIncidentType(description="Medic Response- 7 per Rule", aggregate=medic_aid).save()
    temp115 = FireIncidentType(description="Automatic Medical Alarm", aggregate=medic_aid).save()
    temp116 = FireIncidentType(description="Automatic Fire Alarm Resd", aggregate=false_alarm).save()
    temp117 = FireIncidentType(description="Aid Response Yellow", aggregate=medic_aid).save()
    temp118 = FireIncidentType(description="Motor Vehicle Accident", aggregate=car).save()
    temp119 = FireIncidentType(description="Trans to AMR", aggregate=medic_aid).save()
    temp120 = FireIncidentType(description="Auto Fire Alarm", aggregate=false_alarm).save()
    temp121 = FireIncidentType(description="Medic Response", aggregate=medic_aid).save()
    temp121 = FireIncidentType(description="Aid Response", aggregate=medic_aid).save()
    temp122 = FireIncidentType(description="Car Fire W/Exp.", aggregate=fire).save()


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
                        
                        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
                        
                        initial_date = datetime.datetime.fromtimestamp(float(data['datetime']))               
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        date = updated_date
                        
                        incident_category_obj, created = FireIncidentType.objects.get_or_create(description=data['type'].strip())
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        fire_obj, created = Fire.objects.get_or_create(
                                                            incident_number=data['incident_number'],
                                                            defaults={
                                                                'address':data['address'],
                                                                'incident_category':incident_category_obj,
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
        


def load_historical_fire_data():
    fire = open(os.path.dirname(__file__) + "/historical/Seattle_Real_Time_Fire_911_Calls.csv")
    
    reader = csv.reader(fire, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        if counter != 0:
            initial_date = datetime.datetime.strptime(line[2][:-6], "%m/%d/%Y %I:%M:%S %p") # [:-6] is because %z doesn't work
            interstitial_date = utc.localize(initial_date)
            updated_date = interstitial_date.astimezone(tz)
            date = updated_date
            
            if date >= CUTOFF_DATE and line[3] != '' and line[4] != '': # Verify that match date range and have lat/lng
                try:
                    point = fromstr("POINT(%s %s)" % (line[4], line[3]))
                    
                    incident_category_obj, created = FireIncidentType.objects.get_or_create(description=line[1].strip())
                    
                    # Use get_or_create so that we never risk creating the same incident twice
                    fire_obj, created = Fire.objects.get_or_create(
                                                        incident_number=line[6],
                                                        defaults={
                                                            'address':line[0],
                                                            'incident_category':incident_category_obj,
                                                            'date':date,
                                                            'point':point
                                                        })
                    if created:
                        new_record += 1
                except GEOSException, e:
                    log.error("Geo Error %s importing historical fire record with incident number %s" % (e, line[6]))
                    
        if counter % 1000 == 0:
            log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
        counter += 1
        
    log.info("Created %d new fire records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
    
    fire.close()
    


#################################
#
# Permits
#
def create_permit_ranges():
    ranges = {
        '<= $1':1,
        '<= $1,000':1000,
        '<= $10,000':10000,
        '<= $50,000':50000,
        '<= $100,000':100000,
        '<= $1,000,000':1000000,
        '<= $10,000,000':10000000,
        '> $10,000,000':10000001
    }
    
    for entry in ranges:
        permit_obj, status = PermitValue.objects.get_or_create(label=entry, value=ranges[entry])
    


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
        latest = BuildingPermit.objects.latest('application_date')
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
                                                                'work_type':data['work_type'],
                                                                'point':point
                                                            })
                                                            
                    # From experience, occasionally have missing latitude/longitude
                    except KeyError, e:
                        log.error("Missing key %s in building permit data so skipping :: %s" % (e, data['application_permit_number']))
                        
        else:
            log.error("Non-200 code on get_building_permits_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting building permit data: %s" % e.getcode())


def load_historical_land_use_data():
    land = open(os.path.dirname(__file__) + "/historical/Land_Use_Permits.csv")
    
    reader = csv.reader(land, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        if counter != 0:
            initial_date = datetime.datetime.strptime(line[9], "%m/%d/%Y")
            updated_date = tz.localize(initial_date)
            date = updated_date
            
            if date >= CUTOFF_DATE and line[16] and line[17]: # Skip if no lat/longs
                try:
                    point = fromstr("POINT(%s %s)" % (line[17], line[16]))
                    
                    appealed = True if line[11] == "Y" else False
                    edg_required = True if line[6] == "Y" else False
                    
                    # Use get_or_create so that we never risk creating the same incident twice
                    land_obj, created = LandPermit.objects.get_or_create(
                                                        permit_number=int(line[0]),
                                                        defaults={
                                                            'permit_type':line[1],
                                                            'status':line[13],
                                                            'application_date':date,
                                                            'applicant_name':line[8],
                                                            'edg_required':edg_required,
                                                            'category':line[4],
                                                            'appealed':appealed,
                                                            'address':line[2],
                                                            'description':line[3],
                                                            'value':int(float(line[7][1:len(line[7])])), # Remove leading $
                                                            'decision_type':line[5][0:1],
                                                            'url':line[15],
                                                            'point':point
                                                        })
                                                        
                    if created:
                        new_record += 1
                except GEOSException, e:
                    log.error("Geo Error %s importing historical land use record with permit number %s" % (e, line[0]))
                    
        if counter % 1000 == 0:
            log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
        counter += 1
        
    log.info("Created %d new land use records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
    
    land.close()


def load_historical_building_permit_data():
    building = open(os.path.dirname(__file__) + "/historical/Building_Permits___Current.csv")
    
    reader = csv.reader(building, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        if counter != 0:
            initial_date = datetime.datetime.strptime(line[9], "%m/%d/%Y")
            updated_date = tz.localize(initial_date)
            date = updated_date
            
            if date >= CUTOFF_DATE and line[16] and line[17]: # Skip if no lat/longs
                try:
                    point = fromstr("POINT(%s %s)" % (line[17], line[16]))
                    
                    # Use get_or_create so that we never risk creating the same incident twice
                    building_obj, created = BuildingPermit.objects.get_or_create(
                                                        permit_number=line[0],
                                                        defaults={
                                                            'permit_type':line[1],
                                                            'status':line[13],
                                                            'application_date':date,
                                                            'applicant_name':line[8],
                                                            'category':line[4],
                                                            'action_type':line[5],
                                                            'address':line[2],
                                                            'description':line[3],
                                                            'value':int(float(line[7][1:len(line[7])])), # Remove leading $
                                                            'work_type':line[6],
                                                            'url':line[15],
                                                            'point':point
                                                        })
                                                        
                    if created:
                        new_record += 1
                except GEOSException, e:
                    log.error("Geo Error %s importing historical building permit record with permit number %s" % (e, line[0])) # Means no lat/lng
                    
        if counter % 1000 == 0:
            log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
        counter += 1
        
    log.info("Created %d new building permit records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
    
    building.close()
    


#################################
#
# Code Violations
#
def create_violation_aggregates():
    other, status = ViolationAggregateCategory.objects.get_or_create(category='Other')
    noise, status = ViolationAggregateCategory.objects.get_or_create(category='Noise')
    permit, status = ViolationAggregateCategory.objects.get_or_create(category='Permit Issue')
    building, status = ViolationAggregateCategory.objects.get_or_create(category='Vacant/Unfit Building')
    sign, status = ViolationAggregateCategory.objects.get_or_create(category='Sign Issue')
    condo, status = ViolationAggregateCategory.objects.get_or_create(category='Condo Coming')
    eviction, status = ViolationAggregateCategory.objects.get_or_create(category='Eviction')
    construction, status = ViolationAggregateCategory.objects.get_or_create(category='Illegal Construction or Clearing')
    housing, status = ViolationAggregateCategory.objects.get_or_create(category='Housing Code Violation')
    vegetation, status = ViolationAggregateCategory.objects.get_or_create(category='Vegetation')
    zoning, status = ViolationAggregateCategory.objects.get_or_create(category='Zoning')
    food, status = ViolationAggregateCategory.objects.get_or_create(category='Food Inspection')
    
    violation_mapping = {
        'PREMISES':other,
        'PRESALE':other,
        'OTHER CONSTRUCTION':other,
        'NONCONSTRUCTION NOISE':noise,
        'CONSTRUCTION NOISE':noise,
        'MECHANICAL':permit,
        'ELECTRICAL':permit,
        'BUILDING AND PREMISES':building,
        'SIGNS':sign,
        'CONDO/COOP CONVERSION':condo,
        'JUST CAUSE EVICTION':eviction,
        'SITE':construction,
        '':other,
        'Other':other,
        'VACANT BUILDING':building,
        'HOUSING':housing,
        'BUILDING':construction,
        'WEEDS AND VEGETATION':vegetation,
        'ZONING':zoning,
        'FOOD INSPECTION':food
    }
    
    for violation in violation_mapping:
        category, status = ViolationCategory.objects.get_or_create(category=violation, aggregate=violation_mapping[violation])
    


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
                        
                        if 'case_group' in data:
                            category, status = ViolationCategory.objects.get_or_create(category=data['case_group'],
                                                            defaults={
                                                                'aggregate':ViolationAggregateCategory.objects.get(category='Other')
                                                            })
                        else:
                            category = ViolationCategory.objects.get(category='Other')
                        
                        aggregate = category.aggregate
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        violation_obj, created = Violation.objects.get_or_create(
                                                            case_number=data['case_number'],
                                                            defaults={
                                                                'case_type':data['case_type'],
                                                                'address':data['address'],
                                                                'description':data['description'],
                                                                'group':category,
                                                                'aggregate':aggregate,
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
    # Loads data of King County food establishment inspection cases
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
                            
                            category = ViolationCategory.objects.get(category='FOOD INSPECTION')
                            
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
                                                                    'group':category,
                                                                    'aggregate':category.aggregate,
                                                                    'point':point
                                                                })
                            
                    except KeyError, e:
                        log.error("Missing key %s in food violation data so skipping :: %s" % (e, data['violation_record_id']))
        
        else:
            log.error("Non-200 code on get_food_violations_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting food violation data: %s" % e.getcode())


def load_historical_violations_data():
    violations = open(os.path.dirname(__file__) + "/historical/Code_Violation_Cases.csv")
    
    reader = csv.reader(violations, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        if counter != 0:
            initial_date = datetime.datetime.strptime(line[5], "%m/%d/%Y")
            updated_date = tz.localize(initial_date)
            date = updated_date
            
            if date >= CUTOFF_DATE and line[10] and line[11]: # Skip if missing lat/longs
                try:
                    point = fromstr("POINT(%s %s)" % (line[11], line[10]))
                    
                    # Date last inspection. Not included with every violation
                    if line[6]:
                        initial_date = datetime.datetime.strptime(line[6], "%m/%d/%Y")
                        updated_date = tz.localize(initial_date)
                        last_inspection_date = updated_date
                        inspection_result = line[7]
                    else:
                        last_inspection_date = None
                        inspection_result = ''
                        
                        
                    if line[4]: # For some reason, some records don't get a case_group
                        case_group = line[4]
                        
                        if line[4] in VIOLATION_MAPPING:
                            category = VIOLATION_MAPPING[line[4]]
                        else:
                            category = 'Other'
                    else:
                        case_group = 'Other'
                        category = 'Other'
                        
                    # Use get_or_create so that we never risk creating the same incident twice
                    violation_obj, created = Violation.objects.get_or_create(
                                                        case_number=line[0],
                                                        defaults={
                                                            'case_type':line[1],
                                                            'address':line[2],
                                                            'description':line[3],
                                                            'case_group':case_group,
                                                            'category':category,
                                                            'date_case_created':date,
                                                            'date_last_inspection':last_inspection_date,
                                                            'last_inspection_result':inspection_result,
                                                            'status':line[8],
                                                            'url':line[9],
                                                            'point':point
                                                        })
                    if created:
                        new_record += 1
                except GEOSException, e:
                    log.error("Geo Error %s importing historical violation record with permit number %s" % (e, line[0])) # Means no lat/lng
                    
        if counter % 1000 == 0:
            log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
        counter += 1
        
    log.info("Created %d new violation records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
    
    violations.close()


def load_historical_food_violations_data():
    violations = open(os.path.dirname(__file__) + "/historical/Food_Establishment_Inspection_Data.csv")
    
    reader = csv.reader(violations, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        if counter != 0:
            initial_date = datetime.datetime.strptime(line[2], "%m/%d/%Y")
            updated_date = tz.localize(initial_date)
            date = updated_date
            
            # King County - will include non-Seattle locations
            # Skip if no lat/longs
            if date >= CUTOFF_DATE and line[5].lower() == 'seattle' and line[8] and line[9]:
                try:
                    point = fromstr("POINT(%s %s)" % (line[8], line[9]))
                    
                    violation_code = line[16][0:4]
                    violation_description = line[16][7:len(line[16])]
                    
                    # Use get_or_create so that we never risk creating the same incident twice
                    # This is critical as when I tried downloading the data from King County, some identical records appeared multiple times
                    violation_obj, created = FoodViolation.objects.get_or_create(
                                                        violation_record_num=line[20],
                                                        defaults={
                                                            'name':line[0],
                                                            'program_identifier':line[1],
                                                            'inspection_date':date,
                                                            'place_description':line[3],
                                                            'address':line[4],
                                                            'business_name':line[10],
                                                            'inspection_type':line[11],
                                                            'violation_type':line[15], # Red or blue. Red must be fixed right away
                                                            'violation_code':violation_code,
                                                            'violation_description':violation_description,
                                                            'inspection_serial_num':line[19],
                                                            'point':point
                                                        })
                    
                    if created:
                        new_record += 1
                except GEOSException, e:
                    log.error("Geo Error %s importing historical food violation record with violation record id %s" % (e, line[20])) # Means no lat/lng
        
        if counter % 1000 == 0:
            log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
        
        counter += 1
    
    log.info("Created %d new food violation records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
    
    violations.close()


#################################
#
# Police
#
def create_police_detail_objects():
    traffic, status = PoliceEventAggregateGroup.objects.get_or_create(category="Traffic")
    other, status = PoliceEventAggregateGroup.objects.get_or_create(category="Other")
    arrest, status = PoliceEventAggregateGroup.objects.get_or_create(category="Arrest")
    assault, status = PoliceEventAggregateGroup.objects.get_or_create(category="Assault, Threats and Weapons")
    theft, status = PoliceEventAggregateGroup.objects.get_or_create(category="Theft or Similar")
    mischief, status = PoliceEventAggregateGroup.objects.get_or_create(category="Mischief and Suspicious People")
    disturbance, status = PoliceEventAggregateGroup.objects.get_or_create(category="Disturbances")
    vice, status = PoliceEventAggregateGroup.objects.get_or_create(category="Prostitution, Vice and Gambling")
    drugs, status = PoliceEventAggregateGroup.objects.get_or_create(category="Drugs and Liquor")
    homicide, status = PoliceEventAggregateGroup.objects.get_or_create(category="Homicide")
    false_alarm, status = PoliceEventAggregateGroup.objects.get_or_create(category="False Alarm")
    
    CRIME_MAPPING = {
        'ACCIDENT INVESTIGATION':traffic,
        'ANIMAL COMPLAINT':other,
        'ANIMAL COMPLAINTS':other,
        'ARREST':arrest,
        'ASSAULT':assault,
        'ASSAULTS':assault,
        'AUTO THEFTS':theft,
        'BIAS INCIDENT':other,
        'BIKE':other,
        'BIKE THEFT':theft,
        'BURGLARY':theft,
        'BURGLARY-SECURE PARKING-RES':theft,
        'Bike Theft':theft,
        'CAR PROWL':mischief,
        'COUNTERFEIT':theft,
        'Car Prowl':mischief,
        'DISORDERLY CONDUCT':disturbance,
        'DISPUTE':disturbance,
        'DISTURBANCE':disturbance,
        'DISTURBANCES':disturbance,
        'DRIVE BY (NO INJURY)':disturbance,
        'DUI':drugs,
        'ELUDING':arrest,
        'EMBEZZLE':theft,
        'ESCAPE':other,
        'EXTORTION':theft,
        'FAILURE TO REGISTER (SEX OFFENDER)':other,
        'FALSE ALARMS':false_alarm,
        'FALSE REPORT':false_alarm,
        'FIREWORK':disturbance,
        'FORGERY':theft,
        'FRAUD':theft,
        'FRAUD AND FINANCIAL':theft,
        'FRAUD CALLS':theft,
        'GAMBLE':vice,
        'HARBOR CALLS':other,
        'HAZARDS':other,
        'HOMICIDE':homicide,
        'ILLEGAL DUMPING':disturbance,
        'INJURY':other,
        'LEWD CONDUCT':disturbance,
        'LIQUOR VIOLATION':drugs,
        'LIQUOR VIOLATIONS':drugs,
        'LOITERING':mischief,
        'LOST PROPERTY':other,
        'MAIL THEFT':theft,
        'MENTAL HEALTH':other,
        'MISCELLANEOUS MISDEMEANORS':other,
        'NARCOTICS':drugs,
        'NARCOTICS COMPLAINTS':drugs,
        'NUISANCE, MISCHIEF':mischief,
        'OBSTRUCT':other,
        'OTHER PROPERTY':theft,
        'OTHER VICE':vice,
        'Other Property':theft,
        'PERSON DOWN/INJURY':other,
        'PERSONS - LOST, FOUND, MISSING':other,
        'PICKPOCKET':theft,
        'PORNOGRAPHY':vice,
        'PROPERTY - MISSING, FOUND':other,
        'PROPERTY DAMAGE':disturbance,
        'PROSTITUTION':vice,
        'PROWLER':mischief,
        'PUBLIC NUISANCE':mischief,
        'PURSE SNATCH':theft,
        'Pickpocket':theft,
        'Purse Snatch':theft,
        'RECKLESS BURNING':disturbance,
        'RECOVERED PROPERTY':other,
        'ROBBERY':theft,
        'SHOPLIFTING':theft,
        'STAY OUT OF AREA OF DRUGS':drugs,
        'STAY OUT OF AREA OF PROSTITUTION':vice,
        'STOLEN PROPERTY':theft,
        'SUSPICIOUS CIRCUMSTANCES':mischief,
        'Shoplifting':theft,
        'THEFT OF SERVICES':theft,
        'THREATS':assault,
        'THREATS, HARASSMENT':assault,
        'TRAFFIC':traffic,
        'TRAFFIC RELATED CALLS':traffic,
        'TRESPASS':disturbance,
        'VEHICLE THEFT':theft,
        'VICE CALLS':vice,
        'VIOLATION OF COURT ORDER':arrest,
        'WARRANT ARREST':arrest,
        'WEAPON':assault,
        'WEAPONS CALLS':assault,
        '[INC - CASE DC USE ONLY]':other,
    }
    
    for entry in CRIME_MAPPING:
        item, created = PoliceEventGroup.objects.get_or_create(description=entry, category=CRIME_MAPPING[entry])
    


def get_police_data():
    # Loads data of Seattle 911 police incidents and incident reports
    # 
    # Two separate calls, one for 911 and one for reports
    #
    # JSON response for 911 should be of form:
    # {
    # "event_clearance_code" : "246",
    #  "cad_event_number" : "13000151256",
    #  "event_clearance_subgroup" : "NOISE DISTURBANCE",
    #  "event_clearance_group" : "DISTURBANCES",
    #  "cad_cdw_id" : "1393656",
    #  "event_clearance_date" : "2013-05-06T00:03:00",
    #  "zone_beat" : "N2",
    #  "district_sector" : "N",
    #  "incident_location" : {
    #    "needs_recoding" : false,
    #    "longitude" : "-122.355367628",
    #    "latitude" : "47.696933157"
    #  },
    #  "hundred_block_location" : "92XX BLOCK OF GREENWOOD AV N",
    #  "general_offense_number" : "2013151256",
    #  "event_clearance_description" : "NOISE DISTURBANCE, RESIDENTIAL",
    #  "longitude" : "-122.355367628",
    #  "latitude" : "47.696933157",
    #  "census_tract" : "1700.7010"
    # }
    #
    # JSON response for incident reports should be of form:
    # {
    #  "offense_code" : "2202",
    #  "offense_type" : "BURGLARY-FORCE-RES",
    #  "census_tract_2000" : "9701.1012",
    #  "date_reported" : "2013-05-06T00:00:00",
    #  "location" : {
    #    "needs_recoding" : false,
    #    "longitude" : "-122.409463566",
    #    "latitude" : "47.574985644"
    #  },
    #  "occurred_date_range_end" : "2013-05-05T22:23:00",
    #  "zone_beat" : "W1",
    #  "offense_code_extension" : "0",
    #  "district_sector" : "W",
    #  "hundred_block_location" : "32XX BLOCK OF 60 AV SW",
    #  "summarized_offense_description" : "BURGLARY",
    #  "general_offense_number" : "2013151244",
    #  "longitude" : "-122.409463566",
    #  "summary_offense_code" : "2200",
    #  "latitude" : "47.574985644",
    #  "rms_cdw_id" : "753475",
    #  "occurred_date_or_date_range_start" : "2013-05-05T22:18:00"
    #}
    
    base_url_911 = "http://data.seattle.gov/resource/3k2p-39jp.json"
    base_url_incident = "http://data.seattle.gov/resource/7ais-f98f.json"
    
    tz = pytz.timezone('US/Pacific')
    
    if Police.objects.count() == 0:
        timestamp_911 = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%F %H:%M:%S")
        timestamp_incident = timestamp_911
    else:
        latest_911 = Police.objects.exclude(event_clearance_date__isnull=True).order_by('-event_clearance_date')[0]
        timestamp_911 = latest_911.event_clearance_date.astimezone(tz).strftime("%F %H:%M:%S")
        
        latest_incident = Police.objects.exclude(date_reported__isnull=True).order_by('-date_reported')[0]
        timestamp_incident = latest_incident.date_reported.astimezone(tz).strftime("%F %H:%M:%S")
        
    query_911 = "$where=event_clearance_date > '%s'" % timestamp_911
    url_911 = base_url_911 + "?" + query_911.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    query_incident = "$where=date_reported > '%s'" % timestamp_incident
    url_incident = base_url_incident + "?" + query_incident.replace(" ", "%20").replace("$", "%24").replace(">", "%3E")
    
    # 911
    try:
        response = urllib2.urlopen(url_911)
        
        if response.code == 200:
            all_data = json.load(response)
            
            for data in all_data:
                if 'event_clearance_date' in data: # Ignore records with no descriptions (Are these hang-ups?)
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        hundred_block, status = HundredBlockSection.objects.get_or_create(block=data['hundred_block_location'])
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        police_obj, created = Police.objects.get_or_create(
                                                    general_offense_number=data['general_offense_number'],
                                                    defaults={
                                                        'hundred_block':hundred_block,
                                                        'point':point
                                                    })
                        
                        # Date case created
                        initial_date = datetime.datetime.strptime(data['event_clearance_date'], "%Y-%m-%dT%H:%M:%S")
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        date = updated_date
                        
                        # Update and save all attributes
                        clearance_code, status = ClearanceCode.objects.get_or_create(code=data['event_clearance_code'])
                        clearance_description, status = PoliceEventDetail.objects.get_or_create(description=data['event_clearance_description'].strip(), # Strip as one entry has trailing space
                                                                defaults={
                                                                    'source_911':True,
                                                                })
                        clearance_group, status = PoliceEventGroup.objects.get_or_create(description=data['event_clearance_group'].strip(),
                                                        defaults={
                                                            'source_911':True,
                                                        })
                        
                        # Update and save all attributes
                        police_obj.cad_cdw_id = data['cad_cdw_id']
                        police_obj.cad_event_number = data['cad_event_number']
                        police_obj.clearance_code = clearance_code
                        police_obj.clearance_description = clearance_description
                        police_obj.clearance_group = clearance_group
                        police_obj.event_clearance_date = date
                        
                        if 'district_sector' in data:
                            sector, status = DistrictSector.objects.get_or_create(district=data['district_sector'])
                            police_obj.district = sector
                        if 'zone_beat' in data:
                            beat, status = ZoneBeat.objects.get_or_create(beat=data['zone_beat'])
                            police_obj.beat = beat
                        if 'census_tract' in data:
                            tract, status = CensusTract.objects.get_or_create(tract=data['census_tract'])
                            police_obj.census = tract
                        
                        police_obj.save()
                    except KeyError, e:
                        log.error("Missing key %s in police 911 data so skipping :: %s" % (e, data['general_offense_number']))
        else:
            log.error("Non-200 code on get_police_data, 911 info: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting police data, 911 info: %s" % e.getcode())
    
    # Police Incidents
    try:
        response = urllib2.urlopen(url_incident)
        
        if response.code == 200:
            all_data = json.load(response)
            
            for data in all_data:
                if 'offense_type' in data: # Check valid record
                    try:
                        point = fromstr("POINT(%s %s)" % (data['longitude'], data['latitude']))
                        
                        # Date case created
                        initial_date = datetime.datetime.strptime(data['date_reported'], "%Y-%m-%dT%H:%M:%S")
                        updated_date = tz.localize(initial_date) # Make sure to use localize() and not replace()
                        date = updated_date
                        
                        hundred_block, status = HundredBlockSection.objects.get_or_create(block=data['hundred_block_location'])
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        police_obj, created = Police.objects.get_or_create(
                                                    general_offense_number=data['general_offense_number'],
                                                    defaults={
                                                        'hundred_block':hundred_block,
                                                        'point':point
                                                    })
                        
                        # Update and save all attributes
                        code, status = PoliceOffenseCode.objects.get_or_create(code=data['offense_code'])
                        code_extension, status = PoliceOffenseCodeExtension.objects.get_or_create(code=data['offense_code_extension'])
                        description, status = PoliceEventDetail.objects.get_or_create(description=data['offense_type'].strip(),
                                                                defaults={
                                                                    'source_911':False,
                                                                })
                        code_summary, status = PoliceSummaryOffenseCode.objects.get_or_create(code=data['summary_offense_code'])
                        summary_group, status = PoliceEventGroup.objects.get_or_create(description=data['summarized_offense_description'].strip(),
                                                        defaults={
                                                            'source_911':False,
                                                        })
                        
                        police_obj.rms_cdw_id = data['rms_cdw_id']
                        police_obj.code = code
                        police_obj.code_extension = code_extension
                        police_obj.offense_detail = description
                        police_obj.offense_code_summary = code_summary
                        police_obj.offense_summary = summary_group
                        police_obj.date_reported = date
                        
                        if 'district_sector' in data:
                            sector, status = DistrictSector.objects.get_or_create(district=data['district_sector'])
                            police_obj.district = sector
                        if 'zone_beat' in data:
                            beat, status = ZoneBeat.objects.get_or_create(beat=data['zone_beat'])
                            police_obj.beat = beat
                        if 'census_tract_2000' in data:
                            tract, status = CensusTract.objects.get_or_create(tract=data['census_tract_2000'])
                            police_obj.census = tract
                        
                        police_obj.save()                        
                    except KeyError, e:
                        log.error("Missing key %s in police incident data so skipping :: %s" % (e, data['general_offense_number']))
        else:
            log.error("Non-200 code on get_police_data, incident info: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting police data, incident info: %s" % e.getcode())


def load_historical_police_data(scope='everything'):
    
    if scope == 'everything':
        load_911 = True
        load_incidents = True
    elif scope == '911':
        load_911 = True
        load_incidents = False
    elif scope == 'incidents':
        load_911 = False
        load_incidents = True
    else:
        load_911 = False
        load_incidents = False
    
    # 911 reports
    if load_911:
        police_911 = open(os.path.dirname(__file__) + "/historical/Seattle_Police_Department_911_Incident_Response.csv")
        
        reader = csv.reader(police_911, delimiter=',', quotechar='"')
        
        new_record = 0
        
        log.info("Starting historical police 911 reports")
        
        counter = 0
        for line in reader:
            if counter != 0:
                initial_date = datetime.datetime.strptime(line[7], "%m/%d/%Y %H:%M:%S %p") # sample: 05/14/2013 10:20:00 AM
                updated_date = tz.localize(initial_date)
                date = updated_date
                
                if date >= CUTOFF_DATE:
                    try:
                        point = fromstr("POINT(%s %s)" % (line[12], line[13]))
                        hundred_block, status = HundredBlockSection.objects.get_or_create(block=line[8])
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        police_obj, created = Police.objects.get_or_create(
                                                    general_offense_number=line[2],
                                                    defaults={
                                                        'hundred_block':hundred_block,
                                                        'point':point
                                                    })
                        
                        # Update and save all attributes
                        clearance_code, status = ClearanceCode.objects.get_or_create(code=line[3])
                        clearance_description, status = PoliceEventDetail.objects.get_or_create(description=line[4].strip(),
                                                                defaults={
                                                                    'source_911':True,
                                                                })
                        clearance_group, status = PoliceEventGroup.objects.get_or_create(description=line[6].strip(),
                                                        defaults={
                                                            'source_911':True,
                                                        })
                        
                        police_obj.cad_cdw_id = line[0]
                        police_obj.cad_event_number = line[1]
                        police_obj.clearance_code = clearance_code
                        police_obj.clearance_description = clearance_description
                        police_obj.clearance_group = clearance_group
                        police_obj.event_clearance_date = date
                        
                        if line[9]:
                            sector, status = DistrictSector.objects.get_or_create(district=line[9])
                            police_obj.district = sector
                        if line[10]:
                            beat, status = ZoneBeat.objects.get_or_create(beat=line[10])
                            police_obj.beat = beat
                        if line[11]:
                            tract, status = CensusTract.objects.get_or_create(tract=line[11])
                            police_obj.census = tract
                        
                        police_obj.save()
                        
                        if created:
                            new_record += 1
                    except GEOSException, e:
                        log.error("Geo Error %s importing historical police 911 record with general offense num %s" % (e, line[2])) # Means no lat/lng
            
            if counter % 1000 == 0:
                log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
            counter += 1
        
        log.info("Created %d new police 911 records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
        
        police_911.close()
    
    # Incident reports
    if load_incidents:
        incidents = open(os.path.dirname(__file__) + "/historical/Seattle_Police_Department_Police_Report_Incident.csv")
        
        reader = csv.reader(incidents, delimiter=',', quotechar='"')
        
        new_record = 0
        
        log.info("Starting historical police incident reports")
        
        counter = 0
        for line in reader:
            if counter != 0:
                initial_date = datetime.datetime.strptime(line[7], "%m/%d/%Y %H:%M:%S %p") # sample: 05/14/2013 10:20:00 AM
                updated_date = tz.localize(initial_date)
                date = updated_date
                
                if date >= CUTOFF_DATE:
                    try:
                        point = fromstr("POINT(%s %s)" % (line[14], line[15]))
                        hundred_block, status = HundredBlockSection.objects.get_or_create(block=line[10])
                        
                        # Use get_or_create so that we never risk creating the same incident twice
                        police_obj, created = Police.objects.get_or_create(
                                                    general_offense_number=line[1],
                                                    defaults={
                                                        'hundred_block':hundred_block,
                                                        'point':point
                                                    })
                        
                        # Update and save all attributes
                        code, status = PoliceOffenseCode.objects.get_or_create(code=line[2])
                        code_extension, status = PoliceOffenseCodeExtension.objects.get_or_create(code=line[3])
                        description, status = PoliceEventDetail.objects.get_or_create(description=line[4].strip(),
                                                                defaults={
                                                                    'source_911':False,
                                                                })
                        code_summary, status = PoliceSummaryOffenseCode.objects.get_or_create(code=line[5])
                        summary_group, status = PoliceEventGroup.objects.get_or_create(description=line[6].strip(),
                                                        defaults={
                                                            'source_911':False,
                                                        })
                        
                        
                        police_obj.rms_cdw_id = line[0]
                        police_obj.code = code
                        police_obj.code_extension = code_extension
                        police_obj.offense_detail = description
                        police_obj.offense_code_summary = code_summary
                        police_obj.offense_summary = summary_group
                        police_obj.date_reported = date
                        
                        if line[11]:
                            sector, status = DistrictSector.objects.get_or_create(district=line[11])
                            police_obj.district = sector
                        if line[12]:
                            beat, status = ZoneBeat.objects.get_or_create(beat=line[12])
                            police_obj.beat = beat
                        if line[13]:
                            tract, status = CensusTract.objects.get_or_create(tract=line[13])
                            police_obj.census = tract
                        
                        police_obj.save()
                        
                        if created:
                            new_record += 1
                    except GEOSException, e:
                        log.error("Geo Error %s importing historical police incident record with general offense num %s" % (e, line[1])) # Means no lat/lng
            
            if counter % 1000 == 0:
                log.info("Processed %d records. %s" % (counter, datetime.datetime.now().strftime("%H:%M:%S")))
            
            counter += 1
        
        log.info("Created %d new police incident records. %s" % (new_record, datetime.datetime.now().strftime("%H:%M:%S")))
        
        incidents.close()
    


def max_length_finder(file_name):
    # Quick way to figure out maximum length of fields in a CSV. Helps avoid DatabaseError: value too long for type character varying(XX)
    # Pass path e.g., "/historical/Seattle_Police_Department_911_Incident_Response.csv"
    maxes = {}
    
    csv_file = open(os.path.dirname(__file__) + file_name)
    
    reader = csv.reader(csv_file, delimiter=',', quotechar='"')
    
    new_record = 0
    
    counter = 0
    for line in reader:
        for entry in range(0,len(line)):
            if counter == 0:
                maxes[entry] = {
                    'slug':line[entry],
                    'max_length':0
                }
            else:
                if len(line[entry]) > maxes[entry]['max_length']:
                    maxes[entry]['max_length'] = len(line[entry])
            
        
        counter += 1
    
    for entry in maxes:
        print maxes[entry]
    
