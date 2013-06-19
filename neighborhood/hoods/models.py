from django.contrib.gis.db import models
from django.template.defaultfilters import slugify
from utils import haversine, theta_from_span

PADDING_FACTOR = 0.10
OSM_BASE_URL = "http://api.openstreetmap.org/api/0.6/map"

class Neighborhood(models.Model):
    name = models.CharField(max_length=64) # Not unique as will break import process via LayerMapping
    city = models.CharField(max_length=64)
    region_id = models.IntegerField('Region ID')
    slug = models.SlugField(max_length=64)
    
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        
        super(Neighborhood, self).save(*args, **kwargs)
    
    def height(self):
        left = self.mpoly.envelope.tuple[0][0][0]
        bottom = self.mpoly.envelope.tuple[0][0][1]
        right = self.mpoly.envelope.tuple[0][1][0]
        top = self.mpoly.envelope.tuple[0][2][1]
        
        return haversine((left+right)/2, top, (left+right)/2, bottom)
    
    def width(self):
        left = self.mpoly.envelope.tuple[0][0][0]
        bottom = self.mpoly.envelope.tuple[0][0][1]
        right = self.mpoly.envelope.tuple[0][1][0]
        top = self.mpoly.envelope.tuple[0][2][1]
        
        return haversine(left, (top + bottom)/2, right, (top + bottom)/2)
    
    
    def wider_than_tall(self):
        if self.width() > self.height():
            return True
        else:
            return False
        
    
    def padded_bounds(self):
        """
        Returns square bounds for a given neighborhood, padded by the amount PADDING_FACTOR
        """
        # NOTE: this code would fail at international date line
        left = self.mpoly.envelope.tuple[0][0][0]
        bottom = self.mpoly.envelope.tuple[0][0][1]
        right = self.mpoly.envelope.tuple[0][1][0]
        top = self.mpoly.envelope.tuple[0][2][1]
        
        if self.wider_than_tall():
            distance = right - left
            new_left = left - PADDING_FACTOR * distance
            new_right = right + PADDING_FACTOR * distance
            new_top = (top + bottom)/2 + (distance/2) + PADDING_FACTOR * distance
            new_bottom = (top + bottom)/2 - (distance/2) - PADDING_FACTOR * distance
        else:
            distance = top - bottom
            new_top = top + PADDING_FACTOR * distance
            new_bottom = bottom - PADDING_FACTOR * distance
            new_left = (left + right)/2 - (distance/2) - PADDING_FACTOR * distance
            new_right = (left + right)/2 + (distance/2) + PADDING_FACTOR * distance
        
        return (new_top, new_right, new_bottom, new_left)
    
    def lat(self):
        bottom = self.mpoly.envelope.tuple[0][0][1]
        top = self.mpoly.envelope.tuple[0][2][1]
        
        return (bottom + top)/2
    
    def lng(self):
        left = self.mpoly.envelope.tuple[0][0][0]
        right = self.mpoly.envelope.tuple[0][1][0]
        
        return (left + right)/2
    
    
    class Meta:
        ordering = ['name']
    