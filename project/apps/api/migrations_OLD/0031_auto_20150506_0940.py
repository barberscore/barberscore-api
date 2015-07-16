# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20150506_0928'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, max_length=255, editable=False),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, max_length=255, editable=False),
        ),
    ]
