# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FireIncidentAggregateType'
        db.create_table('data_fireincidentaggregatetype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal('data', ['FireIncidentAggregateType'])

        # Adding model 'FireIncidentType'
        db.create_table('data_fireincidenttype', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
            ('aggregate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FireIncidentAggregateType'])),
        ))
        db.send_create_signal('data', ['FireIncidentType'])

        # Adding model 'Fire'
        db.create_table('data_fire', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('incident_number', self.gf('django.db.models.fields.CharField')(max_length=10, db_index=True)),
            ('incident_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.FireIncidentType'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('point', self.gf('django.contrib.gis.db.models.fields.PointField')()),
        ))
        db.send_create_signal('data', ['Fire'])


    def backwards(self, orm):
        # Deleting model 'FireIncidentAggregateType'
        db.delete_table('data_fireincidentaggregatetype')

        # Deleting model 'FireIncidentType'
        db.delete_table('data_fireincidenttype')

        # Deleting model 'Fire'
        db.delete_table('data_fire')


    models = {
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
        }
    }

    complete_apps = ['data']