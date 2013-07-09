# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Singer'
        db.delete_table(u'bbs_singer')


        # Renaming column for 'Quartet.baritone' to match new field type.
        db.rename_column(u'bbs_quartet', 'baritone_id', 'baritone')
        # Changing field 'Quartet.baritone'
        db.alter_column(u'bbs_quartet', 'baritone', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
        # Removing index on 'Quartet', fields ['baritone']
        db.delete_index(u'bbs_quartet', ['baritone_id'])


        # Renaming column for 'Quartet.lead' to match new field type.
        db.rename_column(u'bbs_quartet', 'lead_id', 'lead')
        # Changing field 'Quartet.lead'
        db.alter_column(u'bbs_quartet', 'lead', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
        # Removing index on 'Quartet', fields ['lead']
        db.delete_index(u'bbs_quartet', ['lead_id'])


        # Renaming column for 'Quartet.tenor' to match new field type.
        db.rename_column(u'bbs_quartet', 'tenor_id', 'tenor')
        # Changing field 'Quartet.tenor'
        db.alter_column(u'bbs_quartet', 'tenor', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
        # Removing index on 'Quartet', fields ['tenor']
        db.delete_index(u'bbs_quartet', ['tenor_id'])


        # Renaming column for 'Quartet.bass' to match new field type.
        db.rename_column(u'bbs_quartet', 'bass_id', 'bass')
        # Changing field 'Quartet.bass'
        db.alter_column(u'bbs_quartet', 'bass', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
        # Removing index on 'Quartet', fields ['bass']
        db.delete_index(u'bbs_quartet', ['bass_id'])


        # Renaming column for 'Chorus.director' to match new field type.
        db.rename_column(u'bbs_chorus', 'director_id', 'director')
        # Changing field 'Chorus.director'
        db.alter_column(u'bbs_chorus', 'director', self.gf('django.db.models.fields.CharField')(default='', max_length=200))
        # Removing index on 'Chorus', fields ['director']
        db.delete_index(u'bbs_chorus', ['director_id'])


    def backwards(self, orm):
        # Adding index on 'Chorus', fields ['director']
        db.create_index(u'bbs_chorus', ['director_id'])

        # Adding index on 'Quartet', fields ['bass']
        db.create_index(u'bbs_quartet', ['bass_id'])

        # Adding index on 'Quartet', fields ['tenor']
        db.create_index(u'bbs_quartet', ['tenor_id'])

        # Adding index on 'Quartet', fields ['lead']
        db.create_index(u'bbs_quartet', ['lead_id'])

        # Adding index on 'Quartet', fields ['baritone']
        db.create_index(u'bbs_quartet', ['baritone_id'])

        # Adding model 'Singer'
        db.create_table(u'bbs_singer', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True)),
        ))
        db.send_create_signal(u'bbs', ['Singer'])


        # Renaming column for 'Quartet.baritone' to match new field type.
        db.rename_column(u'bbs_quartet', 'baritone', 'baritone_id')
        # Changing field 'Quartet.baritone'
        db.alter_column(u'bbs_quartet', 'baritone_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Singer']))

        # Renaming column for 'Quartet.lead' to match new field type.
        db.rename_column(u'bbs_quartet', 'lead', 'lead_id')
        # Changing field 'Quartet.lead'
        db.alter_column(u'bbs_quartet', 'lead_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Singer']))

        # Renaming column for 'Quartet.tenor' to match new field type.
        db.rename_column(u'bbs_quartet', 'tenor', 'tenor_id')
        # Changing field 'Quartet.tenor'
        db.alter_column(u'bbs_quartet', 'tenor_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Singer']))

        # Renaming column for 'Quartet.bass' to match new field type.
        db.rename_column(u'bbs_quartet', 'bass', 'bass_id')
        # Changing field 'Quartet.bass'
        db.alter_column(u'bbs_quartet', 'bass_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Singer']))

        # Renaming column for 'Chorus.director' to match new field type.
        db.rename_column(u'bbs_chorus', 'director', 'director_id')
        # Changing field 'Chorus.director'
        db.alter_column(u'bbs_chorus', 'director_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Singer']))

    models = {
        u'bbs.chorus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Chorus'},
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'bbs.contest': {
            'Meta': {'ordering': "['year', 'level', 'contest_type']", 'object_name': 'Contest'},
            'contest_round': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Contest'", 'max_length': '200'}),
            'panel_size': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'time_zone': ('timezone_field.fields.TimeZoneField', [], {'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'contestant_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'bbs.performance': {
            'Meta': {'ordering': "['contest', 'slot']", 'object_name': 'Performance'},
            'avg_mus_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_mus_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_prs_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_prs_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_score_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_score_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_sng_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_sng_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'avg_total_score': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']", 'null': 'True', 'blank': 'True'}),
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_scratch': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'men_on_stage': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'mus_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'mus_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name_one': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name_two': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'place': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prelim': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prs_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'score_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'sng_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sng_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'stage_time': ('django.db.models.fields.DateTimeField', [], {}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bbs.quartet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Quartet'},
            'baritone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bass': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tenor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'bbs.song': {
            'Meta': {'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['bbs']