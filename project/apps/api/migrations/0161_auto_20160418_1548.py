# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-18 22:48
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0160_auto_20160417_0827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='organization',
            field=mptt.fields.TreeForeignKey(blank=True, help_text=b'\n            The organization hosting the convention.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conventions', to='api.Organization'),
        ),
    ]
