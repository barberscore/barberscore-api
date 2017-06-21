# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-21 21:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0041_auto_20170621_1433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chart',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='entity',
            name='code',
            field=models.CharField(blank=True, help_text='\n            The chapter code.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entity',
            name='location',
            field=models.CharField(blank=True, help_text='\n            The geographical location of the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entity',
            name='long_name',
            field=models.CharField(blank=True, help_text='\n            A long-form name for the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entity',
            name='name',
            field=models.CharField(help_text='\n            The name of the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='entity',
            name='short_name',
            field=models.CharField(blank=True, help_text='\n            A short-form name for the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='office',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='person',
            name='last_name',
            field=models.CharField(default='', help_text='\n            The name of the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='person',
            name='location',
            field=models.CharField(blank=True, help_text='\n            The geographical location of the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='person',
            name='name',
            field=models.CharField(help_text='\n            The name of the resource.', max_length=255),
        ),
        migrations.AlterField(
            model_name='venue',
            name='name',
            field=models.CharField(help_text='\n            The name of the resource.', max_length=255),
        ),
    ]
