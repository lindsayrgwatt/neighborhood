from math import radians, cos, sin, asin, sqrt, pi

EARTH_RADIUS = 6371.0

# From http://stackoverflow.com/questions/4913349/haversine-formula-in-python-bearing-and-distance-between-two-gps-points
def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = EARTH_RADIUS * c
    return km

def theta_from_span(span):
    """
    Calculate a delta lat or lng based on a distance on surface (specified in km)
    """
    return span / EARTH_RADIUS / pi * 180
