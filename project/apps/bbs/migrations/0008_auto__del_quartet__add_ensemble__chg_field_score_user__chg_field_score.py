# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Quartet'
        db.delete_table(u'bbs_quartet')

        # Adding model 'Contestant'
        db.create_table(u'bbs_contestant', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Contestant'])


        # Changing field 'Score.user'
        db.alter_column(u'bbs_score', 'user_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['noncense.MobileUser'], null=True))

        # Changing field 'Score.performance'
        db.alter_column(u'bbs_score', 'performance_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Performance'], null=True))
        # Deleting field 'Performance.quartet'
        db.delete_column(u'bbs_performance', 'quartet_id')

        # Adding field 'Performance.contestant'
        db.add_column(u'bbs_performance', 'contestant',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'], null=True, blank=True),
                      keep_default=False)


        # Changing field 'Performance.contest'
        db.alter_column(u'bbs_performance', 'contest_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'], null=True))

    def backwards(self, orm):
        # Adding model 'Quartet'
        db.create_table(u'bbs_quartet', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'bbs', ['Quartet'])

        # Deleting model 'Contestant'
        db.delete_table(u'bbs_contestant')


        # User chose to not deal with backwards NULL issues for 'Score.user'
        raise RuntimeError("Cannot reverse this migration. 'Score.user' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Score.performance'
        raise RuntimeError("Cannot reverse this migration. 'Score.performance' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Performance.quartet'
        raise RuntimeError("Cannot reverse this migration. 'Performance.quartet' and its values cannot be restored.")
        # Deleting field 'Performance.contestant'
        db.delete_column(u'bbs_performance', 'contestant_id')


        # User chose to not deal with backwards NULL issues for 'Performance.contest'
        raise RuntimeError("Cannot reverse this migration. 'Performance.contest' and its values cannot be restored.")

    models = {
        u'bbs.contest': {
            'Meta': {'object_name': 'Contest'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'bbs.contest': {
            'Meta': {'object_name': 'Contest'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'bbs.contestant': {
            'Meta': {'ordering': "['name']", 'object_name': 'Contestant'},
            'district': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'})
        },
        u'bbs.performance': {
            'Meta': {'ordering': "['contest', 'night', 'slot']", 'object_name': 'Performance'},
            'contest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contest']", 'null': 'True', 'blank': 'True'}),
            'contestant': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['bbs.Contestant']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mus_one': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'mus_two': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'night': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
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