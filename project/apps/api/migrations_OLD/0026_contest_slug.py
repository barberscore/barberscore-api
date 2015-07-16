# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20150505_0926'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True),
        ),
    ]
