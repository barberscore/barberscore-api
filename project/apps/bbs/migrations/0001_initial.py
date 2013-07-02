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
            ('seed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prelim', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contestant_type', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Contestant'])

        # Adding model 'Contest'
        db.create_table(u'bbs_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('contest_type', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Contest'])

        # Adding model 'Performance'
        db.create_table(u'bbs_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'], null=True, blank=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('contest_round', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('slot', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stage_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('song_one', self.gf('django.db.models.fields.CharField')(default='Song One', max_length=200)),
            ('score_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mus_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prs_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sng_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('song_two', self.gf('django.db.models.fields.CharField')(default='Song Two', max_length=200)),
            ('score_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('mus_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prs_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sng_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Performance'])

        # Adding model 'Rating'
        db.create_table(u'bbs_rating', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['noncense.MobileUser'], null=True)),
            ('performance', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Performance'], null=True)),
            ('song_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('song_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Rating'])


    def backwards(self, orm):
        # Deleting model 'Contestant'
        db.delete_table(u'bbs_contestant')

        # Deleting model 'Contest'
        db.delete_table(u'bbs_contest')

        # Deleting model 'Performance'
        db.delete_table(u'bbs_performance')

        # Deleting model 'Rating'
        db.delete_table(u'bbs_rating')


    models = {
        u'bbs.contest': {
            'Meta': {'ordering': "['year', 'level', 'contest_type']", 'object_name': 'Contest'},
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'contestant_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'prelim': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        u'bbs.performance': {
            'Meta': {'ordering': "['contest', 'contest_round', 'slot']", 'object_name': 'Performance'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']", 'null': 'True', 'blank': 'True'}),
            'contest_round': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mus_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mus_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'score_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'score_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'blank': 'True'}),
            'sng_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sng_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'song_one': ('django.db.models.fields.CharField', [], {'default': "'Song One'", 'max_length': '200'}),
            'song_two': ('django.db.models.fields.CharField', [], {'default': "'Song Two'", 'max_length': '200'}),
            'stage_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'bbs.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Performance']", 'null': 'True'}),
            'song_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'song_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['noncense.MobileUser']", 'null': 'True'})
        },
        u'noncense.mobileuser': {
            'Meta': {'object_name': 'MobileUser'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'mobile': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['bbs']