# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0025_auto_20151018_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(default=1, help_text=b'\n            The objective of the contest', choices=[(1, b'Championship'), (2, b'Qualification')]),
        ),
    ]
