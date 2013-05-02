from django.utils import unittest
from hoods.models import Neighborhood

import hoods.load as neighborhood_loader

class NeighborhoodtestCase(unittest.TestCase):
    ClassIsSetup = False
    
    def setUp(self):
        if not self.ClassIsSetup:
            print "Initializing test environment"
            neighborhood_loader.run()
            self.__class__.ClassIsSetup = True
    
    def test_neighborhoods_exist(self):
        """Neighborhoods exist in database"""
        self.assertEqual(len(Neighborhood.objects.filter(name='Ballard')), 1)
        
    def test_geo_search_works(self):
        """Can determine if points exist in Seattle neighborhoods"""
        pnt_wkt = 'POINT(-122.38393 47.66704)' # Ballard farmer's market
        self.assertEqual(Neighborhood.objects.filter(mpoly__contains=pnt_wkt)[0].name, 'Ballard')