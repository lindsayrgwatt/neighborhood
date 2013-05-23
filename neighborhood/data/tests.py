import datetime

from django.contrib.gis.db import models
from django.utils import unittest
from django.contrib.gis.geos import fromstr

from data.models import PermitValue, BuildingPermit

from data.load import create_permit_ranges

class HelperTestCase(unittest.TestCase):
    ClassIsSetup = False
    
    def setUp(self):
        if not self.ClassIsSetup:
            print "Creating permit ranges"
            
            create_permit_ranges()
            
            self.__class__.ClassIsSetup = True
    
    def test_permit_range_calculation(self):
        ballard = fromstr("POINT(-122.38393 47.66704)") # Ballard farmer's market
        today = datetime.datetime.now().date()
                
        permit = BuildingPermit(
                    permit_type="Demolition",
                    application_date=today,
                    permit_number=123,
                    address="123 Main Street",
                    description="Some type o permit",
                    value=0,
                    url="http://www.testpermit.com",
                    point=ballard
        )
        permit.save()
        
        permit_value = PermitValue.objects.get(value=1)
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 1
        permit.save()
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit_value = PermitValue.objects.get(value=1000)
        
        permit.value = 999
        permit.save()
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 1000
        permit.save()
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 1001
        permit.save()
        
        permit_value = PermitValue.objects.get(value=10000)
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 10000000
        permit.save()
        
        permit_value = PermitValue.objects.get(value=10000000)
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 10000001
        permit.save()
        
        permit_value = PermitValue.objects.get(value=10000001)
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.value = 100000000
        permit.save()
        
        self.assertEqual(permit.value_range, permit_value)
        
        permit.delete()
    
