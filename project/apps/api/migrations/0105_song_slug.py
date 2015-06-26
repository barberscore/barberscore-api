# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0104_auto_20150625_1424'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', null=True, editable=False, blank=True),
        ),
    ]
