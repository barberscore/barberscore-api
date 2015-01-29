# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_contest_convention'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True),
            preserve_default=True,
        ),
    ]
