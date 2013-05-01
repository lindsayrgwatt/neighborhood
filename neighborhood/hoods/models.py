from django.contrib.gis.db import models

class Neighborhood(models.Model):
    name = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    region_id = models.IntegerField('Region ID')
    
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ['name']