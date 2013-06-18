# Note: in separate file from utils.py as models.py imports formula from utils.py and get stuck in endless loop

from models import Neighborhood, OSM_BASE_URL, PADDING_FACTOR

def seattle_osm_url():
    neighborhoods = Neighborhood.objects.all()
    
    bounds = neighborhoods[0].padded_bounds()
    
    min_lng = bounds[3]
    min_lat = bounds[2]
    max_lat = bounds[0]
    max_lng = bounds[1]
    
    for hood in neighborhoods:
        bounds = hood.padded_bounds()
        
        if bounds[3] < min_lng:
            min_lng = bounds[3]
        
        if bounds[2] < min_lat:
            min_lat = bounds[2]
        
        if bounds[0] > max_lat:
            max_lat = bounds[0]
        
        if bounds[1] > max_lng:
            max_lng = bounds[1]
        
    
    return OSM_BASE_URL + "?bbox=%.6f,%.6f,%.6f,%.6f" % (min_lng, min_lat, max_lng, max_lat)

def seattle_square_bounds():
    neighborhoods = Neighborhood.objects.all()
    
    bounds = neighborhoods[0].padded_bounds()
    
    min_lng = bounds[3]
    min_lat = bounds[2]
    max_lat = bounds[0]
    max_lng = bounds[1]
    
    for hood in neighborhoods:
        bounds = hood.padded_bounds()
        
        if bounds[3] < min_lng:
            min_lng = bounds[3]
        
        if bounds[2] < min_lat:
            min_lat = bounds[2]
        
        if bounds[0] > max_lat:
            max_lat = bounds[0]
        
        if bounds[1] > max_lng:
            max_lng = bounds[1]
        
    
    delta_x = abs(max_lng - min_lng)
    delta_y = abs(max_lat - min_lat)
    
    mid_lat = (min_lat + max_lat) / 2
    mid_lng = (min_lng + max_lng) / 2
    
    if (delta_x > delta_y):
        min_lng = min_lng - delta_x * PADDING_FACTOR
        max_lng = max_lng + delta_x * PADDING_FACTOR
        min_lat = mid_lat - delta_x/2 - delta_x * PADDING_FACTOR
        max_lat = mid_lat + delta_x/2 + delta_x * PADDING_FACTOR
    else:
        min_lat = min_lat - delta_y * PADDING_FACTOR
        max_lat = max_lat + delta_y * PADDING_FACTOR
        min_lng = mid_lng - delta_y/2 - delta_y * PADDING_FACTOR
        max_lng = mid_lng + delta_y/2 + delta_y * PADDING_FACTOR
        
    
    return "%.6f,%.6f,%.6f,%.6f" % (min_lng, min_lat, max_lng, max_lat)


def tilemill_command_line():
    """
    Creates command-line instructions for rendering individual map pngs via TileMill
    """
    
    neighborhoods = Neighborhood.objects.all()
    
    path = "/Users/lindsayrgwatt/apps/neighborhood_on_dotcloud/neighborhood/static/img/maps/"
    
    for hood in neighborhoods:
        print hood.slug
        print "./index.js export OSMBright %s%s.png --bbox='%s' --width=1024 --height=1024 --format=png" % (path, hood.slug, hood.tilemill_bounds())
        print "./index.js export OSMBright %s%s-mobile.png --bbox='%s' --width=480 --height=480 --format=png" %(path, hood.slug, hood.tilemill_bounds())
    
