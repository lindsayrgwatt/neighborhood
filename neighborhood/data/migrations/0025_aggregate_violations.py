# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        for violation in orm.Violation.objects.all():
            violation.group = orm.ViolationCategory.objects.get(category=violation.case_group)
            violation.aggregate = violation.group.aggregate
            
            violation.save()
        
        for violation in orm.FoodViolation.objects.all():
            violation.group = orm.ViolationCategory.objects.get(category='FOOD INSPECTION')
            violation.aggregate = violation.group.aggregate
            
            violation.save()
        
    
    def backwards(self, orm):
        for violation in orm.Violation.objects.all():
            violation.group = None
            violation.aggregate = None
            
            violation.save()
        
        for violation in orm.FoodViolation.objects.all():
            violation.group = None
            violation.aggregate = None
            
            violation.save()

    models = {
        'data.buildingpermit': {
            'Meta': {'ordering': "['-application_date', 'permit_type']", 'object_name': 'BuildingPermit'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'applicant_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'application_date': ('django.db.models.fields.DateTimeField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'permit_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'value_range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PermitValue']", 'null': 'True'}),
            'work_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'data.censustract': {
            'Meta': {'object_name': 'CensusTract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tract': ('django.db.models.fields.FloatField', [], {'unique': 'True'})
        },
        'data.clearancecode': {
            'Meta': {'object_name': 'ClearanceCode'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.districtsector': {
            'Meta': {'object_name': 'DistrictSector'},
            'district': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.fire': {
            'Meta': {'ordering': "['-date', 'incident_category']", 'object_name': 'Fire'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_aggregate_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentAggregateType']", 'null': 'True'}),
            'incident_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentType']", 'null': 'True'}),
            'incident_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'data.fireincidentaggregatetype': {
            'Meta': {'object_name': 'FireIncidentAggregateType'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.fireincidenttype': {
            'Meta': {'ordering': "['description']", 'object_name': 'FireIncidentType'},
            'aggregate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentAggregateType']"}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.foodviolation': {
            'Meta': {'ordering': "['-inspection_date']", 'object_name': 'FoodViolation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'aggregate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationAggregateCategory']", 'null': 'True'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationCategory']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'inspection_serial_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'inspection_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'place_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'program_identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'violation_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'violation_description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'violation_record_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'violation_type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'})
        },
        'data.hundredblocksection': {
            'Meta': {'object_name': 'HundredBlockSection'},
            'block': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.landpermit': {
            'Meta': {'ordering': "['-application_date', 'permit_type']", 'object_name': 'LandPermit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'appealed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'applicant_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'application_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30', 'db_index': 'True'}),
            'decision_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edg_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'permit_type': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'value_range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PermitValue']", 'null': 'True', 'blank': 'True'})
        },
        'data.permitvalue': {
            'Meta': {'ordering': "['-value']", 'object_name': 'PermitValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'data.police': {
            'Meta': {'ordering': "['-general_offense_number', '-effective_date']", 'object_name': 'Police'},
            'aggregate_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventAggregateGroup']", 'null': 'True', 'blank': 'True'}),
            'beat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ZoneBeat']", 'null': 'True', 'blank': 'True'}),
            'cad_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad_event_number': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_overall'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'census': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CensusTract']", 'null': 'True', 'blank': 'True'}),
            'clearance_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ClearanceCode']", 'null': 'True', 'blank': 'True'}),
            'clearance_description': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_911'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'clearance_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_911'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceOffenseCode']", 'null': 'True', 'blank': 'True'}),
            'code_extension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceOffenseCodeExtension']", 'null': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_overall'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.DistrictSector']", 'null': 'True', 'blank': 'True'}),
            'effective_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'event_clearance_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'general_offense_number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'hundred_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.HundredBlockSection']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offense_code_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceSummaryOffenseCode']", 'null': 'True', 'blank': 'True'}),
            'offense_detail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_incident'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'offense_summary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_incident'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'rms_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.policeeventaggregategroup': {
            'Meta': {'ordering': "['category']", 'object_name': 'PoliceEventAggregateGroup'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policeeventdetail': {
            'Meta': {'ordering': "['description']", 'object_name': 'PoliceEventDetail'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_911': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.policeeventgroup': {
            'Meta': {'ordering': "['description']", 'object_name': 'PoliceEventGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventAggregateGroup']"}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '34'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_911': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.policeoffensecode': {
            'Meta': {'object_name': 'PoliceOffenseCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policeoffensecodeextension': {
            'Meta': {'object_name': 'PoliceOffenseCodeExtension'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policesummaryoffensecode': {
            'Meta': {'object_name': 'PoliceSummaryOffenseCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.violation': {
            'Meta': {'ordering': "['-case_number']", 'object_name': 'Violation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'aggregate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationAggregateCategory']", 'null': 'True'}),
            'case_group': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'case_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'date_case_created': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_last_inspection': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationCategory']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_inspection_result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'data.violationaggregatecategory': {
            'Meta': {'ordering': "['category']", 'object_name': 'ViolationAggregateCategory'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.violationcategory': {
            'Meta': {'ordering': "['category']", 'object_name': 'ViolationCategory'},
            'aggregate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationAggregateCategory']"}),
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.zonebeat': {
            'Meta': {'object_name': 'ZoneBeat'},
            'beat': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['data']
    symmetrical = True
