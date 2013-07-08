# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MobileUser'
        db.create_table(u'noncense_mobileuser', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_login', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('mobile', self.gf('django.db.models.fields.CharField')(unique=True, max_length=12, db_index=True)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_admin', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'noncense', ['MobileUser'])

        # Adding model 'InboundSMS'
        db.create_table(u'noncense_inboundsms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inbound_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smsmessagesid', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('accountsid', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromzip', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('to', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tocity', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smssid', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromstate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tocountry', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('apiversion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromcity', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tozip', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smsstatus', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tostate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromcountry', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'noncense', ['InboundSMS'])


    def backwards(self, orm):
        # Deleting model 'MobileUser'
        db.delete_table(u'noncense_mobileuser')

        # Deleting model 'InboundSMS'
        db.delete_table(u'noncense_inboundsms')


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