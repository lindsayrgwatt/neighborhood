# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'BuildingPermit', fields ['category']
        db.create_index('data_buildingpermit', ['category'])

        # Adding index on 'BuildingPermit', fields ['value']
        db.create_index('data_buildingpermit', ['value'])

        # Adding index on 'BuildingPermit', fields ['permit_number']
        db.create_index('data_buildingpermit', ['permit_number'])

        # Adding index on 'FoodViolation', fields ['violation_type']
        db.create_index('data_foodviolation', ['violation_type'])

        # Adding index on 'FoodViolation', fields ['inspection_date']
        db.create_index('data_foodviolation', ['inspection_date'])

        # Adding index on 'Fire', fields ['date']
        db.create_index('data_fire', ['date'])

        # Adding index on 'Fire', fields ['incident_number']
        db.create_index('data_fire', ['incident_number'])

        # Adding index on 'Fire', fields ['aggregate_incident_type']
        db.create_index('data_fire', ['aggregate_incident_type'])

        # Adding index on 'LandPermit', fields ['category']
        db.create_index('data_landpermit', ['category'])

        # Adding index on 'LandPermit', fields ['value']
        db.create_index('data_landpermit', ['value'])

        # Adding index on 'LandPermit', fields ['permit_type']
        db.create_index('data_landpermit', ['permit_type'])

        # Adding index on 'LandPermit', fields ['permit_number']
        db.create_index('data_landpermit', ['permit_number'])

        # Adding index on 'LandPermit', fields ['application_date']
        db.create_index('data_landpermit', ['application_date'])

        # Adding index on 'Violation', fields ['category']
        db.create_index('data_violation', ['category'])

        # Adding index on 'Violation', fields ['case_number']
        db.create_index('data_violation', ['case_number'])

        # Adding index on 'Violation', fields ['date_case_created']
        db.create_index('data_violation', ['date_case_created'])

        # Adding index on 'Police', fields ['effective_date']
        db.create_index('data_police', ['effective_date'])

        # Adding index on 'Police', fields ['general_offense_number']
        db.create_index('data_police', ['general_offense_number'])

        # Adding index on 'Police', fields ['event_clearance_date']
        db.create_index('data_police', ['event_clearance_date'])

        # Adding index on 'Police', fields ['date_reported']
        db.create_index('data_police', ['date_reported'])

        # Adding index on 'Police', fields ['event_aggregate_category']
        db.create_index('data_police', ['event_aggregate_category'])


    def backwards(self, orm):
        # Removing index on 'Police', fields ['event_aggregate_category']
        db.delete_index('data_police', ['event_aggregate_category'])

        # Removing index on 'Police', fields ['date_reported']
        db.delete_index('data_police', ['date_reported'])

        # Removing index on 'Police', fields ['event_clearance_date']
        db.delete_index('data_police', ['event_clearance_date'])

        # Removing index on 'Police', fields ['general_offense_number']
        db.delete_index('data_police', ['general_offense_number'])

        # Removing index on 'Police', fields ['effective_date']
        db.delete_index('data_police', ['effective_date'])

        # Removing index on 'Violation', fields ['date_case_created']
        db.delete_index('data_violation', ['date_case_created'])

        # Removing index on 'Violation', fields ['case_number']
        db.delete_index('data_violation', ['case_number'])

        # Removing index on 'Violation', fields ['category']
        db.delete_index('data_violation', ['category'])

        # Removing index on 'LandPermit', fields ['application_date']
        db.delete_index('data_landpermit', ['application_date'])

        # Removing index on 'LandPermit', fields ['permit_number']
        db.delete_index('data_landpermit', ['permit_number'])

        # Removing index on 'LandPermit', fields ['permit_type']
        db.delete_index('data_landpermit', ['permit_type'])

        # Removing index on 'LandPermit', fields ['value']
        db.delete_index('data_landpermit', ['value'])

        # Removing index on 'LandPermit', fields ['category']
        db.delete_index('data_landpermit', ['category'])

        # Removing index on 'Fire', fields ['aggregate_incident_type']
        db.delete_index('data_fire', ['aggregate_incident_type'])

        # Removing index on 'Fire', fields ['incident_number']
        db.delete_index('data_fire', ['incident_number'])

        # Removing index on 'Fire', fields ['date']
        db.delete_index('data_fire', ['date'])

        # Removing index on 'FoodViolation', fields ['inspection_date']
        db.delete_index('data_foodviolation', ['inspection_date'])

        # Removing index on 'FoodViolation', fields ['violation_type']
        db.delete_index('data_foodviolation', ['violation_type'])

        # Removing index on 'BuildingPermit', fields ['permit_number']
        db.delete_index('data_buildingpermit', ['permit_number'])

        # Removing index on 'BuildingPermit', fields ['value']
        db.delete_index('data_buildingpermit', ['value'])

        # Removing index on 'BuildingPermit', fields ['category']
        db.delete_index('data_buildingpermit', ['category'])


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
            'work_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'data.fire': {
            'Meta': {'ordering': "['-date', 'incident_type']", 'object_name': 'Fire'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'aggregate_incident_type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_number': ('django.db.models.fields.CharField', [], {'max_length': '10', 'db_index': 'True'}),
            'incident_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'data.foodviolation': {
            'Meta': {'ordering': "['-inspection_date']", 'object_name': 'FoodViolation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
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
            'value': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'})
        },
        'data.police': {
            'Meta': {'ordering': "['-general_offense_number', '-effective_date']", 'object_name': 'Police'},
            'cad_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad_event_number': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'census_tract': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'district_sector': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'effective_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'event_aggregate_category': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_category': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_clearance_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_clearance_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'event_clearance_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event_clearance_group': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_detail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'general_offense_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'hundred_block_location': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offense_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'offense_code_extension': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'offense_type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'rms_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'summarized_offense': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'summary_offense_code': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'zone_beat': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'})
        },
        'data.violation': {
            'Meta': {'ordering': "['-case_number']", 'object_name': 'Violation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'case_group': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'case_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '40', 'db_index': 'True'}),
            'date_case_created': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'date_last_inspection': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_inspection_result': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['data']