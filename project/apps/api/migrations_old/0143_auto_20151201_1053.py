# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0142_contestant_convention'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contest',
            name='panel',
        ),
        migrations.AlterField(
            model_name='contest',
            name='goal',
            field=models.IntegerField(blank=True, help_text=b'\n            The objective of the contest', null=True, choices=[(1, b'Championship'), (2, b'Qualifier')]),
        ),
    ]
