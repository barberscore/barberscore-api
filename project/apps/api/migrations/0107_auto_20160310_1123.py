# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-10 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0106_auto_20160310_1044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='role',
            name='performer',
        ),
        migrations.AlterField(
            model_name='role',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to='api.Group'),
        ),
    ]
