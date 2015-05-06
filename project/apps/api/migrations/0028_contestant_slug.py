# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20150506_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestant',
            name='slug',
            field=autoslug.fields.AutoSlugField(null=True, editable=False, blank=True),
        ),
    ]
