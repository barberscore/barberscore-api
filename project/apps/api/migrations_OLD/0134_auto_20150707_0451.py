# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0133_auto_20150707_0441'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestantsinger',
            name='name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='contestantsinger',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True),
        ),
    ]
