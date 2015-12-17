# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0040_auto_20151216_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='formal_name',
            field=models.CharField(default=b'', max_length=255, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='person',
            name='full_name',
            field=models.CharField(default=b'', max_length=255, editable=False, blank=True),
        ),
    ]
