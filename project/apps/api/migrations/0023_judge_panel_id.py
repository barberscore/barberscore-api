# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0022_convention_stix_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='judge',
            name='panel_id',
            field=models.IntegerField(null=True, blank=True),
        ),
    ]
