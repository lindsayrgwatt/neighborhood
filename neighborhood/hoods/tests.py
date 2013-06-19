# coding: utf-8

import datetime
import pytz

from django.contrib.gis.db import models
from django.utils import unittest
from django.contrib.gis.geos import fromstr
from django.core.urlresolvers import reverse
from django.test.client import Client

from hoods.models import Neighborhood
from data.models import FireIncidentAggregateType, FireIncidentType, Fire
from data.models import PermitValue, BuildingPermit, LandPermit
from data.models import ViolationAggregateCategory, ViolationCategory, Violation, FoodViolation
from data.models import PoliceEventAggregateGroup, PoliceEventGroup, Police911Call, Police911Incident

from hoods.views import calculate_neighborhood, calculate_date, is_weekend, get_police_details, get_fire_details, get_permit_details, get_violation_details
import hoods.load as neighborhood_loader
from data.load import create_permit_ranges, create_violation_aggregates, create_police_aggregates
from hoods.utils import haversine

pacific = pytz.timezone('US/Pacific')

class NeighborhoodTestCase(unittest.TestCase):
    ClassIsSetup = False
    yesterday = pacific.localize(datetime.datetime.now() - datetime.timedelta(1))
    
    def setUp(self):
        if not self.ClassIsSetup:
            print "Initializing test environment"
            neighborhood_loader.run()
            
            print "Creating aggregate records"
            
            fire_aggregate_type, status = FireIncidentAggregateType.objects.get_or_create(description="Other")
            fire_type, status = FireIncidentType.objects.get_or_create(description="Big Fire")
            
            create_permit_ranges()
            create_violation_aggregates()
            create_police_aggregates()
            
            permit_range = PermitValue.objects.get(value=10000000)
            
            food_inspection = ViolationCategory.objects.get(category="FOOD INSPECTION")
            zoning = ViolationCategory.objects.get(category="ZONING")
            homicide = PoliceEventGroup.objects.get(description="HOMICIDE")
            
            print "Adding records in Ballard"
            ballard = fromstr("POINT(-122.38393 47.66704)") # Ballard farmer's market
            
            new_fire = Fire(
                address="in ballard",
                incident_number="F123",
                incident_category=fire_type,
                date=self.yesterday,
                point=ballard
            )
            new_fire.save()
            
            new_building_permit = BuildingPermit(
                permit_type="Construction",
                application_date=self.yesterday,
                permit_number=1,
                address="in ballard",
                description="it's a permit, yo!",
                value=1000,
                url="http://www.lindsayrgwatt/building",
                point=ballard
            )
            new_building_permit.save()
            
            new_land_permit = LandPermit(
                application_date=self.yesterday,
                permit_number=1,
                address="in ballard",
                description="a permit in ballard",
                value=1000,
                url="http://www.lindsayrgwatt.com",
                point=ballard
            )
            new_land_permit.save()
            
            new_violation = Violation(
                case_number=1,
                address="in ballard",
                description="this be a violation",
                group=zoning,
                date_case_created=self.yesterday,
                url="http://www.lindsayrgwatt.com/violation",
                point=ballard
            )
            new_violation.save()
            
            new_food_violation = FoodViolation(
                name="Dirty Chicken",
                inspection_date=self.yesterday,
                address="In Ballard",
                violation_type="Red",
                code="X123",
                description="We came, we saw, we were revolted.",
                violation_num="DEF456",
                point=ballard
            )
            new_food_violation.save()
            
            new_police_call = Police911Call(
                general_offense_number=1234,
                description='Murder she wrote',
                group=homicide,
                date=self.yesterday,
                address='123 Main St',
                point=ballard
            )
            new_police_call.save()
            
            new_police_incident = Police911Incident(
                general_offense_number=1,
                description="Incident for the murder",
                group=homicide,
                date=self.yesterday,
                address='321 Main St',
                point=ballard
            )
            new_police_incident.save()
            
            print "Adding records outside Ballard"
            boeing_field = fromstr("POINT(-122.30 47.53)")
            
            new_fire = Fire(
                address="not in ballard",
                incident_number="F124",
                incident_category=fire_type,
                date=self.yesterday,
                point=boeing_field
            )
            new_fire.save()
            
            new_building_permit = BuildingPermit(
                permit_type="Construction",
                application_date=self.yesterday,
                permit_number=2,
                address="not in ballard",
                description="it's a permit, yo!",
                value=1000,
                url="http://www.lindsayrgwatt/building2",
                point=boeing_field
            )
            new_building_permit.save()
            
            new_land_permit = LandPermit(
                application_date=self.yesterday,
                permit_number=2,
                address="not in ballard",
                description="a permit outside ballard",
                value=1000,
                url="http://www.lindsayrgwatt.com/blog",
                point=boeing_field
            )
            new_land_permit.save()
            
            new_violation = Violation(
                case_number=2,
                address="not in ballard",
                description="this be a violation",
                group=zoning,
                date_case_created=self.yesterday,
                url="http://www.lindsayrgwatt.com/violation2",
                point=boeing_field
            )
            new_violation.save()
            
            new_food_violation = FoodViolation(
                name="Dirty Chicken Boeing Field",
                inspection_date=self.yesterday,
                address="Not In Ballard",
                violation_type="Red",
                code="X123",
                description="We came, we saw, we were revolted.",
                violation_num="ABC123",
                point=boeing_field
            )
            new_food_violation.save()
            
            new_police_call = Police911Call(
                general_offense_number=1235,
                description='Murder she wrote',
                group=homicide,
                date=self.yesterday,
                address='123 Main St',
                point=boeing_field
            )
            new_police_call.save()
            
            new_police_incident = Police911Incident(
                general_offense_number=2,
                description="Incident for the murder",
                group=homicide,
                date=self.yesterday,
                address='321 Main St',
                point=boeing_field
            )
            new_police_incident.save()
            
            self.__class__.ClassIsSetup = True
        
    
    
    def test_lat_lng_getters_work(self):
        police_call = Police911Call.objects.all()[0]
        self.assertEqual(police_call.lat(), police_call.point.get_coords()[1])
        self.assertEqual(police_call.lng(), police_call.point.get_coords()[0])
        
        police_incident = Police911Incident.objects.all()[0]
        self.assertEqual(police_incident.lat(), police_call.point.get_coords()[1])
        self.assertEqual(police_incident.lng(), police_call.point.get_coords()[0])
        
        fire = Fire.objects.all()[0]
        self.assertEqual(fire.lat(), fire.point.get_coords()[1])
        self.assertEqual(fire.lng(), fire.point.get_coords()[0])
        
        land = LandPermit.objects.all()[0]
        self.assertEqual(land.lat(), land.point.get_coords()[1])
        self.assertEqual(land.lng(), land.point.get_coords()[0])
        
        building = BuildingPermit.objects.all()[0]
        self.assertEqual(building.lat(), building.point.get_coords()[1])
        self.assertEqual(building.lng(), building.point.get_coords()[0])
        
        violation = Violation.objects.all()[0]
        self.assertEqual(violation.lat(), violation.point.get_coords()[1])
        self.assertEqual(violation.lng(), violation.point.get_coords()[0])
        
        food_violation = FoodViolation.objects.all()[0]
        self.assertEqual(food_violation.lat(), food_violation.point.get_coords()[1])
        self.assertEqual(food_violation.lng(), food_violation.point.get_coords()[0])
    
    
    def test_neighborhoods_exist(self):
        """Neighborhoods exist in database"""
        self.assertEqual(len(Neighborhood.objects.filter(name='Ballard')), 1)
    
    
    def test_geo_search_works(self):
        """Can determine if points exist in Seattle neighborhoods"""
        pnt_wkt = 'POINT(-122.38393 47.66704)' # Ballard farmer's market
        self.assertEqual(Neighborhood.objects.filter(mpoly__contains=pnt_wkt)[0].name, 'Ballard')
    
    
    def test_neighborhood_find(self):
        """See if can correctly find neighborhoods based on text"""
        self.assertEqual(calculate_neighborhood('asdfasdfasdfasdfasdf'), (False, False, None))
        
        self.assertEqual(calculate_neighborhood('SEATTLE'), (True, True, None))
        self.assertEqual(calculate_neighborhood('seattle'), (True, True, None))
        
        self.assertEqual(calculate_neighborhood('queen-anne'), (True, False, Neighborhood.objects.get(name="Queen Anne")))
        self.assertEqual(calculate_neighborhood('QUEEN-AnNe'), (True, False, Neighborhood.objects.get(name="Queen Anne")))
    
    
    def test_geo_and_time_aggregation_works(self):
        """ See if correctly find objects"""
        ballard = Neighborhood.objects.get(name='Ballard')
        today = (self.yesterday + datetime.timedelta(1)).date()
        
        ballard_fire_objs_today = get_fire_details(today, ballard)
        self.assertEqual(ballard_fire_objs_today[0].count(), 0) # Fires
        
        ballard_permit_objs_today = get_permit_details(today, ballard)
        self.assertEqual(ballard_permit_objs_today[0].count(), 0) # Building Permits
        self.assertEqual(ballard_permit_objs_today[2].count(), 0) # Land Use Permits
        
        ballard_violation_objs_today = get_violation_details(today, ballard)
        self.assertEqual(ballard_violation_objs_today[0].count(), 0) # Code Violations
        self.assertEqual(ballard_violation_objs_today[2].count(), 0) # Food Violations
        
        ballard_police_objs_today = get_police_details(today, ballard)
        self.assertEqual(ballard_police_objs_today[0].count(), 0) # Police 911 Calls
        self.assertEqual(ballard_police_objs_today[2].count(), 0) # Police 911 Incidents
        
        seattle_fire_objs_today = get_fire_details(today)
        self.assertEqual(seattle_fire_objs_today[0].count(), 0) # Fires
        
        seattle_permit_objs_today = get_permit_details(today)
        self.assertEqual(seattle_permit_objs_today[0].count(), 0) # Building Permits
        self.assertEqual(seattle_permit_objs_today[2].count(), 0) # Land Use Permits
        
        seattle_violation_objs_today = get_violation_details(today)
        self.assertEqual(seattle_violation_objs_today[0].count(), 0) # Code Violations
        self.assertEqual(seattle_violation_objs_today[2].count(), 0) # Food Violations
        
        seattle_police_objs_today = get_police_details(today)
        self.assertEqual(seattle_police_objs_today[0].count(), 0) # Police 911 Calls
        self.assertEqual(seattle_police_objs_today[2].count(), 0) # Police 911 Incidents
        
        ballard_fire_objs_yesterday = get_fire_details(self.yesterday, ballard)
        self.assertEqual(ballard_fire_objs_yesterday[0].count(), 1) # Fires
        self.assertEqual(ballard_fire_objs_yesterday[1]['Other'], 1) # Fire count by category
        
        ballard_permit_objs_yesterday = get_permit_details(self.yesterday, ballard)
        self.assertEqual(ballard_permit_objs_yesterday[0].count(), 1) # Building permits
        self.assertEqual(ballard_permit_objs_yesterday[1][u'≤$1K'], 1) # Building permit counts by category
        self.assertEqual(ballard_permit_objs_yesterday[2].count(), 1) # Land use permits
        self.assertEqual(ballard_permit_objs_yesterday[3][u'≤$1K'], 1) # Land use permit counts by category
        
        ballard_violation_objs_yesterday = get_violation_details(self.yesterday, ballard)
        self.assertEqual(ballard_violation_objs_yesterday[0].count(), 1) # Code violations
        self.assertEqual(ballard_violation_objs_yesterday[1]['Zoning'], 1) # Code violation counts by category
        self.assertEqual(ballard_violation_objs_yesterday[1]['Food Inspection'], 1)
        self.assertEqual(ballard_violation_objs_yesterday[2].count(), 1) # Food violations
        
        ballard_police_objs_yesterday = get_police_details(self.yesterday, ballard)
        self.assertEqual(ballard_police_objs_yesterday[0].count(), 1) # Police 911 Calls
        self.assertEqual(ballard_police_objs_yesterday[1]['Homicide'], 1) # Police 911 call counts by category
        self.assertEqual(ballard_police_objs_yesterday[2].count(), 1) # Police 911 Incidents
        self.assertEqual(ballard_police_objs_yesterday[3]['Homicide'], 1) # Police incident counts by category
        
        try:
            ballard_fire_objs_yesterday[1]['Fire']
        except KeyError:
            pass
        else:
            self.fail('Expected exception not thrown')
        
        seattle_fire_objs_yesterday = get_fire_details(self.yesterday)
        self.assertEqual(seattle_fire_objs_yesterday[0].count(), 2) # Fires
        self.assertEqual(seattle_fire_objs_yesterday[1]['Other'], 2) # Fire count by category
        
        seattle_permit_objs_yesterday = get_permit_details(self.yesterday)
        self.assertEqual(seattle_permit_objs_yesterday[0].count(), 2) # Building permits
        self.assertEqual(seattle_permit_objs_yesterday[1][u'≤$1K'], 2) # Building permit counts by category
        self.assertEqual(seattle_permit_objs_yesterday[2].count(), 2) # Land use permits
        self.assertEqual(seattle_permit_objs_yesterday[3][u'≤$1K'], 2) # Land use permit counts by category
        
        seattle_violation_objs_yesterday = get_violation_details(self.yesterday)
        self.assertEqual(seattle_violation_objs_yesterday[0].count(), 2) # Code violations
        self.assertEqual(seattle_violation_objs_yesterday[1]['Zoning'], 2) # Code violation counts by category
        self.assertEqual(seattle_violation_objs_yesterday[1]['Food Inspection'], 2)
        self.assertEqual(seattle_violation_objs_yesterday[2].count(), 2) # Food violations
        
        seattle_police_objs_yesterday = get_police_details(self.yesterday)
        self.assertEqual(seattle_police_objs_yesterday[0].count(), 2) # Police 911 Calls
        self.assertEqual(seattle_police_objs_yesterday[1]['Homicide'], 2) # Police 911 call counts by category
        self.assertEqual(seattle_police_objs_yesterday[2].count(), 2) # Police 911 Incidents
        self.assertEqual(seattle_police_objs_yesterday[3]['Homicide'], 2) # Police incident counts by category
    
    
    def test_neighborhood_bounds_works(self):
        atlantic = Neighborhood.objects.get(name="Atlantic")
        belltown = Neighborhood.objects.get(name="Belltown")
        
        self.assertEqual(belltown.wider_than_tall(), True)
        self.assertEqual(atlantic.wider_than_tall(), False)
        
        bounds = belltown.padded_bounds()
        
        self.assertEqual((bounds[0] - bounds[2]) - (bounds[1] - bounds[3]) < 0.000001, True) # Avoid limits to decimal precision
        self.assertEqual(bounds[0], 47.62780997138224)
        self.assertEqual(bounds[1], -122.33524759443412)
        self.assertEqual(bounds[2], 47.60137586981825)
        self.assertEqual(bounds[3], -122.36168169599812)
        
        bounds = atlantic.padded_bounds()
        
        self.assertEqual((bounds[0] - bounds[2]) - (bounds[1] - bounds[3]) < 0.000001, True)
        self.assertEqual(bounds[0], 47.60424933568962)
        self.assertEqual(bounds[1], -122.28649089225455)
        self.assertEqual(bounds[2], 47.573800714661466)
        self.assertEqual(bounds[3], -122.31693951328269)
    
    
    def test_police_detail_view(self):
        date_string = self.yesterday.strftime("%d%m%Y")
        
        path = reverse('hoods.views.police_detail', args=['ballard', date_string])
        
        c = Client()
        
        response = c.get(path)
        
        ballard = Neighborhood.objects.get(name="Ballard")
        
        self.assertEqual(response.context['neighborhood_name'], 'Ballard')
        self.assertEqual(response.context['date_label'], 'Yesterday')
        self.assertEqual(response.context['date_object'], self.yesterday.date())
        self.assertEqual(response.context['police_call_count'], 1)
        self.assertEqual(response.context['police_incident_count'], 1)
        self.assertEqual(response.context['police_call_detail']['Homicide'], 1)
        self.assertEqual(response.context['police_incident_detail']['Homicide'], 1)
        
    
    
    def test_fire_detail_view(self):
        date_string = self.yesterday.strftime("%d%m%Y")
        
        path = reverse('hoods.views.fire_detail', args=['ballard', date_string])
        
        c = Client()
        
        response = c.get(path)
        
        ballard = Neighborhood.objects.get(name="Ballard")
        
        self.assertEqual(response.context['neighborhood_name'], 'Ballard')
        self.assertEqual(response.context['date_label'], 'Yesterday')
        self.assertEqual(response.context['date_object'], self.yesterday.date())
        self.assertEqual(response.context['fire_count'], 1)
        self.assertEqual(response.context['fire_detail']['Other'], 1)
    
    
    def test_permit_detail_view(self):
        date_string = self.yesterday.strftime("%d%m%Y")
        
        path = reverse('hoods.views.permit_detail', args=['ballard', date_string])
        
        c = Client()
        
        response = c.get(path)
        
        ballard = Neighborhood.objects.get(name="Ballard")
        
        self.assertEqual(response.context['neighborhood_name'], 'Ballard')
        self.assertEqual(response.context['date_label'], 'Yesterday')
        self.assertEqual(response.context['date_object'], self.yesterday.date())
        self.assertEqual(response.context['land_permit_count'], 1)
        self.assertEqual(response.context['building_permit_count'], 1)
        self.assertEqual(response.context['permit_detail'][1]['land'], 1)
        self.assertEqual(response.context['permit_detail'][1]['building'], 1)
    
    
    def test_violation_detail_view(self):
        date_string = self.yesterday.strftime("%d%m%Y")
        
        path = reverse('hoods.views.violation_detail', args=['ballard', date_string])
        
        c = Client()
        
        response = c.get(path)
        
        ballard = Neighborhood.objects.get(name="Ballard")
        
        self.assertEqual(response.context['neighborhood_name'], 'Ballard')
        self.assertEqual(response.context['date_label'], 'Yesterday')
        self.assertEqual(response.context['date_object'], self.yesterday.date())
        self.assertEqual(response.context['code_violations_count'], 1)
        self.assertEqual(response.context['food_violations_count'], 1)
        self.assertEqual(response.context['code_violations_details']['Zoning'], 1)
        self.assertEqual(response.context['code_violations_details']['Food Inspection'], 1)
    
    
    def test_aggregated_detail_view(self):
        date_string = self.yesterday.strftime("%d%m%Y")
        
        path = reverse('hoods.views.detail', args=['ballard', date_string])
        
        c = Client()
        
        response = c.get(path)
        
        ballard = Neighborhood.objects.get(name="Ballard")
        
        self.assertEqual(response.context['neighborhood_name'], 'Ballard')
        self.assertEqual(response.context['neighborhood_slug'], ballard.slug)
        self.assertEqual(response.context['date_label'], 'Yesterday')
        self.assertEqual(response.context['date_object'], self.yesterday.date())
        
        self.assertEqual(response.context['police_call_count'], 1)
        self.assertEqual(response.context['police_incident_count'], 1)
        
        self.assertEqual(response.context['fire_count'], 1)
        
        self.assertEqual(response.context['land_permit_count'], 1)
        self.assertEqual(response.context['building_permit_count'], 1)
        
        self.assertEqual(response.context['code_violations_count'], 1)
        self.assertEqual(response.context['food_violations_count'], 1)
    
    
class HelperTestCase(unittest.TestCase):
    def test_date_calculation(self):
        """Determine if properly parsing date values"""
        self.assertEqual(calculate_date('asdfasdf'), (False, None, ''))
        
        now = datetime.datetime.now()
        now_str = now.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(now_str), (True, now.date(), 'Today'))
        
        future = now + datetime.timedelta(1)
        future_str = future.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(future_str), (True, future.date(), 'In the future'))
        
        yesterday = now - datetime.timedelta(days=1)
        yesterday_str = yesterday.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(yesterday_str), (True, yesterday.date(), 'Yesterday'))
        self.assertEqual(calculate_date(), (True, yesterday.date(), 'Yesterday'))
        
        two_days_ago = now - datetime.timedelta(days=2)
        two_days_ago_str = two_days_ago.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(two_days_ago_str), (True, two_days_ago.date(), 'Two days ago'))
        
        three_days_ago = now - datetime.timedelta(days=3)
        three_days_ago_str = three_days_ago.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(three_days_ago_str), (True, three_days_ago.date(), 'On ' + three_days_ago.strftime("%A")))
        
        two_weeks_ago = now - datetime.timedelta(days=14)
        two_weeks_ago_str = two_weeks_ago.strftime("%d%m%Y")
        
        self.assertEqual(calculate_date(two_weeks_ago_str), (True, two_weeks_ago.date(), 'On ' + two_weeks_ago.strftime("%A, %B %d, %Y")))
    
    
    def test_is_weekend_calculation(self):
        monday = datetime.date(2013, 6, 3)
        tuesday = datetime.date(2013, 6, 4)
        wednesday = datetime.date(2013, 6, 5)
        thursday = datetime.date(2013, 6, 6)
        friday = datetime.date(2013, 6, 7)
        saturday = datetime.date(2013, 6, 8)
        sunday = datetime.date(2013, 6, 9)
        
        self.assertEqual(is_weekend(monday), False)
        self.assertEqual(is_weekend(tuesday), False)
        self.assertEqual(is_weekend(wednesday), False)
        self.assertEqual(is_weekend(thursday), False)
        self.assertEqual(is_weekend(friday), False)
        self.assertEqual(is_weekend(saturday), True)
        self.assertEqual(is_weekend(sunday), True)
    
    
    def test_haversine(self):
        lat_a = 51.885
        lng_a = 0.235
        
        lat_b = 49.008
        lng_b = 2.549
        
        km = haversine(lng_a, lat_a, lng_b, lat_b)
        
        self.assertEqual(359.3823602146919, km)
    
