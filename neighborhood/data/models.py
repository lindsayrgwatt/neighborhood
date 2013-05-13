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
    


class LandPermit(models.Model):
    permit_type = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    application_date = models.DateTimeField()
    applicant_name = models.CharField(max_length=100)
    permit_number = models.IntegerField()
    edg_required = models.BooleanField()
    category = models.CharField(max_length=30)
    appealed = models.BooleanField()
    address = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField()
    decision_type = models.CharField(max_length=1)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.permit_type + " :: " + str(self.permit_number) + " :: " + str(self.application_date)
        
    class Meta:
        ordering = ['-application_date', 'permit_type']
    

class BuildingPermit(models.Model):
    permit_type = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    application_date = models.DateTimeField()
    work_type = models.CharField(max_length=30)
    applicant_name = models.CharField(max_length=100)
    permit_number = models.IntegerField()
    category = models.CharField(max_length=30)
    action_type = models.CharField(max_length=10)
    address = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField()
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.permit_type + " :: " + str(self.permit_number) + " :: "  + str(self.application_date)
        
    class Meta:
        ordering = ['-application_date', 'permit_type']
    

class Violation(models.Model):
    case_number = models.IntegerField()
    case_type = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    description = models.TextField()
    case_group = models.CharField(max_length=40)
    category = models.CharField(max_length=40) # The derived category based on case_group
    date_case_created = models.DateTimeField()
    date_last_inspection = models.DateTimeField(null=True, blank=True)
    last_inspection_result = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=32)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.category + " :: " + str(self.case_number) + " :: "  + str(self.date_case_created)
    
    class Meta:
        ordering = ['-case_number']
    

class FoodViolation(models.Model):
    name = models.CharField(max_length=100)
    program_identifier = models.CharField(max_length=100)
    inspection_date = models.DateTimeField()
    place_description = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    inspection_type = models.CharField(max_length=50)
    violation_type = models.CharField(max_length=10)
    violation_code = models.CharField(max_length=4)
    violation_description = models.CharField(max_length=250)
    inspection_serial_num = models.CharField(max_length=10)
    violation_record_num = models.CharField(max_length=10)
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.business_name + " :: " + str(self.inspection_date)
    
    class Meta:
        ordering = ['-inspection_date']
    