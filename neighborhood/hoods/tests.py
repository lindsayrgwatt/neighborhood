from django.utils import unittest
from hoods.models import Neighborhood

import hoods.load as neighborhood_loader

class NeighborhoodtestCase(unittest.TestCase):
    def setUp(self):
        neighborhood_loader.run()
    
    def test_geo_functions(self):
        """Neighborhoods exist in database"""
        self.assertEqual(len(Neighborhood.objects.filter(name='Ballard')), 1)
        
        """Can determine if points exist in Seattle neighborhoods"""
        pnt_wkt = 'POINT(-122.38393 47.66704)' # Ballard farmer's market
        self.assertEqual(Neighborhood.objects.filter(mpoly__contains=pnt_wkt)[0].name, 'Ballard')