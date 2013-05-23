# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding unique constraint on 'FoodViolation', fields ['violation_num']
        db.create_unique('data_foodviolation', ['violation_num'])


    def backwards(self, orm):
        # Removing unique constraint on 'FoodViolation', fields ['violation_num']
        db.delete_unique('data_foodviolation', ['violation_num'])


    models = {
        'data.buildingpermit': {
            'Meta': {'ordering': "['-application_date', 'permit_type']", 'object_name': 'BuildingPermit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'application_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'permit_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'value_range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PermitValue']"})
        },
        'data.fire': {
            'Meta': {'ordering': "['-date', 'incident_category']", 'object_name': 'Fire'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentType']"}),
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
            'code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inspection_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'violation_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'})
        },
        'data.landpermit': {
            'Meta': {'ordering': "['-application_date', '-permit_number']", 'object_name': 'LandPermit'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'application_date': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'permit_number': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'value': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'value_range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PermitValue']"})
        },
        'data.permitvalue': {
            'Meta': {'ordering': "['-value']", 'object_name': 'PermitValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        },
        'data.violation': {
            'Meta': {'ordering': "['-case_number']", 'object_name': 'Violation'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'case_number': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'date_case_created': ('django.db.models.fields.DateField', [], {'db_index': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ViolationCategory']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
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
        }
    }

    complete_apps = ['data']