# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20151209_1510'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='short_name',
            field=models.CharField(help_text=b'\n            A short-form name for the resource.', max_length=200, blank=True),
        ),
    ]
