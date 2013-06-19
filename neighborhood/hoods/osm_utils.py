# Note: in separate file from utils.py as models.py imports formula from utils.py and get stuck in endless loop

from models import Neighborhood, PADDING_FACTOR

def seattle_lat():
    neighborhoods = Neighborhood.objects.all()
    
    bounds = neighborhoods[0].padded_bounds()
    
    min_lat = bounds[2]
    max_lat = bounds[0]
    
    for hood in neighborhoods:
        bounds = hood.padded_bounds()
        
        if bounds[2] < min_lat:
            min_lat = bounds[2]
        
        if bounds[0] > max_lat:
            max_lat = bounds[0]
    
    return (max_lat + min_lat)/2

def seattle_lng():
    neighborhoods = Neighborhood.objects.all()
    
    bounds = neighborhoods[0].padded_bounds()
    
    min_lng = bounds[3]
    max_lng = bounds[1]
    
    for hood in neighborhoods:
        bounds = hood.padded_bounds()
        
        if bounds[3] < min_lng:
            min_lng = bounds[3]
        
        if bounds[1] > max_lng:
            max_lng = bounds[1]
        
    
    return (min_lng + max_lng)/2

