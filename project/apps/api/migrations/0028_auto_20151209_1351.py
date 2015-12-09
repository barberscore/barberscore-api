# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0027_auto_20151209_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(help_text=b'\n            The objective of the contest.', choices=[(0, b'Championship'), (1, b'Qualifier')]),
        ),
    ]
