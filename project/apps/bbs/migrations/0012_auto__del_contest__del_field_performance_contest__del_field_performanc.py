# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Contest'
        db.delete_table(u'bbs_contest')

        # Deleting field 'Performance.contest'
        db.delete_column(u'bbs_performance', 'contest_id')

        # Deleting field 'Performance.night'
        db.delete_column(u'bbs_performance', 'night')

        # Adding field 'Performance.convention'
        db.add_column(u'bbs_performance', 'convention',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Convention'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Performance.contest_round'
        db.add_column(u'bbs_performance', 'contest_round',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Contest'
        db.create_table(u'bbs_contest', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('convention', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Convention'], null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Contest'])

        # Adding field 'Performance.contest'
        db.add_column(u'bbs_performance', 'contest',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Performance.night'
        db.add_column(u'bbs_performance', 'night',
                      self.gf('django.db.models.fields.IntegerField')(null=True, blank=True),
                      keep_default=False)

        # Deleting field 'Performance.convention'
        db.delete_column(u'bbs_performance', 'convention_id')

        # Deleting field 'Performance.contest_round'
        db.delete_column(u'bbs_performance', 'contest_round')


    models = {
        u'bbs.convention': {
            'Meta': {'object_name': 'Convention'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'contestant_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True'})
        },
        u'bbs.performance': {
            'Meta': {'object_name': 'Performance'},
            'contest_round': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'convention': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Convention']", 'null': 'True', 'blank': 'True'}),
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mus_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mus_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'prs_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'slot': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sng_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'sng_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'song_one': ('django.db.models.fields.CharField', [], {'default': "'Song One'", 'max_length': '200'}),
            'song_two': ('django.db.models.fields.CharField', [], {'default': "'Song Two'", 'max_length': '200'}),
            'user_scores': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['noncense.MobileUser']", 'null': 'True', 'through': u"orm['bbs.Score']", 'blank': 'True'})
        },
        u'bbs.score': {
            'Meta': {'object_name': 'Score'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'performance': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Performance']", 'null': 'True', 'blank': 'True'}),
            'song_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'song_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['noncense.MobileUser']", 'null': 'True', 'blank': 'True'})
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