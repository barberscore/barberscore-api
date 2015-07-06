# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0129_auto_20150706_1615'),
    ]

    operations = [
        migrations.AlterField(
            model_name='performance',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True),
        ),
    ]
