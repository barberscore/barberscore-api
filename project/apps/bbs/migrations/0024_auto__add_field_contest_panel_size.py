# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contest.panel_size'
        db.add_column(u'bbs_contest', 'panel_size',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contest.panel_size'
        db.delete_column(u'bbs_contest', 'panel_size')


    models = {
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
            'song_one': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'song_one'", 'null': 'True', 'to': u"orm['bbs.Song']"}),
            'song_two': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'song_two'", 'null': 'True', 'to': u"orm['bbs.Song']"}),
            'stage_time': ('django.db.models.fields.DateTimeField', [], {}),
            'total_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'bbs.singer': {
            'Meta': {'object_name': 'Singer'},
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'part': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'})
        },
        u'bbs.song': {
            'Meta': {'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['bbs']