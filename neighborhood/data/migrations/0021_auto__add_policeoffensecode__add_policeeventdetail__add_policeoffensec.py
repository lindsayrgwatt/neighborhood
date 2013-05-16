# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PoliceOffenseCode'
        db.create_table('data_policeoffensecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=4)),
        ))
        db.send_create_signal('data', ['PoliceOffenseCode'])

        # Adding model 'PoliceEventDetail'
        db.create_table('data_policeeventdetail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=75)),
            ('source_911', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['PoliceEventDetail'])

        # Adding model 'PoliceOffenseCodeExtension'
        db.create_table('data_policeoffensecodeextension', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('data', ['PoliceOffenseCodeExtension'])

        # Adding model 'PoliceSummaryOffenseCode'
        db.create_table('data_policesummaryoffensecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal('data', ['PoliceSummaryOffenseCode'])

        # Adding model 'PoliceEventAggregateGroup'
        db.create_table('data_policeeventaggregategroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
        ))
        db.send_create_signal('data', ['PoliceEventAggregateGroup'])

        # Adding model 'HundredBlockSection'
        db.create_table('data_hundredblocksection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('block', self.gf('django.db.models.fields.CharField')(unique=True, max_length=80)),
        ))
        db.send_create_signal('data', ['HundredBlockSection'])

        # Adding model 'ClearanceCode'
        db.create_table('data_clearancecode', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('code', self.gf('django.db.models.fields.IntegerField')(unique=True)),
        ))
        db.send_create_signal('data', ['ClearanceCode'])

        # Adding model 'CensusTract'
        db.create_table('data_censustract', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tract', self.gf('django.db.models.fields.FloatField')(unique=True)),
        ))
        db.send_create_signal('data', ['CensusTract'])

        # Adding model 'PoliceEventGroup'
        db.create_table('data_policeeventgroup', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.CharField')(unique=True, max_length=34)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceEventAggregateGroup'])),
            ('source_911', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data', ['PoliceEventGroup'])

        # Adding model 'ZoneBeat'
        db.create_table('data_zonebeat', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('beat', self.gf('django.db.models.fields.CharField')(unique=True, max_length=5)),
        ))
        db.send_create_signal('data', ['ZoneBeat'])

        # Adding model 'DistrictSector'
        db.create_table('data_districtsector', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2)),
        ))
        db.send_create_signal('data', ['DistrictSector'])

        # Deleting field 'Police.hundred_block_location'
        db.delete_column('data_police', 'hundred_block_location')

        # Deleting field 'Police.offense_code'
        db.delete_column('data_police', 'offense_code')

        # Deleting field 'Police.offense_code_extension'
        db.delete_column('data_police', 'offense_code_extension')

        # Deleting field 'Police.census_tract'
        db.delete_column('data_police', 'census_tract')

        # Deleting field 'Police.event_detail'
        db.delete_column('data_police', 'event_detail')

        # Deleting field 'Police.event_clearance_group'
        db.delete_column('data_police', 'event_clearance_group')

        # Deleting field 'Police.event_clearance_description'
        db.delete_column('data_police', 'event_clearance_description')

        # Deleting field 'Police.zone_beat'
        db.delete_column('data_police', 'zone_beat')

        # Deleting field 'Police.event_category'
        db.delete_column('data_police', 'event_category')

        # Deleting field 'Police.summary_offense_code'
        db.delete_column('data_police', 'summary_offense_code')

        # Deleting field 'Police.district_sector'
        db.delete_column('data_police', 'district_sector')

        # Deleting field 'Police.offense_type'
        db.delete_column('data_police', 'offense_type')

        # Deleting field 'Police.event_aggregate_category'
        db.delete_column('data_police', 'event_aggregate_category')

        # Deleting field 'Police.summarized_offense'
        db.delete_column('data_police', 'summarized_offense')

        # Deleting field 'Police.event_clearance_code'
        db.delete_column('data_police', 'event_clearance_code')

        # Adding field 'Police.clearance_code'
        db.add_column('data_police', 'clearance_code',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ClearanceCode'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.clearance_description'
        db.add_column('data_police', 'clearance_description',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='description_911', null=True, to=orm['data.PoliceEventDetail']),
                      keep_default=False)

        # Adding field 'Police.clearance_group'
        db.add_column('data_police', 'clearance_group',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='group_911', null=True, to=orm['data.PoliceEventGroup']),
                      keep_default=False)

        # Adding field 'Police.code'
        db.add_column('data_police', 'code',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceOffenseCode'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.code_extension'
        db.add_column('data_police', 'code_extension',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceOffenseCodeExtension'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.offense_detail'
        db.add_column('data_police', 'offense_detail',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='description_incident', null=True, to=orm['data.PoliceEventDetail']),
                      keep_default=False)

        # Adding field 'Police.offense_code_summary'
        db.add_column('data_police', 'offense_code_summary',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceSummaryOffenseCode'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.offense_summary'
        db.add_column('data_police', 'offense_summary',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='group_incident', null=True, to=orm['data.PoliceEventGroup']),
                      keep_default=False)

        # Adding field 'Police.hundred_block'
        db.add_column('data_police', 'hundred_block',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.HundredBlockSection'], null=True),
                      keep_default=False)

        # Adding field 'Police.district'
        db.add_column('data_police', 'district',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.DistrictSector'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.beat'
        db.add_column('data_police', 'beat',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.ZoneBeat'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.census'
        db.add_column('data_police', 'census',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.CensusTract'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.detail'
        db.add_column('data_police', 'detail',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='description_overall', null=True, to=orm['data.PoliceEventDetail']),
                      keep_default=False)

        # Adding field 'Police.category'
        db.add_column('data_police', 'category',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='group_overall', null=True, to=orm['data.PoliceEventGroup']),
                      keep_default=False)

        # Adding field 'Police.aggregate_category'
        db.add_column('data_police', 'aggregate_category',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['data.PoliceEventAggregateGroup'], null=True, blank=True),
                      keep_default=False)

        # Removing index on 'Police', fields ['general_offense_number']
        db.delete_index('data_police', ['general_offense_number'])

        # Adding unique constraint on 'Police', fields ['general_offense_number']
        db.create_unique('data_police', ['general_offense_number'])


    def backwards(self, orm):
        # Removing unique constraint on 'Police', fields ['general_offense_number']
        db.delete_unique('data_police', ['general_offense_number'])

        # Adding index on 'Police', fields ['general_offense_number']
        db.create_index('data_police', ['general_offense_number'])

        # Deleting model 'PoliceOffenseCode'
        db.delete_table('data_policeoffensecode')

        # Deleting model 'PoliceEventDetail'
        db.delete_table('data_policeeventdetail')

        # Deleting model 'PoliceOffenseCodeExtension'
        db.delete_table('data_policeoffensecodeextension')

        # Deleting model 'PoliceSummaryOffenseCode'
        db.delete_table('data_policesummaryoffensecode')

        # Deleting model 'PoliceEventAggregateGroup'
        db.delete_table('data_policeeventaggregategroup')

        # Deleting model 'HundredBlockSection'
        db.delete_table('data_hundredblocksection')

        # Deleting model 'ClearanceCode'
        db.delete_table('data_clearancecode')

        # Deleting model 'CensusTract'
        db.delete_table('data_censustract')

        # Deleting model 'PoliceEventGroup'
        db.delete_table('data_policeeventgroup')

        # Deleting model 'ZoneBeat'
        db.delete_table('data_zonebeat')

        # Deleting model 'DistrictSector'
        db.delete_table('data_districtsector')


        # User chose to not deal with backwards NULL issues for 'Police.hundred_block_location'
        raise RuntimeError("Cannot reverse this migration. 'Police.hundred_block_location' and its values cannot be restored.")
        # Adding field 'Police.offense_code'
        db.add_column('data_police', 'offense_code',
                      self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.offense_code_extension'
        db.add_column('data_police', 'offense_code_extension',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.census_tract'
        db.add_column('data_police', 'census_tract',
                      self.gf('django.db.models.fields.FloatField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_detail'
        db.add_column('data_police', 'event_detail',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_clearance_group'
        db.add_column('data_police', 'event_clearance_group',
                      self.gf('django.db.models.fields.CharField')(max_length=34, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_clearance_description'
        db.add_column('data_police', 'event_clearance_description',
                      self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.zone_beat'
        db.add_column('data_police', 'zone_beat',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_category'
        db.add_column('data_police', 'event_category',
                      self.gf('django.db.models.fields.CharField')(max_length=34, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.summary_offense_code'
        db.add_column('data_police', 'summary_offense_code',
                      self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.district_sector'
        db.add_column('data_police', 'district_sector',
                      self.gf('django.db.models.fields.CharField')(max_length=2, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.offense_type'
        db.add_column('data_police', 'offense_type',
                      self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_aggregate_category'
        db.add_column('data_police', 'event_aggregate_category',
                      self.gf('django.db.models.fields.CharField')(blank=True, max_length=32, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'Police.summarized_offense'
        db.add_column('data_police', 'summarized_offense',
                      self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Police.event_clearance_code'
        db.add_column('data_police', 'event_clearance_code',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Police.clearance_code'
        db.delete_column('data_police', 'clearance_code_id')

        # Deleting field 'Police.clearance_description'
        db.delete_column('data_police', 'clearance_description_id')

        # Deleting field 'Police.clearance_group'
        db.delete_column('data_police', 'clearance_group_id')

        # Deleting field 'Police.code'
        db.delete_column('data_police', 'code_id')

        # Deleting field 'Police.code_extension'
        db.delete_column('data_police', 'code_extension_id')

        # Deleting field 'Police.offense_detail'
        db.delete_column('data_police', 'offense_detail_id')

        # Deleting field 'Police.offense_code_summary'
        db.delete_column('data_police', 'offense_code_summary_id')

        # Deleting field 'Police.offense_summary'
        db.delete_column('data_police', 'offense_summary_id')

        # Deleting field 'Police.hundred_block'
        db.delete_column('data_police', 'hundred_block_id')

        # Deleting field 'Police.district'
        db.delete_column('data_police', 'district_id')

        # Deleting field 'Police.beat'
        db.delete_column('data_police', 'beat_id')

        # Deleting field 'Police.census'
        db.delete_column('data_police', 'census_id')

        # Deleting field 'Police.detail'
        db.delete_column('data_police', 'detail_id')

        # Deleting field 'Police.category'
        db.delete_column('data_police', 'category_id')

        # Deleting field 'Police.aggregate_category'
        db.delete_column('data_police', 'aggregate_category_id')


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
        'data.censustract': {
            'Meta': {'ordering': "['tract']", 'object_name': 'CensusTract'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tract': ('django.db.models.fields.FloatField', [], {'unique': 'True'})
        },
        'data.clearancecode': {
            'Meta': {'ordering': "['code']", 'object_name': 'ClearanceCode'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.districtsector': {
            'Meta': {'ordering': "['district']", 'object_name': 'DistrictSector'},
            'district': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.fire': {
            'Meta': {'ordering': "['-date', 'incident_category']", 'object_name': 'Fire'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_aggregate_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentAggregateType']", 'null': 'True'}),
            'incident_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.FireIncidentType']", 'null': 'True'}),
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
        'data.hundredblocksection': {
            'Meta': {'ordering': "['block']", 'object_name': 'HundredBlockSection'},
            'block': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
            'aggregate_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventAggregateGroup']", 'null': 'True', 'blank': 'True'}),
            'beat': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ZoneBeat']", 'null': 'True', 'blank': 'True'}),
            'cad_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'cad_event_number': ('django.db.models.fields.BigIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_overall'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'census': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.CensusTract']", 'null': 'True', 'blank': 'True'}),
            'clearance_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.ClearanceCode']", 'null': 'True', 'blank': 'True'}),
            'clearance_description': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_911'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'clearance_group': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_911'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceOffenseCode']", 'null': 'True', 'blank': 'True'}),
            'code_extension': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceOffenseCodeExtension']", 'null': 'True', 'blank': 'True'}),
            'date_reported': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'detail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_overall'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'district': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.DistrictSector']", 'null': 'True', 'blank': 'True'}),
            'effective_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'event_clearance_date': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'general_offense_number': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True'}),
            'hundred_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.HundredBlockSection']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'offense_code_summary': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceSummaryOffenseCode']", 'null': 'True', 'blank': 'True'}),
            'offense_detail': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'description_incident'", 'null': 'True', 'to': "orm['data.PoliceEventDetail']"}),
            'offense_summary': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'group_incident'", 'null': 'True', 'to': "orm['data.PoliceEventGroup']"}),
            'point': ('django.contrib.gis.db.models.fields.PointField', [], {}),
            'rms_cdw_id': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'data.policeeventaggregategroup': {
            'Meta': {'ordering': "['category']", 'object_name': 'PoliceEventAggregateGroup'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policeeventdetail': {
            'Meta': {'ordering': "['description']", 'object_name': 'PoliceEventDetail'},
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_911': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.policeeventgroup': {
            'Meta': {'ordering': "['description']", 'object_name': 'PoliceEventGroup'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['data.PoliceEventAggregateGroup']"}),
            'description': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '34'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'source_911': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'data.policeoffensecode': {
            'Meta': {'ordering': "['code']", 'object_name': 'PoliceOffenseCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policeoffensecodeextension': {
            'Meta': {'object_name': 'PoliceOffenseCodeExtension'},
            'code': ('django.db.models.fields.IntegerField', [], {'unique': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'data.policesummaryoffensecode': {
            'Meta': {'object_name': 'PoliceSummaryOffenseCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        },
        'data.zonebeat': {
            'Meta': {'ordering': "['beat']", 'object_name': 'ZoneBeat'},
            'beat': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['data']