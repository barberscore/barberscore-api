# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'InboundSMS'
        db.create_table(u'noncense_inboundsms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('inbound_raw', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal(u'noncense', ['InboundSMS'])


    def backwards(self, orm):
        # Deleting model 'InboundSMS'
        db.delete_table(u'noncense_inboundsms')


    models = {
        u'noncense.inboundsms': {
            'Meta': {'object_name': 'InboundSMS'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inbound_raw': ('django.db.models.fields.CharField', [], {'max_length': '200'})
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