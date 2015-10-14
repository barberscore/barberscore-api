# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0030_auto_20151013_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific')]),
        ),
    ]
