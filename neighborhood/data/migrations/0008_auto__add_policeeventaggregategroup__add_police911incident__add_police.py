# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PoliceEventAggregateGroup'
        db.create_table('data_policeeventaggregategroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('data', ['PoliceEventAggregateGroup'])

        # Adding model 'Police911Incident'
        db.create_table('data_police911incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_offense_number', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceEventGroup'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('data', ['Police911Incident'])

        # Adding model 'Police911Call'
        db.create_table('data_police911call', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('general_offense_number', self.gf('django.db.models.fields.BigIntegerField')(unique=True)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceEventGroup'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=75)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('data', ['Police911Call'])

        # Adding model 'PoliceEventGroup'
        db.create_table('data_policeeventgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceEventAggregateGroup'])),
        ))
        db.send_create_signal('data', ['PoliceEventGroup'])


    def backwards(self, orm):
        # Deleting model 'PoliceEventAggregateGroup'
        db.delete_table('data_policeeventaggregategroup')

        # Deleting model 'Police911Incident'
        db.delete_table('data_police911incident')

        # Deleting model 'Police911Call'
        db.delete_table('data_police911call')

        # Deleting model 'PoliceEventGroup'
        db.delete_table('data_policeeventgroup')


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
            'violation_num': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'violation_type': ('django.db.models.fields.CharField', [], {'max_length': '4'})
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
        'data.police911call': {
            'Meta': {'ordering': "['-general_offense_number', '-date']", 'object_name': 'Police911Call'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'general_offense_number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'data.police911incident': {
            'Meta': {'ordering': "['-general_offense_number', '-date']", 'object_name': 'Police911Incident'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '75'}),
            'general_offense_number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventGroup']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {})
        },
        'data.policeeventaggregategroup': {
            'Meta': {'ordering': "['category']", 'object_name': 'PoliceEventAggregateGroup'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policeeventgroup': {
            'Meta': {'ordering': "['description']", 'object_name': 'PoliceEventGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventAggregateGroup']"}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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