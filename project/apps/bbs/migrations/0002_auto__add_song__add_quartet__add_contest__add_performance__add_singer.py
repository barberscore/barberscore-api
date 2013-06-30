# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Song'
        db.create_table(u'bbs_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Song'])

        # Adding model 'Quartet'
        db.create_table(u'bbs_quartet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Quartet'])

        # Adding model 'Contest'
        db.create_table(u'bbs_contest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'bbs', ['Contest'])

        # Adding model 'Performance'
        db.create_table(u'bbs_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('quartet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Quartet'])),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'])),
            ('night', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slot', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('song_one', self.gf('django.db.models.fields.related.ForeignKey')(related_name='song_one', to=orm['bbs.Song'])),
            ('mus_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prs_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sng_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('song_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='song_two', to=orm['bbs.Song'])),
            ('mus_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prs_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('sng_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Performance'])

        # Adding model 'Singer'
        db.create_table(u'bbs_singer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, blank=True)),
            ('quartet', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Quartet'])),
        ))
        db.send_create_signal(u'bbs', ['Singer'])


    def backwards(self, orm):
        # Deleting model 'Song'
        db.delete_table(u'bbs_song')

        # Deleting model 'Quartet'
        db.delete_table(u'bbs_quartet')

        # Deleting model 'Contest'
        db.delete_table(u'bbs_contest')

        # Deleting model 'Performance'
        db.delete_table(u'bbs_performance')

        # Deleting model 'Singer'
        db.delete_table(u'bbs_singer')


    models = {
        u'bbs.contest': {
            'Meta': {'ordering': "['date']", 'object_name': 'Contest'},
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        u'bbs.performance': {
            'Meta': {'ordering': "['contest', 'night', 'slot']", 'object_name': 'Performance'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mus_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mus_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'night': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'prs_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'quartet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Quartet']"}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sng_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sng_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'song_one': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'song_one'", 'to': u"orm['bbs.Song']"}),
            'song_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'song_two'", 'to': u"orm['bbs.Song']"})
        },
        u'bbs.quartet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Quartet'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        u'bbs.singer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Singer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quartet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Quartet']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        },
        u'bbs.song': {
            'Meta': {'ordering': "['name']", 'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['bbs']