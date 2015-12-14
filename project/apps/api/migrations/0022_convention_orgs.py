# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_auto_20151213_1957'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='orgs',
            field=mptt.fields.TreeManyToManyField(help_text=b'\n            The organization hosting the convention.', related_name='orgs', to='api.Organization'),
        ),
    ]
