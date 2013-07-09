# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Score'
        db.create_table(u'bbs_score', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'])),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'])),
            ('contest_round', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('song1', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mus1', self.gf('django.db.models.fields.IntegerField')()),
            ('prs1', self.gf('django.db.models.fields.IntegerField')()),
            ('sng1', self.gf('django.db.models.fields.IntegerField')()),
            ('song2', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('mus2', self.gf('django.db.models.fields.IntegerField')()),
            ('prs2', self.gf('django.db.models.fields.IntegerField')()),
            ('sng2', self.gf('django.db.models.fields.IntegerField')()),
            ('men_on_stage', self.gf('django.db.models.fields.IntegerField')(default=4, null=True)),
        ))
        db.send_create_signal(u'bbs', ['Score'])


    def backwards(self, orm):
        # Deleting model 'Score'
        db.delete_table(u'bbs_score')


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
            'contest_level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contest_round': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_complete': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
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
        u'bbs.convention': {
            'Meta': {'object_name': 'Convention'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
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
        u'bbs.score': {
            'Meta': {'object_name': 'Score'},
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
        },
        u'bbs.song': {
            'Meta': {'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        }
    }

    complete_apps = ['bbs']