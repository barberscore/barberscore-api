# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-07 00:00
from __future__ import unicode_literals

from django.db import migrations
import django_fsm


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0042_convention_is_archived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='status',
            field=django_fsm.FSMIntegerField(choices=[(0, 'New'), (2, 'Published')], default=0),
        ),
    ]
