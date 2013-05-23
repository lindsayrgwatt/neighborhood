# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PermitValue'
        db.create_table('data_permitvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.IntegerField')(unique=True)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('data', ['PermitValue'])

        # Adding model 'BuildingPermit'
        db.create_table('data_buildingpermit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('permit_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('application_date', self.gf('django.db.models.fields.DateField')(db_index=True)),
            ('permit_number', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('value', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
            ('value_range', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PermitValue'], null=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('data', ['BuildingPermit'])


    def backwards(self, orm):
        # Deleting model 'PermitValue'
        db.delete_table('data_permitvalue')

        # Deleting model 'BuildingPermit'
        db.delete_table('data_buildingpermit')


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
            'value_range': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PermitValue']", 'null': 'True'})
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
        'data.permitvalue': {
            'Meta': {'ordering': "['-value']", 'object_name': 'PermitValue'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'value': ('django.db.models.fields.IntegerField', [], {'unique': 'True'})
        }
    }

    complete_apps = ['data']