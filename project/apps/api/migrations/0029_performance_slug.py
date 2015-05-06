# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0028_contestant_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='performance',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True),
        ),
    ]
