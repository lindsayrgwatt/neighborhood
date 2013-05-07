import urllib
import urllib2
import json
import datetime
import pytz
import logging

from django.contrib.gis.geos import fromstr

from data.models import Fire

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
                        log.error("Missing key %s so skipping" % e)
        
        else:
            log.error("Non-200 code on get_fire_data: %s" % str(response.code))
    except urllib2.HTTPError, e:
        log.error("Error getting fire data: %s" % e.getcode())
        
