# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Song'
        db.delete_table(u'bbs_song')


        # Renaming column for 'Performance.song_one' to match new field type.
        db.rename_column(u'bbs_performance', 'song_one_id', 'song_one')
        # Changing field 'Performance.song_one'
        db.alter_column(u'bbs_performance', 'song_one', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Removing index on 'Performance', fields ['song_one']
        db.delete_index(u'bbs_performance', ['song_one_id'])


        # Renaming column for 'Performance.song_two' to match new field type.
        db.rename_column(u'bbs_performance', 'song_two_id', 'song_two')
        # Changing field 'Performance.song_two'
        db.alter_column(u'bbs_performance', 'song_two', self.gf('django.db.models.fields.CharField')(max_length=200))
        # Removing index on 'Performance', fields ['song_two']
        db.delete_index(u'bbs_performance', ['song_two_id'])


    def backwards(self, orm):
        # Adding index on 'Performance', fields ['song_two']
        db.create_index(u'bbs_performance', ['song_two_id'])

        # Adding index on 'Performance', fields ['song_one']
        db.create_index(u'bbs_performance', ['song_one_id'])

        # Adding model 'Song'
        db.create_table(u'bbs_song', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'bbs', ['Song'])


        # Renaming column for 'Performance.song_one' to match new field type.
        db.rename_column(u'bbs_performance', 'song_one', 'song_one_id')
        # Changing field 'Performance.song_one'
        db.alter_column(u'bbs_performance', 'song_one_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Song']))

        # Renaming column for 'Performance.song_two' to match new field type.
        db.rename_column(u'bbs_performance', 'song_two', 'song_two_id')
        # Changing field 'Performance.song_two'
        db.alter_column(u'bbs_performance', 'song_two_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Song']))

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
            'song_one': ('django.db.models.fields.CharField', [], {'default': "'Song One'", 'max_length': '200'}),
            'song_two': ('django.db.models.fields.CharField', [], {'default': "'Song Two'", 'max_length': '200'})
        },
        u'bbs.quartet': {
            'Meta': {'ordering': "['name']", 'object_name': 'Quartet'},
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'bbs.singer': {
            'Meta': {'ordering': "['name']", 'object_name': 'Singer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'quartet': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Quartet']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'blank': 'True'})
        }
    }

    complete_apps = ['bbs']