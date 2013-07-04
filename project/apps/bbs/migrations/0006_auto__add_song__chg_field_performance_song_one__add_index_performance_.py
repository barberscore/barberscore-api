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
            ('name', self.gf('django.db.models.fields.CharField')(default='Unknown', max_length=200)),
        ))
        db.send_create_signal(u'bbs', ['Song'])


        # Renaming column for 'Performance.song_one' to match new field type.
        db.rename_column(u'bbs_performance', 'song_one', 'song_one_id')
        # Changing field 'Performance.song_one'
        db.alter_column(u'bbs_performance', 'song_one_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Song']))
        # Adding index on 'Performance', fields ['song_one']
        db.create_index(u'bbs_performance', ['song_one_id'])


        # Renaming column for 'Performance.song_two' to match new field type.
        db.rename_column(u'bbs_performance', 'song_two', 'song_two_id')
        # Changing field 'Performance.song_two'
        db.alter_column(u'bbs_performance', 'song_two_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['bbs.Song']))
        # Adding index on 'Performance', fields ['song_two']
        db.create_index(u'bbs_performance', ['song_two_id'])


    def backwards(self, orm):
        # Removing index on 'Performance', fields ['song_two']
        db.delete_index(u'bbs_performance', ['song_two_id'])

        # Removing index on 'Performance', fields ['song_one']
        db.delete_index(u'bbs_performance', ['song_one_id'])

        # Deleting model 'Song'
        db.delete_table(u'bbs_song')


        # Renaming column for 'Performance.song_one' to match new field type.
        db.rename_column(u'bbs_performance', 'song_one_id', 'song_one')
        # Changing field 'Performance.song_one'
        db.alter_column(u'bbs_performance', 'song_one', self.gf('django.db.models.fields.CharField')(max_length=200))

        # Renaming column for 'Performance.song_two' to match new field type.
        db.rename_column(u'bbs_performance', 'song_two_id', 'song_two')
        # Changing field 'Performance.song_two'
        db.alter_column(u'bbs_performance', 'song_two', self.gf('django.db.models.fields.CharField')(max_length=200))

    models = {
        u'bbs.contest': {
            'Meta': {'ordering': "['year', 'level', 'contest_type']", 'object_name': 'Contest'},
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'Contest'", 'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'contestant_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
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
            'song_one': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'song_one'", 'null': 'True', 'to': u"orm['bbs.Song']"}),
            'song_two': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'song_two'", 'null': 'True', 'to': u"orm['bbs.Song']"}),
            'stage_time': ('django.db.models.fields.DateTimeField', [], {})
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
            'name': ('django.db.models.fields.CharField', [], {'default': "'Unknown'", 'max_length': '200'})
        }
    }

    complete_apps = ['bbs']