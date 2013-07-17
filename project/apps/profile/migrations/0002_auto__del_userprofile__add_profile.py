# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table(u'profile_userprofile')

        # Adding model 'Profile'
        db.create_table(u'profile_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['noncense.MobileUser'], unique=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25, blank=True)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'profile', ['Profile'])


    def backwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table(u'profile_userprofile', (
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['noncense.MobileUser'], unique=True)),
            ('timezone', self.gf('timezone_field.fields.TimeZoneField')(null=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'profile', ['UserProfile'])

        # Deleting model 'Profile'
        db.delete_table(u'profile_profile')


    models = {
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
        },
        u'profile.profile': {
            'Meta': {'object_name': 'Profile'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'blank': 'True'}),
            'timezone': ('timezone_field.fields.TimeZoneField', [], {'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['noncense.MobileUser']", 'unique': 'True'})
        }
    }

    complete_apps = ['profile']