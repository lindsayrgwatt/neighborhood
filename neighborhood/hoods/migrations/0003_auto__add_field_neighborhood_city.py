# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Neighborhood.city'
        db.add_column('hoods_neighborhood', 'city',
                      self.gf('django.db.models.fields.CharField')(default='default', max_length=64),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Neighborhood.city'
        db.delete_column('hoods_neighborhood', 'city')


    models = {
        'hoods.neighborhood': {
            'Meta': {'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['hoods']