# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Performance'
        db.delete_table(u'bbs_performance')

        # Deleting model 'Convention'
        db.delete_table(u'bbs_convention')

        # Deleting model 'Quartet'
        db.delete_table(u'bbs_quartet')

        # Deleting model 'Chorus'
        db.delete_table(u'bbs_chorus')

        # Deleting model 'Song'
        db.delete_table(u'bbs_song')


        # Changing field 'Contestant.district'
        db.alter_column(u'bbs_contestant', 'district', self.gf('django.db.models.fields.IntegerField')(default=1))
        # Deleting field 'Contest.contest_round'
        db.delete_column(u'bbs_contest', 'contest_round')

        # Deleting field 'Contest.date'
        db.delete_column(u'bbs_contest', 'date')

        # Deleting field 'Contest.convention_id'
        db.delete_column(u'bbs_contest', 'convention_id_id')

        # Deleting field 'Contest.name'
        db.delete_column(u'bbs_contest', 'name')

        # Deleting field 'Contest.level'
        db.delete_column(u'bbs_contest', 'level')

        # Deleting field 'Contest.is_complete'
        db.delete_column(u'bbs_contest', 'is_complete')


    def backwards(self, orm):
        # Adding model 'Performance'
        db.create_table(u'bbs_performance', (
            ('prelim', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('name_two', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('avg_mus_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('prs_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('total_score', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('men_on_stage', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('name_one', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('avg_total_score', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_sng_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contestant', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contestant'], null=True, blank=True)),
            ('seed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sng_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_mus_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_sng_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('score_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('score_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_score_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('slot', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, blank=True)),
            ('mus_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('avg_prs_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('contest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bbs.Contest'], null=True, blank=True)),
            ('prs_one', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_scratch', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('place', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sng_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('mus_two', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('stage_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('avg_score_two', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('avg_prs_one', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('is_complete', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'bbs', ['Performance'])

        # Adding model 'Convention'
        db.create_table(u'bbs_convention', (
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'bbs', ['Convention'])

        # Adding model 'Quartet'
        db.create_table(u'bbs_quartet', (
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('bass', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('tenor', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('baritone', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('lead', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'bbs', ['Quartet'])

        # Adding model 'Chorus'
        db.create_table(u'bbs_chorus', (
            ('director', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
            ('facebook', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('district', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('website', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True)),
        ))
        db.send_create_signal(u'bbs', ['Chorus'])

        # Adding model 'Song'
        db.create_table(u'bbs_song', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, unique=True)),
        ))
        db.send_create_signal(u'bbs', ['Song'])


        # Changing field 'Contestant.district'
        db.alter_column(u'bbs_contestant', 'district', self.gf('django.db.models.fields.IntegerField')(null=True))
        # Adding field 'Contest.contest_round'
        db.add_column(u'bbs_contest', 'contest_round',
                      self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contest.date'
        db.add_column(u'bbs_contest', 'date',
                      self.gf('django.db.models.fields.DateField')(null=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Contest.convention_id'
        raise RuntimeError("Cannot reverse this migration. 'Contest.convention_id' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Contest.name'
        raise RuntimeError("Cannot reverse this migration. 'Contest.name' and its values cannot be restored.")
        # Adding field 'Contest.level'
        db.add_column(u'bbs_contest', 'level',
                      self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Contest.is_complete'
        db.add_column(u'bbs_contest', 'is_complete',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    models = {
        u'bbs.contest': {
            'Meta': {'ordering': "['year', 'contest_level', 'contest_type']", 'object_name': 'Contest'},
            'contest_level': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'contest_type': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
            'district': ('django.db.models.fields.IntegerField', [], {}),
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
        }
    }

    complete_apps = ['bbs']