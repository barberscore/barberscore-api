# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'MobileUser.time_zone'
        db.add_column(u'noncense_mobileuser', 'time_zone',
                      self.gf('timezone_field.fields.TimeZoneField')(null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'MobileUser.time_zone'
        db.delete_column(u'noncense_mobileuser', 'time_zone')


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
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'prediction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'time_zone': ('timezone_field.fields.TimeZoneField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['noncense']