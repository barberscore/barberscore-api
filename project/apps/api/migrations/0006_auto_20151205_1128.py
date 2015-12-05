# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20151205_1111'),
    ]

    operations = [
        migrations.AlterField(
            model_name='convention',
            name='kind',
            field=models.IntegerField(help_text=b'\n            The kind of convention.', choices=[(1, b'International'), (2, b'Midwinter'), (3, b'Fall'), (4, b'Spring'), (5, b'Pacific'), (6, b'Southeast and Southwest'), (7, b'Northeast and Northwest'), (8, b'District')]),
        ),
    ]
