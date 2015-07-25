# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_auto_20150724_2357'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='fuzzy',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='fuzzy',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='song',
            name='fuzzy',
            field=models.TextField(null=True, blank=True),
        ),
    ]
