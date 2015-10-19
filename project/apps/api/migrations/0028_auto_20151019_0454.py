# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20151019_0453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(default=1, help_text=b'\n            The objective of the contest', choices=[(1, b'Championship'), (2, b'Prelims')]),
        ),
        migrations.AlterField(
            model_name='contest',
            name='level',
            field=models.IntegerField(default=1, help_text=b'\n            The level of the contest (currently only International is supported.)', choices=[(1, b'International'), (2, b'District'), (3, b'Division'), (4, b'Prelims')]),
        ),
    ]
