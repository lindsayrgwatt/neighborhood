import logging

from django.contrib.gis.db import models

log = logging.getLogger(__name__)

##############################################
# 
# Fire Info
#
class FireIncidentAggregateType(models.Model):
    description = models.CharField(max_length=40, unique=True)
    
    def __unicode__(self):
        return self.description


class FireIncidentType(models.Model):
    description = models.CharField(max_length=40, unique=True) # Free text field from standard codes
    aggregate = models.ForeignKey('FireIncidentAggregateType')
    
    def __unicode__(self):
        return self.description
    
    class Meta:
        ordering = ['description']
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'aggregate'):
            self.aggregate = FireIncidentAggregateType.objects.get(description='Other')
            log.info("New type of fire category: %s" % self.description)
        
        super(FireIncidentType, self).save(*args, **kwargs)
    


class Fire(models.Model):
    address = models.CharField(max_length=60) # Max length of 52 in initial data set
    incident_number = models.CharField(max_length=10, db_index=True) # There are nulls in raw data, but we skip those as presumed error
    incident_category = models.ForeignKey('FireIncidentType')
    date = models.DateTimeField(db_index=True) # UTC in database
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.incident_number + " :: " + self.incident_category.description + " :: " + str(self.date)
    
    class Meta:
        ordering = ['-date', 'incident_category']
    

##############################################
# 
# Land/Building Info
#
def calc_permit_value(permit):
    ranges = PermitValue.objects.all()
    
    range_mapping = {}
    for item in ranges:
        range_mapping[item.value] = item
    
    values = [item.value for item in ranges]
    values.sort()
    
    counter = 0
    
    for value in values:
        if permit.value <= value:
            break
        counter += 1
    
    if counter < len(values):
        permit.value_range=range_mapping[values[counter]]
    else:
        permit.value_range=range_mapping[values[len(values)-1]]
    
    return permit


class PermitValue(models.Model):
    value = models.IntegerField(unique=True)
    label = models.CharField(max_length=20)
    
    def __unicode__(self):
        return self.label
    
    class Meta:
        ordering = ['-value']
    

class BuildingPermit(models.Model):
    permit_type = models.CharField(max_length=16)
    application_date = models.DateField(db_index=True)
    permit_number = models.IntegerField(db_index=True)
    address = models.CharField(max_length=60)
    description = models.TextField()
    value = models.IntegerField(db_index=True)
    value_range = models.ForeignKey('PermitValue', db_index=True)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.permit_type + " :: " + str(self.permit_number) + " :: "  + str(self.application_date)
    
    def save(self, *args, **kwargs):
        self = calc_permit_value(self)
        
        super(BuildingPermit, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-application_date', 'permit_type']
    

class LandPermit(models.Model):
    application_date = models.DateField(db_index=True)
    permit_number = models.IntegerField(db_index=True)
    address = models.CharField(max_length=60)
    description = models.TextField()
    value = models.IntegerField(db_index=True)
    value_range = models.ForeignKey('PermitValue', db_index=True)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return str(self.permit_number) + " :: " + str(self.application_date)
    
    def save(self, *args, **kwargs):
        self = calc_permit_value(self)
        
        super(LandPermit, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-application_date', '-permit_number']
    

##############################################
# 
# Violation Info
#
class ViolationAggregateCategory(models.Model):
    category = models.CharField(max_length=40, unique=True)
    
    def __unicode__(self):
        return self.category
    
    class Meta:
        ordering = ['category']
    


class ViolationCategory(models.Model):
    category = models.CharField(max_length=40, unique=True)
    aggregate = models.ForeignKey('ViolationAggregateCategory')
    
    def __unicode__(self):
        return self.category + " :: " + self.aggregate.category
    
    class Meta:
        ordering = ['category']
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'aggregate'):
            self.aggregate = ViolationAggregateCategory.objects.get(description='Other')
            log.info("New type of violation category: %s" % self.description)
        
        super(ViolationCategory, self).save(*args, **kwargs)
    

class Violation(models.Model):
    case_number = models.IntegerField(unique=True)
    address = models.CharField(max_length=100)
    description = models.TextField()
    group = models.ForeignKey('ViolationCategory', db_index=True)
    date_case_created = models.DateField(db_index=True)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.group.category + " :: " + str(self.case_number) + " :: "  + str(self.date_case_created)
    
    class Meta:
        ordering = ['-case_number']
    

class FoodViolation(models.Model):
    name = models.CharField(max_length=100)
    inspection_date = models.DateField(db_index=True)
    address = models.CharField(max_length=100)
    group = models.ForeignKey('ViolationCategory', db_index=True)
    code = models.CharField(max_length=4)
    description = models.CharField(max_length=100)
    violation_num = models.CharField(max_length=10, unique=True)
    violation_type = models.CharField(max_length=4) # Red or Blue; Red must be fixed right away
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.name + " :: " + str(self.inspection_date)
    
    def save(self, *args, **kwargs):
        self.group = ViolationCategory.objects.get(category='FOOD INSPECTION')
        
        super(FoodViolation, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-inspection_date']
    

##############################################
# 
# Police Info
#
class PoliceEventAggregateGroup(models.Model):
    category = models.CharField(max_length=32, unique=True)
    
    def __unicode__(self):
        return self.category
    
    class Meta:
        ordering = ['category']
    

class PoliceEventGroup(models.Model):
    # Union of Police911Incident "Event Clearance Group" and  Police911Incident "Summarized Offense Description"
    description = models.CharField(max_length=40, unique=True)
    category = models.ForeignKey('PoliceEventAggregateGroup')
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'category'):
            self.category = PoliceEventAggregateGroup.objects.get(category='Other')
            log.info("New type of police event aggregate category: %s" % self.description)
        
        super(PoliceEventGroup, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.description + " :: " + self.category.category
    
    class Meta:
        ordering = ['description']
    

# Issues with Seattle police data:
# 1) Descriptions of issues change across same General Offense Number (look up 201399972 in both data sets)
# 2) Multiple duplicate records in incident reports
# 3) Sometimes lat/lng for Police911Incidents is (0,0)

# 911 Calls are turned into 911 Incidents
class Police911Call(models.Model):
    general_offense_number = models.BigIntegerField(unique=True)
    description = models.CharField(max_length=75) # Event Clearance Description
    group = models.ForeignKey('PoliceEventGroup') # Event Clearance Group
    date = models.DateTimeField() # Event clearance date
    address = models.CharField(max_length=75) # Hundred block location
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return str(self.general_offense_number) + " :: " + self.description + " :: "+ str(self.date)
    
    class Meta:
        ordering = ['-date', '-general_offense_number'] # Some general_offense_numbers have extra digit so 10X larger than others
    

class Police911Incident(models.Model):
    general_offense_number = models.BigIntegerField(unique=True)
    description = models.CharField(max_length=75) # Offense Type
    group = models.ForeignKey('PoliceEventGroup') # Summarized Offense Description
    date = models.DateTimeField() # Date reported
    address = models.CharField(max_length=75) # Hundred block location
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return str(self.general_offense_number) + " :: " + self.description + " :: "+ str(self.date)
    
    class Meta:
        ordering = ['-date', '-general_offense_number']
    
