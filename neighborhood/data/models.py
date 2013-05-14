import logging

from django.contrib.gis.db import models

log = logging.getLogger(__name__)

CRIME_MAPPING = {
    'ACCIDENT INVESTIGATION':'Traffic',
    'ANIMAL COMPLAINT':'Other',
    'ANIMAL COMPLAINTS':'Other',
    'ARREST':'Arrest',
    'ASSAULT':'Assault, Threats and Weapons',
    'ASSAULTS':'Assault, Threats and Weapons',
    'AUTO THEFTS':'Theft or Similar',
    'BIAS INCIDENT':'Other',
    'BIKE':'Other',
    'BIKE THEFT':'Theft or Similar',
    'BURGLARY':'Theft or Similar',
    'BURGLARY-SECURE PARKING-RES':'Theft or Similar',
    'Bike Theft':'Theft or Similar',
    'CAR PROWL':'Mischief and Suspicious People',
    'COUNTERFEIT':'Theft or Similar',
    'Car Prowl':'Mischief and Suspicious People',
    'DISORDERLY CONDUCT':'Disturbances',
    'DISPUTE':'Disturbances',
    'DISTURBANCE':'Disturbances',
    'DISTURBANCES':'Disturbances',
    'DRIVE BY (NO INJURY)':'Disturbances',
    'DUI':'Drugs and Liquor',
    'ELUDING':'Arrest',
    'EMBEZZLE':'Theft or Similar',
    'ESCAPE':'Other',
    'EXTORTION':'Theft or Similar',
    'FAILURE TO REGISTER (SEX OFFENDER)':'Other',
    'FALSE ALARMS':'False Alarm',
    'FALSE REPORT':'False Alarm',
    'FIREWORK':'Disturbances',
    'FORGERY':'Theft or Similar',
    'FRAUD':'Theft or Similar',
    'FRAUD AND FINANCIAL':'Theft or Similar',
    'FRAUD CALLS':'Theft or Similar',
    'GAMBLE':'Prostitution, Vice and Gambling',
    'HARBOR CALLS':'Other',
    'HAZARDS':'Other',
    'HOMICIDE':'Homicide',
    'ILLEGAL DUMPING':'Disturbances',
    'INJURY':'Other',
    'LEWD CONDUCT':'Disturbances',
    'LIQUOR VIOLATION':'Drugs and Liquor',
    'LIQUOR VIOLATIONS':'Drugs and Liquor',
    'LOITERING':'Mischief and Suspicious People',
    'LOST PROPERTY':'Other',
    'MAIL THEFT':'Theft or Similar',
    'MENTAL HEALTH':'Other',
    'MISCELLANEOUS MISDEMEANORS':'Other',
    'NARCOTICS':'Drugs and Liquor',
    'NARCOTICS COMPLAINTS':'Drugs and Liquor',
    'NUISANCE, MISCHIEF':'Mischief and Suspicious People',
    'NUISANCE, MISCHIEF':'Mischief and Suspicious People',
    'OBSTRUCT':'Other',
    'OTHER PROPERTY':'Theft or Similar',
    'OTHER VICE':'Prostitution, Vice and Gambling',
    'Other Property':'Theft or Similar',
    'PERSON DOWN/INJURY':'Other',
    'PERSONS - LOST, FOUND, MISSING':'Other',
    'PICKPOCKET':'Theft or Similar',
    'PORNOGRAPHY':'Prostitution, Vice and Gambling',
    'PROPERTY - MISSING, FOUND':'Other',
    'PROPERTY DAMAGE':'Disturbances',
    'PROSTITUTION':'Prostitution, Vice and Gambling',
    'PROWLER':'Mischief and Suspicious People',
    'PUBLIC NUISANCE':'Mischief and Suspicious People',
    'PURSE SNATCH':'Theft or Similar',
    'Pickpocket':'Theft or Similar',
    'Purse Snatch':'Theft or Similar',
    'RECKLESS BURNING':'Disturbances',
    'RECOVERED PROPERTY':'Other',
    'ROBBERY':'Theft or Similar',
    'SHOPLIFTING':'Theft or Similar',
    'STAY OUT OF AREA OF DRUGS':'Drugs and Liquor',
    'STAY OUT OF AREA OF PROSTITUTION':'Prostitution, Vice and Gambling',
    'STOLEN PROPERTY':'Theft or Similar',
    'SUSPICIOUS CIRCUMSTANCES':'Mischief and Suspicious People',
    'Shoplifting':'Theft or Similar',
    'THEFT OF SERVICES':'Theft or Similar',
    'THREATS':'Assault, Threats and Weapons',
    'THREATS, HARASSMENT':'Assault, Threats and Weapons',
    'TRAFFIC':'Traffic',
    'TRAFFIC RELATED CALLS':'Traffic',
    'TRESPASS':'Disturbances',
    'VEHICLE THEFT':'Theft or Similar',
    'VICE CALLS':'Prostitution, Vice and Gambling',
    'VIOLATION OF COURT ORDER':'Arrest',
    'WARRANT ARREST':'Arrest',
    'WEAPON':'Assault, Threats and Weapons',
    'WEAPONS CALLS':'Assault, Threats and Weapons',
    '[INC - CASE DC USE ONLY]':'Other',
}

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
    
    general_offense_number = models.IntegerField() # Join across both 911 and incident repsonse
    
    # Only for 911
    cad_cdw_id = models.IntegerField(blank=True, null=True)
    cad_event_number = models.BigIntegerField(blank=True, null=True)
    event_clearance_code = models.IntegerField(blank=True, null=True)
    event_clearance_description = models.CharField(blank=True, null=True, max_length=100) # Best 911 description
    event_clearance_group = models.CharField(blank=True, null=True, max_length=32) # Aggregated 911 description
    event_clearance_date = models.DateTimeField(blank=True, null=True)
    
    # Only for incident reports
    rms_cdw_id = models.IntegerField(blank=True, null=True)
    offense_code = models.CharField(blank=True, null=True, max_length=5) # Some have value 'X' but most are integers
    offense_code_extension = models.IntegerField(blank=True, null=True)
    offense_type = models.CharField(blank=True, null=True, max_length=100) # Best incident report description
    summary_offense_code = models.CharField(blank=True, null=True, max_length=5) 
    summarized_offense = models.CharField(blank=True, null=True, max_length=32) # Aggregated incident report description
    date_reported = models.DateTimeField(blank=True, null=True)
    
    # Common to both 911 and incident reports
    # Blanks and nulls are allowed based on experience with data; sometimes it's just missing
    hundred_block_location = models.CharField(max_length=50)
    district_sector = models.CharField(max_length=1, blank=True, null=True)
    zone_beat = models.CharField(max_length=2, blank=True, null=True)
    census_tract = models.FloatField(blank=True, null=True) 
    
    # Calculated values
    # Allow null values so that can use get_or_create effectively
    event_detail = models.CharField(max_length=100, blank=True, null=True)
    event_category = models.CharField(max_length=32, blank=True, null=True)
    event_aggregate_category = models.CharField(max_length=32, blank=True, null=True)
    effective_date = models.DateTimeField(blank=True, null=True)
    
    point = models.PointField(help_text="Represented as 'POINT(longitude, latitude)'")
    objects = models.GeoManager()
    
    def save(self, *args, **kwargs):
        # For descriptions, police incident reports trump 911
        if self.offense_type:
            self.event_detail = self.offense_type
        elif self.event_clearance_description:
            self.event_detail = self.event_clearance_description
        
        if self.summarized_offense:
            self.event_category = self.summarized_offense
        elif self.event_clearance_group:
            self.event_category = self.event_clearance_group
        
        # For reporting times, 911 trumps police incident reports
        if self.event_clearance_date:
            self.effective_date = self.event_clearance_date
        elif self.date_reported:
            self.effective_date = self.event_clearance_date
        
        if self.event_category in CRIME_MAPPING:
            self.event_aggregate_category = CRIME_MAPPING[self.event_category]
        else:
            self.event_aggregate_category = 'Other'
            if self.event_category != '' and self.event_category != ' ' and self.event_category != None:
                log.error("New type of crime category: %s" % self.event_category)
        
        super(Police, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return str(self.general_offense_number) + " :: " + self.event_aggregate_category + " :: "+ str(self.effective_date)
    
    class Meta:
        ordering = ['-general_offense_number', '-effective_date']

