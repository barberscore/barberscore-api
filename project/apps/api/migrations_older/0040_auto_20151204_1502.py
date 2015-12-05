# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0039_auto_20151204_1501'),
    ]

    operations = [
        migrations.AlterField(
            model_name='judge',
            name='kind',
            field=models.IntegerField(choices=[(10, b'Official'), (20, b'Practice'), (30, b'Composite')]),
        ),
        migrations.AlterField(
            model_name='score',
            name='kind',
            field=models.IntegerField(choices=[(10, b'Official'), (20, b'Practice'), (30, b'Composite')]),
        ),
    ]
