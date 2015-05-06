# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_performance_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(max_length=255, null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='round',
            field=models.IntegerField(default=1, choices=[(1, b'Finals'), (2, b'Semis'), (3, b'Quarters')]),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(max_length=255, null=True, editable=False, blank=True),
        ),
    ]
