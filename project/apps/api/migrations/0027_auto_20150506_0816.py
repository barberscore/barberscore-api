# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_contest_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(unique=True, editable=False),
        ),
    ]
