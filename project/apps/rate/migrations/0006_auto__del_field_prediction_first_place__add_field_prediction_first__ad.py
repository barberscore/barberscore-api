# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Prediction.first_place'
        db.delete_column(u'rate_prediction', 'first_place_id')

        # Adding field 'Prediction.first'
        db.add_column(u'rate_prediction', 'first',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.second'
        db.add_column(u'rate_prediction', 'second',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.third'
        db.add_column(u'rate_prediction', 'third',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.fourth'
        db.add_column(u'rate_prediction', 'fourth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.fifth'
        db.add_column(u'rate_prediction', 'fifth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.sixth'
        db.add_column(u'rate_prediction', 'sixth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.seventh'
        db.add_column(u'rate_prediction', 'seventh',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.eigth'
        db.add_column(u'rate_prediction', 'eigth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.ninth'
        db.add_column(u'rate_prediction', 'ninth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'Prediction.tenth'
        db.add_column(u'rate_prediction', 'tenth',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Prediction.first_place'
        db.add_column(u'rate_prediction', 'first_place',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'], null=True),
                      keep_default=False)

        # Deleting field 'Prediction.first'
        db.delete_column(u'rate_prediction', 'first')

        # Deleting field 'Prediction.second'
        db.delete_column(u'rate_prediction', 'second')

        # Deleting field 'Prediction.third'
        db.delete_column(u'rate_prediction', 'third')

        # Deleting field 'Prediction.fourth'
        db.delete_column(u'rate_prediction', 'fourth')

        # Deleting field 'Prediction.fifth'
        db.delete_column(u'rate_prediction', 'fifth')

        # Deleting field 'Prediction.sixth'
        db.delete_column(u'rate_prediction', 'sixth')

        # Deleting field 'Prediction.seventh'
        db.delete_column(u'rate_prediction', 'seventh')

        # Deleting field 'Prediction.eigth'
        db.delete_column(u'rate_prediction', 'eigth')

        # Deleting field 'Prediction.ninth'
        db.delete_column(u'rate_prediction', 'ninth')

        # Deleting field 'Prediction.tenth'
        db.delete_column(u'rate_prediction', 'tenth')


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
        u'bbs.song': {
            'Meta': {'object_name': 'Song'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'noncense.mobileuser': {
            'Meta': {'object_name': 'MobileUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mobile': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        u'rate.prediction': {
            'Meta': {'object_name': 'Prediction'},
            'eigth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fifth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'first': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'fourth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ninth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'second': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'seventh': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'sixth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'tenth': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'third': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['noncense.MobileUser']", 'null': 'True'})
        },
        u'rate.rating': {
            'Meta': {'object_name': 'Rating'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Performance']", 'null': 'True'}),
            'song_one': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'song_two': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['noncense.MobileUser']", 'null': 'True'})
        }
    }

    complete_apps = ['rate']