# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20151013_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='arrangement',
            name='bhs_arranger',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='bhs_songname',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='fuzzy',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='person_match',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='arrangement',
            name='song_match',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='dates',
            field=models.CharField(help_text=b'\n            The convention dates (will be replaced by start/end).', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='convention',
            name='location',
            field=models.CharField(help_text=b'\n            The location of the convention ', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='long_name',
            field=models.CharField(help_text=b'\n            A long-form name for the resource.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='district',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='chapter_name',
            field=models.CharField(help_text=b'\n            The name of the director(s) of the chorus.', max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='fuzzy',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='penalty',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='email',
            field=models.EmailField(help_text=b'\n            The contact email of the resource.', max_length=254, blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='fuzzy',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='person',
            name='notes',
            field=models.TextField(help_text=b'\n            Notes (for internal use only).', blank=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='fuzzy',
            field=models.TextField(blank=True),
        ),
    ]
