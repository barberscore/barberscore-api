# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0066_contest_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(editable=False, populate_from=b'name', always_update=True, unique=True),
        ),
    ]
