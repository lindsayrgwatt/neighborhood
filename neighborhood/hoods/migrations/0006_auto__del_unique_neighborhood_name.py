# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['name']
        db.delete_unique('hoods_neighborhood', ['name'])


    def backwards(self, orm):
        # Adding unique constraint on 'Neighborhood', fields ['name']
        db.create_unique('hoods_neighborhood', ['name'])


    models = {
        'hoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['hoods']