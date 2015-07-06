# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0127_performance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(unique=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
    ]
