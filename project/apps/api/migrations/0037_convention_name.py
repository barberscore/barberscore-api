# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0036_contest_district'),
    ]

    operations = [
        migrations.AddField(
            model_name='convention',
            name='name',
            field=models.CharField(help_text=b'\n            The name of the convention.', max_length=200, null=True, blank=True),
        ),
    ]
