# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20150727_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='slug',
            field=autoslug.fields.AutoSlugField(default='Foo', editable=False, populate_from=b'name', always_update=True),
            preserve_default=False,
        ),
    ]
