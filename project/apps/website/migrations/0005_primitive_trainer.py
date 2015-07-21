# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_load_primitives'),
    ]

    operations = [
        migrations.AddField(
            model_name='primitive',
            name='trainer',
            field=jsonfield.fields.JSONField(null=True, blank=True),
        ),
    ]
