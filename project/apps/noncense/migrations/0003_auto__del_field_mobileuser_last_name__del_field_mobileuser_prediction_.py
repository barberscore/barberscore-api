# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'MobileUser.last_name'
        db.delete_column(u'noncense_mobileuser', 'last_name')

        # Deleting field 'MobileUser.prediction'
        db.delete_column(u'noncense_mobileuser', 'prediction')

        # Deleting field 'MobileUser.first_name'
        db.delete_column(u'noncense_mobileuser', 'first_name')

        # Deleting field 'MobileUser.time_zone'
        db.delete_column(u'noncense_mobileuser', 'time_zone')


    def backwards(self, orm):
        # Adding field 'MobileUser.last_name'
        db.add_column(u'noncense_mobileuser', 'last_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True),
                      keep_default=False)

        # Adding field 'MobileUser.prediction'
        db.add_column(u'noncense_mobileuser', 'prediction',
                      self.gf('django.db.models.fields.TextField')(null=True, blank=True),
                      keep_default=False)

        # Adding field 'MobileUser.first_name'
        db.add_column(u'noncense_mobileuser', 'first_name',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=25, blank=True),
                      keep_default=False)

        # Adding field 'MobileUser.time_zone'
        db.add_column(u'noncense_mobileuser', 'time_zone',
                      self.gf('timezone_field.fields.TimeZoneField')(null=True, blank=True),
                      keep_default=False)


    models = {
        u'noncense.mobileuser': {
            'Meta': {'object_name': 'MobileUser'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'mobile': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '12', 'db_index': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['noncense']