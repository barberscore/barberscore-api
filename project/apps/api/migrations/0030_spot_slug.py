# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0029_auto_20150727_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='spot',
            name='slug',
            field=autoslug.fields.AutoSlugField(default=None, editable=False, populate_from=b'name', always_update=True, unique=True),
            preserve_default=False,
        ),
    ]
