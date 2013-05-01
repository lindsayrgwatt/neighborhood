# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Neighborhood'
        db.create_table('hoods_neighborhood', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('region_id', self.gf('django.db.models.fields.IntegerField')()),
            ('mpoly', self.gf('django.contrib.gis.db.models.fields.MultiPolygonField')()),
        ))
        db.send_create_signal('hoods', ['Neighborhood'])


    def backwards(self, orm):
        # Deleting model 'Neighborhood'
        db.delete_table('hoods_neighborhood')


    models = {
        'hoods.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hoods']