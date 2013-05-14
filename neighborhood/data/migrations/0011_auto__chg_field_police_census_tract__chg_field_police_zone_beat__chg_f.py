# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Police.census_tract'
        db.alter_column('data_police', 'census_tract', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'Police.zone_beat'
        db.alter_column('data_police', 'zone_beat', self.gf('django.db.models.fields.CharField')(max_length=2, null=True))

        # Changing field 'Police.district_sector'
        db.alter_column('data_police', 'district_sector', self.gf('django.db.models.fields.CharField')(max_length=1, null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Police.census_tract'
        raise RuntimeError("Cannot reverse this migration. 'Police.census_tract' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Police.zone_beat'
        raise RuntimeError("Cannot reverse this migration. 'Police.zone_beat' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Police.district_sector'
        raise RuntimeError("Cannot reverse this migration. 'Police.district_sector' and its values cannot be restored.")

    models = {
        'data.buildingpermit': {
            'Meta': {'ordering': "['-application_date', 'permit_type']", 'object_name': 'BuildingPermit'},
            'action_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'applicant_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'application_date': ('django.db.models.fields.DateTimeField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {}),
            'permit_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {}),
            'work_type': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        'data.fire': {
            'Meta': {'ordering': "['-date', 'incident_type']", 'object_name': 'Fire'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'aggregate_incident_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'incident_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'data.foodviolation': {
            'Meta': {'ordering': "['-inspection_date']", 'object_name': 'FoodViolation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'business_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateTimeField', [], {}),
            'inspection_serial_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'inspection_type': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'place_description': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'program_identifier': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'violation_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'violation_description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'violation_record_num': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'violation_type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        'data.landpermit': {
            'Meta': {'ordering': "['-application_date', 'permit_type']", 'object_name': 'LandPermit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'appealed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'applicant_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'application_date': ('django.db.models.fields.DateTimeField', [], {}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'decision_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'edg_required': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {}),
            'permit_type': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {})
        },
        'data.police': {
            'Meta': {'ordering': "['-effective_date']", 'object_name': 'Police'},
            'cad_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad_event_number': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'census_tract': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'district_sector': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'effective_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_aggregate_category': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_category': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_clearance_code': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'event_clearance_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'event_clearance_description': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'event_clearance_group': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'event_detail': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'general_offense_number': ('django.db.models.fields.IntegerField', [], {}),
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
            'case_number': ('django.db.models.fields.IntegerField', [], {}),
            'case_type': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'date_case_created': ('django.db.models.fields.DateTimeField', [], {}),
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