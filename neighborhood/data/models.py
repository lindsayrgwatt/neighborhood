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
    address = models.CharField(max_length=100)
    incident_number = models.CharField(max_length=10, db_index=True)
    incident_category = models.ForeignKey('FireIncidentType', null=True)
    incident_aggregate_category = models.ForeignKey('FireIncidentAggregateType', null=True, editable=False)
    date = models.DateTimeField(db_index=True)
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.incident_number + " :: " + self.incident_category.description + " :: " + str(self.date)
    
    class Meta:
        ordering = ['-date', 'incident_category']
    
    def save(self, *args, **kwargs):
        self.incident_aggregate_category = self.incident_category.aggregate
        
        super(Fire, self).save(*args, **kwargs)
    


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
        if permit.value < value:
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
    


class LandPermit(models.Model):
    permit_type = models.CharField(max_length=40, db_index=True)
    status = models.CharField(max_length=50)
    application_date = models.DateTimeField(db_index=True)
    applicant_name = models.CharField(max_length=100)
    permit_number = models.IntegerField(db_index=True)
    edg_required = models.BooleanField()
    category = models.CharField(max_length=30, db_index=True)
    appealed = models.BooleanField()
    address = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(db_index=True)
    value_range = models.ForeignKey('PermitValue', db_index=True, null=True, blank=True)
    decision_type = models.CharField(max_length=1)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.permit_type + " :: " + str(self.permit_number) + " :: " + str(self.application_date)
        
    def save(self, *args, **kwargs):
        self = calc_permit_value(self)
        
        super(LandPermit, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-application_date', 'permit_type']
    


class BuildingPermit(models.Model):
    permit_type = models.CharField(max_length=30)
    status = models.CharField(max_length=50)
    application_date = models.DateTimeField()
    work_type = models.CharField(max_length=30)
    applicant_name = models.CharField(max_length=100)
    permit_number = models.IntegerField(db_index=True)
    category = models.CharField(max_length=30, db_index=True)
    action_type = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    description = models.TextField()
    value = models.IntegerField(db_index=True)
    value_range = models.ForeignKey('PermitValue', db_index=True, null=True)
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
    

class Violation(models.Model):
    case_number = models.IntegerField(db_index=True)
    case_type = models.CharField(max_length=40)
    address = models.CharField(max_length=100)
    description = models.TextField()
    #case_group = models.CharField(max_length=40)
    group = models.ForeignKey('ViolationCategory', db_index=True, null=True)
    #category = models.CharField(max_length=40, db_index=True) # The derived category based on case_group
    aggregate = models.ForeignKey('ViolationAggregateCategory', db_index=True, null=True)
    date_case_created = models.DateTimeField(db_index=True)
    date_last_inspection = models.DateTimeField(null=True, blank=True)
    last_inspection_result = models.CharField(max_length=10, null=True, blank=True)
    status = models.CharField(max_length=32)
    url = models.URLField()
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.group.category + " :: " + str(self.case_number) + " :: "  + str(self.date_case_created)
    
    class Meta:
        ordering = ['-case_number']
    


class FoodViolation(models.Model):
    name = models.CharField(max_length=100)
    program_identifier = models.CharField(max_length=100)
    inspection_date = models.DateTimeField(db_index=True)
    place_description = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    business_name = models.CharField(max_length=100)
    inspection_type = models.CharField(max_length=50)
    violation_type = models.CharField(max_length=10, db_index=True)
    group = models.ForeignKey('ViolationCategory', db_index=True, null=True)
    aggregate = models.ForeignKey('ViolationAggregateCategory', db_index=True, null=True)
    violation_code = models.CharField(max_length=4)
    violation_description = models.CharField(max_length=250)
    inspection_serial_num = models.CharField(max_length=10)
    violation_record_num = models.CharField(max_length=10)
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def __unicode__(self):
        return self.business_name + " :: " + str(self.inspection_date)
    
    def save(self):
        self.group = ViolationCategory.objects.get(category='FOOD INSPECTION')
        self.aggregate = self.group.aggregate
        
        super(FoodViolation, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['-inspection_date']


##############################################
# 
# Police Info
#
class HundredBlockSection(models.Model):
    block = models.CharField(max_length=80, unique=True)
    
    def __unicode__(self):
        return self.block
    


class ZoneBeat(models.Model):
    beat = models.CharField(max_length=5, unique=True)
    
    def __unicode__(self):
        return self.beat
    


class DistrictSector(models.Model):
    district = models.CharField(max_length=2, unique=True)
    
    def __unicode__(self):
        return self.district
    


class CensusTract(models.Model):
    tract = models.FloatField(unique=True)
    
    def __unicode__(self):
        return str(self.tract)
    


class ClearanceCode(models.Model):
    code = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return str(self.code)
    


class PoliceEventDetail(models.Model):
    # Union of 911 Event Clearance Descriptions and Incident Reports' 
    description = models.CharField(max_length=75, unique=True)
    source_911 = models.BooleanField() # True if description came from 911 reports, not incident reports
    
    def __unicode__(self):
        return self.description
    
    class Meta:
        ordering = ['description']
    


class PoliceEventAggregateGroup(models.Model):
    category = models.CharField(max_length=32, unique=True)
    
    def __unicode__(self):
        return self.category
    
    class Meta:
        ordering = ['category']
    


class PoliceEventGroup(models.Model):
    # Union of 911 Event Clearance Group and Incident Reports' 
    description = models.CharField(max_length=34, unique=True)
    category = models.ForeignKey('PoliceEventAggregateGroup')
    source_911 =models.BooleanField() # True if description came from 911 reports, not incident reports
    
    def save(self, *args, **kwargs):
        if not hasattr(self, 'category'):
            self.category = PoliceEventAggregateGroup.objects.get(category='Other')
            log.info("New type of police event aggregate category: %s" % self.description)
        
        super(PoliceEventGroup, self).save(*args, **kwargs)
    
    
    def __unicode__(self):
        return self.description + " :: " + self.category.category
    
    class Meta:
        ordering = ['description']


class PoliceOffenseCode(models.Model):
    code = models.CharField(max_length=4, unique=True) # Some have value 'X' but most are integers
    
    def __unicode__(self):
        return self.code
    


class PoliceOffenseCodeExtension(models.Model):
    code = models.IntegerField(unique=True)
    
    def __unicode__(self):
        return str(self.code)
    


class PoliceSummaryOffenseCode(models.Model):
    code = models.CharField(max_length=5, unique=True)
    
    def __unicode__(self):
        return self.code
    


class Police(models.Model):
    # This model unifies 911 police incident reports and actual police incident reports
    # Idea is that the union of both represents how citizens feel crime is occuring
    # 911: https://data.seattle.gov/Public-Safety/Seattle-Police-Department-911-Incident-Response/3k2p-39jp
    # Report incidents: https://data.seattle.gov/Public-Safety/Seattle-Police-Department-Police-Report-Incident/7ais-f98f
    #
    # Several issues with this:
    # 1) Descriptions of issues change across same General Offense Number (look up 201399972 in both data sets)
    # 2) Multiple duplicate records in incident reports
    # 
    # Model uses computed fields on save() to reconcile everything
    
    general_offense_number = models.BigIntegerField(unique=True) # Join across both 911 and incident repsonse
    
    # Only for 911
    cad_cdw_id = models.IntegerField(blank=True, null=True)
    cad_event_number = models.BigIntegerField(blank=True, null=True)
    clearance_code = models.ForeignKey('ClearanceCode', blank=True, null=True)
    clearance_description = models.ForeignKey('PoliceEventDetail', blank=True, null=True, related_name='description_911') # Best 911 description
    clearance_group = models.ForeignKey('PoliceEventGroup', blank=True, null=True, related_name='group_911') # Roll up of 911 descriptions
    event_clearance_date = models.DateTimeField(blank=True, null=True, db_index=True)
    
    # Only for incident reports
    rms_cdw_id = models.IntegerField(blank=True, null=True)
    code = models.ForeignKey('PoliceOffenseCode', blank=True, null=True)
    code_extension = models.ForeignKey('PoliceOffenseCodeExtension', blank=True, null=True)
    offense_detail = models.ForeignKey('PoliceEventDetail', blank=True, null=True, related_name='description_incident') # Best incident report description
    offense_code_summary = models.ForeignKey('PoliceSummaryOffenseCode', blank=True, null=True)
    offense_summary = models.ForeignKey('PoliceEventGroup', blank=True, null=True, related_name='group_incident') #Roll up of incident report descriptions
    date_reported = models.DateTimeField(blank=True, null=True, db_index=True)
    
    # Common to both 911 and incident reports
    # Blanks and nulls are allowed based on experience with data; sometimes it's just missing
    hundred_block = models.ForeignKey('HundredBlockSection', null=True)
    district = models.ForeignKey('DistrictSector', blank=True, null=True)
    beat = models.ForeignKey('ZoneBeat', blank=True, null=True)
    census = models.ForeignKey('CensusTract', blank=True, null=True)
    
    # Calculated values
    # Allow null values so that can use get_or_create effectively
    detail = models.ForeignKey('PoliceEventDetail', blank=True, null=True, editable=False, db_index=True, related_name='description_overall')
    category = models.ForeignKey('PoliceEventGroup', blank=True, null=True, editable=False, db_index=True, related_name='group_overall')
    aggregate_category = models.ForeignKey('PoliceEventAggregateGroup', blank=True, null=True, editable=False, db_index=True)
    effective_date = models.DateTimeField(blank=True, null=True, db_index=True)
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def save(self, *args, **kwargs):
        # For descriptions, police incident reports trump 911
        if self.clearance_description:
            self.detail = self.clearance_description
        if self.offense_detail:
            self.detail = self.offense_detail
        
        if self.clearance_group:
            self.category = self.clearance_group
        elif self.offense_summary:
            self.category = self.offense_summary
        
        if self.category:
            self.aggregate_category = self.category.category
        
        # For reporting times, 911 trumps police incident reports
        if self.event_clearance_date:
            self.effective_date = self.event_clearance_date
        if self.date_reported:
            self.effective_date = self.date_reported
        
        super(Police, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return str(self.general_offense_number) + " :: " + self.category.description + " :: "+ str(self.effective_date)
    
    class Meta:
        ordering = ['-general_offense_number', '-effective_date']

