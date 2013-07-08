# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contestant'
        db.create_table(u'bbs_contestant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('director', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('contestant_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Contestant'])

        # Adding model 'Singer'
        db.create_table(u'bbs_singer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('part', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'])),
        ))
        db.send_create_signal(u'bbs', ['Singer'])

        # Adding model 'Contest'
        db.create_table(u'bbs_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='Contest', max_length=200)),
            ('date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('time_zone', self.gf('timezone_field.fields.TimeZoneField')(null=True, blank=True)),
            ('contest_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('contest_round', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('panel_size', self.gf('django.db.models.fields.IntegerField')(null=True)),
        ))
        db.send_create_signal(u'bbs', ['Contest'])

        # Adding model 'Song'
        db.create_table(u'bbs_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal(u'bbs', ['Song'])

        # Adding model 'Performance'
        db.create_table(u'bbs_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'], null=True, blank=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('slot', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prelim', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_scratch', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('men_on_stage', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('stage_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('name_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mus_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prs_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sng_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('score_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_mus_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_prs_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_sng_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_score_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('name_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('mus_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prs_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sng_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('score_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_mus_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_prs_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_sng_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_score_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('total_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_total_score', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Performance'])


    def backwards(self, orm):
        # Deleting model 'Contestant'
        db.delete_table(u'bbs_contestant')

        # Deleting model 'Singer'
        db.delete_table(u'bbs_singer')

        # Deleting model 'Contest'
        db.delete_table(u'bbs_contest')

        # Deleting model 'Song'
        db.delete_table(u'bbs_song')

        # Deleting model 'Performance'
        db.delete_table(u'bbs_performance')


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