# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-25 17:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_person_is_deceased'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='dues_thru',
        ),
    ]
