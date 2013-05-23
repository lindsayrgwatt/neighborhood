from django.contrib.gis.db import models
from django.template.defaultfilters import slugify

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
    
    class Meta:
        ordering = ['name']
    