import os

from django.contrib.gis.utils import LayerMapping
from hoods.models import Neighborhood

# Zillow provides neighborhood boundaries across the US
# These are typical more descriptive of actual perceived boundaries than government boundaries
#
# http://www.zillow.com/howto/api/neighborhood-boundaries.htm

neighborhood_shape = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/ZillowNeighborhoods-WA/ZillowNeighborhoods-WA.shp'))

mapping = {
    'name' : 'NAME',
    'city' : 'CITY',
    'region_id': 'REGIONID',
    'mpoly' : 'MULTIPOLYGON',
}

def run(verbose=True):
    if len(Neighborhood.objects.all()) == 0:
        lm = LayerMapping(Neighborhood, neighborhood_shape, mapping)
        lm.save(strict=True, verbose=verbose)
        Neighborhood.objects.exclude(city='Seattle').delete()
        print "There are %d neighborhoods in Seattle" % len(Neighborhood.objects.all())
    else:
        print "Neighborhood shapefile already loaded (at least one neighborhood exists). Delete existing records via admin tool"
