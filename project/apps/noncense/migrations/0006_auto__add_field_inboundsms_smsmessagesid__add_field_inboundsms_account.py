# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'InboundSMS.smsmessagesid'
        db.add_column(u'noncense_inboundsms', 'smsmessagesid',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.accountsid'
        db.add_column(u'noncense_inboundsms', 'accountsid',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.body'
        db.add_column(u'noncense_inboundsms', 'body',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.fromzip'
        db.add_column(u'noncense_inboundsms', 'fromzip',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.to'
        db.add_column(u'noncense_inboundsms', 'to',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.tocity'
        db.add_column(u'noncense_inboundsms', 'tocity',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.smssid'
        db.add_column(u'noncense_inboundsms', 'smssid',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.fromstate'
        db.add_column(u'noncense_inboundsms', 'fromstate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.tocountry'
        db.add_column(u'noncense_inboundsms', 'tocountry',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS._from'
        db.add_column(u'noncense_inboundsms', '_from',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.apiversion'
        db.add_column(u'noncense_inboundsms', 'apiversion',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.fromcity'
        db.add_column(u'noncense_inboundsms', 'fromcity',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.tozip'
        db.add_column(u'noncense_inboundsms', 'tozip',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.smsstatus'
        db.add_column(u'noncense_inboundsms', 'smsstatus',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.tostate'
        db.add_column(u'noncense_inboundsms', 'tostate',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'InboundSMS.fromcountry'
        db.add_column(u'noncense_inboundsms', 'fromcountry',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'InboundSMS.smsmessagesid'
        db.delete_column(u'noncense_inboundsms', 'smsmessagesid')

        # Deleting field 'InboundSMS.accountsid'
        db.delete_column(u'noncense_inboundsms', 'accountsid')

        # Deleting field 'InboundSMS.body'
        db.delete_column(u'noncense_inboundsms', 'body')

        # Deleting field 'InboundSMS.fromzip'
        db.delete_column(u'noncense_inboundsms', 'fromzip')

        # Deleting field 'InboundSMS.to'
        db.delete_column(u'noncense_inboundsms', 'to')

        # Deleting field 'InboundSMS.tocity'
        db.delete_column(u'noncense_inboundsms', 'tocity')

        # Deleting field 'InboundSMS.smssid'
        db.delete_column(u'noncense_inboundsms', 'smssid')

        # Deleting field 'InboundSMS.fromstate'
        db.delete_column(u'noncense_inboundsms', 'fromstate')

        # Deleting field 'InboundSMS.tocountry'
        db.delete_column(u'noncense_inboundsms', 'tocountry')

        # Deleting field 'InboundSMS._from'
        db.delete_column(u'noncense_inboundsms', '_from')

        # Deleting field 'InboundSMS.apiversion'
        db.delete_column(u'noncense_inboundsms', 'apiversion')

        # Deleting field 'InboundSMS.fromcity'
        db.delete_column(u'noncense_inboundsms', 'fromcity')

        # Deleting field 'InboundSMS.tozip'
        db.delete_column(u'noncense_inboundsms', 'tozip')

        # Deleting field 'InboundSMS.smsstatus'
        db.delete_column(u'noncense_inboundsms', 'smsstatus')

        # Deleting field 'InboundSMS.tostate'
        db.delete_column(u'noncense_inboundsms', 'tostate')

        # Deleting field 'InboundSMS.fromcountry'
        db.delete_column(u'noncense_inboundsms', 'fromcountry')


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
            'smsmessagesid': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
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