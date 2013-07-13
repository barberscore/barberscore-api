# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'InboundSMS'
        db.delete_table(u'noncense_inboundsms')


    def backwards(self, orm):
        # Adding model 'InboundSMS'
        db.create_table(u'noncense_inboundsms', (
            ('body', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromzip', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smssid', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smsstatus', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromcountry', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('fromcity', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('apiversion', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('to', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tozip', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tocountry', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tostate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('accountsid', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('_from', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('inbound_raw', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('tocity', self.gf('django.db.models.fields.TextField')(blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fromstate', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('smsmessagesid', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
        ))
        db.send_create_signal(u'noncense', ['InboundSMS'])


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