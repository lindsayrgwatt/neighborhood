from django.contrib.gis.db import models

class Fire(models.Model):
    address = models.CharField(max_length=100)
    incident_number = models.CharField(max_length=10)
    incident_type = models.CharField(max_length=50) # Free text field from standard codes
    aggregate_incident_type = models.CharField(max_length=50)
    date = models.DateTimeField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.incident_type + " :: " + str(self.date)
    
    class Meta:
        ordering = ['-date', 'incident_type']
