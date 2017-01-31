# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-30 18:19
from __future__ import unicode_literals

from django.db import migrations

def assignment_fks(apps, schema_editor):
    Assignment = apps.get_model("app", "Assignment")
    ass = Assignment.objects.all()
    for a in ass:
        a.convention = a.session.convention
        a.save()

class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20170130_1019'),
    ]

    operations = [
        migrations.RunPython(assignment_fks),
    ]
