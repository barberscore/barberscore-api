# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-08 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20170407_2131'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='num',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
