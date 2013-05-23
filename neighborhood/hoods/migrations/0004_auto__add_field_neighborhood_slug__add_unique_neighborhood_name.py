# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Neighborhood.slug'
        db.add_column('hoods_neighborhood', 'slug',
                      self.gf('django.db.models.fields.SlugField')(default=' ', max_length=64),
                      keep_default=False)

        # Adding unique constraint on 'Neighborhood', fields ['name']
        db.create_unique('hoods_neighborhood', ['name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Neighborhood', fields ['name']
        db.delete_unique('hoods_neighborhood', ['name'])

        # Deleting field 'Neighborhood.slug'
        db.delete_column('hoods_neighborhood', 'slug')


    models = {
        'hoods.neighborhood': {
            'Meta': {'ordering': "['name']", 'object_name': 'Neighborhood'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mpoly': ('django.contrib.gis.db.models.fields.MultiPolygonField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'region_id': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['hoods']