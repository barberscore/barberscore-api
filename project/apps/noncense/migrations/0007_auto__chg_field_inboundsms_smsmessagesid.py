# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'InboundSMS.smsmessagesid'
        db.alter_column(u'noncense_inboundsms', 'smsmessagesid', self.gf('django.db.models.fields.CharField')(max_length=200))

    def backwards(self, orm):

        # Changing field 'InboundSMS.smsmessagesid'
        db.alter_column(u'noncense_inboundsms', 'smsmessagesid', self.gf('django.db.models.fields.TextField')())

    models = {
        u'noncense.inboundsms': {
            'Meta': {'object_name': 'InboundSMS'},
            '_from': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'accountsid': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'apiversion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'body': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromcity': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromcountry': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromstate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'fromzip': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound_raw': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'smsmessagesid': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'smssid': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'smsstatus': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'to': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tocity': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tocountry': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tostate': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'tozip': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
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