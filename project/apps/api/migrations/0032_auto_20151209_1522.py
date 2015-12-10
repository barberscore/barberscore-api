# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import autoslug.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0031_organization_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organization',
            name='slug',
            field=autoslug.fields.AutoSlugField(always_update=True, populate_from=b'name', max_length=255, editable=False),
        ),
    ]
