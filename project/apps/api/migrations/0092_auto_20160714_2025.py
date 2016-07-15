# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-15 03:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0091_auto_20160714_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='nomen',
            field=models.TextField(blank=True, editable=False, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='bhs_id',
            field=models.IntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='nomen',
            field=models.TextField(editable=False, max_length=255, unique=True),
        ),
    ]
