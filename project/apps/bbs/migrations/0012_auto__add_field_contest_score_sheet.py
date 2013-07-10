# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contest.score_sheet'
        db.add_column(u'bbs_contest', 'score_sheet',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contest.score_sheet'
        db.delete_column(u'bbs_contest', 'score_sheet')


    models = {
        u'bbs.contest': {
            'Meta': {'ordering': "['year', 'contest_level', 'contest_type']", 'object_name': 'Contest'},
            'contest_level': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'panel_size': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'score_sheet': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'time_zone': ('timezone_field.fields.TimeZoneField', [], {'default': "'US/Eastern'"}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'baritone': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'bass': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'contestant_type': ('django.db.models.fields.IntegerField', [], {}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {}),
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
        u'bbs.score': {
            'Meta': {'ordering': "['contest', 'contest_round', 'contestant']", 'object_name': 'Score'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']"}),
            'contest_round': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'men_on_stage': ('django.db.models.fields.IntegerField', [], {'default': '4', 'null': 'True'}),
            'mus1': ('django.db.models.fields.IntegerField', [], {}),
            'mus2': ('django.db.models.fields.IntegerField', [], {}),
            'prs1': ('django.db.models.fields.IntegerField', [], {}),
            'prs2': ('django.db.models.fields.IntegerField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'sng1': ('django.db.models.fields.IntegerField', [], {}),
            'sng2': ('django.db.models.fields.IntegerField', [], {}),
            'song1': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'song2': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['bbs']