# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contestant.phone'
        db.add_column(u'bbs_contestant', 'phone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=20, blank=True),
                      keep_default=False)

        # Adding field 'Contestant.lead'
        db.add_column(u'bbs_contestant', 'lead',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Contestant.tenor'
        db.add_column(u'bbs_contestant', 'tenor',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Contestant.baritone'
        db.add_column(u'bbs_contestant', 'baritone',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)

        # Adding field 'Contestant.bass'
        db.add_column(u'bbs_contestant', 'bass',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


        # Changing field 'Contestant.slug'
        db.alter_column(u'bbs_contestant', 'slug', self.gf('django.db.models.fields.SlugField')(default=None, unique=True, max_length=50))
        # Adding unique constraint on 'Contestant', fields ['slug']
        db.create_unique(u'bbs_contestant', ['slug'])


        # Changing field 'Contestant.director'
        db.alter_column(u'bbs_contestant', 'director', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Contestant.location'
        db.alter_column(u'bbs_contestant', 'location', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

        # Changing field 'Contestant.contestant_type'
        db.alter_column(u'bbs_contestant', 'contestant_type', self.gf('django.db.models.fields.IntegerField')(default=None))

        # Changing field 'Quartet.district'
        db.alter_column(u'bbs_quartet', 'district', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'Chorus.district'
        db.alter_column(u'bbs_chorus', 'district', self.gf('django.db.models.fields.IntegerField')(null=True))

    def backwards(self, orm):
        # Removing unique constraint on 'Contestant', fields ['slug']
        db.delete_unique(u'bbs_contestant', ['slug'])

        # Deleting field 'Contestant.phone'
        db.delete_column(u'bbs_contestant', 'phone')

        # Deleting field 'Contestant.lead'
        db.delete_column(u'bbs_contestant', 'lead')

        # Deleting field 'Contestant.tenor'
        db.delete_column(u'bbs_contestant', 'tenor')

        # Deleting field 'Contestant.baritone'
        db.delete_column(u'bbs_contestant', 'baritone')

        # Deleting field 'Contestant.bass'
        db.delete_column(u'bbs_contestant', 'bass')


        # Changing field 'Contestant.slug'
        db.alter_column(u'bbs_contestant', 'slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True))

        # Changing field 'Contestant.director'
        db.alter_column(u'bbs_contestant', 'director', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Contestant.location'
        db.alter_column(u'bbs_contestant', 'location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

        # Changing field 'Contestant.contestant_type'
        db.alter_column(u'bbs_contestant', 'contestant_type', self.gf('django.db.models.fields.IntegerField')(null=True))

        # User chose to not deal with backwards NULL issues for 'Quartet.district'
        raise RuntimeError("Cannot reverse this migration. 'Quartet.district' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Chorus.district'
        raise RuntimeError("Cannot reverse this migration. 'Chorus.district' and its values cannot be restored.")

    models = {
        u'bbs.chorus': {
            'Meta': {'ordering': "['name']", 'object_name': 'Chorus'},
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
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
            'baritone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bass': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'contestant_type': ('django.db.models.fields.IntegerField', [], {}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'facebook': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lead': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'tenor': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
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
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
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