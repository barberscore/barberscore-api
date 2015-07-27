# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_spot_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='spot',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', editable=False),
        ),
    ]
